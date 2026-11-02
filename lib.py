"""Shared design system for the edit: fonts, CSS, icons, markup helpers.

Every scene file is generated from these pieces so the whole film reads as
one system: a deep sage-green "world", Liquid Glass style cards, Bengali
type set in Opekkha (display) and Hind Siliguri (text), and all English
text in Poppins. Font stacks put Poppins first: it has no Bengali glyphs,
so Latin lands in Poppins and Bengali falls through to the Bengali face.
"""
import html
import re

W, H = 1920, 1080

FONTS_CSS = """
@font-face{font-family:'Opekkha';src:url('assets/fonts/Opekkha.ttf') format('truetype');font-weight:100 900;}
@font-face{font-family:'Hind Siliguri';src:url('assets/fonts/HindSiliguri-Light.ttf') format('truetype');font-weight:300;}
@font-face{font-family:'Hind Siliguri';src:url('assets/fonts/HindSiliguri-Regular.ttf') format('truetype');font-weight:400;}
@font-face{font-family:'Hind Siliguri';src:url('assets/fonts/HindSiliguri-Medium.ttf') format('truetype');font-weight:500;}
@font-face{font-family:'Hind Siliguri';src:url('assets/fonts/HindSiliguri-SemiBold.ttf') format('truetype');font-weight:600;}
@font-face{font-family:'Hind Siliguri';src:url('assets/fonts/HindSiliguri-Bold.ttf') format('truetype');font-weight:700 900;}
@font-face{font-family:'Poppins';src:url('assets/fonts/Poppins-Thin.ttf') format('truetype');font-weight:100;}
@font-face{font-family:'Poppins';src:url('assets/fonts/Poppins-Light.ttf') format('truetype');font-weight:300;}
@font-face{font-family:'Poppins';src:url('assets/fonts/Poppins-Regular.ttf') format('truetype');font-weight:400;}
@font-face{font-family:'Poppins';src:url('assets/fonts/Poppins-Medium.ttf') format('truetype');font-weight:500;}
@font-face{font-family:'Poppins';src:url('assets/fonts/Poppins-SemiBold.ttf') format('truetype');font-weight:600;}
@font-face{font-family:'Poppins';src:url('assets/fonts/Poppins-Bold.ttf') format('truetype');font-weight:700;}
@font-face{font-family:'Poppins';src:url('assets/fonts/Poppins-ExtraBold.ttf') format('truetype');font-weight:800;}
@font-face{font-family:'Poppins';src:url('assets/fonts/Poppins-Black.ttf') format('truetype');font-weight:900;}
"""

# Palette: green-black stage, sage glows, smoked-glass cards, one sage accent.
GREEN = "#4f8462"   # caption boxes, highlighted cards
SAGE = "#90b79c"    # glows, rims, lines
SAGE_L = "#b8d8c2"  # emphasis text
INK = "#0c1f15"     # dark text on light tiles
DEEP = "#2f6b47"    # accent marks on light tiles

