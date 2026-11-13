#!/usr/bin/env bash
# video-edit-pro toolchain. Idempotent: re-running skips what exists.
# Usage: bash bootstrap.sh <workdir> [--light]     (--light = transcription + Remotion only, no torch stacks)
# Every step below ran successfully on a 4-core, CPU-only Linux container (Python 3.11-3.13, Node 22).
set -euo pipefail
export VEP_WORK_HINT="Scripts read venvs/models from VEP_WORK=<workdir>"
W="${1:?usage: bootstrap.sh <workdir> [--light]}"; LIGHT="${2:-}"
SKILL="$(cd "$(dirname "$0")/.." && pwd)"
mkdir -p "$W/venvs" "$W/models/sr" "$W/models/hf"
say(){ printf '\n== %s\n' "$*"; }
command -v ffmpeg >/dev/null || { echo "ffmpeg missing: install it first (apt-get install -y ffmpeg)"; exit 1; }
command -v uv >/dev/null || { echo "uv missing: curl -LsSf https://astral.sh/uv/install.sh | sh"; exit 1; }

say "Transcription: faster-whisper + large-v3"
if [ ! -x "$W/venvs/asr/bin/python" ]; then uv venv -q --python 3.13 "$W/venvs/asr"; uv pip install -q --python "$W/venvs/asr/bin/python" faster-whisper==1.2.1; fi
HF_HOME="$W/models/hf" "$W/venvs/asr/bin/python" -c "from huggingface_hub import snapshot_download as s; print(s('Systran/faster-whisper-large-v3'))"

say "Remotion overlay project"
if [ ! -d "$W/remotion/node_modules" ]; then
  mkdir -p "$W/remotion" && cp -r "$SKILL/remotion/." "$W/remotion/"
  (cd "$W/remotion" && npm install --no-audit --no-fund --loglevel=error && npx remotion browser ensure >/dev/null && npx tsc --noEmit)
fi

if [ "$LIGHT" = "--light" ]; then say "light install done"; exit 0; fi

say "Voice: ClearVoice MossFormer2 (Apache-2.0)"
if [ ! -x "$W/venvs/cv/bin/python" ]; then uv venv -q --python 3.11 "$W/venvs/cv"
  uv pip install -q --python "$W/venvs/cv/bin/python" --index-url https://download.pytorch.org/whl/cpu torch torchaudio
  uv pip install -q --python "$W/venvs/cv/bin/python" clearvoice==0.1.2 soundfile; fi

say "Voice: DeepFilterNet3 + WPE (light denoise / experiments)"
if [ ! -x "$W/venvs/dfn/bin/python" ]; then uv venv -q --python 3.11 "$W/venvs/dfn"
  uv pip install -q --python "$W/venvs/dfn/bin/python" --index-url https://download.pytorch.org/whl/cpu "torch==2.1.2+cpu" "torchaudio==2.1.2+cpu"
  uv pip install -q --python "$W/venvs/dfn/bin/python" "numpy<2" deepfilternet==0.5.6 soundfile scipy nara_wpe; fi
if [ ! -d "$W/models/dfn/DeepFilterNet3" ]; then mkdir -p "$W/models/dfn"
  curl -sSL -o "$W/models/dfn/DeepFilterNet3.zip" https://raw.githubusercontent.com/Rikorose/DeepFilterNet/main/models/DeepFilterNet3.zip
  python3 -I -c "import zipfile,sys; z=zipfile.ZipFile(sys.argv[1]); assert not [n for n in z.namelist() if n.startswith('/') or '..' in n]; z.extractall(sys.argv[2])" "$W/models/dfn/DeepFilterNet3.zip" "$W/models/dfn"; fi

say "Picture: Real-ESRGAN general x4v3 via spandrel (BSD-3, safetensors)"
if [ ! -x "$W/venvs/enh/bin/python" ]; then uv venv -q --python 3.11 "$W/venvs/enh"
  uv pip install -q --python "$W/venvs/enh/bin/python" --index-url https://download.pytorch.org/whl/cpu "torch==2.1.1+cpu" "torchvision==0.16.1+cpu"
  uv pip install -q --python "$W/venvs/enh/bin/python" spandrel==0.4.2 safetensors "numpy<2" pillow; fi
[ -s "$W/models/sr/realesr-general-x4v3.safetensors" ] || curl -sSL -o "$W/models/sr/realesr-general-x4v3.safetensors" https://huggingface.co/OzzyGT/RealESRGAN_general_x4v3/resolve/main/model.safetensors

say "Fonts available to Pillow-based scripts"
mkdir -p "$W/fonts" && cp "$SKILL"/remotion/public/fonts/* "$W/fonts/"

say "done: $W"
du -sh "$W/venvs" "$W/models" 2>/dev/null || true
