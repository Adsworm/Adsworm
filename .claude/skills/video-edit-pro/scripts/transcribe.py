"""Local Whisper large-v3 transcription with word timestamps. Usage: transcribe.py <audio> <out.json> <lang|auto> [initial prompt]"""
import sys, json, time, wave
import numpy as np
from faster_whisper import WhisperModel
audio, out, lang = sys.argv[1], sys.argv[2], sys.argv[3]
prompt = sys.argv[4] if len(sys.argv) > 4 else None
t0 = time.time()
model = WhisperModel('large-v3', device='cpu', compute_type='int8', cpu_threads=4)
_w = wave.open(audio); assert _w.getframerate() == 16000 and _w.getnchannels() == 1 and _w.getsampwidth() == 2
pcm = np.frombuffer(_w.readframes(_w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
segs, info = model.transcribe(pcm, language=None if lang == 'auto' else lang, task='transcribe', beam_size=5, best_of=5,
                              word_timestamps=True, vad_filter=False, condition_on_previous_text=False, initial_prompt=prompt,
                              temperature=[0.0, 0.2, 0.4], no_speech_threshold=0.6)
res = {'language': info.language, 'language_probability': info.language_probability, 'duration': info.duration, 'segments': []}
for s in segs:
    res['segments'].append({'start': s.start, 'end': s.end, 'text': s.text, 'avg_logprob': s.avg_logprob, 'no_speech_prob': s.no_speech_prob,
                            'words': [{'w': w.word, 's': w.start, 'e': w.end, 'p': w.probability} for w in (s.words or [])]})
json.dump(res, open(out, 'w'), ensure_ascii=False, indent=1)
print(f'[{lang}] detected={info.language} p={info.language_probability:.2f} in {time.time()-t0:.0f}s')
for s in res['segments']: print(f"  {s['start']:6.2f}-{s['end']:6.2f}  ({s['avg_logprob']:.2f}) {s['text']}")
