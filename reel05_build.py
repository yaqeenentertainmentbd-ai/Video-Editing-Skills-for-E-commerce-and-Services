"""Vertical reel 05 (1080x1920) from chapter 04: search anything with Claude (jobs, leads, products) and let Cowork order it.

Run:  python -I tools/reel05_build.py --cut   then   npx hyperframes render edit -c reel05.html
Same method as tools/reel04_build.py (pre-graded, frame-cut A-roll; full <-> stacked framing; bottom-half panels;
captions on every spoken second), plus a new music bed with a ducking lane and its drop placed on the story's turn.
Every time in SEGS / CAPS / MODES / PANELS is on the source clock; seg() maps it onto the reel clock.
"""
import json
import os
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from lib import FONTS_CSS, BASE_CSS, GREEN, esc, plain, world_html, world_motion_js, words_html  # noqa: E402
import scenes  # noqa: E402
from build import _split, _spans, write  # noqa: E402

sys.stdout.reconfigure(encoding="utf-8")
RW, RH = 1080, 1920
FPS = 30
MASTER = 1.12           # Shorts/Reels sit near -14 LUFS (checked after render)
FACE_X, FACE_Y = 940, 420  # speaker's face on the 1920x1080 source
NAME = "reel05"
P = "u"                 # id prefix: never clashes with reel04's "v" or reel03's "w"
TAIL = 1.6              # the closing CTA card holds after the last word while the music resolves

# ------------------------------------------------------------------ the cut
# Chapter 04 runs 374.9-501.8. The payoff "two days later the product is at your door" (494.5-497.6) moves up as
# the hook. Two fillers go: "ঠিক আছে, এখন আপনি কি পারেন" (390.9-392.2) and "বুঝতেছেন" (494.0-494.5).
# Raw.mp4 has no cuts or dissolves in 374-502. Every edge sits in a breath of voice.wav (20 ms envelope).
SEGS = [
    (494.50, 497.62),   # hook: two days later, your product is at your door
    (374.88, 390.90),   # search anything -> how you did it before -> Claude removed that -> e.g. a job
    (392.24, 494.04),   # filters -> results -> worldwide -> job sites -> browser -> leads/clients -> mouse -> Cowork orders
    (497.70, 501.78),   # no more hours of research
]
GRADED_FROM = 374.0          # first source second in assets/reel05_src_graded.mp4


def _snap(t):
    """Segment edges sit on frame boundaries of the graded source, so the cut video and the voice agree."""
    return round(GRADED_FROM + round((t - GRADED_FROM) * FPS) / FPS, 4)


SEGS = [(_snap(a), _snap(b)) for a, b in SEGS]
REEL_DUR = round(sum(b - a for a, b in SEGS) + TAIL, 3)


def seg(t):
    """Source time -> reel time (the segment that contains t)."""
    for strict in (True, False):           # a time on a seam belongs to the segment that starts there
        acc = 0.0
        for a, b in SEGS:
            if a - 0.02 <= t < b - 0.02 if strict else a - 0.02 <= t <= b + 0.02:
                return round(acc + t - a, 3)
            acc += b - a
    raise ValueError(f"{t} is outside the reel")


def cuts():
    acc, out = 0.0, []
    for a, b in SEGS[:-1]:
        acc += b - a
        out.append(round(acc, 3))
    return out


# ------------------------------------------------------------------ music
# "Autofahren" by Mauro Urbina (Mixkit, Mixkit Stock Music Free License: commercial and monetised use, no credit
# required). Deep house, 120 BPM, hypnotic and futuristic: a soft 32 s intro, the bass drops at 32.40 s, then the
# top end keeps building for two minutes. The drop lands on "Claude একদম নাই করে দিয়েছে": the story's turn.
MUSIC = "assets/music/autofahren.mp3"
MUSIC_DROP = 32.40          # s into the track where the bass enters
DROP_SRC = 384.78           # source time of "নাই"
MUSIC_OPEN = 0.33           # bed level in gaps (x MASTER): about 8 dB under the voice
MUSIC_DUCK = 0.56           # lane value while the voice speaks: about -5 dB more (about 13 dB under the voice)

# layout over time: "full" = face crop fills the frame, "stack" = speaker on top, panel below.
# Every full <-> stack switch lands on a caption start, so a caption never changes zone (or covers the face).
MODES = [  # (source start, mode, zoom)
    (494.50, "stack", 1.0), (495.86, "stack", 1.06),
    (374.88, "full", 1.12), (376.64, "full", 1.04), (378.40, "stack", 1.0), (380.48, "stack", 1.06),
    (382.90, "full", 1.08), (384.40, "full", 1.16), (385.58, "stack", 1.0), (388.82, "stack", 1.06),
    (392.24, "stack", 1.0), (395.22, "stack", 1.06), (397.90, "full", 1.12), (399.22, "stack", 1.0),
    (402.80, "stack", 1.06), (405.60, "stack", 1.0), (408.40, "stack", 1.06), (412.58, "stack", 1.0),
    (414.90, "stack", 1.06), (419.42, "full", 1.14), (420.56, "full", 1.06), (421.80, "stack", 1.0),
    (423.80, "stack", 1.06), (426.30, "stack", 1.0), (428.52, "stack", 1.06), (431.05, "stack", 1.0),
    (434.36, "stack", 1.06), (438.16, "full", 1.12), (439.78, "full", 1.04), (441.20, "stack", 1.0),
    (443.60, "stack", 1.06), (445.82, "full", 1.14), (447.22, "full", 1.06), (449.44, "stack", 1.0),
    (452.50, "stack", 1.06), (456.40, "full", 1.04), (459.08, "full", 1.14), (462.44, "stack", 1.0),
    (465.86, "stack", 1.06), (469.32, "stack", 1.0), (473.42, "stack", 1.06), (477.52, "full", 1.12),
    (479.74, "stack", 1.0), (482.88, "stack", 1.06), (485.98, "stack", 1.0), (489.62, "stack", 1.06),
    (497.70, "stack", 1.0), (499.36, "stack", 1.06),
]

