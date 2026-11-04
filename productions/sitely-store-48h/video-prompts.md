# Image-to-video shot prompts — clothing store "48 hours" reel (18s, 9:16)

Upload each start-frame + `reference/character-sheet.png`. Prepend GLOBAL STYLE, append NEGATIVE.
See `productions/DEFAULT_VIDEO_STYLE.md` for the full style bible. Generate 5s/10s, trim to timeline.

## GLOBAL STYLE (prepend)
```
Cinematic hybrid live-action + 3D. Exactly ONE stylized 3D cel-shaded anime character (18yo guy,
voluminous short dark curly hair, brown eyes, tan skin, black oversized hoodie, black cargo pants,
white-grey sneakers, matching the reference sheet) inside a 100% photoreal real streetwear clothing
store. He is the only stylized element: real soft shadows, window/spot light and color bounce, glass
and screen reflections, matching grain, lens blur, depth of field, exposure. Full-body mocap realism,
feet planted no sliding, fabric folds and settles, natural blinking and lip-sync. Real customers and
staff move with purpose; street motion through the window. Vertical 9:16, handheld smartphone cinema,
shallow bokeh, subtle grain. Warm light, palette black/cream/dark green. Real store ambience, no music.
```

## NEGATIVE (append)
```
illustrated background, cartoon environment, CGI city, extra stylized characters, identity drift,
face morphing, foot sliding, floating feet, stiff robotic motion, lip-sync drift, dead eyes, text
artifacts, gibberish signage, watermark, logo, slow motion, music, soundtrack, character sheet,
reference sheet, printed sheet, paper in hand, paper in pocket, poster, name tag, stats label, text on
clothing, collage, multiple character views, turnaround panels
```

> The character sheet is a HIDDEN style reference only — it must never appear inside any frame.

## SHOT 1 · HOOK (0–3) — `keyframes/shot1-hook.png`
Tracking follow: teen walks fast down the aisle between clothing racks, dodges a real customer,
spins to lens walking backward, eyebrow raise, says: "Great clothes... but online, nobody knows you
exist." Behind him the real owner folds clothes and shakes his head. Handheld, slight motion blur.

## SHOT 2 · REVEAL (3–8) — `keyframes/shot2-laptop-reveal.png`
OTS at the counter. Teen opens laptop: "Give me 48 hours." Owner (40s, stubble, dark green apron),
arms crossed: "A website? I can't afford that." Teen turns laptop showing a clean streetwear store
site (product grid, $ prices, green Shop/WhatsApp button). Push-in on owner: brow raise, slow nod,
uncrosses arms: "Wait... those are my clothes?" Teen leans back, small confident smile.

## SHOT 3a · PHONE (8–10.2) — `keyframes/shot3a-phone-order.png`
Macro insert: real hand, real phone, clothing site loads instantly, thumb taps green Shop button,
"New order" notification slides in with a ping. Teen + owner blurred in background bokeh.

## SHOT 3b · PAYOFF (10.2–13) — `keyframes/shot3b-handshake.png`
Wide tracking: store busy, owner hands a paper bag to a real customer who says "Thanks, found you
online!" Owner turns and gives the teen a firm handshake into a hug. Real contact and weight.

## SHOT 4 · CTA (13–18) — `keyframes/shot4-selfie-cta.png`
Selfie, direct lens eye contact, genuine slightly shy smile: "Want your store online in 48 hours?
DM '48H'." Owner leans in behind, waves + thumbs up. End card "Your website. In 48 hours."

## Model routing
Veo 3.x for dialogue shots (1,2,4); Kling/Wan/Seedance + Lip Sync for silent renders; use `audio/`
stems for consistency. Always attach the character sheet; keep one stylized person; no music.
