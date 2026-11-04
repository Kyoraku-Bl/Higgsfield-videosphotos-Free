# Default video style — sitely_studioo hybrid cinematic reel

Locked as the default style for future video requests unless the user explicitly overrides it.
Reference production: `productions/sitely-cafe-18s/`.

> Note: the latest attached image available in the workspace was the E2B 403 screenshot, not a new
> visual reference. This preset therefore locks the style of the delivered café reel. If a different
> reference is intended, replace this file with the new style bible.

## 1. Core look

- **Format:** vertical 9:16, 1080×1920, 30 fps, short-form ad/reel energy.
- **Hybrid rule:** exactly ONE stylized 3D cel-shaded anime-style character inside a 100% photoreal,
  real-world environment. Everything else is photographic live-action: location, people, objects,
  screens, light, textures, reflections.
- **Character:** sitely_studioo / Reda — 18-year-old guy, voluminous short dark curly hair, brown
  eyes, tan skin, slim athletic build, black oversized hoodie, black cargo pants, white-grey
  sneakers. Always attach `productions/sitely-cafe-18s/reference/character-sheet.png`.
- **Integration:** the stylized character casts real soft shadows, receives real window light and
  color bounce, reflects in glass/screens, and matches footage grain, lens blur, depth of field and
  exposure. No illustrated backgrounds, no CGI city, no second stylized person.

## 2. Performance

- Full-body motion-capture realism: heel-to-toe walking, weight shifts, hip/shoulder rotation, head
  turns before body turns, hands gesturing while speaking.
- Feet planted, no sliding, correct contact shadows.
- Hoodie/cargo fabric folds, swings and settles naturally.
- Natural lip-sync with small imperfections, blinking, micro-expressions, eyebrow raises, breathing,
  asymmetric smile.
- Confident, relaxed, slightly cool teenager energy. Never robotic, stiff or cartoonish.
- Real eye contact with lens in selfie shots; correct eyelines to people/objects otherwise.

## 3. Living world

- Every real person has a purpose: staff working, customers entering/leaving, typing, laughing,
  handing objects, reacting naturally.
- Background depth layers: foreground, midground, background. Street motion through windows:
  pedestrians, cyclists, cabs.
- Steam, dust, door bells, light shifts as people pass.
- Real people do not look at the camera except when motivated; only sitely_studioo breaks lens in
  selfie/CTA shots.

## 4. Camera & grade

- Cinematic smartphone look: handheld natural shake, motivated moves (tracking follow, push-in, whip
  pan, OTS, shot/reverse-shot), shallow depth of field, real bokeh, subtle film grain, slightly
  imperfect framing.
- Warm natural window light, soft volumetric rays, dust in air.
- Palette: **black, cream, dark green** (`#1E4D38` green, `#F5EFE0` cream).
- Authentic UGC energy with cinema-level blocking.

## 5. Audio

- Real location ambience + realistic SFX (clicks, pings, cups, footsteps, doors, machines).
- **No music** by default.
- Natural voices with room tone. Main character voice stays consistent across all shots.
- Loudness target around −16 LUFS, true peak ≤ −1.5 dBTP.

## 6. Text & captions

- Bold Instagram Reels-style subtitles, animated word-by-word, bottom third.
- Cream text with dark-green highlight on keywords.
- Font: Montserrat ExtraBold/Black.
- Hook card early, end card with CTA/brand line.
- Default end-card style: short declarative brand promise, e.g. “Your website. Done for you.”

## 7. Default deliverable package

For each new video request, produce:

1. **Animatic MP4** — frame-accurate previz with keyframes, camera moves, dialogue mix, subtitles,
   hook/end cards, placeholder ambience/SFX.
2. **Instagram cover** — a 9:16 cover image (1080×1920) with bold hook text, safe for the 1:1 grid
   crop, in the same black/cream/dark-green palette.
3. **Instagram caption** — ready-to-post copy with hook line, value, CTA and line breaks/emojis.
4. **Hashtags** — a tuned set (mix of broad + niche + local + service tags) for the page.
5. **Keyframes** — one start-frame per shot/beat, character-matched to the sheet.
6. **Video-generation prompts** — per-shot I2V prompts + global style/negative blocks + model routing.
7. **Dialogue stems** — consistent voices, timed to the edit.
8. **Subtitles** — SRT + word-by-word ASS if burned.
9. **Timing sheet** — locked timeline JSON/README.
10. **Working direct links** — publish/share via public GitHub raw links or a deployed static host,
    not a protected E2B sandbox URL.

## 8. Global negative prompt

```
illustrated background, cartoon environment, CGI city, extra stylized characters, identity drift,
face morphing, foot sliding, floating feet, stiff robotic motion, cartoonish physics, lip-sync drift,
dead eyes, text artifacts, gibberish signage, watermark, logo, slow motion, music, soundtrack
```

## 9. Override rule

If the user provides a new reference image, script, brand, city, character, palette, or format, treat
that as an explicit override for that request only. Otherwise use this preset.