# bottom-half panels: (id, kind, src start, src end, spec). Times inside spec are local to the panel.
# A panel that ends where the next one starts hands over: it holds while the next slides up over it.
PANELS = [
    ("u1", "broll", 494.50, 497.62, dict(src="b09_parcel_door_a.mp4", ms=0.5)),
    ("u2", "list", 378.40, 382.90, dict(title="*আগে* যা করতেন", title_at=0.1, numbered=True,
        items=[dict(logo="google.svg", text="গুগলে সার্চ", at=1.16), dict(icon="globe", text="ওয়েবসাইটে ঘোরা", at=2.6),
               dict(icon="list", text="ফিল্টার করে বোঝা", at=3.36)])),
    ("u3", "title", 385.58, 388.82, dict(kicker="Claude দিয়ে", icon="search", title="যেকোনো কিছু *খুঁজুন*", title_at=0.15,
                                       sub="শুধু আপনার প্রেফারেন্স বলুন", sub_at=1.8)),
    ("u4", "broll", 388.82, 390.90, dict(src="b07_interview_handshake.mp4", ms=4.5)),
    ("u5", "list", 392.24, 397.90, dict(title="আপনি কী *পারেন*?", title_at=0.1,
        items=[dict(icon="chat", text="সোশ্যাল মিডিয়া ম্যানেজমেন্ট", at=1.46), dict(icon="grad", text="ইংলিশ টিউটর", at=4.9)])),
    ("u6", "list", 399.22, 408.40, dict(title="আপনার *ফিল্টার*", title_at=0.1,
        items=[dict(icon="dollar", text="স্যালারি রেঞ্জ", at=0.45), dict(icon="home", text="এরিয়া", at=2.2),
               dict(icon="store", text="স্কুল / কলেজ", at=3.6), dict(icon="shield", text="সরকারি / প্রাইভেট", at=6.48)])),
    ("u7", "search", 408.40, 414.90, dict(query="সোশ্যাল মিডিয়া ম্যানেজার · ঢাকা · ৳৩০k+", type_at=1.1, type_dur=1.4,
        results=[dict(icon="chat", text="Social Media Executive", sub="ঢাকা · প্রাইভেট", badge="৳৩৫k", at=4.6),
                 dict(icon="grad", text="English Tutor", sub="স্কুল · ধানমন্ডি", badge="৳২৫k", at=5.0),
                 dict(icon="star", text="Content & Social Lead", sub="রিমোট", badge="৳৪৫k", at=5.4)])),
    ("u8", "broll", 414.90, 419.42, dict(src="b01_desk_stressed_a.mp4", ms=1.0)),
    ("u9", "title", 421.80, 426.30, dict(kicker="শুধু বাংলাদেশ না", icon="globe", title="*ওয়ার্ল্ডওয়াইড*", title_at=0.7,
                                       sub="ইন্টারন্যাশনাল জব", sub_at=2.0)),
    ("u10", "logos", 426.30, 431.05, dict(title="Claude + আপনার *ব্রাউজার*", title_at=0.1,
        items=[dict(logo="claude.svg", label="Claude", at=0.75), dict(logo="chrome.svg", label="ব্রাউজার", at=3.3)])),
    ("u11", "logos", 431.05, 438.16, dict(title="আরও *হাজারো* ওয়েবসাইট", title_at=6.0, tile=200,
        items=[dict(logo="upwork.svg", label="Upwork", at=0.55), dict(logo="peopleperhour.png", label="PeoplePerHour", at=1.8),
               dict(logo="linkedin.svg", label="LinkedIn", at=3.3), dict(logo="indeed.svg", label="Indeed", at=4.7)])),
    ("u12", "list", 441.20, 445.82, dict(title="Claude *নিজেই*", title_at=0.1, numbered=True,
        items=[dict(icon="globe", text="আপনার ব্রাউজার ইউজ করবে", at=0.6), dict(icon="search", text="নিজে নিজে সার্চ", at=1.84),
               dict(icon="check", text="চাকরি খুঁজে আনবে", at=3.2)])),
    ("u13", "grid", 449.44, 456.40, dict(title="শুধু চাকরি *না*", title_at=0.1, cols=2, cw=380, ch=196,
        items=[dict(icon="laptop", text="চাকরি", at=0.15), dict(icon="user", text="লিড", at=0.6),
               dict(icon="star", text="ক্লায়েন্ট", at=1.7), dict(icon="heart", text="ডাক্তার", at=3.08),
               dict(icon="package", text="প্রোডাক্ট", at=4.5), dict(icon="home", text="ক্লিনিক", at=5.8)])),
    ("u14", "broll", 462.44, 465.86, dict(src="b08_mouse_closeup_a.mp4", ms=4.0)),
    ("u15", "search", 465.86, 477.52, dict(query="ওয়্যারলেস মাউস · সবচেয়ে কম দাম · ইন-স্টক", type_at=1.6, type_dur=2.4,
        results=[dict(icon="store", text="Shop A — ইন স্টক", sub="ঢাকা · ২৪ ঘণ্টায় ডেলিভারি", badge="৳১,৮৫০", at=6.66),
                 dict(icon="store", text="Shop B — ইন স্টক", sub="চট্টগ্রাম", badge="৳১,৯২০", at=7.56),
                 dict(icon="alert", text="Shop C — স্টক আউট", sub="সবচেয়ে কম দাম, কিন্তু স্টকে নেই", badge="৳১,৭৯০", at=8.64)])),
    ("u16", "chat", 479.74, 485.98, dict(name="Claude Cowork", prompt="এই নাও আমার ইনফরমেশন — প্রোডাক্টটা খুঁজে অর্ডার করো",
        type_at=1.6, type_dur=1.8, reply=["ঠিক আছে! খুঁজে দেখছি…"], reply_at=4.2)),
    ("u17", "list", 485.98, 494.04, dict(title="Cowork যা *করবে*", title_at=0.1, numbered=True,
        items=[dict(icon="dollar", text="সবচেয়ে কম দাম", at=0.44), dict(icon="box", text="ইন-স্টক", at=1.6),
               dict(icon="shield", text="ট্রাস্টেড শপ", at=2.86), dict(icon="pen", text="আপনার তথ্য ফিল", at=5.28),
               dict(icon="cart", text="ঠিকানায় অর্ডার", at=7.3)])),
    ("u18", "title", 497.70, 501.78, dict(kicker="Claude দিয়ে প্রথম", icon="search", title="কী *খুঁজবেন*?", title_at=1.7,
                                        sub="কমেন্টে লিখুন", sub_at=2.6)),
]

