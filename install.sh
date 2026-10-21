#!/usr/bin/env bash
# Adsworm Motion Studio installer — Claude Code skills, plugins and MCPs for coded motion,
# video editing and Meta ad creative.
#
#   ./install.sh                 core profile (recommended start)
#   ./install.sh core html taste install several profiles
#   ./install.sh all             everything below
#   ./install.sh --dry-run all   print the commands, change nothing
#
# Profiles
#   core     motion-studio (this repo) + Remotion official plugin + LottieFiles motion-design + ElevenLabs audio skills
#   html     HyperFrames (HeyGen, Apache-2.0) + GSAP official skills — the license-free second engine.
#            HyperFrames alone adds ~4.1k always-on tokens: between jobs, claude plugin disable hyperframes@hyperframes
#   taste    design-taste-frontend + Emil Kowalski animation skills — raises the visual ceiling
#   editing  video-use (footage cutdowns) + Kinocut MCP (headless ffmpeg editing)
#   genai    Runway skills + Higgsfield skills + fal MCP — AI footage for the hybrid lane
#   desktop  prints setup for DaVinci / Premiere / After Effects MCPs (need the desktop apps)
#
# Every skill you install is listed in Claude's context on every message, so third-party repos are
# filtered to the skills this workflow uses. Check cost with: claude plugin details <plugin>
set -uo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
marketplace_src="${ADSWORM_MARKETPLACE:-$here}"   # set to Adsworm/Adsworm to install from GitHub
dry=0
profiles=()
failed=()

for arg in "$@"; do
  case "$arg" in
    --dry-run) dry=1 ;;
    -h|--help) sed -n '2,22p' "$0"; exit 0 ;;
    all) profiles+=(core html taste editing genai desktop) ;;
    core|html|taste|editing|genai|desktop) profiles+=("$arg") ;;
    *) echo "unknown profile: $arg (see --help)"; exit 1 ;;
  esac
done
(( ${#profiles[@]} )) || profiles=(core)

run() {
  printf '→ %s\n' "$*"
  (( dry )) && return 0
  "$@" || { failed+=("$*"); printf '  ✗ failed, continuing\n'; }
}
skill() { run npx -y skills@latest add "$@" -a claude-code -g -y; }
plugin() { run claude plugin marketplace add "$1"; run claude plugin install "$2"; }
need() { command -v "$1" >/dev/null 2>&1 || { echo "missing: $1 — $2"; (( dry )) || exit 1; }; }

need claude "install Claude Code: https://code.claude.com"
need node "Node 22+ (HyperFrames needs 22): https://nodejs.org"
need ffmpeg "ffmpeg is required for rendering and QA"
node_major=$(node -p 'process.versions.node.split(".")[0]' 2>/dev/null || echo 0)
(( node_major >= 22 )) || echo "warning: Node $node_major detected — HyperFrames needs 22+"

for p in "${profiles[@]}"; do
  echo; echo "== $p"
  case "$p" in
    core)
      plugin "$marketplace_src" motion-studio@adsworm
      plugin remotion-dev/claude-code-plugin remotion@remotion
      skill LottieFiles/motion-design-skill
      skill elevenlabs/skills --skill text-to-speech sound-effects music speech-to-text dubbing
      ;;
    html)
      plugin heygen-com/hyperframes hyperframes@hyperframes
      skill greensock/gsap-skills --skill gsap-core gsap-timeline gsap-plugins gsap-performance
      echo "  tip: npx hyperframes telemetry disable"
      ;;
    taste)
      skill Leonxlnx/taste-skill --skill design-taste-frontend
      skill emilkowalski/skills --skill animate review-animations animation-vocabulary apple-design
      ;;
    editing)
      need git "git is required for video-use"
      dir="${VIDEO_USE_DIR:-$HOME/.local/share/video-use}"
      [[ -d "$dir" ]] || run git clone https://github.com/browser-use/video-use "$dir"
      run mkdir -p "$HOME/.claude/skills"
      run ln -sfn "$dir" "$HOME/.claude/skills/video-use"
      if command -v uv >/dev/null 2>&1; then run uv sync --project "$dir"; else echo "  install uv, then: uv sync --project $dir (video-use also needs an ElevenLabs key)"; fi
      run claude mcp add --scope user kinocut -- uvx --from kinocut kino --mcp
      ;;
    genai)
      plugin runwayml/skills runway-api@runway-dev
      skill higgsfield-ai/skills --skill higgsfield-generate higgsfield-product-photoshoot higgsfield-brandkit
      run claude mcp add --transport http --scope user fal https://mcp.fal.ai/mcp-relay
      echo "  then authenticate inside Claude Code with /mcp (fal), and connect Higgsfield/Runway accounts"
      ;;
    desktop)
      cat <<'EOF'
  Desktop-app MCPs (run on the editor's machine, not in a cloud container):
    DaVinci Resolve   npx davinci-resolve-mcp setup        (Studio: Preferences → General → External scripting = Local)
    Premiere Pro      claude plugin marketplace add leancoderkavy/premiere-pro-mcp
                      claude plugin install premiere-pro@premiere-pro-mcp
                      npx -y premiere-pro-mcp@1.24.3 --install-cep
    After Effects     github.com/Dakkshin/after-effects-mcp — npm run build && npm run install-bridge,
                      then open Window → mcp-bridge-auto.jsx in AE
    Blender (3D)      claude mcp add blender uvx mcp-for-blender
EOF
      ;;
  esac
done

echo
if (( ${#failed[@]} )); then
  echo "Done with ${#failed[@]} failure(s):"; printf '  ✗ %s\n' "${failed[@]}"; exit 1
fi
echo "Done. Start a new Claude Code session, then: /motion-studio:motion-director <your brief>"
echo "Already have remotion-best-practices synced from claude.ai? Disable one copy to avoid duplicate context."
