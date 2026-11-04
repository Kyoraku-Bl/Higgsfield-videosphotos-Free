#!/usr/bin/env python3
"""Build the 18s vertical animatic for the sitely_studioo clothing-store 48h reel."""
import json, os, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.abspath(__file__))
AUDIO = os.path.join(ROOT, "audio"); KEY = os.path.join(ROOT, "keyframes")
FONTS = os.path.join(ROOT, "fonts"); BUILD = os.path.join(ROOT, "build_animatic")
os.makedirs(BUILD, exist_ok=True)
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SR = 44100; FPS = 30; TOTAL = 18.0; W, H = 1080, 1920
CREAM = (245, 239, 224); GREEN = (30, 77, 56)


def run(cmd):
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr[-4000:])
    return p


def read_wav(path):
    with wave.open(path) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768.0


def write_wav(path, data):
    pcm = (np.clip(data, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())


def trim_silence(data, rel=0.02, pad=0.035):
    peak = np.max(np.abs(data))
    if peak == 0:
        return data
    win = int(0.01 * SR)
    energy = np.convolve(np.abs(data), np.ones(win) / win, mode="same")
    idx = np.where(energy > rel * peak)[0]
    if len(idx) == 0:
        return data
    return data[max(0, idx[0] - int(pad * SR)):min(len(data), idx[-1] + int(pad * SR))]


LINES = [
    ("reda-01-hook.wav", 0.50, 3.90, 1.35, "Great clothes... but online, nobody knows you exist.", {"nobody", "exist."}),
    ("reda-02-48h.wav", 3.95, 5.30, 1.30, "Give me 48 hours.", {"48", "hours."}),
    ("owner-01-afford.wav", 5.40, 7.50, 1.30, "A website? I can't afford that.", {"afford"}),
    ("owner-02-my-clothes.wav", 7.60, 9.10, 1.30, "Wait... those are my clothes?", {"my", "clothes?"}),
    ("reda-03-voiceover.wav", 9.20, 12.20, 1.20, "A clean online store, and sales start coming to you.", {"online", "store,", "sales"}),
    ("customer-thanks.wav", 12.30, 13.60, 1.20, "Thanks, found you online!", {"online!"}),
    ("reda-04-cta-v2.wav", 13.70, 17.20, 1.20, "Want your store online in 48 hours? DM '48H'.", {"48", "hours?", "'48H'."}),
]

print("== dialogue timing ==")
processed = []; prev_end = 0.0
for fname, want, max_end, max_tempo, text, keywords in LINES:
    raw = trim_silence(read_wav(os.path.join(AUDIO, fname)))
    dur = len(raw) / SR
    start = max(want, prev_end + 0.08)
    tempo = min(max_tempo, max(1.0, dur / max(0.3, max_end - start)))
    tp = os.path.join(BUILD, "trim_" + fname); write_wav(tp, raw)
    op = os.path.join(BUILD, "fit_" + fname)
    if tempo > 1.001:
        run([FFMPEG, "-y", "-i", tp, "-filter:a", f"atempo={tempo:.4f}", op])
    else:
        write_wav(op, raw)
    final = read_wav(op); fdur = len(final) / SR; end = start + fdur; prev_end = end
    processed.append(dict(file=fname, start=start, end=end, tempo=tempo, text=text,
                          keywords=sorted(keywords), samples=final))
    print(f"  {fname:28s} {start:5.2f} -> {end:5.2f}  (tempo {tempo:.2f})")

print("== ambience bed ==")
rng = np.random.default_rng(11); n = int(TOTAL * SR); t = np.arange(n) / SR; bed = np.zeros(n)


def add(sig, at, gain=1.0):
    a = int(at * SR); b = min(n, a + len(sig)); bed[a:b] += sig[: b - a] * gain


noise = rng.standard_normal(n); brown = np.cumsum(noise)
brown -= np.convolve(brown, np.ones(2000) / 2000, mode="same"); brown /= np.max(np.abs(brown)) + 1e-9
bed += brown * 0.013
mur = rng.standard_normal(n); k = int(0.004 * SR)
mur = np.convolve(mur, np.ones(k) / k, mode="same")
mur -= np.convolve(mur, np.ones(int(0.05 * SR)) / int(0.05 * SR), mode="same")
mur /= np.max(np.abs(mur)) + 1e-9
bed += mur * 0.010 * (0.7 + 0.3 * np.sin(2 * np.pi * 0.21 * t))


def blip(freqs, decays, dur, gains):
    tt = np.arange(int(dur * SR)) / SR; s = np.zeros_like(tt)
    for f, d, g in zip(freqs, decays, gains):
        s += g * np.sin(2 * np.pi * f * tt) * np.exp(-d * tt)
    return s


add(blip([1568, 2093], [9, 10], 0.55, [0.22, 0.12]), 8.45)          # order ping
click = rng.standard_normal(int(0.03 * SR)) * np.exp(-np.arange(int(0.03 * SR)) / (0.006 * SR))
add(click, 3.30, 0.18)                                             # laptop click
add(blip([2400, 3200], [6, 7], 0.5, [0.06, 0.04]), 9.20)           # door bell
add(blip([160, 300], [18, 24], 0.2, [0.2, 0.08]), 10.30)           # bag on counter
rustle = rng.standard_normal(int(0.5 * SR))
rustle -= np.convolve(rustle, np.ones(5) / 5, mode="same")
env = np.minimum(np.arange(len(rustle)) / (0.1 * SR), 1) * np.minimum((len(rustle) - np.arange(len(rustle))) / (0.25 * SR), 1)
add(rustle * env, 10.9, 0.03)                                      # fabric rustle

mix = bed.copy()
for p in processed:
    a = int(p["start"] * SR); b = min(n, a + len(p["samples"]))
    mix[a:b] += p["samples"][: b - a] * 0.95
mix *= 0.89 / np.max(np.abs(mix))
master_path = os.path.join(BUILD, "master.wav"); write_wav(master_path, mix)
print("  master.wav written")


def patch_font(src, family, dst):
    f = TTFont(src); ps = family.replace(" ", "") + "-Regular"
    for rec in f["name"].names:
        if rec.nameID in (1, 16): rec.string = family
        elif rec.nameID in (2, 17): rec.string = "Regular"
        elif rec.nameID == 4: rec.string = family + " Regular"
        elif rec.nameID == 6: rec.string = ps
    f.save(dst)


patch_font(os.path.join(FONTS, "Montserrat-800.ttf"), "MontserratSub", os.path.join(FONTS, "MontserratSub.ttf"))

SUB_SIZE = 64; SUB_Y = 1560
font_pil = ImageFont.truetype(os.path.join(FONTS, "Montserrat-800.ttf"), SUB_SIZE)
SPACE = font_pil.getlength(" ")


def clean(w): return w.strip(".,!?...'\"").lower()


def phrases_for(line):
    words = line["text"].split(); groups, cur = [], []
    for w in words:
        trial = cur + [w]
        width = sum(font_pil.getlength(x) for x in trial) + SPACE * (len(trial) - 1)
        if width > 980 and cur:
            groups.append(cur); cur = [w]
        else:
            cur = trial
    if cur: groups.append(cur)
    return groups


def word_times(line, words):
    weights = []
    for w in words:
        wt = max(2, len(clean(w))) + 1
        if w.endswith((",", "...", "?", ".")): wt += 1.2
        weights.append(wt)
    total = sum(weights); span = line["end"] - line["start"]; times, acc = [], line["start"]
    for wt in weights:
        times.append(acc); acc += span * wt / total
    return times


ass_events = []; srt_blocks = []; srt_i = 1
for line in processed:
    groups = phrases_for(line); all_words = line["text"].split(); all_times = word_times(line, all_words)
    idx = 0
    for gi, g in enumerate(groups):
        ws = all_words[idx:idx + len(g)]; ts = all_times[idx:idx + len(g)]; idx += len(g)
        phrase_end = all_times[idx] - 0.02 if gi + 1 < len(groups) else line["end"] + 0.04
        width = sum(font_pil.getlength(x) for x in ws) + SPACE * (len(ws) - 1)
        x = (W - width) / 2; centers = []
        for w in ws:
            ww = font_pil.getlength(w); centers.append(x + ww / 2); x += ww + SPACE
        for w, wt, cx in zip(ws, ts, centers):
            key = clean(w) in {clean(k) for k in line["keywords"]}
            style = r"\an5\pos(%d,%d)\fad(40,0)\fscx70\fscy70\t(0,90,\fscx100\fscy100)" % (cx, SUB_Y)
            if key: style += r"\3c&H00384D1E&\bord8"
            ass_events.append((wt, phrase_end, "{%s}%s" % (style, w)))
        def srt_ts(s):
            ms = int(round(s * 1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
        srt_blocks.append(f"{srt_i}\n{srt_ts(ts[0])} --> {srt_ts(phrase_end)}\n{' '.join(ws)}\n"); srt_i += 1


def ass_ts(s):
    cs = int(round(s * 100)); return f"{cs//360000}:{cs//6000%60:02d}:{cs//100%60:02d}.{cs%100:02d}"


ass_header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Reels,MontserratSub,{SUB_SIZE},&H00E0EFF5,&H00E0EFF5,&H00141414,&H00000000,0,0,0,0,100,100,0,0,1,3,0,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ass_body = "\n".join(f"Dialogue: 0,{ass_ts(a)},{ass_ts(b)},Reels,,0,0,0,,{txt}" for a, b, txt in ass_events)
ass_path = os.path.join(BUILD, "subs.ass")
with open(ass_path, "w") as f: f.write(ass_header + ass_body + "\n")
with open(os.path.join(ROOT, "subtitles.srt"), "w") as f: f.write("\n".join(srt_blocks))
with open(os.path.join(ROOT, "timing.json"), "w") as f:
    json.dump([{k: v for k, v in p.items() if k != "samples"} for p in processed], f, indent=2)
print("== subtitles written ==")


def make_card(lines_spec, path, size=76):
    fnt = ImageFont.truetype(os.path.join(FONTS, "Montserrat-900.ttf"), size)
    pad_x, pad_y, gap = 44, 30, 14
    widths = [fnt.getlength(s) for s, _ in lines_spec]
    cw = int(max(widths) + pad_x * 2); ch = int(size * 1.25 * len(lines_spec) + gap * (len(lines_spec) - 1) + pad_y * 2)
    img = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, cw - 1, ch - 1], radius=26, fill=GREEN + (235,))
    y = pad_y
    for s, col in lines_spec:
        wpx = fnt.getlength(s); d.text(((cw - wpx) / 2, y), s, font=fnt, fill=col + (255,)); y += size * 1.25 + gap
    img.save(path); return cw, ch


hook_path = os.path.join(BUILD, "card_hook.png"); end_path = os.path.join(BUILD, "card_end.png")
make_card([("THIS STORE IS", CREAM), ("INVISIBLE ONLINE", CREAM)], hook_path, 66)
make_card([("Your website.", CREAM), ("In 48 hours.", CREAM)], end_path, 80)

SEGMENTS = [
    ("shot1-hook.png", 3.0, "1.0+0.12*on/{N}", 10, 0),
    ("shot2-laptop-reveal.png", 5.0, "1.0+0.09*on/{N}", 4, 0),
    ("shot3a-phone-order.png", 2.2, "1.0+0.16*on/{N}", 2, 0),
    ("shot3b-handshake.png", 2.8, "1.10", 6, 60),
    ("shot4-selfie-cta.png", 5.0, "1.10-0.08*on/{N}", 14, 0),
]
inputs = []; filters = []
for i, (img, secs, zexpr, amp, drift) in enumerate(SEGMENTS):
    inputs += ["-i", os.path.join(KEY, img)]
    frames = int(round(secs * FPS)); last = frames - 1; zexpr = zexpr.replace("{N}", str(last))
    x = f"(iw-iw/zoom)/2+{amp}*sin(on*0.35)+{amp*0.6}*sin(on*0.9)"
    if drift: x += f"+(on/{last}-0.5)*{drift}"
    y = f"(ih-ih/zoom)/2+{amp*0.8}*cos(on*0.29)+{amp*0.5}*sin(on*0.77)"
    filters.append(f"[{i}:v]scale=2160:3840:flags=lanczos,zoompan=z='{zexpr}':x='{x}':y='{y}':d={frames}:s={W}x{H}:fps={FPS},setsar=1[v{i}]")
concat_in = "".join(f"[v{i}]" for i in range(len(SEGMENTS)))
filters.append(f"{concat_in}concat=n={len(SEGMENTS)}:v=1:a=0[vc]")
filters.append(f"[vc]subtitles={ass_path}:fontsdir={FONTS}[vs]")
ci = len(SEGMENTS)
inputs += ["-loop", "1", "-t", str(TOTAL), "-framerate", str(FPS), "-i", hook_path]
inputs += ["-loop", "1", "-t", str(TOTAL), "-framerate", str(FPS), "-i", end_path]
filters.append(f"[{ci}:v]format=rgba,fade=t=in:st=0.05:d=0.12:alpha=1[hook]")
filters.append(f"[{ci+1}:v]format=rgba,fade=t=in:st=17.15:d=0.20:alpha=1[endc]")
filters.append("[vs][hook]overlay=x=(W-w)/2:y='88-22*max(0\\,1-(t-0.05)/0.18)':enable='between(t,0.05,2.95)'[v1]")
filters.append("[v1][endc]overlay=x=(W-w)/2:y=1210:enable='gte(t,17.15)'[v2]")
filters.append("[v2]noise=alls=5:allf=t+u,vignette=angle=PI/5.5,eq=saturation=1.06:contrast=1.03,colorbalance=rs=0.02:bs=-0.02[vout]")
ai = ci + 2; inputs += ["-i", master_path]
out = os.path.join(ROOT, "sitely-store-48h-animatic.mp4")
cmd = [FFMPEG, "-y"] + inputs + ["-filter_complex", ";".join(filters), "-map", "[vout]", "-map", f"{ai}:a",
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000",
    "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-pix_fmt", "yuv420p",
    "-c:a", "aac", "-b:a", "192k", "-r", str(FPS), "-t", str(TOTAL), "-movflags", "+faststart", out]
print("== rendering video ==")
run(cmd)
print("DONE:", out, os.path.getsize(out), "bytes")
