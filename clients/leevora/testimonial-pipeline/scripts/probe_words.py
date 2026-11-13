"""Transcribe many short windows of one file with a single model load. Used to locate word boundaries at edit points
without trusting one long-context pass (the language model fills in plausible words).
Usage: probe_words.py <16k mono s16 wav> a-b [a-b ...]"""
import sys, wave, numpy as np
from faster_whisper import WhisperModel
w = wave.open(sys.argv[1]); assert w.getframerate() == 16000 and w.getnchannels() == 1
x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
m = WhisperModel('large-v3', device='cpu', compute_type='int8', cpu_threads=3)
pad = np.zeros(int(0.4 * 16000), dtype=np.float32)
for spec in sys.argv[2:]:
    a, b = map(float, spec.split('-')); seg = x[int(a * 16000):int(b * 16000)].copy()
    n = min(160, len(seg) // 4); seg[:n] *= np.linspace(0, 1, n); seg[-n:] *= np.linspace(1, 0, n)
    segs, _ = m.transcribe(np.concatenate([pad, seg, pad]), language='en', beam_size=5, word_timestamps=False, vad_filter=False, condition_on_previous_text=False, temperature=0.0, no_speech_threshold=0.9)
    print(f'  {a:6.2f}-{b:6.2f}  ->  ' + ' '.join(s.text.strip() for s in segs), flush=True)
