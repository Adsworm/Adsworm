"""Transcribe several files with one model load; print text and word-level differences against a reference."""
import sys, subprocess, re, difflib, numpy as np
from faster_whisper import WhisperModel
ref = sys.argv[1].lower().split(); m = WhisperModel('large-v3', device='cpu', compute_type='int8', cpu_threads=4)
for p in sys.argv[2:]:
    x = np.frombuffer(subprocess.run(['ffmpeg', '-v', 'error', '-t', '34.06', '-i', p, '-ac', '1', '-ar', '16000', '-af', 'dynaudnorm=f=500:g=31:p=0.5', '-f', 'f32le', '-'], capture_output=True).stdout, dtype=np.float32)
    segs, _ = m.transcribe(x, language='en', beam_size=5, vad_filter=False, condition_on_previous_text=False, temperature=0.0)
    hyp = re.sub(r"[^a-z' ]", ' ', ' '.join(s.text for s in segs).lower()).split()
    ops = [(t, ' '.join(ref[i1:i2]), ' '.join(hyp[j1:j2])) for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ref, hyp).get_opcodes() if t != 'equal']
    print(f"{p.split('/')[-1]:26s} {len(hyp)} words, {len(ops)} differences: " + ' | '.join(f"[{a}]->[{b}]" for _, a, b in ops), flush=True)