# extra hits on the source clock: a ping on the delivery hook, an impact on the drop, a glitch on the out-of-stock shop
EXTRA_SFX = [(494.58, "notif"), (384.78, "impact"), (474.50, "glitch"), (493.28, "pop")]

# captions cover every spoken second (each holds until the next one starts).
# (start, end, text, start of the last word); the emphasis word is in *stars*.
CAPS = [
    (494.52, 495.84, "দুই দিন পরে *দেখবেন*", 495.46),
    (495.86, 497.60, "আপনার প্রোডাক্ট *দরজায়* চলে আসছে", 497.32),
    (374.90, 376.62, "আপনি যদি অনলাইন থেকে *যেকোনো কিছু*", 376.52),
    (376.64, 378.36, "বুঝতে চান — সেটা *যাই হোক না কেন*", 378.14),
    (378.42, 379.40, "আগে আপনি *কি করতেন?*", 379.00),
    (379.44, 380.46, "*গুগলে* গিয়ে সার্চ করতেন", 380.20),
    (380.48, 381.72, "তারপর বিভিন্ন *ওয়েবসাইটে* ঢুকতেন", 381.36),
    (381.76, 382.88, "ফিল্টার করে করে *বুঝতেন*", 382.46),
    (382.92, 384.38, "এখন এই জিনিসটা *Claude*", 384.10),
    (384.40, 385.56, "*একদম নাই* করে দিয়েছে", 385.20),
    (385.60, 386.56, "*কিভাবে* নাই করেছে?", 386.12),
    (386.60, 388.80, "ধরেন আপনার *প্রেফারেন্স* সম্পর্কে বললেন", 388.44),
    (388.84, 390.88, "ধরেন আপনি একটা *চাকরি* খুঁজতেছেন", 390.40),
    (392.30, 394.16, "ধরেন আপনি *সোশ্যাল মিডিয়া*", 393.98),
    (394.18, 395.22, "*ম্যানেজমেন্ট* করতে পারেন", 394.82),
    (395.24, 397.88, "বা আপনি ভালো একজন *ইংলিশ টিউটর*", 397.58),
    (397.92, 399.20, "এখন আপনি…", 398.34),
    (399.26, 401.12, "কত টাকা *স্যালারির* মধ্যে চাকরি চাচ্ছেন", 400.52),
    (401.16, 402.78, "কোন *এরিয়ার* মধ্যে চাকরি চাচ্ছেন", 402.24),
    (402.82, 405.60, "স্কুলে না *কলেজে*, বা দুটোই", 404.84),
    (405.62, 408.38, "*গভর্নমেন্ট* নাকি প্রাইভেট প্রতিষ্ঠানে", 407.60),
    (408.42, 410.76, "সবকিছু Claude কে লিখে *ইনপুট* দেন", 410.30),
    (410.80, 412.98, "Claude আপনার জন্য *ফিল্টার* অনুযায়ী", 413.00),
    (413.02, 414.88, "সুন্দর একটা *চাকরি* খুঁজে আনবে", 414.46),
    (414.92, 417.10, "যেটা আপনাকে এখন *ঘণ্টার পর ঘণ্টা*", 416.54),
    (417.14, 419.40, "ব্যয় করে *গুগলে* খুঁজতে হবে না", 419.06),
    (419.46, 420.54, "এটা তো *বাংলাদেশের* জন্য না", 420.42),
    (420.56, 421.78, "এটা *ইন্টারন্যাশনালি*", 420.86),
    (421.82, 423.76, "পুরো *ওয়ার্ল্ডওয়াইড* করতে পারবেন", 423.38),
    (423.80, 426.28, "চাকরি খোঁজার অনেক ভালো ভালো *ওয়েবসাইট* আছে", 425.92),
    (426.32, 428.50, "চাইলে Claude এর সাথে সেগুলো *কানেক্ট* করে", 428.32),
    (428.52, 431.06, "বা আপনার *ব্রাউজারে* সেই ওয়েবসাইটগুলোতে", 430.48),
    (431.10, 432.84, "যেমন *Upwork* বলতে পারেন", 432.40),
    (432.86, 434.34, "*PeoplePerHour* বলতে পারেন", 433.76),
    (434.36, 435.76, "*LinkedIn* বলতে পারেন", 435.10),
    (435.78, 437.00, "*Indeed* বলতে পারেন", 436.40),
    (437.02, 438.14, "আরও *হাজারো* ওয়েবসাইট আছে", 437.92),
    (438.18, 439.76, "সেখানে আপনার *ব্রাউজারে*", 439.12),
    (439.78, 441.18, "আইডি *লগইন* করা থাকলে", 440.90),
    (441.24, 442.72, "Claude আপনার *ব্রাউজার* ইউজ করে", 442.30),
    (442.74, 444.40, "নিজে নিজে *সার্চ* করে", 443.58),
    (444.42, 445.80, "*চাকরি* খুঁজে আনবে আপনার জন্য", 445.46),
    (445.86, 447.20, "অ্যান্ড আরও *মজার বিষয়* কি জানেন?", 446.88),
    (447.24, 449.40, "এটা জাস্ট চাকরির জন্য *লিমিটেড না*", 449.02),
    (449.46, 451.10, "চাইলে *লিড* খুঁজতে পারবেন", 450.66),
    (451.12, 452.48, "*ক্লায়েন্ট* খুঁজতে পারবেন", 451.76),
    (452.50, 453.70, "*ডাক্তার* খুঁজতে পারবেন", 453.32),
    (453.72, 455.20, "কোনো *প্রোডাক্ট* খুঁজতে পারবেন", 454.64),
    (455.22, 456.38, "*ক্লিনিক* খুঁজতে পারবেন", 455.84),
    (456.42, 459.06, "আপনি কোনো একটা *প্রোডাক্ট* কিনতে গেলে", 458.82),
    (459.10, 460.98, "সেই প্রোডাক্টের *প্রাইস* পর্যন্ত", 460.38),
    (461.00, 462.40, "Claude থেকে *বের করতে* পারবেন", 461.90),
    (462.46, 465.10, "ধরেন আপনি একটা *মাউস* কিনবেন", 464.72),
    (465.12, 465.84, "কথার কথা", 465.42),
    (465.92, 467.94, "এই মাউসটার *মডেল* লিখে", 467.52),
    (467.96, 469.30, "*Claude কে* বলবেন যে", 469.04),
    (469.32, 470.88, "পুরো *বাংলাদেশের* মধ্যে", 470.58),
    (470.90, 473.40, "সবথেকে *কম দামে* কারা বিক্রি করতেছে", 472.82),
    (473.42, 474.92, "কাদের কাছে *ইন-স্টক* আছে", 474.50),
    (474.94, 475.84, "সেই *লিস্ট* আমাকে দাও", 475.56),
    (475.86, 477.50, "এইটাও আপনাকে *বের করে* দেবে", 477.02),
    (477.56, 479.70, "এমনকি একটু আগে *Cowork* এর কথা বললাম না?", 479.52),
    (479.78, 481.40, "আপনি যদি বলে যান যে", 480.70),
    (481.42, 482.86, "এই নাও আমার *ইনফরমেশন*", 482.26),
    (482.88, 483.74, "তুমি কি *করবা*", 483.26),
    (483.76, 485.96, "আমার জন্য এই *প্রোডাক্টটা* খুঁজবা", 484.92),
    (486.00, 487.46, "সবথেকে *কম প্রাইসে* যেখানে পাবা", 487.20),
    (487.48, 488.44, "*ইন-স্টক* যেখানে পাবা", 488.18),
    (488.46, 489.60, "মোটামুটি *ট্রাস্টেড* হবে", 489.26),
    (489.62, 492.10, "সেইখানে আমার *ইনফরমেশন* ফিল করে", 491.70),
    (492.14, 494.02, "আমার ঠিকানায় *অর্ডার* করে দিবা", 493.64),
    (497.72, 499.34, "আপনার *ঘণ্টার পর ঘণ্টা*", 498.52),
    (499.36, 500.84, "কোনো প্রোডাক্ট নিয়ে *অনেক বেশি*", 500.66),
    (500.86, 501.76, "*রিসার্চ* করতে হবে না", 501.58),
]