BASE_CSS = """
#root{position:absolute;inset:0;overflow:hidden;font-family:'Poppins','Hind Siliguri',sans-serif;font-weight:500;color:#fff;
  -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision;}
.abs{position:absolute;}
.world{position:absolute;overflow:hidden;background:#07120c;}
.w-base{position:absolute;inset:0;background:
  radial-gradient(80% 70% at 70% 6%,rgba(120,170,136,.34) 0%,rgba(120,170,136,0) 62%),
  radial-gradient(70% 60% at 8% 100%,rgba(2,6,4,.8) 0%,rgba(2,6,4,0) 70%),
  linear-gradient(160deg,#173322 0%,#10261a 38%,#0a1a11 70%,#050d08 100%);}
.w-glow{position:absolute;border-radius:50%;}
.w-glow.g1{width:1100px;height:1100px;left:-300px;top:-520px;background:radial-gradient(circle,rgba(144,183,156,.24),rgba(144,183,156,0) 62%);}
.w-glow.g2{width:900px;height:900px;right:-260px;bottom:-460px;background:radial-gradient(circle,rgba(94,148,112,.22),rgba(94,148,112,0) 62%);}
.w-rays{position:absolute;left:-20%;top:-30%;width:140%;height:160%;transform:rotate(-24deg);}
.ray{position:absolute;top:0;height:100%;background:linear-gradient(90deg,rgba(210,235,218,0),rgba(210,235,218,.075) 50%,rgba(210,235,218,0));}
.w-grid{position:absolute;inset:0;background-image:linear-gradient(rgba(190,225,200,.04) 1px,transparent 1px),linear-gradient(90deg,rgba(190,225,200,.04) 1px,transparent 1px);
  background-size:80px 80px;-webkit-mask-image:radial-gradient(75% 70% at 50% 45%,#000 20%,transparent 80%);mask-image:radial-gradient(75% 70% at 50% 45%,#000 20%,transparent 80%);}
.w-vig{position:absolute;inset:0;background:radial-gradient(120% 95% at 50% 40%,rgba(0,0,0,0) 55%,rgba(0,4,2,.55) 100%);}

.glass{position:absolute;border-radius:34px;
  background:linear-gradient(160deg,rgba(255,255,255,.14) 0%,rgba(255,255,255,.05) 45%,rgba(255,255,255,.03) 70%,rgba(255,255,255,.08) 100%),rgba(14,32,22,.52);
  -webkit-backdrop-filter:blur(24px) saturate(140%);backdrop-filter:blur(24px) saturate(140%);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.30),inset 0 -1px 0 rgba(255,255,255,.08),
    0 24px 60px rgba(0,0,0,.42),0 0 50px rgba(144,183,156,.07);}
.glass::before{content:"";position:absolute;inset:0;border-radius:inherit;pointer-events:none;
  background:radial-gradient(120% 80% at 12% -10%,rgba(255,255,255,.16),rgba(255,255,255,0) 52%),
             radial-gradient(80% 60% at 100% 110%,rgba(144,183,156,.14),rgba(144,183,156,0) 60%);}
.glass::after{content:"";position:absolute;inset:0;border-radius:inherit;padding:1.5px;pointer-events:none;
  background:linear-gradient(135deg,rgba(225,242,230,.62),rgba(144,183,156,.10) 40%,rgba(144,183,156,.42) 74%,rgba(225,242,230,.46));
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude;}
.glass.dark{background:linear-gradient(160deg,rgba(255,255,255,.07),rgba(255,255,255,.02)),rgba(6,16,10,.74);}
.glass.accent{background:linear-gradient(160deg,rgba(255,255,255,.12),rgba(255,255,255,.02)),rgba(64,112,82,.62);}
.glass.solid{background:linear-gradient(150deg,#f2f7f3,#e2ebe4);color:#0c1f15;}
.glass.solid::before{background:radial-gradient(120% 80% at 12% -10%,rgba(255,255,255,.9),rgba(255,255,255,0) 52%);}
.glass .in{position:relative;z-index:2;}

.kicker{font-family:'Poppins','Hind Siliguri',sans-serif;font-weight:500;letter-spacing:0;font-size:30px;color:rgba(214,234,220,.82);}
.t-hero{font-family:'Poppins','Opekkha',sans-serif;font-weight:700;line-height:1.12;letter-spacing:0;}
.t-title{font-family:'Poppins','Hind Siliguri',sans-serif;font-weight:600;line-height:1.18;}
.t-body{font-family:'Poppins','Hind Siliguri',sans-serif;font-weight:400;line-height:1.32;}
.t-light{font-family:'Poppins','Hind Siliguri',sans-serif;font-weight:300;}
.lat{font-family:'Poppins',sans-serif;}
em{font-style:normal;color:#b8d8c2;-webkit-text-fill-color:#b8d8c2;}
.silver,.silver .w{color:#fff;}
.glow{text-shadow:0 1px 2px rgba(0,0,0,.22);}
.w{display:inline-block;white-space:pre;}
.w-orbs{position:absolute;inset:0;}
.orb{position:absolute;border-radius:50%;background:#90b79c;}
.ic{display:block;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;}
.logo-img{display:block;object-fit:contain;}
.pill{position:absolute;border-radius:999px;}
.dot{position:absolute;border-radius:50%;}
"""

