# Plan: reel engine v2 + series (English, international)

## Diagnosis of reel 03
1. **Copy of someone else's module.** Two avatars under a card is the reference reel's format, not ours.
2. **Language.** Hinglish caps the audience to India; the account's winners are English AI-news reels.
3. **Motion is static.** The card is fixed, avatars stand still, and nothing moves through space.
4. **Voice.** Each line was synthesised separately and sped up 40%, so it sounds stitched.
5. **Avatar ≠ Aman.** It had glasses and a thin face; Aman has a full beard, swept hair and no glasses.

## What the data says
@amanrai.official: the AI-tool news reels got **55K and 48K views**. The Meta-ads and clinic tips reels got **60–700**. Make AI and creative-tech news the hook, and use the agency lens as the edge: "what this means for your ad spend and CPA". Other AI-news pages don't have that lens.

## The new format: "AMAN'S AI DESK" (ours, not borrowed)
- **One infinite canvas, a flying camera.** Each beat is a "room" on a 3D canvas. The camera glides, tilts and zooms between rooms with motion blur. There are no cuts and no static card. Built with CSS 3D perspective, springs and `@remotion/motion-blur`.
- **Live UI, not screenshots.** The product or announcement is rebuilt in React: Ads Manager panels, the tool's interface, dashboards whose numbers count up. The source stays as a small receipt chip, so every claim still has proof.
- **Aman as the guide.** A face-matched 3D-style avatar (olive hoodie, beard, no glasses) walks into frame, points at and reacts to the UI, and can pop up as a small "picture-in-picture" bubble.
- **New sparring partner: "THE ALGORITHM".** A glowing coded orb character (SVG, morphs while it talks) replaces the generic female founder. It voices what the platform "thinks", and Aman translates that into money. The orb is memorable and easy to repeat across episodes, and it costs no image credits.
- **Structure (45–55 s):** result-first hook (0–2 s) → "here's why" in 3 rooms → agency verdict (spend/CPA impact) → CTA (comment a keyword for the guide).

## Voice
- **ElevenLabs v4 dialogue through Higgsfield.** The whole script goes in **one call**, which is the fix for the stitched sound. It costs about 5 credits per reel. Word timings come from local Whisper, so captions stay synced.
- **Best option: Aman's own cloned voice.** He records 1–2 minutes of clean, natural English once in the Higgsfield voice widget. Every reel then speaks in his voice.
- **Free fallback:** edge-tts `en-US-AndrewMultilingualNeural` with the full paragraph in one call.

## Series plan (the account is more than just Aman)
| Series | Hook pattern | Why |
|---|---|---|
| **AI Tool Verdict** | "I tested X on a real ad account. Here's the verdict." Expectation vs reality, scored | Matches the account's proven winners |
| **Meta Decoded** | "Meta quietly changed 3 things before Q4" | Agency authority; global framing (BFCM + Diwali) |
| **The Algorithm Says** | The orb explains why an ad died | Recurring character people return for |
| **60-Second Ad Teardown** | Famous global ad decoded (hook rate, offer, edit) | International appeal, shareable |
| **Receipts** | Anonymised Adsworm client results on the canvas | Lead generation for the agency |

## Pilot: reel 04 = "Meta quietly changed 3 things before Q4" (English remake of 03 on engine v2)
It uses the same verified receipts (Advantage+ image-to-video, GEM +18.9%, WhatsApp pricing), re-scripted for a global audience. It's built first because the facts are already verified. Then comes episode 1 of AI Tool Verdict.

## Cost and token budget
- Credits: avatar sheets about 6, voice about 5 per reel, plus about 1 for a test. Under 15 credits per reel.
- Agents: one low-cost reviewer per storyboard with a short verdict. No parallel agent swarms.
- Context lives in `docs/CONTEXT.md`. Start new work from that file, not from the long chat.

## Owner inputs needed
1. A 1–2 minute voice recording in the Higgsfield "Create Voice" widget, to use your own voice. Optional: until then the preset voice is used.
2. Approval of the avatar look.
3. A Go on the pilot topic, or a different first topic.

## Reviewer changes (adopted)
1. **The hook is a stake, not a topic.** "Meta just changed how your ads get made, and your CPA will feel it by Black Friday." Frame 1 is a ticking counter or the orb reacting. "3 things" lives in a progress rail.
2. **The orb is the spine.** Each room ends with an "ALGORITHM SAYS → AMAN TRANSLATES" snap, for example "I reward variety" → "Ship 20 creatives, not 3". It's quotable and shareable.
3. **Camera moves are punctuated, not a constant glide.** The camera hard-stops with a 0.4 s hold on each key number. One pattern-interrupt at about 20 s: a whip, a hit, or Aman breaking the fourth wall.
4. **Runtime is 35–40 s, not 55 s.** The last line loops back into the hook so the reel replays. CTA: a comment keyword plus a pinned reply.
5. **UI mocks carry an "illustrative" tag.** Only sourced numbers are shown as real. The Meta and IG chrome is generic, not a replica. The post is labelled AI-generated in Instagram.