HOOK = ("Claude নিজেই *অর্ডার* করে দেয়", "খোঁজা থেকে ডেলিভারি — সব AI")
HOOK_DUR = 2.85         # the hook title leaves on the seam into "search anything"


# ------------------------------------------------------------------ pieces
def panel_comp(pid, kind, dur, spec, leave=True, enter=True):
    sc = dict(spec, id=pid, kind=kind, dur=dur, layout="panel")
    s = scenes.S(sc)
    bw, bh = RW, 960
    if kind == "broll":
        scenes.k_broll(s)
        s.html = [h.replace("width:1920px;height:1080px", f"width:{bw}px;height:{bh}px") for h in s.html]
        inner = "".join(s.html)
    else:
        scenes.CONTENT[kind](s, bw, bh)
        s.js.insert(0, world_motion_js(pid, dur))
        inner = f'{world_html(pid, bw, bh)}<div class="abs" style="left:0;top:0;width:{bw}px;height:{bh}px">{"".join(s.html)}</div>'
    stage = (f'<div class="abs" id="{pid}-stage" style="left:0;top:0;width:{bw}px;height:{bh}px;overflow:hidden">{inner}'
             f'<div class="abs" style="left:0;top:0;width:100%;height:2px;background:linear-gradient(90deg,rgba(255,255,255,.1),rgba(255,255,255,.7),rgba(255,255,255,.1))"></div></div>')
    if enter:   # the opening panel is already in place on frame 1, so the first frame is a full picture
        s.js.insert(0, f'tl.fromTo("#{pid}-stage",{{y:{bh}}},{{y:0,duration:.6,ease:"power3.inOut"}},0);')
        s.cue(0.05, "swipe")
    if leave:   # the panel slides out in step with the camera's push back to full frame (build() adds the 0.5 s)
        s.js.append(f'tl.to("#{pid}-stage",{{y:{bh},duration:.5,ease:"power3.inOut"}},{dur-0.5:.3f});')
    body = f'''<template>
<style>{FONTS_CSS}{BASE_CSS}</style>
<div id="root" data-composition-id="{pid}" data-width="{bw}" data-height="{bh}" data-layout-allow-overlap data-layout-allow-overflow>
{stage}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{scenes.JS_HELPERS}
{chr(10).join(s.js)}
tl.set({{}}, {{}}, {dur:.3f});
window.__timelines["{pid}"] = tl;
</script>
</template>
'''
    write(os.path.join(PROJ, "compositions", f"{pid}.html"), body)
    return s.sfx


