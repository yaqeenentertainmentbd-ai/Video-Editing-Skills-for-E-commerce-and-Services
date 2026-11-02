"""Measure set text the way the browser will: HarfBuzz shaping with the film's font stacks.

Stacks put Poppins first; Bengali code points fall through to the Bengali face, so a string
is split into runs by script and each run is shaped with the font that will draw it.
"""
import os
import re

import uharfbuzz as hb

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(os.path.dirname(HERE), "assets", "fonts")

_FILES = {
    ("latin", 300): "Poppins-Light.ttf", ("latin", 400): "Poppins-Regular.ttf", ("latin", 500): "Poppins-Medium.ttf",
    ("latin", 600): "Poppins-SemiBold.ttf", ("latin", 700): "Poppins-Bold.ttf",
    ("hind", 300): "HindSiliguri-Light.ttf", ("hind", 400): "HindSiliguri-Regular.ttf", ("hind", 500): "HindSiliguri-Medium.ttf",
    ("hind", 600): "HindSiliguri-SemiBold.ttf", ("hind", 700): "HindSiliguri-Bold.ttf",
    ("opekkha", 400): "Opekkha.ttf",
}
_cache = {}
BN = re.compile(r"[ঀ-৿‌‍]+")


def _font(face, weight):
    key = (face, weight)
    if key not in _cache:
        path = os.path.join(FONTS, _FILES[key])
        blob = hb.Blob.from_file_path(path)
        f = hb.Font(hb.Face(blob))
        _cache[key] = (f, f.face.upem)
    return _cache[key]


def _shape(text, face, weight, size, script):
    f, upem = _font(face, weight)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    if script:
        buf.script = script
    hb.shape(f, buf, {})
    return sum(p.x_advance for p in buf.glyph_positions) * size / upem


def width(text, size, role="display", weight=None):
    """role: display (Poppins 700 / Opekkha), title (600 / Hind), body (400 / Hind), light (300 / Hind)."""
    text = text.replace("*", "")
    lw = {"display": 700, "title": 600, "body": 400, "light": 300, "medium": 500}[role] if weight is None else weight
    bn_face, bn_w = ("opekkha", 400) if role == "display" else ("hind", min(700, max(300, lw)))
    total, pos = 0.0, 0
    for m in BN.finditer(text):
        if m.start() > pos:
            total += _shape(text[pos:m.start()], "latin", lw, size, None)
        total += _shape(m.group(0), bn_face, bn_w, size, "beng")
        pos = m.end()
    if pos < len(text):
        total += _shape(text[pos:], "latin", lw, size, None)
    return total
