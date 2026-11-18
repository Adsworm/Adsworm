# Vendored copy

- **Source:** https://github.com/Moh4696/cinematic-skill, folder `skills/cinematic-film/`
- **Commit:** `bf435561c6203f90f971300efe952b68b5ec3417` (9 Nov 2026, v1.0.1)
- **Licence:** MIT, copyright 2026 exploraX. The full text is in `LICENSE` in this folder.
- **Copied on:** 18 Nov 2026

## Why a copy and not a live install

The project was nine days old with one author when it was added. This copy is the code that was read and tested; a live install would follow whatever is pushed upstream later.

## What was checked before copying

- All 16 scripts searched for shell, network, environment and file-delete calls. Found: ffmpeg and ffprobe calls; one `shell=True` in `tts_say.py`, used only when the caller passes their own `--cmd`; downloads in `get_fonts.py`, `make_map.py` and `fetch_commons.py` to GitHub, jsdelivr and Wikimedia Commons; deletes of the scripts' own temporary files.
- `SKILL.md` and the six reference files read for instructions that do not belong in a film skill (installs, uploads, credentials, outside links). None found.
- Starter project built and rendered end to end (25 s, 1280x720, 54 s).

## Changes from upstream

- `SKILL.md`: the `description` line is shorter, and an "Adsworm notes" section is added at the end. Nothing else is edited.
- `LICENSE` and this file are added.

## Updating

Read the upstream diff from the commit above to the new one, re-run the starter project, then copy the folder again and re-apply the two `SKILL.md` changes.