ICONS = {
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "zap": '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"/>',
    "file": '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>',
    "search": '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/>',
    "phone": '<rect width="14" height="20" x="5" y="2" rx="2" ry="2"/><path d="M12 18h.01"/>',
    "laptop": '<path d="M20 16V7a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v9m16 0H4m16 0 1.28 2.55a1 1 0 0 1-.9 1.45H3.62a1 1 0 0 1-.9-1.45L4 16"/>',
    "cart": '<circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/>',
    "calendar": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4"/><path d="M8 2v4"/><path d="M3 10h18"/>',
    "sparkles": '<path d="M9.94 14.06 12 21l2.06-6.94L21 12l-6.94-2.06L12 3 9.94 9.94 3 12z"/><path d="M19 3v4"/><path d="M21 5h-4"/>',
    "code": '<path d="m16 18 6-6-6-6"/><path d="m8 6-6 6 6 6"/>',
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "dollar": '<path d="M12 2v20"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
    "video": '<path d="m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
    "star": '<path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>',
    "chart": '<path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/>',
    "user": '<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "grad": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/>',
    "package": '<path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/>',
    "table": '<rect width="18" height="18" x="3" y="3" rx="2"/><path d="M3 9h18"/><path d="M3 15h18"/><path d="M9 3v18"/>',
    "bulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "wand": '<path d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72"/><path d="m14 7 3 3"/>',
    "folder": '<path d="M20 20a2 2 0 0 0 2-2V8a2 2 0 0 0-2-2h-7.9a2 2 0 0 1-1.69-.9L9.6 3.9A2 2 0 0 0 7.93 3H4a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2Z"/>',
    "mic": '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><path d="M12 19v3"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
    "trend": '<path d="M22 7 13.5 15.5 8.5 10.5 2 17"/><path d="M16 7h6v6"/>',
    "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "store": '<path d="m2 7 4.41-4.41A2 2 0 0 1 7.83 2h8.34a2 2 0 0 1 1.42.59L22 7"/><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><path d="M2 7h20"/><path d="M22 7v3a2 2 0 0 1-2 2 2.7 2.7 0 0 1-2-1 2.7 2.7 0 0 1-2 1 2.7 2.7 0 0 1-2-1 2.7 2.7 0 0 1-2 1 2.7 2.7 0 0 1-2-1 2.7 2.7 0 0 1-2 1 2.7 2.7 0 0 1-2-1 2.7 2.7 0 0 1-2 1 2 2 0 0 1-2-2V7"/>',
    "terminal": '<path d="m4 17 6-6-6-6"/><path d="M12 19h8"/>',
    "puzzle": '<path d="M15.39 4.39a1 1 0 0 0 1.68-.474 2.5 2.5 0 1 1 3.014 3.015 1 1 0 0 0-.474 1.68l1.683 1.682a2.414 2.414 0 0 1 0 3.414L19.61 15.39a1 1 0 0 1-1.68-.474 2.5 2.5 0 1 0-3.014 3.015 1 1 0 0 1 .474 1.68l-1.683 1.682a2.414 2.414 0 0 1-3.414 0L8.61 19.61a1 1 0 0 0-1.68.474 2.5 2.5 0 1 1-3.014-3.015 1 1 0 0 0 .474-1.68l-1.683-1.682a2.414 2.414 0 0 1 0-3.414L4.39 8.61a1 1 0 0 1 1.68.474 2.5 2.5 0 1 0 3.014-3.015 1 1 0 0 1-.474-1.68l1.683-1.682a2.414 2.414 0 0 1 3.414 0z"/>',
    "history": '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l4 2"/>',
    "pen": '<path d="M12 20h9"/><path d="M16.376 3.622a1 1 0 0 1 3.002 3.002L7.368 18.635a2 2 0 0 1-.855.506l-2.872.838a.5.5 0 0 1-.62-.62l.838-2.872a2 2 0 0 1 .506-.854z"/>',
    "image": '<rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/>',
    "brain": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M12 5v13"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/>',
    "layers": '<path d="m12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83Z"/><path d="m22 17.65-9.17 4.16a2 2 0 0 1-1.66 0L2 17.65"/><path d="m22 12.65-9.17 4.16a2 2 0 0 1-1.66 0L2 12.65"/>',
    "send": '<path d="M14.536 21.686a.5.5 0 0 0 .937-.024l6.5-19a.496.496 0 0 0-.635-.635l-19 6.5a.5.5 0 0 0-.024.937l7.93 3.18a2 2 0 0 1 1.112 1.11z"/><path d="m21.854 2.147-10.94 10.939"/>',
    "plug": '<path d="M12 22v-5"/><path d="M9 8V2"/><path d="M15 8V2"/><path d="M18 8v5a4 4 0 0 1-4 4h-4a4 4 0 0 1-4-4V8Z"/>',
    "gift": '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5A4.8 8 0 0 1 12 8a4.8 8 0 0 1 4.5-5 2.5 2.5 0 0 1 0 5"/>',
    "eye": '<path d="M2.062 12.348a1 1 0 0 1 0-.696 10.75 10.75 0 0 1 19.876 0 1 1 0 0 1 0 .696 10.75 10.75 0 0 1-19.876 0"/><circle cx="12" cy="12" r="3"/>',
    "home": '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "list": '<path d="M3 12h.01"/><path d="M3 18h.01"/><path d="M3 6h.01"/><path d="M8 12h13"/><path d="M8 18h13"/><path d="M8 6h13"/>',
    "box": '<path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/>',
    "infinity": '<path d="M12 12c-2-2.67-4-4-6-4a4 4 0 1 0 0 8c2 0 4-1.33 6-4Zm0 0c2 2.67 4 4 6 4a4 4 0 0 0 0-8c-2 0-4 1.33-6 4Z"/>',
}


