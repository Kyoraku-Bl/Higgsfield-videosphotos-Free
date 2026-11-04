# Image-to-video shot prompts — sitely_studioo café reel (18s, 9:16)

Upload the shot's **start-frame** + `reference/character-sheet.png` with every generation.
Prepend the GLOBAL STYLE block to every prompt; append the NEGATIVE block where the model supports it.
Generate at the model's native duration (5s / 10s) and trim to the locked timeline in `README.md`.

---

## GLOBAL STYLE (prepend to every shot)

```
Cinematic hybrid live-action + 3D, shot like a scene from a real movie. Exactly ONE stylized
character: an 18-year-old guy, voluminous short dark curly hair, brown eyes, tan skin, slim athletic
build, black oversized hoodie, black cargo pants, white-grey sneakers — 3D cel-shaded anime look,
clean linework, matching the reference sheet exactly. He is the ONLY stylized element inside a 100%
photoreal, real-world coffee shop in Williamsburg, Brooklyn. He casts real soft shadows, receives
real window light and color bounce, reflects in glass, and matches the footage's grain, lens blur,
depth of field and exposure. Full-body motion-capture realism: natural heel-to-toe gait, weight
shifts, hip/shoulder rotation, head turns before body turns, feet planted with no sliding, hoodie and
cargo fabric folding and settling, natural blinking, micro-expressions, breathing, asymmetric smile,
accurate lip-sync. Every real person has a purpose: baristas steaming milk, customers walking in and
out, someone typing, a couple laughing, pedestrians / yellow cabs / cyclists outside the window.
No one looks at the camera except the stylized character in selfie shots. Vertical 9:16, handheld
smartphone cinema look, motivated camera moves, shallow depth of field with real bokeh, subtle film
grain. Warm natural window light, soft volumetric rays, dust in the air. Grade: black, cream, dark
green. Real café ambience, no music.
```

## NEGATIVE (append where supported)

```
illustrated background, cartoon environment, CGI city, extra stylized characters, identity drift,
face morphing, foot sliding, floating feet, stiff robotic motion, cartoonish physics, lip-sync drift,
dead eyes, text artifacts, gibberish signage, watermark, logo, slow motion, music, soundtrack,
character sheet, reference sheet, printed sheet, paper in hand, paper in pocket, poster, name tag,
stats label, text on clothing, collage, multiple character views, turnaround panels
```

> The character sheet is a HIDDEN style reference only — it must never appear inside any frame.

---

## SHOT 1 · HOOK — trim to 0.00–3.00 (generate 5s)

**Start-frame:** `keyframes/shot1-hook.png` · **Camera:** handheld tracking follow → push-in

```
The camera is already moving. Tracking shot follows the stylized teen walking fast through the busy
café, weaving between real customers and staff; a real barista carrying cups sidesteps behind him
shouting "Behind you!" and he dodges with a smooth full-body sidestep, weight shifting onto his lead
foot. He spins to face the camera and keeps walking backward, gesturing with one hand, and says with
energy: "Your business is open... but online, nobody can find you." Eyebrow raise on "nobody".
Behind him, the real owner in a dark green apron stares at an empty phone search screen and shakes
his head. Natural handheld shake, slight motion blur on background people, he stays sharp.
```

**Dialogue (audio-native models):** barista (off-screen): "Behind you!" · Reda: "Your business is
open... but online, nobody can find you."
**Edit note:** the hook line J-cuts to 3.76s over shot 2 — keep his backward walk alive through the cut.

## SHOT 2 · THE REVEAL — trim to 3.00–8.00 (generate 8–10s, or two 5s clips)

**Start-frame:** `keyframes/shot2-laptop-reveal.png` · **Camera:** OTS → push-in on owner

