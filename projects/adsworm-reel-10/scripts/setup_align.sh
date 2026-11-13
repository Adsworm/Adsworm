#!/usr/bin/env bash
# One-time setup for scripts/align_ctc.py (word timing for karaoke captions). Safe to run again; asks nothing.
#
#   bash scripts/setup_align.sh
#
# 1. creates the virtualenv ~/.venvs/align (override with ALIGN_VENV=/some/path)
# 2. installs CPU-only PyTorch, transformers, numpy and huggingface_hub into it   (about 1.2 GB)
# 3. downloads the alignment model named at the top of align_ctc.py              (about 0.4 GB, Hugging Face cache)
# 4. loads the model once to prove the install works
#
# Tested with Python 3.13, torch 2.15.0+cpu, transformers 5.23.0, numpy 2.5.4, huggingface_hub 2.4.0.
# Proxy and certificate settings come from the environment (HTTPS_PROXY, PIP_CERT, SSL_CERT_FILE); nothing is changed here.
set -euo pipefail

VENV="${ALIGN_VENV:-$HOME/.venvs/align}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

say() { echo "setup_align: $*"; }
die() { echo "setup_align: $*" >&2; exit 1; }

command -v python3 >/dev/null || die "python3 not found"
command -v ffmpeg >/dev/null || die "ffmpeg not found (align_ctc.py reads audio with it)"
[ -f "$HERE/align_ctc.py" ] || die "align_ctc.py is not next to this script"

if [ ! -x "$VENV/bin/python" ]; then
  say "creating virtualenv $VENV"
  mkdir -p "$(dirname "$VENV")"
  python3 -m venv "$VENV" || die "could not create the virtualenv (on Debian/Ubuntu: apt install python3-venv)"
fi
PY="$VENV/bin/python"
PIP=("$PY" -m pip --no-input --disable-pip-version-check)

if ! "$PY" -c "import torch" >/dev/null 2>&1; then
  say "installing PyTorch (CPU build)"
  "${PIP[@]}" install --quiet torch --index-url https://download.pytorch.org/whl/cpu
fi
if ! "$PY" -c "import transformers, numpy, huggingface_hub" >/dev/null 2>&1; then
  say "installing transformers, numpy, huggingface_hub"
  "${PIP[@]}" install --quiet transformers numpy huggingface_hub
fi

say "fetching and loading the model"
ALIGN_DIR="$HERE" PYTHONDONTWRITEBYTECODE=1 "$PY" - <<'PY'
import os, sys
sys.path.insert(0, os.environ["ALIGN_DIR"])
import align_ctc as a

try:   # uses the local copy when it is complete, downloads the pinned revision otherwise
    model, vocab = a.load_model()
except a.AlignError as e:
    sys.exit(f"setup_align: {e}")
import torch, transformers
print(f"setup_align: ok - {a.MODEL_ID} ({sum(p.numel() for p in model.parameters()) / 1e6:.0f} M parameters, {len(vocab)} letters), "
      f"torch {torch.__version__}, transformers {transformers.__version__}")
PY
say "ready:  $PY $HERE/align_ctc.py AUDIO WORDS_JSON OUT_JSON"