def icon(name, size=28, color="currentColor", stroke=2.0):
    return (f'<svg class="ic" width="{size}" height="{size}" viewBox="0 0 24 24" '
            f'style="color:{color};stroke-width:{stroke}">{ICONS[name]}</svg>')


LATIN = re.compile(r"[A-Za-z]")


def esc(s):
    return html.escape(s, quote=False)


def rich(text):
    """`*word*` -> <em>word</em>; everything else escaped."""
    out = []
    parts = re.split(r"(\*[^*]+\*)", text)
    for p in parts:
        if p.startswith("*") and p.endswith("*") and len(p) > 2:
            out.append(f"<em>{esc(p[1:-1])}</em>")
        else:
            out.append(esc(p))
    return "".join(out)


def words_html(text, cls="w"):
    """Split into word spans; `*a b*` marks an emphasised run (punctuation may follow the closing *)."""
    out = []
    emph = False
    for tok in text.split(" "):
        if not tok:
            continue
        m = re.match(r"^(\*?)(.*?)(\*?)([!?,.;:।—…)\]]*)$", tok)
        opn, body, cls_e, tail = m.groups()
        if opn:
            emph = True
        inner = f"<em>{esc(body)}</em>" if emph else esc(body)
        out.append(f'<span class="{cls}">{inner}{esc(tail)}</span>')
        if cls_e:
            emph = False
    return " ".join(out)


def plain(text):
    return text.replace("*", "")


def world_html(sid, w=W, h=H, x=0, y=0, rays=None):
    rays = rays or [(140, 150, .9), (420, 90, .6), (700, 220, 1.0), (1080, 120, .7), (1380, 260, .85), (1760, 110, .55)]
    # the world drifts in a few bokeh orbs (fixed seeds, like the ZTA ad's stage)
    orbs = "".join(
        f'<i class="orb" style="left:{ox}px;top:{oy}px;width:{os_}px;height:{os_}px;opacity:{oo};filter:blur({os_//4}px)"></i>'
        for ox, oy, os_, oo in [(180, 760, 120, .10), (520, 180, 70, .08), (930, 860, 160, .07), (1320, 300, 90, .10),
                               (1620, 740, 140, .08), (260, 420, 50, .12), (1500, 120, 60, .09), (1100, 560, 40, .12)]
        if ox < w + 100 and oy < h + 100)
    ray_html = "".join(
        f'<i class="ray" style="left:{rx}px;width:{rw}px;opacity:{ro}"></i>' for rx, rw, ro in rays)
    return (f'<div class="world" id="{sid}-world" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<div class="w-base"></div><div class="w-glow g1" id="{sid}-g1"></div><div class="w-glow g2" id="{sid}-g2"></div>'
            f'<div class="w-rays" id="{sid}-rays">{ray_html}</div><div class="w-orbs" id="{sid}-orbs">{orbs}</div>'
            f'<div class="w-grid"></div><div class="w-vig"></div></div>')


def world_motion_js(sid, dur):
    # Continuous, slow motion in the world behind the content: rays drift, glows travel, orbs rise.
    return (f'tl.fromTo("#{sid}-rays",{{x:-50}},{{x:70,duration:{dur:.3f},ease:"none"}},0);'
            f'tl.fromTo("#{sid}-g1",{{x:0,y:0}},{{x:140,y:60,duration:{dur:.3f},ease:"sine.inOut"}},0);'
            f'tl.fromTo("#{sid}-g2",{{x:0,y:0}},{{x:-120,y:-40,duration:{dur:.3f},ease:"sine.inOut"}},0);'
            f'tl.fromTo("#{sid}-orbs",{{y:0}},{{y:{-14 * dur:.0f},duration:{dur:.3f},ease:"none"}},0);')