def mode_at(t_src_list, t):
    """mode and zoom active at reel time t."""
    cur = ("full", 1.0)
    for ts, m, z in sorted(((seg(a), m, z) for a, m, z in t_src_list)):
        if ts <= t + 1e-6:
            cur = (m, z)
    return cur


CAP_SETTLE = 0.35       # s a caption waits after a full <-> stacked reframe


def reframes():
    """Reel times where the layout changes between full and stacked with a camera move (not on a hard cut)."""
    out, prev = [], None
    for ts, m, _ in sorted(((seg(a), m, z) for a, m, z in MODES)):
        if prev is not None and m != prev and not any(abs(ts - c) < 0.02 for c in cuts()):
            out.append(ts)
        prev = m
    return out


def build_caps():
    from textfit import width
    groups, js = [], []
    for i, (t0, t1, text, t_last) in enumerate(CAPS):
        gid = f"{P}c{i:02d}"
        r0 = seg(t0)
        r1 = r0 + (t1 - t0)              # same segment as the start, even on a seam
        nxt = seg(CAPS[i + 1][0]) if i + 1 < len(CAPS) else REEL_DUR
        if 0 < nxt - r1 < 0.8:
            r1 = nxt - 0.04            # hold to the next caption: words on screen 100% of the time
        for c in cuts():               # ...but never across a seam, where the framing jumps
            if r0 < c < r1 + 0.02:
                r1 = c - 0.04
        toks = [w for w in text.split(" ") if w]
        lens = [max(1, len(plain(w))) for w in toks]
        span = max(0.2, seg(t_last) - r0)
        acc, wt = 0, []
        for L in lens:
            wt.append(r0 + span * acc / sum(lens))
            acc += L
        # a caption that starts on a reframe waits until the camera and panel are mostly settled,
        # so it never sits on the face or on a panel that is still moving
        delay = CAP_SETTLE if any(abs(r0 - ts) < 0.12 for ts in reframes()) else 0.0
        wt = [max(w, r0 + delay) for w in wt]
        lead, punch, tail = _split(toks)
        if len(plain(" ".join(punch))) > 16:     # keep the boxed line inside the 9:16 frame
            i1 = next((i for i, w in enumerate(punch) if w.rstrip("!?,.;:।—…)").endswith("*")), len(punch) - 1)
            punch, tail = punch[:i1 + 1], punch[i1 + 1:] + tail
        pw = width(plain(" ".join(punch)), 92, "display") + 56 if punch else 0
        if pw > 980:
            print(f"  ! caption {gid} box {pw:.0f}px wide: {text}")
        mode, _ = mode_at(MODES, r0 + min(0.3, (r1 - r0) / 2))   # a caption that starts just before a reframe sits where it will live
        bottom = 1010 if mode == "stack" else 330
        lead_html = f'<div class="cl">{_spans(lead, "wl", 0)}</div>' if lead else ""
        punch_html = ""
        if punch:
            k = len(lead)
            punch_html = (f'<div class="cp-row"><div class="cp-box"><i class="cp-bg" id="{gid}-box"></i><span class="cp" id="{gid}-cp">{_spans(punch, "wp", k)}</span></div>'
                          f'{" <span class=cl-tail>" + _spans(tail, "wl", k + len(punch)) + "</span>" if tail else ""}</div>')
        else:
            lead_html = f'<div class="cl solo">{_spans(lead, "wl", 0)}</div>'
        groups.append(f'<div class="clip rcap" id="{gid}" data-start="{r0-0.04:.3f}" data-duration="{r1-r0+0.3:.3f}" style="bottom:{bottom}px">'
                      f'<div class="cap-in">{lead_html}{punch_html}</div></div>')
        js.append(f'tl.fromTo("#{gid} .cap-in",{{opacity:0}},{{opacity:1,duration:.1}},{r0+delay-0.03:.3f});')
        for j in range(len(toks)):
            tw = wt[j]
            sel = f'#{gid} [data-k=\\"{j}\\"]'
            if punch and len(lead) <= j < len(lead) + len(punch):
                if j == len(lead):
                    js.append(f'tl.fromTo("#{gid}-box",{{scaleX:0}},{{scaleX:1,duration:.3,ease:"expo.out"}},{tw-0.04:.3f});')
                    js.append(f'tl.fromTo("#{gid}-cp",{{x:-26}},{{x:0,duration:.34,ease:"power3.out"}},{tw:.3f});')
                    js.append(f'tl.fromTo("{sel}",{{opacity:0}},{{opacity:1,duration:.2}},{tw:.3f});')
                    if len(punch) > 1:
                        js.append(f'tl.fromTo("#{gid} .wp:not([data-k=\\"{j}\\"])",{{opacity:0}},{{opacity:.42,duration:.2}},{tw:.3f});')
                else:
                    js.append(f'tl.fromTo("{sel}",{{opacity:.42}},{{opacity:1,duration:.14,immediateRender:false}},{max(tw, wt[len(lead)] + 0.21):.3f});')
            else:
                js.append(f'tl.fromTo("{sel}",{{opacity:0,y:12,filter:"blur(4px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.24,ease:"power3.out"}},{tw:.3f});')
        js.append(f'tl.to("#{gid} .cap-in",{{opacity:0,duration:.08}},{r1+0.02:.3f});')
        js.append(f'tl.set("#{gid} .cap-in",{{visibility:"hidden"}},{r1+0.12:.3f});')
    css = f"""
.rcap{{position:absolute;left:50px;width:980px;display:flex;flex-direction:column;align-items:center;text-align:center;}}
.cap-in{{display:flex;flex-direction:column;align-items:center;}}
.cl{{font-family:'Poppins','Hind Siliguri',sans-serif;font-weight:400;font-size:50px;line-height:1.25;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.3);margin-bottom:12px;}}
.cl.solo{{font-family:'Poppins','Opekkha',sans-serif;font-weight:700;font-size:72px;margin-bottom:0;}}
.cp-row{{display:flex;align-items:flex-end;justify-content:center;gap:16px;flex-wrap:wrap;}}
.cp-box{{position:relative;display:inline-block;padding:2px 28px 12px;}}
.cp-bg{{position:absolute;inset:0;background:{GREEN};border-radius:16px;transform-origin:0 50%;box-shadow:0 2px 6px rgba(0,0,0,.16);}}
.cp{{position:relative;display:inline-block;font-family:'Poppins','Opekkha',sans-serif;font-weight:700;font-size:92px;line-height:1.16;color:#fff;white-space:nowrap;}}
.cl-tail{{font-family:'Poppins','Hind Siliguri',sans-serif;font-weight:400;font-size:46px;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,.3);padding-bottom:12px;}}
.hook{{position:absolute;left:60px;width:960px;top:1070px;text-align:center;}}
.hook .h1{{font-family:'Poppins','Opekkha',sans-serif;font-weight:700;font-size:96px;line-height:1.12;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.3);}}
.hook .h1 em{{color:#fff;-webkit-text-fill-color:#fff;background:{GREEN};border-radius:16px;padding:0 22px 8px;}}
.hook .h2{{display:inline-block;margin-top:22px;padding:12px 32px;border-radius:999px;background:rgba(10,26,17,.84);border:1.5px solid rgba(144,183,156,.55);
  font-family:'Poppins','Hind Siliguri',sans-serif;font-weight:600;font-size:40px;color:#fff;}}
.endpill{{position:absolute;left:0;width:1080px;top:1700px;display:flex;justify-content:center;}}
.endpill .p{{display:flex;align-items:center;gap:18px;padding:16px 36px;border-radius:999px;background:rgba(10,26,17,.9);border:1.5px solid rgba(144,183,156,.6);
  font-family:'Poppins','Hind Siliguri',sans-serif;font-weight:600;font-size:40px;color:#fff;}}
.endpill img{{width:46px;height:46px;}}
"""
    # hook title in the top of the panel for the first 2.6 s, and a follow pill at the end
    groups.append(f'<div class="clip hook" id="hook" data-start="0" data-duration="{HOOK_DUR}"><div class="h1">{words_html(HOOK[0])}</div><div class="h2" id="hook2">{esc(HOOK[1])}</div></div>')
    js.append('tl.fromTo("#hook .w",{opacity:0,y:30,filter:"blur(6px)"},{opacity:1,y:0,filter:"blur(0px)",duration:.42,stagger:.08,ease:"power3.out"},0.05);')
    js.append('tl.fromTo("#hook2",{opacity:0,y:16,scale:.94},{opacity:1,y:0,scale:1,duration:.4,ease:"expo.out"},0.55);')
    js.append(f'tl.to("#hook > div",{{opacity:0,filter:"blur(8px)",duration:.25,ease:"power2.in"}},{HOOK_DUR - 0.3:.2f});')
    e0 = REEL_DUR - 1.85
    groups.append(f'<div class="clip endpill" id="endp" data-start="{e0:.3f}" data-duration="{REEL_DUR-e0:.3f}"><div class="p" id="endp-p">'
                  f'<img src="assets/logos/youtube.svg"><img src="assets/logos/facebook.svg"><span>ফলো করুন — পুরো ভিডিও চ্যানেলে</span></div></div>')
    js.append(f'tl.fromTo("#endp-p",{{opacity:0,y:30,scale:.9}},{{opacity:1,y:0,scale:1,duration:.45,ease:"expo.out"}},{e0+0.05:.3f});')
    body = f'''<template>
<style>{FONTS_CSS}{BASE_CSS}{css}</style>
<div id="root" data-composition-id="{P}caps" data-width="{RW}" data-height="{RH}" data-layout-allow-overlap data-layout-allow-overflow data-layout-allow-caption-zone>
{chr(10).join(groups)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
tl.set({{}}, {{}}, {REEL_DUR:.3f});
window.__timelines["{P}caps"] = tl;
</script>
</template>
'''
    write(os.path.join(PROJ, "compositions", f"{P}caps.html"), body)


