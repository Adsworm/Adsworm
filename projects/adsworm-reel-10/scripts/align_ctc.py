#!/usr/bin/env python3
"""Forced alignment for Hinglish voice-over: audio + the exact words spoken → start/end time of every word.

The text is known, so nothing is transcribed. A Hindi CTC acoustic model gives, for every 20 ms of audio, the
probability of each Devanagari letter; a Viterbi search then finds the one path that spells the given words in
order. English words (Latin script) are respelled in Devanagari for the search only; digits become Hindi words.

Install (once; CPU only, about 1.2 GB for the virtualenv + 0.4 GB for the model):
    bash scripts/setup_align.sh
  which is the same as
    python3 -m venv ~/.venvs/align
    ~/.venvs/align/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
    ~/.venvs/align/bin/pip install transformers numpy huggingface_hub
  plus a one-time model download. ffmpeg must be on PATH.

Use:
    ~/.venvs/align/bin/python scripts/align_ctc.py AUDIO WORDS_JSON OUT_JSON [--lead SECONDS]
  WORDS_JSON: JSON list of words in spoken order, e.g. ["October", "में", "मेरे", "ads"].
  OUT_JSON:   [{"w": word, "start": s, "end": e, "score": x}, ...] one entry per input word, same order,
              seconds on the audio's own timeline.
  From Python:  from align_ctc import align_file;  align_file("dialogue.mp3", words)

Measured on the 72.6 s two-voice test clip (130 words, truth = the TTS engine's word-boundary events):
    start error  mean 23 ms · median 19 ms · p90 49 ms · max 73 ms · 0 % of words over 150 ms · 0 % over 300 ms
    end error    mean 33 ms
    (Whisper word timestamps + fuzzy matching on the same clip: mean 126 · median 106 · p90 172 · max 649 · 18 % over 150 ms)
    run time 9 s for the clip on 4 CPU cores (4 s of it loading the model; 4 s per further clip when imported),
    0.9 GB of memory. With noise added down to 10 dB SNR, at 64 kbps MP3 or at 0.9x-1.15x tempo: mean 22-26 ms.

Two things a caller must know:
  * LEAD_S. On that clip the TTS word-boundary times run ahead of the sound: after every pause the "true" start is
    about 100 ms (65-170 ms) before the first audible sound. The aligner finds the acoustic onset and subtracts LEAD_S so
    its times follow the same convention (a caption that lights up a moment early reads as in sync; one that
    lights up late does not). Pass --lead 0 (or lead=0) for the acoustic onset itself. Without the lead the same
    clip scores mean 93 ms against that truth, nearly all of it constant offset.
  * score. exp(mean log-probability of the word's letters), 0..1. Below LOW_SCORE the model did not clearly hear the
    word as spelled (typical for English words a voice says its own way, and for a clipped first word). The time is
    usually still right because the neighbours pin it; several low words in a row deserve a look. If more than
    half of all words are low the text does not belong to the audio and the script fails instead of answering.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import unicodedata

import numpy as np

# Hindi wav2vec2 CTC model (95 M parameters, 378 MB), trained on 4200 h by the Vakyansh team at EkStep.
# Licence: MIT — the model card front matter says "license: mit" (read on 2026-11-13). Commercial use is allowed.
# Not used on purpose: Meta MMS forced-alignment models (CC-BY-NC), ai4bharat/indicwav2vec-hindi (Apache-2.0 but gated),
# theainerd/Wav2Vec2-large-xlsr-hindi (card states no licence). Harveenchadha/hindi_large_wav2vec2 (Apache-2.0)
# was tested too: same accuracy, three times the size and run time.
MODEL_ID = "Harveenchadha/vakyansh-wav2vec2-hindi-him-4200"
MODEL_REVISION = "e2568c3f7868d8aa3aaabcf28fa100d10d54c170"   # pinned commit
MODEL_FILES = ["config.json", "vocab.json", "pytorch_model.bin"]
BLANK_TOKEN = "<s>"       # fairseq-style CTC: the blank is <s> (id 0), not the pad token the config names

SR = 16000
HOP = 320                 # samples per model frame (20 ms)
FRAME = HOP / SR

LEAD_S = 0.095            # output start = acoustic onset - LEAD_S (see the header)
SPIKE_LAG_S = 0.015       # the model writes a letter 15-20 ms after its sound begins (measured at phrase starts)
PAUSE_S = 0.30            # this long without a letter: the next word starts a new phrase
LOW_SCORE = 0.30          # words scoring below this are "not clearly heard"

# The model stops writing after a pause of about 0.5 s inside its input and misses the first word unless silence
# comes first. So the audio is cut at pauses and every piece gets digital silence in front.
MIN_PAUSE_S = 0.25        # pauses at least this long are cut out
KEEP_S = 0.10             # audio kept on each side of speech
SPEECH_DB = -40.0         # speech = 20 ms frame louder than (95th-percentile loudness + SPEECH_DB)
MAX_PIECE_S = 8.0         # longest piece for one model call (accuracy drops on long input)
SILENCE_IN_FRONT_S = 0.30
SILENCE_RMS = 3e-4        # below this (-70 dB full scale) a frame is silence whatever the rest of the file is like


class AlignError(RuntimeError):
    """Alignment cannot be done or cannot be trusted. The CLI prints the message and exits non-zero."""


# ================================================================================================
# 1. Text: one caller word → Devanagari pieces the model can spell
# ================================================================================================
_NUM = ("शून्य एक दो तीन चार पाँच छह सात आठ नौ दस ग्यारह बारह तेरह चौदह पंद्रह सोलह सत्रह अठारह उन्नीस "
        "बीस इक्कीस बाईस तेईस चौबीस पच्चीस छब्बीस सत्ताईस अट्ठाईस उनतीस तीस इकतीस बत्तीस तैंतीस चौंतीस पैंतीस छत्तीस सैंतीस अड़तीस उनतालीस "
        "चालीस इकतालीस बयालीस तैंतालीस चौवालीस पैंतालीस छियालीस सैंतालीस अड़तालीस उनचास पचास इक्यावन बावन तिरपन चौवन पचपन छप्पन सत्तावन अट्ठावन उनसठ "
        "साठ इकसठ बासठ तिरसठ चौंसठ पैंसठ छियासठ सड़सठ अड़सठ उनहत्तर सत्तर इकहत्तर बहत्तर तिहत्तर चौहत्तर पचहत्तर छिहत्तर सतहत्तर अठहत्तर उनासी "
        "अस्सी इक्यासी बयासी तिरासी चौरासी पचासी छियासी सत्तासी अट्ठासी नवासी नब्बे इक्यानवे बानवे तिरानवे चौरानवे पंचानवे छियानवे सत्तानवे अट्ठानवे निन्यानवे").split()
assert len(_NUM) == 100


def hindi_number(n: int) -> list[str]:
    """Cardinal number as Hindi words, Indian grouping: 1250 → एक हज़ार दो सौ पचास."""
    if n < 100:
        return [_NUM[n]]
    out = []
    for size, name in ((10_000_000, "करोड़"), (100_000, "लाख"), (1000, "हज़ार"), (100, "सौ")):
        if n >= size:
            out += hindi_number(n // size) + [name]
            n %= size
    return out + ([_NUM[n]] if n else [])


_LETTER = dict(zip("abcdefghijklmnopqrstuvwxyz", "ए बी सी डी ई एफ जी एच आई जे के एल एम एन ओ पी क्यू आर एस टी यू वी डब्ल्यू एक्स वाई ज़ेड".split()))
_SYMBOL = {"%": "परसेंट", "₹": "रुपये", "$": "डॉलर", "&": "एंड", "+": "प्लस", "@": "ऐट", "#": "हैशटैग"}

# Usual Hindi spellings of common English words (ad vocabulary first); looked up before the rules below.
# Plurals and -ed/-ing forms of listed words are derived. Alignment does not depend on this list (the rules alone
# give the same times on the test clip); it keeps the scores of well-heard English words high.
OVERRIDE = dict(kv.split("=") for kv in """
ad=ऐड ads=ऐड्स account=अकाउंट instagram=इंस्टाग्राम campaign=कैंपेन meta=मेटा customer=कस्टमर offer=ऑफर post=पोस्ट boost=बूस्ट
comment=कमेंट video=वीडियो save=सेव business=बिज़नेस machine=मशीन photo=फोटो budget=बजट click=क्लिक sale=सेल brand=ब्रांड
creative=क्रिएटिव create=क्रिएट creator=क्रिएटर facebook=फेसबुक whatsapp=व्हाट्सऐप youtube=यूट्यूब google=गूगल reel=रील story=स्टोरी
follower=फॉलोअर follow=फॉलो like=लाइक share=शेयर link=लिंक lead=लीड enquiry=इंक्वायरी inquiry=इंक्वायरी conversion=कन्वर्शन
audience=ऑडियंस target=टारगेट reach=रीच view=व्यू result=रिज़ल्ट report=रिपोर्ट cost=कॉस्ट price=प्राइस order=ऑर्डर
online=ऑनलाइन website=वेबसाइट page=पेज profile=प्रोफाइल message=मैसेज setup=सेटअप setting=सेटिंग structure=स्ट्रक्चर
festive=फेस्टिव diwali=दिवाली october=अक्टूबर week=वीक peak=पीक bid=बिड busy=बिज़ी edit=एडिट set=सेट plate=प्लेट
andromeda=एंड्रोमेडा personal=पर्सनल shopper=शॉपर switch=स्विच type=टाइप shelf=शेल्फ number=नंबर
algorithm=एल्गोरिदम update=अपडेट learning=लर्निंग phase=फेज़ scale=स्केल test=टेस्ट testing=टेस्टिंग data=डेटा pixel=पिक्सल
market=मार्केट marketing=मार्केटिंग agency=एजेंसी client=क्लाइंट product=प्रोडक्ट service=सर्विस office=ऑफिस shop=शॉप store=स्टोर
free=फ्री discount=डिस्काउंट festival=फेस्टिवल season=सीज़न trend=ट्रेंड viral=वायरल content=कंटेंट caption=कैप्शन hook=हुक
hashtag=हैशटैग manager=मैनेजर dashboard=डैशबोर्ड optimize=ऑप्टिमाइज़ performance=परफॉर्मेंस return=रिटर्न profit=प्रॉफिट
revenue=रेवेन्यू retarget=रीटारगेट retargeting=रीटारगेटिंग landing=लैंडिंग form=फॉर्म call=कॉल mobile=मोबाइल phone=फोन app=ऐप
payment=पेमेंट cash=कैश bank=बैंक loan=लोन money=मनी rupee=रुपी percent=परसेंट daily=डेली weekly=वीकली monthly=मंथली
the=द a=अ of=ऑफ to=टू do=डू you=यू your=योर one=वन two=टू is=इज़ are=आर was=वॉज़ this=दिस that=दैट with=विद they=दे
there=देयर their=देयर them=देम then=देन these=दीज़ those=दोज़ other=अदर what=व्हाट who=हू why=व्हाई how=हाउ now=नाउ
allow=अलाउ drive=ड्राइव five=फाइव arrive=अराइव have=हैव has=हैज़ give=गिव get=गेट live=लाइव love=लव move=मूव some=सम
come=कम done=डन only=ओनली any=एनी many=मेनी people=पीपल because=बिकॉज़ use=यूज़ user=यूज़र easy=ईज़ी ready=रेडी
great=ग्रेट design=डिज़ाइन music=म्यूज़िक visit=विज़िट future=फ्यूचर nature=नेचर sure=श्योर secure=सिक्योर minute=मिनट
hour=आवर our=आवर idea=आइडिया area=एरिया real=रियल school=स्कूल tech=टेक group=ग्रुप young=यंग touch=टच double=डबल
country=कंट्री control=कंट्रोल home=होम most=मोस्ट host=होस्ट study=स्टडी full=फुल push=पुश pull=पुल put=पुट
apply=अप्लाई reply=रिप्लाई supply=सप्लाई image=इमेज engine=इंजन ok=ओके okay=ओके hi=हाय hello=हेलो bye=बाय yes=येस no=नो
wow=वाओ sir=सर madam=मैडम please=प्लीज़ sorry=सॉरी thanks=थैंक्स roas=रोआस wifi=वाईफाई ecommerce=ईकॉमर्स email=ईमेल
upi=यूपीआई gst=जीएसटी emi=ईएमआई ai=एआई dm=डीएम ctr=सीटीआर cpm=सीपीएम cpc=सीपीसी cpa=सीपीए roi=आरओआई seo=एसईओ
ceo=सीईओ faq=एफएक्यू otp=ओटीपी sms=एसएमएस url=यूआरएल
""".split())
# short words that are words even in capitals (other capitals of up to three letters are read letter by letter)
_SHORT_WORDS = set("new now yes no top big buy get ads ad off on in up out all day pay win hot red app the and for you one two six ten go so do".split())

_VOW = {"A": ("अ", ""), "aa": ("आ", "ा"), "i": ("इ", "ि"), "ii": ("ई", "ी"), "u": ("उ", "ु"), "uu": ("ऊ", "ू"),
        "e": ("ए", "े"), "ai": ("ऐ", "ै"), "o": ("ओ", "ो"), "au": ("औ", "ौ"), "aw": ("ऑ", "ॉ")}
_K = "[b-df-hj-np-tv-xz]"       # a consonant letter (not y)
_KR = "[b-df-hj-np-qstv-xz]"    # a consonant letter other than r


def _prior_vowel(s, i):
    return bool(re.search(r"[aeiou]|(?<=.)y", s[:i]))


# English spelling → sounds, tried in order at the current position; the first match wins.
# Units: Devanagari consonants, vowel names from _VOW ("A" is the unwritten short a), N = anusvara.
# A function gets (word, position) and returns the units. Rough on purpose: consonants carry the alignment.
_RULES = [(re.compile(p), u) for p, u in [
    # endings and consonant groups
    (r"tion|ssion", "श A न"), (r"(?<=[aeiou])sion", "ज़ A न"), (r"sion", "श A न"),
    (r"[ct]ial", "श A ल"), (r"[ct]ious", "श A स"), (r"cian", "श A न"),
    (r"ture(?=s?$)", "च A र"), (r"sure$", "श A र"),
    (r"eigh", "e"), (r"igh", "aa i"), (r"ough", "aw"),
    (r"tch|ch", "च"), (r"sch", "स क"), (r"sh", "श"), (r"ph", "फ"), (r"th", "थ"), (r"^gh", "ग"), (r"gh", ""),
    (r"wh", "व"), (r"^wr", "र"), (r"^kn", "न"), (r"ck", "क"), (r"qu", "क व"), (r"q", "क"),
    (r"^x", "ज़"), (r"x", "क स"), (r"dge?(?=s?$)|dg", "ज"), (r"gn$|^gn", "न"), (r"mb$", "म"), (r"^ps", "स"),
    (r"gu(?=[aeiy])", "ग"), (r"gg", "ग"), (r"g(?=et|ear|irl|ive|ift)", "ग"), (r"ge$", "ज"), (r"g(?=[eiy])", "ज"), (r"g", "ग"),
    (r"cc(?=[eiy])", "क स"), (r"c(?=[eiy])", "स"), (r"cc?", "क"),
    (r"(?<=[aeiouy])n(?=[cdgjkqstxz])", "N"), (r"(?<=[aeiouy])m(?=[pb])", "N"),
    # a
    (r"a(?=ll)|al(?=k)", "aw"), (r"^a(?=(" + _K + r")\1?[aeiou])", "A"), (r"ai|ay", "e"), (r"au|aw", "aw"),
    (r"are$", "e य A र"), (r"(?<=[aeiouy]l)ar$", "A र"), (r"ar(?![aeiouy])", "aa र"),
    (r"a(?=" + _K + r"e[sd]?$)|a(?=" + _K + r"ing$)|a(?=ble|nge|ste$)", "e"),
    (r"(?<=[aeiouy]" + _K + r")a(?=n(t|ts|ce|cy)$)", "e"),
    (r"(?<=[aeiouy]" + _K + r")al$|(?<=[aeiou])al$", "A ल"), (r"a$", "aa"), (r"a", "ai"),
    # e
    (r"ear$", "i य A र"), (r"ear(?=" + _K + ")", "A र"), (r"ee|ea", "ii"),
    (r"(?<=[rlj])ew", "uu"), (r"eu|ew", "य uu"), (r"eo$", "i य o"), (r"ey$", "ii"), (r"ey", "e"), (r"ei", "ii"),
    (r"er$", "A र"), (r"er(?=" + _KR + ")", "A र"),
    (r"e$", lambda s, i: "" if _prior_vowel(s, i) else "ii"),
    (r"e(?=s$)", lambda s, i: "" if _prior_vowel(s, i) and s[i - 1] not in "sxzcg" and s[i - 2:i] not in ("ch", "sh") else "e"),
    (r"e(?=d$)", lambda s, i: "" if _prior_vowel(s, i) and s[i - 1] not in "td" else "e"),
    (r"e(?=ments?$)", lambda s, i: "" if i >= 2 and s[i - 2] in "aeiou" else "e"),
    (r"e(?=[lmn]$)", lambda s, i: "A" if _prior_vowel(s, i) else "e"),
    (r"e", "e"),
    # i
    (r"iew", "य uu"), (r"ign(?=s?$|ed$|ing$|ment)", "aa i न"),
    (r"ie$", lambda s, i: "ii" if _prior_vowel(s, i) else "aa i"), (r"ie(?=n)", "i e"), (r"ie", "ii"),
    (r"io$", "i य o"), (r"ial$", "i य A ल"), (r"ian$", "i य A न"), (r"ia", "i य aa"),
    (r"i(?=ves?$)", "i"), (r"i(?=" + _K + r"e[sd]?$)|i(?=nd$|ld$)", "aa i"),
    (r"ir(?=" + _KR + "|$)", "A र"), (r"i$", "ii"), (r"^i(?=" + _K + "[aeiou])", "aa i"), (r"i", "i"),
    # o
    (r"oo", "uu"), (r"ould", "u ड"), (r"ous$", "A स"), (r"our", "o र"), (r"ou", "aa u"),
    (r"ow(?=n|d|er|el)", "aa u"), (r"ow", "o"), (r"oa", "o"), (r"oi", "aw i"), (r"oy", "aw य"),
    (r"ore$", "o र"), (r"or$", lambda s, i: "A र" if _prior_vowel(s, i) else "aw र"),
    (r"(?<=w)or(?=" + _K + ")", "A र"), (r"or(?=" + _KR + ")", "aw र"),
    (r"o(?=" + _K + r"e[sd]?$)|o(?=ld)|o(?=lls?$)|o$", "o"),
    (r"o(?=[nm]$)", lambda s, i: "A" if _prior_vowel(s, i) else "aw"),
    (r"^o(?=" + _K + "[aeiou])", "o"), (r"o", "aw"),
    # u
    (r"ue$", lambda s, i: "" if s[i - 1:i] in ("g", "q") else ("uu" if s[i - 1:i] in ("r", "l") else "य uu")),
    (r"ui(?=l)", "i"), (r"ui", "uu"), (r"uy", "aa i"), (r"ure$", "A र"), (r"ur(?=" + _KR + "|$)", "A र"),
    (r"(?<=[rlj])u(?=" + _K + r"e[sd]?$)", "uu"), (r"u(?=" + _K + r"e[sd]?$)", "य uu"),
    (r"(?<=f)u(?=l$)", "u"), (r"u$", "uu"), (r"^u(?=ni|s[eua]|ti|tu)", "य uu"),
    (r"u(?=" + _K + "[aeiouy])|u(?=[aeio])", "u"), (r"u", "A"),
    # y
    (r"^y(?=[aeiou])", "य"), (r"(?<=f)y$", "aa ii"), (r"y$", lambda s, i: "ii" if _prior_vowel(s, i) else "aa i"),
    (r"y(?=" + _K + "e$)", "aa i"), (r"(?<=[aeiou])y", "य"), (r"y", "i"),
    # single consonants
    (r"(?<=" + _K + r")le(?=s?$)", "A ल"),
    (r"b", "ब"), (r"d", "ड"), (r"f", "फ"), (r"h", "ह"), (r"j", "ज"), (r"k", "क"), (r"l", "ल"), (r"m", "म"), (r"n", "न"),
    (r"p", "प"), (r"r", "र"), (r"s", "स"), (r"t", "ट"), (r"v", "व"), (r"w", "व"), (r"z", "ज़"),
]]


def transliterate(word: str) -> str:
    """Rough English spelling → Devanagari: "customer" → कस्टॉमर, "festive" → फेस्टिव. For alignment only."""
    s = re.sub(r"[^a-z]", "", word.lower())
    units, i = [], 0
    while i < len(s):
        if i + 1 < len(s) and s[i] == s[i + 1] and s[i] in "bdfklmnprstvz":   # doubled consonant = one sound
            i += 1
            continue
        for pat, u in _RULES:
            m = pat.match(s, i)
            if m:
                units += (u(s, i) if callable(u) else u).split()
                i = m.end()
                break
        else:
            i += 1
    out, prev = [], None
    for u in units:
        if u in _VOW:
            out.append(_VOW[u][1] if prev == "C" else _VOW[u][0])
            prev = "V"
        elif u == "N":
            out.append("्न" if prev == "C" else ("ं" if prev else "अं"))
            prev = "C" if prev == "C" else "V"
        else:
            out.append(("्" if prev == "C" else "") + u)
            prev = "C"
    return "".join(out)


def _latin(run: str):
    """Latin-script run → (Devanagari spelling, True if it came from the rough rules)."""
    low = run.lower()
    if low in OVERRIDE:
        return OVERRIDE[low], False
    for suffix in ("s", "es", "d", "ed", "ing"):                       # plural / verb form of a listed word
        stem = low[: -len(suffix)]
        if low.endswith(suffix) and len(stem) > 1 and stem in OVERRIDE:
            base = OVERRIDE[stem]
            after_vowel = unicodedata.category(base[-1]) != "Lo" or base[-1] in "अआइईउऊएऐओऔऑ"
            if suffix in ("s", "es"):
                tail = "ज़" if after_vowel else ("ेस" if base[-1] in "सजशच़" else "्स")
            elif suffix in ("d", "ed"):
                tail = "ड" if after_vowel else ("ेड" if base[-1] in "टड" else "्ड")
            else:
                tail = "इंग" if after_vowel else "िंग"
            return base + tail, False
    spelled_out = len(low) == 1 or not re.search(r"[aeiouy]", low) or (run.isupper() and len(run) <= 3 and low not in _SHORT_WORDS)
    if spelled_out:
        return "".join(_LETTER[c] for c in low), False
    return transliterate(low), True


_PIECE = re.compile(r"[ऀ-ॣ०-ॿ]+|[A-Za-z]+|\d+(?:[.,]\d+)*|[%₹$&+@#]")
_DEV_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")
_FOLD = {"ऍ": "ए", "ऎ": "ए", "ऒ": "ओ", "ॆ": "े", "ॊ": "ो", "ॠ": "ऋ", "ॐ": "ओम"}


def spoken_pieces(word: str) -> list[tuple[str, bool]]:
    """One caller word → [(Devanagari piece, rough)] in spoken order; [] when nothing in it is spoken.
    "टू-पॉइंट-ओ" → टू, पॉइंट, ओ · "accounts" → अकाउंट्स · "₹500" → पाँच, सौ, रुपये · "2.5" → दो, पॉइंट, पाँच."""
    w = unicodedata.normalize("NFC", word).translate(_DEV_DIGITS).replace("'", "").replace("’", "")
    w = re.sub(r"([₹$])\s*(\d+(?:[.,]\d+)*)", r"\2\1", w)                # "₹500" is said "पाँच सौ रुपये"
    out = []
    for m in _PIECE.finditer(w):
        p = m.group()
        if p[0].isdigit():
            whole, _, frac = p.replace(",", "").partition(".")
            out += [(x, False) for x in hindi_number(int(whole))]
            if frac:
                out += [("पॉइंट", False)] + [(_NUM[int(d)], False) for d in frac if d.isdigit()]
        elif p in _SYMBOL:
            out.append((_SYMBOL[p], False))
        elif p[0].isascii():
            out.append(_latin(p))
        else:                                                            # Devanagari; NFD splits ज़ into ज + nukta
            out.append(("".join(_FOLD.get(c, c) for c in unicodedata.normalize("NFD", p)), False))
    return out


# ================================================================================================
# 2. Audio, model, per-frame letter probabilities
# ================================================================================================
_loaded = None


def load_model():
    """(model, vocab), loaded once. AlignError with the reason if that is not possible."""
    global _loaded
    if _loaded is not None:
        return _loaded
    try:
        import torch  # noqa: F401  (checked here so a missing install gives the message below)
        from huggingface_hub import snapshot_download
        from transformers import Wav2Vec2ForCTC
        from transformers.utils import logging as hf_logging
    except Exception as e:  # noqa: BLE001
        raise AlignError(f"Python packages missing ({type(e).__name__}: {e}). Run scripts/setup_align.sh and call this "
                         "script with ~/.venvs/align/bin/python.") from e
    try:
        hf_logging.set_verbosity_error()
        hf_logging.disable_progress_bar()
        try:                                                            # the copy setup_align.sh downloaded
            path = snapshot_download(MODEL_ID, revision=MODEL_REVISION, allow_patterns=MODEL_FILES, local_files_only=True)
            if not all(os.path.exists(os.path.join(path, f)) for f in MODEL_FILES):
                raise FileNotFoundError("incomplete local copy")
        except Exception:  # noqa: BLE001
            path = snapshot_download(MODEL_ID, revision=MODEL_REVISION, allow_patterns=MODEL_FILES)
        with open(os.path.join(path, "vocab.json"), encoding="utf-8") as f:
            vocab = json.load(f)
        # use_safetensors=False: load exactly the pinned pytorch_model.bin (weights-only load), no extra download
        model = Wav2Vec2ForCTC.from_pretrained(path, use_safetensors=False, local_files_only=True).eval()
    except Exception as e:  # noqa: BLE001
        raise AlignError(f"cannot load the alignment model {MODEL_ID} (revision {MODEL_REVISION[:8]}): {type(e).__name__}: {e}\n"
                         "Run scripts/setup_align.sh once with network access, then retry.") from e
    if model.config.vocab_size != len(vocab) or vocab.get(BLANK_TOKEN) != 0 or "|" not in vocab or "क" not in vocab:
        raise AlignError(f"{MODEL_ID}: unexpected vocabulary; this script needs a Devanagari CTC model with blank {BLANK_TOKEN!r} and delimiter '|'")
    _loaded = (model, vocab)
    return _loaded


def load_audio(path: str) -> np.ndarray:
    """Any audio file → 16 kHz mono float32 (ffmpeg)."""
    if not os.path.isfile(path):
        raise AlignError(f"audio file not found: {path}")
    try:
        raw = subprocess.run(["ffmpeg", "-nostdin", "-loglevel", "error", "-i", str(path), "-ar", str(SR), "-ac", "1", "-f", "f32le", "-"],
                             capture_output=True, check=True).stdout
    except FileNotFoundError as e:
        raise AlignError("ffmpeg is not installed (needed to read the audio)") from e
    except subprocess.CalledProcessError as e:
        raise AlignError(f"ffmpeg could not read {path}: {' '.join(e.stderr.decode(errors='replace').split())[-300:]}") from e
    x = np.frombuffer(raw, dtype=np.float32)
    if len(x) < SR // 10:
        raise AlignError(f"{path}: no audio in the file")
    return x


def _rms(x: np.ndarray, hop: int, win: int) -> np.ndarray:
    """Loudness curve: RMS over `win` samples every `hop` samples."""
    p = np.convolve(x.astype(np.float64) ** 2, np.ones(win) / win, mode="same")
    return np.sqrt(p[: (len(x) // hop) * hop: hop] + 1e-12)


def speech_pieces(x: np.ndarray) -> list[tuple[int, int]]:
    """Stretches of audio to give the model, as (first frame, end frame) on the 20 ms grid: speech with KEEP_S around it,
    pauses of MIN_PAUSE_S or more left out, long stretches cut at their quietest frame."""
    e = _rms(x, HOP, HOP)
    idx = np.flatnonzero(e > max(np.percentile(e, 95) * 10 ** (SPEECH_DB / 20), SILENCE_RMS))
    if len(idx) == 0:
        return []
    gap, keep, limit = round(MIN_PAUSE_S / FRAME), round(KEEP_S / FRAME), round(MAX_PIECE_S / FRAME)
    runs, a, p = [], idx[0], idx[0]
    for i in idx[1:]:
        if i - p - 1 >= gap:
            runs.append((a, p + 1))
            a = i
        p = i
    runs.append((a, p + 1))
    out = []
    stack = [(max(0, a - keep), min(len(e), b + keep)) for a, b in runs][::-1]
    while stack:
        a, b = stack.pop()
        if b - a <= limit:
            out.append((int(a), int(b)))
            continue
        lo, hi = a + (b - a) // 4, b - (b - a) // 4
        c = lo + int(np.argmin(np.convolve(e[lo:hi], np.ones(5) / 5, mode="same")))
        stack += [(c, b), (a, c)]
    return out


def emissions(x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Letter log-probabilities for the speech frames: (logp [T, letters], frame number on the 20 ms grid [T]).
    Frames in cut-out pauses are not returned; nothing is spoken there."""
    import torch
    model, vocab = load_model()
    xp = np.concatenate([x, np.zeros(2 * HOP, np.float32)])
    e = _rms(xp, HOP, HOP)
    loud = e > max(np.percentile(e[: len(x) // HOP], 95) * 10 ** (SPEECH_DB / 20), SILENCE_RMS)
    z = round(SILENCE_IN_FRONT_S / FRAME)

    def run(a, b):
        seg = np.concatenate([np.zeros(z * HOP, np.float32), xp[a * HOP: b * HOP + 80]])
        seg = (seg - seg.mean()) / (seg.std() + 1e-7)
        with torch.inference_mode():
            lp = torch.log_softmax(model(torch.from_numpy(seg)[None]).logits[0], -1).numpy()
        return lp[z: z + b - a]

    lps, frames = [], []
    for a, b in speech_pieces(x):
        if b - a < 3:
            continue
        out = np.empty((b - a, len(vocab)), np.float32)
        start = a
        for _ in range(8):
            lp = run(start, b)
            out[start - a:] = lp
            # Safety net for a pause the cutting missed: the model has stopped writing but speech is left → run the rest again.
            wrote = np.flatnonzero(lp.argmax(1) != 0)
            last = start + (int(wrote[-1]) if len(wrote) else 0)
            hi = min(b - 5, last + 75)
            if loud[last + 10: b].sum() < 15 or (len(wrote) == 0 and start > a) or hi <= last + 3:
                break
            start = last + 2 + int(np.argmin(np.convolve(e[last + 2: hi], np.ones(5) / 5, mode="same")))
        lps.append(out)
        frames.append(np.arange(a, b))
    if not lps:
        raise AlignError("no speech found in the audio")
    return np.concatenate(lps), np.concatenate(frames)


# ================================================================================================
# 3. Forced alignment: Viterbi over the CTC trellis
# ================================================================================================
_MATRAS = "ािीुूृेैॅॉोौ"
_INDEP = "अआइईउऊएऐऑओऔ"
_SAME = ["िी", "ुू", "इई", "उऊ", "ँं"]              # spelling variants the model is free to choose between
_ROUGH_SAME = ["टत", "डद", "थठत", "सशष", "वब"]       # same, for letters that came from the rough English rules


def _letters(piece: str, vocab) -> list[str]:
    """Devanagari piece → the model's letters (longest match). Characters the model does not have are dropped."""
    out, i = [], 0
    while i < len(piece):
        two = piece[i: i + 2]
        if len(two) == 2 and two in vocab:
            out.append(two)
            i += 2
            continue
        if piece[i] in vocab and piece[i] != "|" and not piece[i].isascii():
            out.append(piece[i])
        i += 1
    return out


def _accept(letter: str, rough: bool, vocab) -> tuple[set, bool]:
    """Vocabulary ids that count as this letter, and whether the path may skip it."""
    ids, optional = {vocab[letter]}, letter == "़"                     # the nukta dot is often not written
    for group in _SAME + (_ROUGH_SAME if rough else []):
        if letter in group:
            ids |= {vocab[c] for c in group if c in vocab}
    if len(letter) == 2 and letter[1] == "़" and letter[0] in vocab:
        ids.add(vocab[letter[0]])
    if rough:                                                           # rule-made spelling: any vowel sign will do
        if letter in _MATRAS:
            ids |= {vocab[c] for c in _MATRAS if c in vocab}
            optional = True
        elif letter in _INDEP:
            ids |= {vocab[c] for c in _INDEP if c in vocab}
        elif letter == "्":
            optional = True
    return ids, optional


def _states(words, vocab):
    """The path to walk: blank, letter, blank, letter … with an optional word delimiter between words.
    Returns per state: accepted ids, optional flag, word index (-1 for blanks and delimiters)."""
    accept, optional, word_of = [{0}], [False], [-1]

    def add(ids, opt, w):
        accept.extend([ids, {0}])
        optional.extend([opt, False])
        word_of.extend([w, -1])

    for w, word in enumerate(words):
        for piece, rough in spoken_pieces(word):
            letters = _letters(piece, vocab)
            if not letters:
                continue
            if len(accept) > 1:
                add({vocab["|"]}, True, -1)
            for ch in letters:
                add(*_accept(ch, rough, vocab), w)
    return accept, optional, np.array(word_of)


def _viterbi(lp: np.ndarray, accept, optional):
    """Most probable path. Returns (state per frame, emission matrix [frames, states])."""
    T, S = len(lp), len(accept)
    if T * S > 400_000_000:
        raise AlignError(f"too much for one pass ({T} speech frames x {S} states); split the audio and the word list")
    E = np.empty((T, S), np.float32)
    for s, ids in enumerate(accept):
        ids = list(ids)
        E[:, s] = lp[:, ids[0]] if len(ids) == 1 else lp[:, ids].max(1)
    # Besides staying (0) and stepping (1): jump over a blank, and over optional letters, onto a letter.
    jumps = {}
    for s in range(1, S, 2):
        k = 2
        while s - k >= 0:
            if any(not optional[j] for j in range(s - k + 1, s) if j % 2):
                break
            if (s - k) % 2 == 0 or not (accept[s - k] & accept[s]):     # a repeated letter needs a blank in between
                jumps.setdefault(k, np.zeros(S, bool))[s] = True
            k += 1
    must = [s for s in range(1, S, 2) if not optional[s]]
    if not must:
        return np.zeros(T, np.int64), E
    if len(must) > T:
        raise AlignError(f"the text has more letters ({len(must)}) than the audio has speech frames ({T}): wrong audio or wrong text?")
    NEG = np.float32(-1e30)
    v = np.full(S, NEG, np.float32)
    v[: must[0] + 1] = E[0, : must[0] + 1]
    back = np.zeros((T, S), np.int8)
    c = np.empty(S, np.float32)
    for t in range(1, T):
        best, arg = v.copy(), back[t]
        c[0] = NEG
        c[1:] = v[:-1]
        m = c > best
        best[m], arg[m] = c[m], 1
        for k, allowed in jumps.items():
            c[:k] = NEG
            c[k:] = v[:-k]
            m = allowed & (c > best)
            best[m], arg[m] = c[m], k
        v = best + E[t]
    s = must[-1] + int(np.argmax(v[must[-1]:]))
    path = np.empty(T, np.int64)
    for t in range(T - 1, -1, -1):
        path[t] = s
        s -= int(back[t, s])
    return path, E


def _onset(env, thr, t):
    """Where sound begins before a phrase's first letter at time t: the first loud 5 ms step after 60 ms of quiet,
    looked for from 100 ms before t to 30 ms after it. None if there is no such point (e.g. a breath runs into the word)."""
    q = 12
    a = max(0, round((t - 0.10) / 0.005) - q)
    b = min(len(env), round((t + 0.03) / 0.005))
    quiet, found = (q if a == 0 else 0), None
    for i in range(a, b):
        if env[i] <= thr:
            quiet += 1
        else:
            if quiet >= q:
                found = i
            quiet = 0
    return None if found is None else found * 0.005


def _offset(env, thr, t):
    """Where sound ends after a phrase's last letter at time t: the start of the first 60 ms of quiet within 0.6 s."""
    q, quiet = 12, 0
    a = round(t / 0.005)
    for i in range(a, min(len(env), a + 120)):
        if env[i] <= thr:
            quiet += 1
            if quiet >= q:
                return (i - q + 1) * 0.005
        else:
            quiet = 0
    return None


def align_samples(x: np.ndarray, words: list[str], lead: float = LEAD_S) -> list[dict]:
    """Align `words` (spoken order) to 16 kHz mono float32 audio. One dict per word: w, start, end, score."""
    words = list(words)
    if not words:
        return []
    _, vocab = load_model()
    accept, optional, word_of = _states(words, vocab)
    n, duration = len(words), len(x) / SR
    first, last, score = [None] * n, [None] * n, [0.0] * n
    if len(accept) > 1:
        lp, frames = emissions(x)
        path, E = _viterbi(lp, accept, optional)
        w_at = np.where(path % 2 == 1, word_of[path], -1)               # word whose letter sits on each frame
        for w in np.unique(w_at[w_at >= 0]):
            t = np.flatnonzero(w_at == w)
            first[w], last[w] = frames[t[0]] * FRAME, frames[t[-1]] * FRAME
            score[w] = float(np.exp(np.mean([E[t[path[t] == s], s].max() for s in np.unique(path[t])])))
    heard = [w for w in range(n) if first[w] is not None]
    if len(heard) >= 8 and sum(score[w] < LOW_SCORE for w in heard) > len(heard) / 2:
        raise AlignError(f"{sum(score[w] < LOW_SCORE for w in heard)} of {len(heard)} words were not heard where the text puts them: "
                         "the words do not match this audio (wrong file, wrong order, or another language)")
    env = _rms(x, 80, 160)                                               # loudness every 5 ms
    thr = np.percentile(env, 95) * 10 ** (-35 / 20)
    start, end = [None] * n, [None] * n
    for k, w in enumerate(heard):                                        # starts
        opens = k == 0 or first[w] - last[heard[k - 1]] > PAUSE_S
        onset = _onset(env, thr, first[w]) if opens else None
        start[w] = max(0.0, (onset if onset is not None else first[w] - SPIKE_LAG_S) - lead)
        if k and start[w] < start[heard[k - 1]] + 0.02:
            start[w] = start[heard[k - 1]] + 0.02
    for k, w in enumerate(heard):                                        # ends: next word's start, or where the sound stops
        nxt = heard[k + 1] if k + 1 < len(heard) else None
        if nxt is not None and first[nxt] - last[w] <= PAUSE_S:
            end[w] = start[nxt]
        else:
            off = _offset(env, thr, last[w])
            end[w] = off if off is not None else last[w] + 0.10
            if nxt is not None:
                end[w] = min(end[w], start[nxt])
        end[w] = min(max(end[w], start[w] + 0.02), max(duration, start[w] + 0.02))
    # words with nothing to hear (punctuation, emoji): share the time between their neighbours
    i = 0
    while i < n:
        if start[i] is not None:
            i += 1
            continue
        j = i
        while j < n and start[j] is None:
            j += 1
        a = end[i - 1] if i else 0.0
        b = max(a, start[j] if j < n else min(duration, a + 0.3 * (j - i)))
        for k in range(i, j):
            start[k], end[k] = a + (b - a) * (k - i) / (j - i), a + (b - a) * (k - i + 1) / (j - i)
        i = j
    return [{"w": words[w], "start": round(float(start[w]), 3), "end": round(float(end[w]), 3), "score": round(score[w], 3)} for w in range(n)]


def align_file(audio_path: str, words: list[str], lead: float = LEAD_S) -> list[dict]:
    """Align `words` to an audio file (anything ffmpeg reads). Raises AlignError when it cannot be done."""
    return align_samples(load_audio(audio_path), words, lead)


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    lead = LEAD_S
    try:
        if "--lead" in argv:
            i = argv.index("--lead")
            lead = float(argv[i + 1])
            del argv[i: i + 2]
        if len(argv) != 3:
            raise IndexError
    except (IndexError, ValueError):
        print("usage: align_ctc.py AUDIO WORDS_JSON OUT_JSON [--lead SECONDS]", file=sys.stderr)
        return 2
    audio, words_json, out_json = argv
    try:
        try:
            with open(words_json, encoding="utf-8") as f:
                words = json.load(f)
        except (OSError, ValueError) as e:
            raise AlignError(f"cannot read the word list {words_json}: {e}") from e
        if not isinstance(words, list) or not all(isinstance(w, str) for w in words):
            raise AlignError(f"{words_json}: expected a JSON list of strings")
        result = align_file(audio, words, lead)
    except AlignError as e:
        print(f"align_ctc: {e}", file=sys.stderr)
        return 1
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    low = [r["w"] for r in result if r["score"] < LOW_SCORE]
    print(f"align_ctc: {len(result)} words aligned, {len(low)} with a low score" + (": " + " ".join(low) if low else ""), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
