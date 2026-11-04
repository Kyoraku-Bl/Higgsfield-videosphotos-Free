#!/usr/bin/env python3
"""Build the 4-reel Sitely Studio campaign. Each reel: 18s 9:16, persistent brand badge,
hook/end cards, word-by-word captions, ambience. Reel 4 gets a night grade."""
import json, os, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
PROD = os.path.dirname(ROOT)
AUDIO = os.path.join(ROOT, "audio")
FONTS = os.path.join(PROD, "_shared", "fonts")
BRAND = os.path.join(PROD, "brand")
import imageio_ffmpeg
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SR = 44100; FPS = 30; TOTAL = 18.0; W, H = 1080, 1920
CREAM = (245, 239, 224); GREEN = (30, 77, 56)


def run(c):
    p = subprocess.run(c, capture_output=True, text=True)
    if p.returncode != 0: raise RuntimeError(p.stderr[-3500:])
    return p


def rw(p):
    with wave.open(p) as w: return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(float)/32768.0


def ww(p, d):
    with wave.open(p, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(d, -1, 1)*32767).astype(np.int16).tobytes())


def trim(d, rel=.02, pad=.035):
    pk = np.max(np.abs(d))
    if pk == 0: return d
    e = np.convolve(np.abs(d), np.ones(int(.01*SR))/int(.01*SR), "same")
    i = np.where(e > rel*pk)[0]
    return d[max(0, i[0]-int(pad*SR)):min(len(d), i[-1]+int(pad*SR))] if len(i) else d


CTA = ("cta-site.wav", 12.5, 17.2, 1.2, "Want your business online in 48 hours? DM SITE for a free mockup.", {"48", "SITE", "mockup."})
REELS = [
 dict(id="reel-1-speed", night=False,
   hook=["LIVE IN", "48 HOURS"], end=["Your website.", "In 48 hours."],
   cover=["YOUR WEBSITE", "LIVE IN 48H"],
   lines=[("r1-hook.wav", .5, 4.2, 1.3, "Your website. Live in 48 hours.", {"website.", "48", "hours."}),
          ("r1-middle.wav", 6.0, 9.6, 1.3, "Send your logo today. Go live in two days.", {"logo", "two", "days."}), CTA]),
 dict(id="reel-2-invisible", night=False,
   hook=["INVISIBLE", "ONLINE?"], end=["Be found.", "Get customers."],
   cover=["STOP BEING", "INVISIBLE ONLINE"],
   lines=[("r2-hook.wav", .5, 4.4, 1.3, "They search. They find your competitor. Not you.", {"competitor.", "Not", "you."}),
          ("r2-middle.wav", 6.5, 9.0, 1.3, "A website puts you on the map.", {"website", "map."}), CTA]),
 dict(id="reel-3-affordable", night=False,
   hook=["TOO", "EXPENSIVE?"], end=["Simple. Fast.", "Affordable."],
   cover=["A WEBSITE THAT", "FITS YOUR BUDGET"],
   lines=[("r3-hook.wav", .5, 2.8, 1.3, "A website doesn't cost a fortune.", {"fortune."}),
          ("r3-owner.wav", 3.2, 5.4, 1.3, "But agencies charge thousands!", {"thousands!"}),
          ("r3-reply.wav", 6.0, 9.8, 1.3, "Not with me. Simple, fast, affordable.", {"affordable."}), CTA]),
 dict(id="reel-4-247", night=True,
   hook=["OPEN", "24/7"], end=["Sells while", "you sleep."],
   cover=["SELLS WHILE", "YOU SLEEP"],
   lines=[("r4-hook.wav", .5, 4.8, 1.3, "Your shop closes at six. Your website sells at 2 AM.", {"closes", "2", "AM."}),
          ("r4-middle.wav", 6.5, 8.6, 1.3, "Orders while you sleep.", {"Orders", "sleep."}), CTA]),
]
SEGS = [("hook.png", 5.5, "1.0+0.10*on/{N}", 8, 0),
        ("demo.png", 6.5, "1.0+0.09*on/{N}", 4, 0),
        ("cta.png", 6.0, "1.08-0.06*on/{N}", 12, 0)]

font_sub = ImageFont.truetype(os.path.join(FONTS, "Montserrat-800.ttf"), 64)
SPACE = font_sub.getlength(" ")
clean = lambda w: w.strip(".,!?...'\"").lower()