def music_start():
    """Track time at reel 0, so MUSIC_DROP lands on DROP_SRC."""
    ms = MUSIC_DROP - seg(DROP_SRC)
    assert ms >= 0, ms
    return round(ms, 3)


def speech_spans():
    """Reel-time spans where the voice is speaking (50 ms RMS over -36 dBFS, gaps under 0.4 s bridged)."""
    sr, hop = 8000, 400
    spans = []
    acc = 0.0
    for a, b in SEGS:
        raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", os.path.join(PROJ, "assets", "voice.wav"),
                              "-ac", "1", "-ar", str(sr), "-f", "f32le", "-"], capture_output=True, check=True).stdout
        x = np.frombuffer(raw, dtype=np.float32)
        n = len(x) // hop
        db = 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1)) + 1e-9)
        on = db > -36
        i = 0
        while i < n:
            if on[i]:
                j = i
                while j < n and on[j]:
                    j += 1
                spans.append([acc + i * hop / sr, acc + j * hop / sr])
                i = j
            else:
                i += 1
        acc += b - a
    merged = []
    for s0, s1 in spans:
        if merged and s0 - merged[-1][1] < 0.4:
            merged[-1][1] = s1
        else:
            merged.append([s0, s1])
    return merged


def duck_points():
    """Volume lane: open before the drop and in gaps, ducked while the voice speaks after the drop."""
    drop = seg(DROP_SRC)
    pts = [{"t": 0.0, "v": 1.0}]
    for s0, s1 in speech_spans():
        s0, s1 = max(s0, drop - 0.3), s1
        if s1 <= s0:
            continue
        pts += [{"t": round(s0 - 0.18, 3), "v": 1.0}, {"t": round(s0, 3), "v": MUSIC_DUCK},
                {"t": round(s1 + 0.12, 3), "v": MUSIC_DUCK}, {"t": round(s1 + 0.5, 3), "v": 1.0}]
    out = []
    for p in sorted(pts, key=lambda p: p["t"]):
        if p["t"] < 0:
            continue
        if out and p["t"] <= out[-1]["t"] + 0.01:
            out[-1] = p if p["v"] < out[-1]["v"] else out[-1]   # overlapping ramps: keep the ducked value
            continue
        out.append(p)
    # drop redundant middle points of flat runs
    flat = [out[0]] + [p for k, p in enumerate(out[1:-1], 1) if not (out[k - 1]["v"] == p["v"] == out[k + 1]["v"])] + [out[-1]]
    assert len(flat) <= 512, len(flat)
    return flat