```
Inside the real café. The stylized teen slides into a wooden table, opens the real laptop and says to
the owner: "Give me five minutes." The real owner — man in his 40s, dark green apron, stubble, flour
on his forearm — stands with arms crossed and says: "I don't have time for this." Over-the-shoulder
shot between them. The teen turns the laptop toward him with a smooth hand gesture; on the real
screen, a clean modern café website with menu prices in dollars, food photos and a green WhatsApp
order button. Slow push-in on the owner's face: worried, then a raised brow, then a slow nod. He
uncrosses his arms and says: "Wait... that's my café?" The teen leans back with a small confident
smile. Real laptop click, ceramic cups on wood, warm window light.
```

**Dialogue:** Reda: "Give me five minutes." · Owner: "I don't have time for this." · Owner:
"Wait... that's my café?"
**Split option:** 2A = slide-in + "five minutes" + owner refusal (OTS); 2B = laptop turn + owner
reaction push-in. **Post:** corner-pin the real mockup screen recording onto the laptop display.

## SHOT 3a · PHONE INSERT — trim to 8.00–10.20 (generate 5s)

**Start-frame:** `keyframes/shot3a-phone-order.png` · **Camera:** macro insert, near-stable

```
Extreme close-up of a real smartphone in a real hand inside the café. The café website loads
instantly; a real thumb scrolls the menu and taps the green WhatsApp order button. A "New order"
notification slides onto the top of the screen with a soft ping. Real glass reflections, real skin
texture. In the creamy bokeh background the stylized teen and the real owner talk at the wooden
table; background customers move naturally. Shallow depth of field, subtle handheld drift.
```

**Audio:** notification ping at 8.45 · Reda VO over the whole montage (same voice as on camera):
"A simple, fast website and customers start coming to you."

## SHOT 3b · THE PAYOFF — trim to 10.20–13.00 (generate 5s)

**Start-frame:** `keyframes/shot3b-handshake.png` · **Camera:** wide tracking, lateral drift

```
Wide tracking shot: the real café is now full. The owner laughs and hands a paper cup of coffee to a
real customer, who says "Thanks, found you online!" The owner turns and gives the stylized teen a
firm handshake that turns into a hug — real physical contact, weight and shoulder momentum. The teen
grins, relaxed. Behind them: barista steaming milk, couple laughing, someone typing, steam rising
from cups, a yellow cab and a cyclist passing the storefront window. Feet planted, correct contact
shadows, fabric settling.
```

**Dialogue:** customer: "Thanks, found you online!" · Reda VO continues over the cut.

## SHOT 4 · SELFIE CTA — trim to 13.00–18.00 (generate 5s)

**Start-frame:** `keyframes/shot4-selfie-cta.png` · **Camera:** selfie, arm's-length, gentle sway

```
Selfie angle in the busy café, owner and real customers moving behind him. The stylized teen looks
straight into the lens with real eye contact, smiles slightly — genuine, a bit shy — and says:
"Want a website for your business? DM 'FREE' to get your free mockup." Natural lip-sync with small
imperfections, natural blinking, breathing. The real owner leans into frame behind him, waves and
gives a thumbs up. Authentic UGC selfie energy, slight wide-angle distortion, warm window light,
subtle handheld sway.
```

**Dialogue:** Reda: "Want a website for your business? DM 'FREE' to get your free mockup."
**Post:** end card "Your website. Done for you." from 17.15s; captions per `subtitles.srt`.

---

## Model routing (via this repo's studios / MuAPI)

| Model | Use | Audio |
|---|---|---|
| **Veo 3.x** | First choice for shots 1, 2, 4 — speaks the dialogue + native ambience | Native dialogue/SFX; still replace ambience in the mix for consistency |
| **Kling 2.x** | Start-frame + motion prompt, strong human motion | Silent — use `audio/` stems + Lip Sync studio for Reda's on-camera lines |
| **Seedance / Hailuo** | Fast alternates for inserts (3a) and crowd motion (3b) | Silent — stems in the edit |
| **Wan 2.x (local)** | Free local drafts via the repo's local inference | Silent — stems in the edit |

**Consistency rules:** always attach the character sheet; never let a second stylized person enter
frame; keep Reda's voice identical in every shot; real people never address the lens; no music
anywhere. Swap the city by replacing "Williamsburg, Brooklyn" and the street cues (yellow cabs) in
the GLOBAL STYLE block.
