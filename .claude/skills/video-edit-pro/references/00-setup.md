# 00 · Setup

`setup/bootstrap.sh <workdir>` creates everything below inside `<workdir>`. It is idempotent: it skips what already exists and prints what it did. Every command in it ran successfully on a 4-core CPU-only Linux container (Python 3.11–3.13, Node 22).

| Environment | Contents | Used for |
|---|---|---|
| `venvs/asr` (py3.13) | faster-whisper 1.2.1 + Whisper large-v3 (≈3 GB, Hugging Face) | Transcripts, word timings, word-accuracy checks |
| `venvs/dfn` (py3.11) | torch 2.1.2+cpu, deepfilternet 0.5.6, numpy<2, scipy, nara_wpe | Light denoise, de-reverb experiments |
| `venvs/cv` (py3.11) | ClearVoice 0.1.2 (MossFormer2_SE_48K, Apache-2.0) | Main speech enhancement |
| `venvs/enh` (py3.11) | torch 2.1.1+cpu, spandrel 0.4.2, safetensors | Real-ESRGAN detail plates |
| `models/dfn/DeepFilterNet3` | From `raw.githubusercontent.com/Rikorose/DeepFilterNet/main/models/DeepFilterNet3.zip` | DFN weights (github.com release links are blocked by the proxy; raw works) |
| `models/sr/` | `OzzyGT/RealESRGAN_general_x4v3` model.safetensors (BSD-3) | AI detail |
| `remotion/` | This skill's `remotion/` template + `npm install` + `npx remotion browser ensure` | Captions, titles, end cards |

Install traps that cost time:
- **DeepFilterNet:** install PyTorch from the CPU index first, then deepfilternet from PyPI. A combined install fails on index ordering.
- **faster-whisper 1.2.1 with PyAV 19:** `decode_audio` breaks. `scripts/transcribe.py` reads the WAV itself and passes samples to the model.
- **spandrel:** needs `torchvision==0.16.1+cpu` to match torch 2.1.1; use `--index-strategy unsafe-best-match`.
- **Remotion:** render with `--color-space=bt709`, or the overlay is untagged and colours shift when composited.
- **Licence:** Remotion is free for individuals and companies of up to 3 people; above that a Company Licence is required. Check the headcount before using it commercially.

Other tools registered as skills on the first job (clone them again in a new container if needed; see `08-tools.md`): video-use, rea-video, video-shotcraft, openmotion, moviepy.

Network notes for cloud sessions: Hugging Face, PyPI, npm, raw.githubusercontent.com and Google Drive public downloads (`drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t`) work. YouTube blocks transcript and video access from cloud IPs.
