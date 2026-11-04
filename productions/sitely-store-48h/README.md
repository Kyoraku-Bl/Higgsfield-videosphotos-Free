# sitely_studioo — "Your store online in 48 hours" · 18s Reel (clothing store)

Style preset: `productions/DEFAULT_VIDEO_STYLE.md`. Character: Reda / sitely_studioo.
Service: websites for small & medium businesses in 48 hours. Client: a clothing / pants store.

## Deliverables
| File | What |
|---|---|
| `sitely-store-48h-animatic.mp4` | 18s 9:16 animatic (1080×1920, 30fps, −16 LUFS) |
| `cover/instagram-cover.png` | Reel cover 9:16 |
| `cover/instagram-cover-grid.png` | 1:1 grid preview |
| `instagram-caption.md` | Caption + hashtags + posting notes |
| `keyframes/` | 5 start-frames for image-to-video |
| `audio/` | Dialogue stems (3 voices) |
| `video-prompts.md` | Per-shot I2V prompts |
| `subtitles.srt` / `timing.json` | Captions + locked timing |
| `build_animatic.py` / `make_cover.py` | Regenerate video / cover |

## Timeline
| Time | Shot | Audio |
|---|---|---|
| 0–3 | Hook walk through store | "Great clothes... but online, nobody knows you exist." + hook card |
| 3–8 | Laptop reveal at counter | "Give me 48 hours." / "A website? I can't afford that." / "Wait... those are my clothes?" |
| 8–10.2 | Phone order insert | VO "A clean online store, and sales start coming to you." + ping |
| 10.2–13 | Handshake, busy store | "Thanks, found you online!" |
| 13–18 | Selfie CTA | "Want your store online in 48 hours? DM '48H'." + end card |

## Regenerate
```bash
pip install --user imageio-ffmpeg numpy pillow fonttools brotli
python3 build_animatic.py && python3 make_cover.py
```