def card(lines, path, size=72, logo=None):
    f = ImageFont.truetype(os.path.join(FONTS, "Montserrat-900.ttf"), size)
    px, py, gap = 44, 30, 14
    tw = max(f.getlength(s) for s in lines)
    logo_w = 120 if logo else 0
    cw = int(tw + px*2 + logo_w + (gap if logo else 0))
    ch = int(size*1.25*len(lines) + gap*(len(lines)-1) + py*2)
    img = Image.new("RGBA", (cw, ch), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, cw-1, ch-1], 26, fill=GREEN+(235,))
    x0 = px
    if logo:
        lg = Image.open(logo).convert("RGBA").resize((100, 100), Image.LANCZOS)
        img.alpha_composite(lg, (px, (ch-100)//2)); x0 = px + 100 + gap
    y = py
    for s in lines:
        d.text((x0, y), s, font=f, fill=CREAM+(255,)); y += size*1.25 + gap
    img.save(path)


for reel in REELS:
    rd = os.path.join(ROOT, reel["id"]); B = os.path.join(rd, "build"); os.makedirs(B, exist_ok=True)
    print("==", reel["id"], "==")
    processed = []; prev = 0.0
    for fn, want, me, mt, text, kw in reel["lines"]:
        raw = trim(rw(os.path.join(AUDIO, fn))); dur = len(raw)/SR
        st = max(want, prev+.08); tempo = min(mt, max(1.0, dur/max(.3, me-st)))
        tp = os.path.join(B, "t_"+fn); ww(tp, raw); op = os.path.join(B, "f_"+fn)
        if tempo > 1.001: run([FFMPEG, "-y", "-i", tp, "-filter:a", f"atempo={tempo:.4f}", op])
        else: ww(op, raw)
        fin = rw(op); en = st + len(fin)/SR; prev = en
        processed.append(dict(start=st, end=en, text=text, keywords=sorted(kw), samples=fin))
        print(f"   {fn:14s} {st:5.2f}->{en:5.2f} t{tempo:.2f}")
    # ambience
    rng = np.random.default_rng(5); n = int(TOTAL*SR); t = np.arange(n)/SR; bed = np.zeros(n)
    noise = rng.standard_normal(n); br = np.cumsum(noise); br -= np.convolve(br, np.ones(2000)/2000, "same"); br /= np.max(np.abs(br))+1e-9
    bed += br*.013
    def add(sig, at, g=1.0):
        a = int(at*SR); b = min(n, a+len(sig)); bed[a:b] += sig[:b-a]*g
    def blip(fr, de, du, ga):
        tt = np.arange(int(du*SR))/SR; s = np.zeros_like(tt)
        for f, d, g in zip(fr, de, ga): s += g*np.sin(2*np.pi*f*tt)*np.exp(-d*tt)
        return s
    add(blip([1568, 2093], [9, 10], .5, [.2, .11]), 8.4)
    mix = bed.copy()
    for p in processed:
        a = int(p["start"]*SR); b = min(n, a+len(p["samples"])); mix[a:b] += p["samples"][:b-a]*.95
    mix *= .89/np.max(np.abs(mix)); mp = os.path.join(B, "master.wav"); ww(mp, mix)
    # subtitles
    ev = []; srt = []; si = 1
    for line in processed:
        words = line["text"].split(); groups, cur = [], []
        for w in words:
            tr = cur+[w]
            if sum(font_sub.getlength(x) for x in tr)+SPACE*(len(tr)-1) > 980 and cur: groups.append(cur); cur = [w]
            else: cur = tr
        if cur: groups.append(cur)
        weights = [max(2, len(clean(w)))+1+(1.2 if w.endswith((",", "...", "?", ".")) else 0) for w in words]
        tot = sum(weights); span = line["end"]-line["start"]; times, acc = [], line["start"]
        for wt in weights: times.append(acc); acc += span*wt/tot
        idx = 0
        for gi, g in enumerate(groups):
            ws = words[idx:idx+len(g)]; wts = times[idx:idx+len(g)]; idx += len(g)
            pe = times[idx]-.02 if gi+1 < len(groups) else line["end"]+.04
            width = sum(font_sub.getlength(x) for x in ws)+SPACE*(len(ws)-1); x = (W-width)/2; cen = []
            for w in ws:
                ww_ = font_sub.getlength(w); cen.append(x+ww_/2); x += ww_+SPACE
            for w, wt, cx in zip(ws, wts, cen):
                key = clean(w) in {clean(k) for k in line["keywords"]}
                stl = r"\an5\pos(%d,%d)\fad(40,0)\fscx70\fscy70\t(0,90,\fscx100\fscy100)" % (cx, 1560)
                if key: stl += r"\3c&H00384D1E&\bord8"
                ev.append((wt, pe, "{%s}%s" % (stl, w)))
            def srt_ts(s):
                ms = int(round(s*1000)); return f"{ms//3600000:02d}:{ms//60000%60:02d}:{ms//1000%60:02d},{ms%1000:03d}"
            srt.append(f"{si}\n{srt_ts(wts[0])} --> {srt_ts(pe)}\n{' '.join(ws)}\n"); si += 1
    def ats(s):
        c = int(round(s*100)); return f"{c//360000}:{c//6000%60:02d}:{c//100%60:02d}.{c%100:02d}"
    ass = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Reels,MontserratSub,64,&H00E0EFF5,&H00E0EFF5,&H00141414,&H00000000,0,0,0,0,100,100,0,0,1,3,0,5,40,40,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(f"Dialogue: 0,{ats(a)},{ats(b)},Reels,,0,0,0,,{x}" for a, b, x in ev) + "\n"
    ap = os.path.join(B, "subs.ass"); open(ap, "w").write(ass)
    open(os.path.join(rd, "subtitles.srt"), "w").write("\n".join(srt))
    json.dump([{k: v for k, v in p.items() if k != "samples"} for p in processed], open(os.path.join(rd, "timing.json"), "w"), indent=2)
    # cards
    hp = os.path.join(B, "hook.png"); ep = os.path.join(B, "end.png")
    card(reel["hook"], hp, 70); card(reel["end"], ep, 76, logo=os.path.join(BRAND, "sitely-logo.png"))
    # render
    inputs = []; filt = []
    for i, (img, secs, z, amp, dr) in enumerate(SEGS):
        inputs += ["-i", os.path.join(rd, "keyframes", img)]
        fr = int(round(secs*FPS)); last = fr-1; z = z.replace("{N}", str(last))
        x = f"(iw-iw/zoom)/2+{amp}*sin(on*0.35)+{amp*0.6}*sin(on*0.9)"
        y = f"(ih-ih/zoom)/2+{amp*0.8}*cos(on*0.29)+{amp*0.5}*sin(on*0.77)"
        filt.append(f"[{i}:v]scale=2160:3840:flags=lanczos,zoompan=z='{z}':x='{x}':y='{y}':d={fr}:s={W}x{H}:fps={FPS},setsar=1[v{i}]")
    filt.append("".join(f"[v{i}]" for i in range(3))+"concat=n=3:v=1:a=0[vc]")
    filt.append(f"[vc]subtitles={ap}:fontsdir={FONTS}[vs]")
    ci = 3
    inputs += ["-loop", "1", "-t", str(TOTAL), "-framerate", str(FPS), "-i", hp]
    inputs += ["-loop", "1", "-t", str(TOTAL), "-framerate", str(FPS), "-i", ep]
    inputs += ["-loop", "1", "-t", str(TOTAL), "-framerate", str(FPS), "-i", os.path.join(BRAND, "sitely-badge.png")]
    filt.append(f"[{ci}:v]format=rgba,fade=t=in:st=0.05:d=0.12:alpha=1[hk]")
    filt.append(f"[{ci+1}:v]format=rgba,fade=t=in:st=17.1:d=0.2:alpha=1[ec]")
    filt.append(f"[{ci+2}:v]scale=340:-1[bdg]")
    filt.append("[vs][hk]overlay=x=(W-w)/2:y='150-22*max(0\\,1-(t-0.05)/0.18)':enable='between(t,0.05,3.2)'[v1]")
    filt.append("[v1][ec]overlay=x=(W-w)/2:y=1210:enable='gte(t,17.1)'[v2]")
    filt.append("[v2][bdg]overlay=x=36:y=36[v3]")
    grade = "[v3]noise=alls=5:allf=t+u,vignette=angle=PI/5.5,eq=saturation=1.06:contrast=1.03,colorbalance=rs=0.02:bs=-0.02"
    if reel["night"]: grade += ",eq=brightness=-0.07:saturation=0.92,colorbalance=bs=0.07:gs=0.01"
    grade += "[vout]"
    filt.append(grade)
    inputs += ["-i", mp]
    out = os.path.join(rd, f"{reel['id']}.mp4")
    run([FFMPEG, "-y"]+inputs+["-filter_complex", ";".join(filt), "-map", "[vout]", "-map", f"{ci+3}:a",
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:v", "libx264", "-crf", "19", "-preset", "medium",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-r", str(FPS), "-t", str(TOTAL), "-movflags", "+faststart", out])
    print("   wrote", out, os.path.getsize(out))
print("CAMPAIGN DONE")