def build():
    import build as B
    # the source frame scaled to full height: 3413 x 1920, face centred
    k = RH / 1080
    vw, vh = round(1920 * k), RH
    vx, vy = round(RW / 2 - FACE_X * k), 0
    fy = round(FACE_Y * k)
    videos, voice, sfx = [], [], []
    acc = 0.0
    total = REEL_DUR
    # assets/reel05_aroll.mp4: the SEGS cut out of the graded source and joined (tools/reel05_build.py --cut);
    # one video element, so the cuts never swap media elements mid-capture
    videos.append(f'<video id="{P}a" class="clip aroll" src="assets/{NAME}_aroll.mp4" data-start="0" data-duration="{total:.3f}" '
                  f'data-track-index="0" muted playsinline></video>')
    for i, (a, b) in enumerate(SEGS):
        d = b - a
        voice.append(f'<audio id="{P}v{i}" class="clip" src="assets/voice.wav" data-start="{acc:.3f}" data-duration="{d:.3f}" data-media-start="{a:.3f}" '
                     f'data-track-index="10" data-volume="{MASTER}" data-fade-in="0.02" data-fade-out="0.03"></audio>')
        acc += d
    for t in cuts():
        sfx.append((t, "whoosh"))
    # camera: full <-> stacked framing, with a zoom per beat
    cam = ['tl.set("#frame",{scale:1,y:0},0);']
    prev = None
    for ts, m, z in sorted(((seg(a), m, z) for a, m, z in MODES)):
        sc_ = (0.66 if m == "stack" else 1.0) * z
        y = round((430 - fy) if m == "stack" else (0 if z == 1.0 else -40))
        hard = any(abs(ts - c) < 0.02 for c in cuts()) or ts == 0
        if prev is None:            # a zero-length set at t=0 is skipped by the renderer: hold the opening frame instead
            cam[0] = f'tl.fromTo("#frame",{{scale:{sc_:.3f},y:{y}}},{{scale:{sc_:.3f},y:{y},duration:0.05,immediateRender:true}},0);'
        elif hard:                              # a jump cut reframes instantly; a tween across a cut ghosts
            cam.append(f'tl.set("#frame",{{scale:{sc_:.3f},y:{y}}},{ts:.3f});')
        elif m == "stack" and prev[0] == "stack":   # a breath of push-in on the speaker while the panel stays
            cam.append(f'tl.to("#frame",{{scale:{sc_:.3f},y:{y},duration:1.2,ease:"sine.inOut"}},{ts:.3f});')
        else:
            cam.append(f'tl.to("#frame",{{scale:{sc_:.3f},y:{y},duration:.55,ease:"power3.inOut"}},{ts:.3f});')
        prev = (m, z)
    hosts = []
    spans = [(seg(a), seg(a) + (b - a)) for _, _, a, b, _ in PANELS]
    for n_, (pid, kind, a, b, spec) in enumerate(PANELS):
        r0, r1 = spans[n_]
        handover = any(abs(s0 - r1) < 0.05 for s0, _ in spans)        # it hands over: hold under the next one
        last = abs(r1 - (REEL_DUR - TAIL)) < 0.05                      # the closing card stays to the last frame
        on_cut = any(abs(r1 - c) < 0.02 for c in cuts())               # a seam: the panel goes with the hard cut
        leave = not (handover or last or on_cut)
        d = r1 - r0 + (0.62 if handover else 0) + (TAIL if last else 0) + (0.5 if leave else 0)
        cues = panel_comp(pid, kind, round(d, 3), spec, leave=leave, enter=r0 > 0.01)
        hosts.append(f'<div id="{pid}" data-composition-id="{pid}" data-composition-src="compositions/{pid}.html" data-start="{r0:.3f}" data-duration="{d:.3f}" '
                     f'data-track-index="{2 + n_ % 3}" data-track-kind="graphics" data-width="{RW}" data-height="960" style="position:absolute;left:0;top:960px;width:{RW}px;height:960px;z-index:{20 + n_}"></div>')
        sfx += [(r0 + t, c) for t, c in cues if c]
    sfx += [(seg(t), c) for t, c in EXTRA_SFX]
    build_caps()
    # music: the Autofahren bed, its drop on the story's turn, ducked under the voice by a volume lane
    chain = json.dumps({"version": 1, "nodes": [
        {"type": "highpass", "id": "m1", "label": "Clear the low end", "params": {"frequency": 40}},
        {"type": "peaking", "id": "m2", "label": "Make room for the voice", "params": {"frequency": 2600, "gain": -5, "q": 0.8}},
        {"type": "peaking", "id": "m3", "label": "Keep the sub off the voice's chest", "params": {"frequency": 180, "gain": -2, "q": 1.0}}]})
    lane = json.dumps({"version": 1, "lanes": [{"target": "volume", "points": duck_points()}]})
    audio = voice + [f'<audio id="{P}mus" class="clip" src="{MUSIC}" data-start="0" data-duration="{REEL_DUR:.3f}" data-media-start="{music_start():.3f}" '
                     f'data-volume="{MUSIC_OPEN * MASTER:.3f}" data-fade-in="0.4" data-fade-out="2.4" data-fx-chain="{esc(chain).replace(chr(34), "&quot;")}" '
                     f'data-automation="{esc(lane).replace(chr(34), "&quot;")}" data-track-index="30"></audio>']
    lanes, n = [], 0
    for t, cat in B.thin_sfx(sfx):
        dur_override = None
        if cat.startswith("type:"):
            dur_override = float(cat.split(":")[1])
            cat = "type"
        f = B.pick(cat)
        m = B.SFX_FILES[f]
        start = max(0.0, t - m["peak"] + 1 / FPS)
        d = m["dur"] if not dur_override else min(m["dur"], dur_override + 0.05)
        d = min(d, REEL_DUR - start)
        if d <= 0.02:
            continue
        n += 1
        lane = next((k for k, e in enumerate(lanes) if e <= start), None)
        if lane is None:
            lanes.append(0)
            lane = len(lanes) - 1
        lanes[lane] = start + d
        audio.append(f'<audio id="{P}s{n:03d}" class="clip" src="assets/sfx2/{f}" data-start="{start:.3f}" data-duration="{d:.3f}" data-volume="{m["gain"] * MASTER:.3f}" data-track-index="{12 + lane}"></audio>')
    html = f'''<!doctype html>
<html lang="bn">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={RW}, height={RH}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {RW}px; height: {RH}px; overflow: hidden; background: #050d08; }}
      #frame {{ position: absolute; left: 0; top: 0; width: {RW}px; height: {RH}px; transform-origin: 540px {fy}px; }}
      .aroll {{ position: absolute; left: {vx}px; top: {vy}px; width: {vw}px; height: {vh}px; object-fit: cover; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="{NAME}" data-start="0" data-duration="{REEL_DUR:.3f}" data-width="{RW}" data-height="{RH}">
      <div id="frame">
        {chr(10).join("        " + v for v in videos)}
      </div>
      {chr(10).join("      " + h for h in hosts)}
      <div id="{P}caps" data-composition-id="{P}caps" data-composition-src="compositions/{P}caps.html" data-start="0" data-duration="{REEL_DUR:.3f}" data-track-index="1" data-track-kind="captions" data-width="{RW}" data-height="{RH}" style="position:absolute;inset:0;z-index:60"></div>
      {chr(10).join("      " + a for a in audio)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join("      " + c for c in cam)}
      tl.set({{}}, {{}}, {REEL_DUR:.3f});
      window.__timelines["{NAME}"] = tl;
    </script>
  </body>
</html>
'''
    write(os.path.join(PROJ, f"{NAME}.html"), html)
    covered = sorted((seg(c[0]), seg(c[0]) + (c[1] - c[0])) for c in CAPS)
    cov, end = 0.0, 0.0
    for x0, x1 in covered:
        cov += max(0.0, x1 - max(x0, end))
        end = max(end, x1)
    print(f"{NAME} {REEL_DUR:.1f}s  segments {len(SEGS)}  panels {len(PANELS)}  captions {len(CAPS)} (~{100*cov/REEL_DUR:.0f}% incl. holds)  sfx {n}")


def cut():
    import subprocess
    fr = lambda t: round((t - GRADED_FROM) * FPS)      # cut on frame numbers: exact, whatever the file's pts look like
    tail = REEL_DUR - sum(b - a for a, b in SEGS)   # the last frame holds under the end pill
    parts = [f"[0:v]trim=start_frame={fr(a)}:end_frame={fr(b)},setpts=PTS-STARTPTS[v{i}]" for i, (a, b) in enumerate(SEGS)]
    fc = (";".join(parts) + ";" + "".join(f"[v{i}]" for i in range(len(SEGS))) + f"concat=n={len(SEGS)}:v=1:a=0[cat];"
          f"[cat]tpad=stop_mode=clone:stop_duration={tail:.3f}[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(PROJ, "assets", f"{NAME}_src_graded.mp4"), "-filter_complex", fc,
                    "-map", "[out]", "-r", str(FPS), "-c:v", "h264_nvenc", "-preset", "p5", "-cq", "16", "-g", "30", "-bf", "0",
                    "-pix_fmt", "yuv420p", os.path.join(PROJ, "assets", f"{NAME}_aroll.mp4")], check=True)


if __name__ == "__main__":
    if "--cut" in sys.argv:
        cut()
    build()
