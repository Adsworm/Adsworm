"""What a speech recogniser hears in each take, against the script. usage: heard_en.py PROJECT TAKES_DIR"""
import difflib, json, pathlib, re, sys
import numpy as np, soundfile as sf
from scipy.signal import resample_poly
from faster_whisper import WhisperModel

def load16(path):
    a, sr = sf.read(str(path), dtype='float32')
    a = a.mean(axis=1) if a.ndim > 1 else a
    return resample_poly(a, 16000, sr).astype(np.float32)
proj, takes = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
m = WhisperModel("small.en", device="cpu", compute_type="int8")
NUM = {"210": "two hundred and ten", "147": "one forty seven", "165": "one sixty five", "164": "one sixty four", "18": "eighteen", "15": "fifteen",
       "17": "seventeen", "13": "thirteen", "16": "sixteen", "5": "five", "1000": "a thousand", "3": "three", "2": "two", "%": " percent"}
def norm(s):
    s = s.lower().replace(",", "").replace("-", " ")
    s = re.sub(r"\d+|%", lambda x: " " + NUM.get(x.group(0), x.group(0)) + " ", s)
    return re.sub(r"[^a-z ]", " ", s).split()
tot = hit = 0
for take in json.loads((proj / "script.json").read_text())["takes"]:
    want = norm(" ".join(l["spoken"] for l in take["lines"]))
    segs, _ = m.transcribe(load16(takes / f"{take['take']}.wav"), language="en", beam_size=5, condition_on_previous_text=False)
    text = " ".join(s.text for s in segs); got = norm(text)
    sm = difflib.SequenceMatcher(a=want, b=got, autojunk=False)
    ok = sum(b.size for b in sm.get_matching_blocks()); tot += len(want); hit += ok
    miss = [(" ".join(want[i1:i2]), " ".join(got[j1:j2])) for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]
    print(f"{take['take']}: {ok}/{len(want)}", "| differs:", miss if miss else "none")
    print("   heard:", text.strip()[:400])
print(f"TOTAL {hit}/{tot}")
