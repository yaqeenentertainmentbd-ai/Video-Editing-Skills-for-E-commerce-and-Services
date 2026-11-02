# VIDEO EDITING SFX MASTER GUIDE

**Owner:** Abir Hossen Soajol (Bangla AI / tech videos, ZTA Lab)
**Guide version:** 1.0, written 31 October 2026
**Applies to:** every long-form video, Short, Reel and TikTok we edit
**Built from:** the SFX library itself, our edit-builder code, and the six finished edits made with it (main video plus Reels 01–05)

This guide is the single source of truth for how we use sound effects. It is written so that a Claude instance on a different computer, with no memory of our earlier work, can reproduce our sound design using only:

1. this file, and
2. our SFX folder.

---

## 0. How to read this guide

### 0.1 Two kinds of statements

Every rule in this guide carries one of two labels:

| Label | Meaning | How Claude must treat it |
|---|---|---|
| **[VERIFIED]** | Measured from the audio files, or read directly from our builder code and the six finished edits. This is what we actually do. | Follow it exactly. Do not change it without the user's approval. |
| **[RECOMMENDED]** | New guidance for situations our edits have not covered yet. It follows the same logic as the verified rules but has not been tested in a finished video. | Use it when the situation comes up, and tell the user you applied a recommendation, not an established rule. |

Where something could not be verified, the guide says so under **Section 15 (Known gaps)**. Do not fill those gaps with guesses.

### 0.2 Units used in this guide

- **Time:** seconds, measured on the finished video's timeline, unless a row says "source clock".
- **Level (dB):** the loudest 100 ms RMS window of the file, mono mix at 48 kHz, in dBFS. Section 6.1 explains why we use this measure.
- **Gain (×):** linear amplitude multiplier applied to the file. `dB = 20 × log10(gain)`.
- **Sync point (s):** the time inside the file where its loudest 100 ms window is centred. This is the moment the ear hears as "the hit".
- **MASTER:** the volume multiplier we apply to the voice in a given edit. Every SFX volume is multiplied by the same MASTER so SFX stay at a fixed distance from the voice.

### 0.3 Table of contents

1. Instructions for Claude (read first)
2. Locating and verifying the SFX library
3. Library inventory and file manifest
4. The family system (how we group, rank and level SFX)
5. Event-to-SFX rules (what gets a sound, and when)
6. Timing, levels and mixing
7. Density, spacing and restraint
8. Situation guidelines (captions, B-roll, motion graphics, zooms, scene changes, reveals, music, layering)
9. SFX reference database (every file, by family)
10. Real examples from our projects
11. Step-by-step workflow for a new edit
12. Fallback rules
13. Reference implementation (portable Python)
14. Licensing and credits
15. Known gaps and unverified items
16. Appendix A: legacy library (not part of the active workflow)
17. Appendix B: full checksum manifest

---

## 1. Instructions for Claude (read first)

You are about to edit a video for this creator. Follow these instructions in order.

1. **Read this entire guide before you place a single sound.** The rules depend on each other: timing depends on the sync points in Section 9, levels depend on the family targets in Section 4, and density limits in Section 7 override everything else.
2. **Locate the SFX library** using Section 2. Ask the user for the folder path if it was not given. Never assume a path from this guide; the original machine's paths are recorded only as history.
3. **Verify the library** with the check in Section 2.4. Every file you plan to use must exist and match its checksum. Report missing or changed files to the user before editing.
4. **Analyse the video before choosing sounds.** Build a list of visual events with timestamps: graphics entering, cards and list items landing, number count-ups, typing animations, notifications, hard cuts, B-roll cutaways, punch-in zooms, chapter titles and big claims. Also note the music and the speech pauses.
5. **Map each event to a family** with the table in Section 5. If an event is not in that table, it gets **no sound**. Do not add sounds for variety.
6. **Place each sound** with the timing formula in Section 6.2, the volume formula in Section 6.3 and the rotation rule in Section 6.5.
7. **Thin the cue list** with the one-sound-per-moment rule in Section 6.4, then check density against Section 7.
8. **Balance with the music** using Section 6.6.
9. **Check the final mix** with the QA checklist in Section 11.3. Report the measured loudness to the user.
10. **Tell the user what you did:** how many SFX, which families, any recommended (unverified) rules you applied, and any file you could not find.

Hard rules that apply to every edit:

- **Never invent a filename.** Use only files listed in Section 3 or files the user adds and you have measured (Section 12.4).
- **Never download or generate replacement SFX** without asking the user, and never use a file whose licence is unknown.
- **Never put a sound on an ordinary caption change.** Captions are silent in our style [VERIFIED].
- **Never let an SFX cover a spoken word.** Our levels already sit well under the voice; do not raise them to "make the edit feel bigger".
- **One dominant sound per moment.** When two cues fall within 0.2 s, keep only the higher-priority one (Section 6.4).

---

## 2. Locating and verifying the SFX library

### 2.1 What the SFX folder looks like

The library root (called **`SFX_ROOT`** in this guide) is a folder that contains these 15 subfolders and catalogue files [VERIFIED]:

```
SFX_ROOT/
├── 01_whoosh_soft/
├── 02_whoosh_fast_whip/
├── 03_pop_ui/
├── 04_click_tap/
├── 05_glass_liquid/
├── 06_tick_counter/
├── 07_typing_keys/
├── 08_riser/
├── 09_impact_hit/
├── 10_glitch_digital/
├── 11_notification/
├── 12_swipe_scroll/
├── 13_shimmer_sparkle/
├── 14_reverse_suck/
├── 15_camera_shutter/
├── SFX_CATALOGUE.md          (sources, licences, descriptions)
├── SFX_CATALOGUE.csv         (same data as CSV)
├── REFERENCE_SOUND_ANALYSIS.md  (analysis of the style reference video)
└── VIDEO_EDITING_SFX_MASTER_GUIDE.md  (this file)
```

On the original machine `SFX_ROOT` was the folder `sfx` inside the project folder `Editing`. That location is history only; do not rely on it.

### 2.2 Five active files that live outside SFX_ROOT

Our active set also uses five files that were **not** stored in `SFX_ROOT` on the original machine [VERIFIED]:

| File | Family | Original location (relative to the project folder `Editing/`) | Used in edits |
|---|---|---|---|
| `whoosh_soft_02.wav` | whoosh | `work/sfx/whoosh_soft_02.wav` | 23 times |
| `whoosh_soft_04.wav` | whoosh | `work/sfx/whoosh_soft_04.wav` | 22 times |
| `fun_double_blink.mp3` | fun | `work/sfx_fun/fun_double_blink.mp3` | 1 time |
| `fun_xylo_sting.mp3` | fun | `work/sfx_fun/fun_xylo_sting.mp3` | never |
| `fun_cute_bounce.mp3` | fun | `work/sfx_fun/fun_cute_bounce.mp3` | never |

A sixth file, `work/sfx_fun/fun_mild_surprise.mp3`, sits next to them but was never part of the active set.

**Before moving to a new computer [RECOMMENDED]:** copy these files into `SFX_ROOT` so the folder is self-contained, for example:

```
SFX_ROOT/01_whoosh_soft/whoosh_soft_02.wav
SFX_ROOT/01_whoosh_soft/whoosh_soft_04.wav
SFX_ROOT/16_fun_sting/fun_double_blink.mp3
SFX_ROOT/16_fun_sting/fun_xylo_sting.mp3
SFX_ROOT/16_fun_sting/fun_cute_bounce.mp3
SFX_ROOT/16_fun_sting/fun_mild_surprise.mp3
```

The lookup method in 2.3 finds files by name anywhere under the folders you search, so it works whether or not they were moved. If they are missing, Section 12 explains what to use instead.

### 2.3 How to resolve a file

Never build a path from this guide's history. Resolve each file like this:

1. Get `SFX_ROOT` from the user. If the user also gives an "extras" folder, search it too.
2. **Search by exact filename**, recursively, under every search folder. File names in this library are unique.
3. If found, **check the MD5** against Appendix B. A mismatch means the file was edited or replaced: warn the user and do not use it until they confirm.
4. If not found by name, **search by MD5** (the file may have been renamed). If found, use it and tell the user about the new name.
5. If still not found, apply the fallback for that file's family (Section 12).
6. Paths in this guide are written relative to `SFX_ROOT` with forward slashes. Convert to the local separator only when you call a tool.

### 2.4 Verification check

Run this before every editing session. It needs only Python 3 (standard library).

```python
import hashlib, os, sys

SFX_ROOT = sys.argv[1]                 # e.g. "D:/projects/sfx" or "/Users/me/sfx"
EXTRA = sys.argv[2:]                   # optional extra folders to search
MANIFEST = {                           # filename -> md5, copied from Appendix B
    "whoosh_soft_digital-whoosh-soft_02.mp3": "b4afe3c92a350575bc129f97bd3eaa62",
    "whoosh_soft_swing-1-5_01.mp3": "35ae4c786cbc136c555b39f518e0041f",
    "whoosh_soft_whoosh-soft_03.mp3": "81caef265e60a53d7c21adff2de280ae",
    "whoosh_fast_whip_clean-fast-swoosh_01.mp3": "dd1467f64e834cc215071df28d8cc693",
    "whoosh_fast_whip_whip-10_04.mp3": "2df86d41f98d8a3c222c4c274b6a7e0c",
    "whoosh_fast_whip_whip-8_02.mp3": "59d841d3c03add4d29f1796c9a05ef7d",
    "whoosh_fast_whip_whip-9_03.mp3": "0fe32340cd56bc188db3ddffedae9e7d",
    "pop_ui_bop-sound-effect-button_04.mp3": "ceea4f42ccfd173c628b52f817568817",
    "pop_ui_click-pop-two-part_01.mp3": "e893eba58846b0cf4e9edb0252038043",
    "pop_ui_the-best-bubble-pop-sound-for-ga_03.mp3": "a0aacd980e638b0e63405f9b170c7ec9",
    "pop_ui_ui-series-hollow-pop_02.mp3": "84f83efe13c2f666f79ce5cac7be17ed",
    "click_tap_lego-click-short_02.mp3": "a50330028a3c048d78b8093e5536250c",
    "click_tap_menu-fx-03-descending_04.mp3": "6e072a6bb1b68d29ab82e8bbab2fa9e4",
    "click_tap_snap-click-07_01.mp3": "6e33b59f838ac1f78aab2c327e4614e8",
    "click_tap_ui-click_03.mp3": "81779696d268ae55fa76cc6fae61cae3",
    "glass_liquid_sci-fi-bubble-pop_04.mp3": "477219c9f4f30bb0641847e2af473d0f",
    "glass_liquid_soap-bubble-pop-mouth-perc_01.mp3": "ab90327eca84710a0d24875c814e3398",
    "glass_liquid_the-best-bubble-pop-sound-for-ga_02.mp3": "a0aacd980e638b0e63405f9b170c7ec9",
    "tick_counter_mab-clock-tick-1-20080713_02.mp3": "f5e9ffc7049d5f13600591bf0e17965b",
    "tick_counter_sfx-ambiance-clock-tick_01.mp3": "8320b7d1869b566252a051f73509bc34",
    "tick_counter_soft-ui-digital-tick_04.mp3": "ce2ebd737bac3df7ebacaa7729d030e5",
    "typing_keys_keyboard-computer-mechanical-typ_04.mp3": "10f067577f6c9898675a6a65d549e3da",
    "typing_keys_mech-keyboard-01_02.mp3": "a3c51ce4fbbce0a88e4e6ab4da4942f8",
    "typing_keys_mech-keyboard-02_03.mp3": "b8d74b820939b7108a3dfdaadf75b114",
    "riser_brush-rising-woosh-muffle-000212_03.mp3": "477735a956d87fccf5905ed78a212ca0",
    "riser_energy-riser_01.mp3": "7be97b89bc9f25ec0d66e97361fb9e3f",
    "riser_riser_02.mp3": "13146f8aa3d8dd8a627403d0cfae865f",
    "riser_whoosh_04.mp3": "56416e83afb708bfe7560460b1e51e6c",
    "impact_hit_deep-cinematic-impact_01.mp3": "7208b6f26f91e32df262440b91e509a3",
    "impact_hit_dia-s15-warped-bass-hits-1_03.mp3": "8e40ed24925d765bde40f62098771be9",
    "impact_hit_super-low-bass-hit-kick-drum-wav_02.mp3": "048172ff677aff92322e470750d44d5c",
    "glitch_digital_glitch-corruption_03.mp3": "2ed49d25cd3ff816801a505cc19ca199",
    "glitch_digital_interference_01.mp3": "6f21bb38a0aa8253c9f35314aec7ef4d",
    "glitch_digital_static-glitch_02.mp3": "e4a5d86dae693fe284b234f58c70432f",
    "notification_chime-notification_04.mp3": "68f9c5e8f246a3465b23ceda5de166a4",
    "notification_notification-sound_02.mp3": "580c64e4bed11173ba0104b5b4ccf9bb",
    "notification_notification-sound_03.mp3": "75902399e68a14f3cf487a666baebb06",
    "swipe_scroll_sfx-whoosh-high-1-12_01.mp3": "26f205061082859c4ecd8c23ebb924e8",
    "swipe_scroll_whip01_03.mp3": "926f5584176bb93ab5cd9d6466c2f6d1",
    "swipe_scroll_whip02_02.mp3": "ab53e514a653c3510976a96fa603ae62",
    "swipe_scroll_whips04_04.mp3": "59f341090ddef02d186cc1a6dc708cda",
    "shimmer_sparkle_fantasy-ui-button-3_03.mp3": "acb60b776ef1d9d35c474ae5866eb985",
    "shimmer_sparkle_transition-action-jump-pitch-shi_01.mp3": "24cde79cb5e123174d76fa52b0ed0d55",
    "shimmer_sparkle_transition-action-jump-pitch-shi_02.mp3": "8aa80691802ec33249e0fdea091d411e",
    "reverse_suck_backwards-whoosh_02.mp3": "7fc6e5a841af00d294138a3459d3d2ed",
    "reverse_suck_reverse-cymbal_05.mp3": "d96eb7ac6b52c615dc450fab976ba4a9",
    "reverse_suck_sfx-weird-watery-sucking-sound_03.mp3": "4b7c089d7c5dbd65f4f636e1d259daea",
    "camera_shutter_camera-shutter-analogue-film-slr_02.mp3": "de0277b9b3271d2a457e6e13ecc25d0a",
    "camera_shutter_camera-shutter-analogue-film-slr_04.mp3": "143c36a24f6e0c48346d0739ff67b5a5",
    "camera_shutter_shutter_03.mp3": "c6b2c75d46eec4af4b5314eaa490ea37",
    "camera_shutter_taking-photo-with-camera_01.mp3": "bb5fc0da39ca642454c9ab6d6bbb0baf",
    "fun_cute_bounce.mp3": "5b6caf0d7ce67043b3ad628be029cfba",
    "fun_double_blink.mp3": "dec54b7ea883ac9e97a644a8893c836c",
    "fun_mild_surprise.mp3": "4a72057b0e5858a887a229b9bf3ef773",
    "fun_xylo_sting.mp3": "77aa74a316ebb6e82573f6eb95a5f295",
    "whoosh_soft_02.wav": "9f05710d4ec2f3111f980134397e2d27",
    "whoosh_soft_04.wav": "286e01e802ccf40d3de652dd947b7752",
}

index = {}
for root in [SFX_ROOT, *EXTRA]:
    for d, _, files in os.walk(root):
        for f in files:
            index.setdefault(f, []).append(os.path.join(d, f))

by_md5 = {}
def md5(p):
    return hashlib.md5(open(p, "rb").read()).hexdigest()

missing, changed, ok = [], [], 0
for name, h in MANIFEST.items():
    hits = index.get(name, [])
    if not hits:
        if not by_md5:
            for paths in index.values():
                for p in paths:
                    if p.lower().endswith((".mp3", ".wav", ".ogg")):
                        by_md5[md5(p)] = p
        if h in by_md5:
            print("RENAMED", name, "->", by_md5[h]); ok += 1
        else:
            missing.append(name)
    elif md5(hits[0]) != h:
        changed.append(name)
    else:
        ok += 1
print(f"ok {ok}  missing {len(missing)}  changed {len(changed)}")
for n in missing: print("MISSING", n)
for n in changed: print("CHANGED", n)
```

Report the result to the user. Missing files in the active set (Section 3.2) matter; missing files that are not in the active set do not block editing.

### 2.5 Tools this workflow assumes

- **ffmpeg / ffprobe** for measuring, trimming and loudness checks [VERIFIED: used for every measurement in this guide].
- **Python 3** with **numpy** for the measurement in Section 6.1 and the reference implementation in Section 13.
- An editor or renderer that supports per-clip start time, duration, media offset, volume and fades. Our edits used HyperFrames (HTML/GSAP rendered to video) with `<audio>` clips, but the rules are tool-independent. Section 13.3 explains how to translate them for Premiere Pro, DaVinci Resolve or CapCut.

---

## 3. Library inventory and file manifest

### 3.1 Summary [VERIFIED]

- **SFX_ROOT:** 51 audio files in 15 category folders, all MP3 (Freesound HQ previews, not re-encoded). Every category has 3–4 takes.
- **Licences:** 46 CC0, 3 CC BY 4.0, 2 CC BY 3.0 (details in `SFX_CATALOGUE.md` and Section 14).
- **Extras outside SFX_ROOT:** 2 WAV whooshes (Mixkit licence) and 4 "fun" stings (CC0 per our credits file).
- **Active set:** 45 files make up the set our edit builder draws from: 40 from `SFX_ROOT` plus the 5 extras listed in 2.2. Of these, 34 were actually played in at least one finished edit.
- **Not in the active set:** 11 files in `SFX_ROOT`. Five are CC BY (left out so no SFX credit is needed). The reason for excluding the other six was not recorded (Section 15).

Total SFX placements in finished edits: **345** (main video 198, Reel 01 12, Reel 02 33, Reel 03 29, Reel 04 34, Reel 05 39).

### 3.2 Inventory by category

#### 01_whoosh_soft

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `whoosh_soft_digital-whoosh-soft_02.mp3` | `01_whoosh_soft/whoosh_soft_digital-whoosh-soft_02.mp3` | whoosh | 0.95 | CC0 1.0 | Active, used 27× |
| `whoosh_soft_swing-1-5_01.mp3` | `01_whoosh_soft/whoosh_soft_swing-1-5_01.mp3` | whoosh | 0.91 | CC0 1.0 | Not active |
| `whoosh_soft_whoosh-soft_03.mp3` | `01_whoosh_soft/whoosh_soft_whoosh-soft_03.mp3` | whoosh | 0.37 | CC BY 4.0 | Not active |

#### 02_whoosh_fast_whip

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `whoosh_fast_whip_clean-fast-swoosh_01.mp3` | `02_whoosh_fast_whip/whoosh_fast_whip_clean-fast-swoosh_01.mp3` | whip | 0.92 | CC0 1.0 | Active, used 4× |
| `whoosh_fast_whip_whip-10_04.mp3` | `02_whoosh_fast_whip/whoosh_fast_whip_whip-10_04.mp3` | whip | 0.43 | CC0 1.0 | Active, used 3× |
| `whoosh_fast_whip_whip-8_02.mp3` | `02_whoosh_fast_whip/whoosh_fast_whip_whip-8_02.mp3` | whip | 0.64 | CC0 1.0 | Active, used 3× |
| `whoosh_fast_whip_whip-9_03.mp3` | `02_whoosh_fast_whip/whoosh_fast_whip_whip-9_03.mp3` | whip | 0.54 | CC0 1.0 | Active, used 3× |

#### 03_pop_ui

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `pop_ui_bop-sound-effect-button_04.mp3` | `03_pop_ui/pop_ui_bop-sound-effect-button_04.mp3` | pop | 0.17 | CC0 1.0 | Active, used 27× |
| `pop_ui_click-pop-two-part_01.mp3` | `03_pop_ui/pop_ui_click-pop-two-part_01.mp3` | pop | 0.50 | CC0 1.0 | Active, used 27× |
| `pop_ui_the-best-bubble-pop-sound-for-ga_03.mp3` | `03_pop_ui/pop_ui_the-best-bubble-pop-sound-for-ga_03.mp3` | pop | 0.31 | CC0 1.0 | Active, used 23× |
| `pop_ui_ui-series-hollow-pop_02.mp3` | `03_pop_ui/pop_ui_ui-series-hollow-pop_02.mp3` | pop | 0.51 | CC0 1.0 | Active, used 21× |

#### 04_click_tap

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `click_tap_lego-click-short_02.mp3` | `04_click_tap/click_tap_lego-click-short_02.mp3` | click | 0.18 | CC0 1.0 | Active, never used |
| `click_tap_menu-fx-03-descending_04.mp3` | `04_click_tap/click_tap_menu-fx-03-descending_04.mp3` | click | 0.24 | CC0 1.0 | Active, never used |
| `click_tap_snap-click-07_01.mp3` | `04_click_tap/click_tap_snap-click-07_01.mp3` | click | 0.21 | CC0 1.0 | Active, never used |
| `click_tap_ui-click_03.mp3` | `04_click_tap/click_tap_ui-click_03.mp3` | click | 0.60 | CC0 1.0 | Not active |

#### 05_glass_liquid

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `glass_liquid_sci-fi-bubble-pop_04.mp3` | `05_glass_liquid/glass_liquid_sci-fi-bubble-pop_04.mp3` | glass | 0.49 | CC0 1.0 | Active, used 8× |
| `glass_liquid_soap-bubble-pop-mouth-perc_01.mp3` | `05_glass_liquid/glass_liquid_soap-bubble-pop-mouth-perc_01.mp3` | glass | 0.75 | CC0 1.0 | Not active |
| `glass_liquid_the-best-bubble-pop-sound-for-ga_02.mp3` | `05_glass_liquid/glass_liquid_the-best-bubble-pop-sound-for-ga_02.mp3` | glass | 0.31 | CC0 1.0 | Active, used 6× |

#### 06_tick_counter

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `tick_counter_mab-clock-tick-1-20080713_02.mp3` | `06_tick_counter/tick_counter_mab-clock-tick-1-20080713_02.mp3` | tick | 0.25 | CC BY 3.0 | Not active |
| `tick_counter_sfx-ambiance-clock-tick_01.mp3` | `06_tick_counter/tick_counter_sfx-ambiance-clock-tick_01.mp3` | tick | 0.11 | CC0 1.0 | Active, used 8× |
| `tick_counter_soft-ui-digital-tick_04.mp3` | `06_tick_counter/tick_counter_soft-ui-digital-tick_04.mp3` | tick | 0.24 | CC0 1.0 | Active, used 6× |

#### 07_typing_keys

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `typing_keys_keyboard-computer-mechanical-typ_04.mp3` | `07_typing_keys/typing_keys_keyboard-computer-mechanical-typ_04.mp3` | type | 2.39 | CC BY 4.0 | Not active |
| `typing_keys_mech-keyboard-01_02.mp3` | `07_typing_keys/typing_keys_mech-keyboard-01_02.mp3` | type | 1.28 | CC0 1.0 | Active, used 9× |
| `typing_keys_mech-keyboard-02_03.mp3` | `07_typing_keys/typing_keys_mech-keyboard-02_03.mp3` | type | 1.28 | CC0 1.0 | Active, used 4× |

#### 08_riser

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `riser_brush-rising-woosh-muffle-000212_03.mp3` | `08_riser/riser_brush-rising-woosh-muffle-000212_03.mp3` | riser | 1.77 | CC0 1.0 | Active, used 2× |
| `riser_energy-riser_01.mp3` | `08_riser/riser_energy-riser_01.mp3` | riser | 1.93 | CC0 1.0 | Active, used 1× |
| `riser_riser_02.mp3` | `08_riser/riser_riser_02.mp3` | riser | 2.00 | CC0 1.0 | Active, used 1× |
| `riser_whoosh_04.mp3` | `08_riser/riser_whoosh_04.mp3` | riser | 3.62 | CC BY 3.0 | Not active |

#### 09_impact_hit

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `impact_hit_deep-cinematic-impact_01.mp3` | `09_impact_hit/impact_hit_deep-cinematic-impact_01.mp3` | impact | 2.00 | CC BY 4.0 | Not active |
| `impact_hit_dia-s15-warped-bass-hits-1_03.mp3` | `09_impact_hit/impact_hit_dia-s15-warped-bass-hits-1_03.mp3` | impact | 0.37 | CC0 1.0 | Active, used 6× |
| `impact_hit_super-low-bass-hit-kick-drum-wav_02.mp3` | `09_impact_hit/impact_hit_super-low-bass-hit-kick-drum-wav_02.mp3` | impact | 0.33 | CC0 1.0 | Active, used 3× |

#### 10_glitch_digital

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `glitch_digital_glitch-corruption_03.mp3` | `10_glitch_digital/glitch_digital_glitch-corruption_03.mp3` | glitch | 1.34 | CC0 1.0 | Active, used 2× |
| `glitch_digital_interference_01.mp3` | `10_glitch_digital/glitch_digital_interference_01.mp3` | glitch | 0.60 | CC0 1.0 | Active, never used |
| `glitch_digital_static-glitch_02.mp3` | `10_glitch_digital/glitch_digital_static-glitch_02.mp3` | glitch | 0.36 | CC0 1.0 | Active, never used |

#### 11_notification

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `notification_chime-notification_04.mp3` | `11_notification/notification_chime-notification_04.mp3` | notif | 0.32 | CC0 1.0 | Active, used 6× |
| `notification_notification-sound_02.mp3` | `11_notification/notification_notification-sound_02.mp3` | notif | 0.41 | CC0 1.0 | Active, used 4× |
| `notification_notification-sound_03.mp3` | `11_notification/notification_notification-sound_03.mp3` | notif | 0.69 | CC0 1.0 | Active, used 4× |

#### 12_swipe_scroll

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `swipe_scroll_sfx-whoosh-high-1-12_01.mp3` | `12_swipe_scroll/swipe_scroll_sfx-whoosh-high-1-12_01.mp3` | swipe | 0.50 | CC0 1.0 | Not active |
| `swipe_scroll_whip01_03.mp3` | `12_swipe_scroll/swipe_scroll_whip01_03.mp3` | swipe | 0.78 | CC0 1.0 | Active, used 28× |
| `swipe_scroll_whip02_02.mp3` | `12_swipe_scroll/swipe_scroll_whip02_02.mp3` | swipe | 0.67 | CC0 1.0 | Active, used 27× |
| `swipe_scroll_whips04_04.mp3` | `12_swipe_scroll/swipe_scroll_whips04_04.mp3` | swipe | 0.59 | CC0 1.0 | Active, used 25× |

#### 13_shimmer_sparkle

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `shimmer_sparkle_fantasy-ui-button-3_03.mp3` | `13_shimmer_sparkle/shimmer_sparkle_fantasy-ui-button-3_03.mp3` | shimmer | 1.26 | CC0 1.0 | Active, used 6× |
| `shimmer_sparkle_transition-action-jump-pitch-shi_01.mp3` | `13_shimmer_sparkle/shimmer_sparkle_transition-action-jump-pitch-shi_01.mp3` | shimmer | 1.32 | CC0 1.0 | Active, used 2× |
| `shimmer_sparkle_transition-action-jump-pitch-shi_02.mp3` | `13_shimmer_sparkle/shimmer_sparkle_transition-action-jump-pitch-shi_02.mp3` | shimmer | 1.15 | CC0 1.0 | Active, used 2× |

#### 14_reverse_suck

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `reverse_suck_backwards-whoosh_02.mp3` | `14_reverse_suck/reverse_suck_backwards-whoosh_02.mp3` | suck | 0.66 | CC0 1.0 | Active, used 1× |
| `reverse_suck_reverse-cymbal_05.mp3` | `14_reverse_suck/reverse_suck_reverse-cymbal_05.mp3` | suck | 2.00 | CC0 1.0 | Active, never used |
| `reverse_suck_sfx-weird-watery-sucking-sound_03.mp3` | `14_reverse_suck/reverse_suck_sfx-weird-watery-sucking-sound_03.mp3` | suck | 2.00 | CC0 1.0 | Not active |

#### 15_camera_shutter

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `camera_shutter_camera-shutter-analogue-film-slr_02.mp3` | `15_camera_shutter/camera_shutter_camera-shutter-analogue-film-slr_02.mp3` | shutter | 0.67 | CC0 1.0 | Active, never used |
| `camera_shutter_camera-shutter-analogue-film-slr_04.mp3` | `15_camera_shutter/camera_shutter_camera-shutter-analogue-film-slr_04.mp3` | shutter | 0.63 | CC0 1.0 | Active, never used |
| `camera_shutter_shutter_03.mp3` | `15_camera_shutter/camera_shutter_shutter_03.mp3` | shutter | 0.64 | CC0 1.0 | Active, never used |
| `camera_shutter_taking-photo-with-camera_01.mp3` | `15_camera_shutter/camera_shutter_taking-photo-with-camera_01.mp3` | shutter | 0.77 | CC0 1.0 | Not active |

#### Extras outside SFX_ROOT

| File | Rel. path | Family | Len (s) | Licence | Status |
|---|---|---|---:|---|---|
| `fun_cute_bounce.mp3` | `work/sfx_fun/fun_cute_bounce.mp3 (extra)` | fun | 0.34 | CC0 (per credits file) | Active, never used |
| `fun_double_blink.mp3` | `work/sfx_fun/fun_double_blink.mp3 (extra)` | fun | 1.66 | CC0 (per credits file) | Active, used 1× |
| `fun_mild_surprise.mp3` | `work/sfx_fun/fun_mild_surprise.mp3 (extra)` | fun | 3.65 | CC0 (per credits file) | Not active |
| `fun_xylo_sting.mp3` | `work/sfx_fun/fun_xylo_sting.mp3 (extra)` | fun | 1.90 | CC0 (per credits file) | Active, never used |
| `whoosh_soft_02.wav` | `work/sfx/whoosh_soft_02.wav (extra)` | whoosh | 1.39 | Mixkit SFX Free License | Active, used 23× |
| `whoosh_soft_04.wav` | `work/sfx/whoosh_soft_04.wav (extra)` | whoosh | 1.10 | Mixkit SFX Free License | Active, used 22× |


**Status column:**
- **Active, used N×**: in the active set and placed N times across the six finished edits.
- **Active, never used**: in the active set, but no finished edit has needed it yet.
- **Not active**: in the library but excluded from the active set. Do not use it unless the user approves (and, for CC BY files, adds the credit from Section 14).

---

## 4. The family system

Every SFX belongs to one **family**. A family is the unit we choose, level and rotate. Rules in this guide always name a family first, then the file is chosen by rotation (Section 6.5).

### 4.1 Families, levels and priority [VERIFIED]

| Priority | Family | Library folder | Level target (dBFS, loudest 100 ms) | Distance below voice* | Active takes | Typical length |
|---:|---|---|---:|---:|---:|---|
| 1 | **impact** | `09_impact_hit` | -25 | 8.6 dB | 2 | 0.33–0.37 s |
| 2 | **riser** | `08_riser` | -27 | 10.6 dB | 3 | 1.77–2.00 s |
| 3 | **fun** | `(extras: fun stings)` | -30 | 13.6 dB | 3 | 0.34–1.90 s |
| 4 | **whip** | `02_whoosh_fast_whip` | -29 | 12.6 dB | 4 | 0.43–0.92 s |
| 5 | **suck** | `14_reverse_suck` | -29 | 12.6 dB | 2 | 0.66–2.00 s |
| 6 | **notif** | `11_notification` | -32 | 15.6 dB | 3 | 0.32–0.69 s |
| 7 | **whoosh** | `01_whoosh_soft` | -31 | 14.6 dB | 3 | 0.95–1.39 s |
| 8 | **swipe** | `12_swipe_scroll` | -32 | 15.6 dB | 3 | 0.59–0.78 s |
| 9 | **type** | `07_typing_keys` | -36 | 19.6 dB | 2 | 1.28–1.28 s |
| 10 | **pop** | `03_pop_ui` | -33 | 16.6 dB | 4 | 0.17–0.51 s |
| 11 | **glass** | `05_glass_liquid` | -33 | 16.6 dB | 2 | 0.31–0.49 s |
| 12 | **click** | `04_click_tap` | -34 | 17.6 dB | 3 | 0.18–0.24 s |
| 13 | **tick** | `06_tick_counter` | -35 | 18.6 dB | 2 | 0.11–0.24 s |
| 14 | **shimmer** | `13_shimmer_sparkle` | -33 | 16.6 dB | 3 | 1.15–1.32 s |
| 15 | **glitch** | `10_glitch_digital` | -33 | 16.6 dB | 3 | 0.36–1.34 s |
| 16 | **shutter** | `15_camera_shutter` | -31 | 14.6 dB | 3 | 0.63–0.67 s |

\* "Distance below voice" compares the family target with the median loudness of our raw voice recording (−16.4 dBFS per 100 ms window; −16.0 LUFS integrated). If the voice in a new project is louder or quieter, keep the **distance**, not the absolute number (Section 6.3).

**Priority** decides which cue survives when two cues collide (Section 6.4): rank 1 beats everything below it.

### 4.2 What the levels say about our style

- **Impacts are the loudest sound we use, and still about 9 dB under the voice.** Nothing ever competes with speech.
- **Small UI sounds (pop, glass, click, tick, typing) sit 16–20 dB under the voice.** They are felt more than heard: they confirm that something landed.
- **Motion sounds (whoosh, swipe, whip) sit 13–16 dB under the voice.** They carry the transitions.
- **Risers sit about 11 dB under the voice** at their climax and are always paired with a payoff (an impact or a hero word).

---

## 5. Event-to-SFX rules

This is the core of our style. If an event is not listed here, it gets no sound.

### 5.1 Events that always get a sound [VERIFIED]

Offsets are seconds from the moment the visual event starts. "Scene" means a graphic composition (panel, card, full-screen graphic).

| Visual event | Family | Placement | Notes |
|---|---|---|---|
| Full-screen graphic enters (blur/focus-pull in) | whoosh | scene start +0.00 | Exit is silent. |
| B-roll cutaway enters (blur in) | whoosh | B-roll start +0.00 | Exit is silent. |
| Side panel slides in (long-form split screen) | swipe | panel start +0.05 | Silent if the panel cross-fades from a previous panel on the same side. |
| Bottom panel slides up (Shorts/Reels stacked layout) | swipe | panel start +0.05 | Silent for the panel that is already on screen at frame 0. |
| Hard cut / seam between source segments (Shorts/Reels) | whoosh | exactly on the cut | Cued on every seam in Reels 01–05 (a higher-priority cue within 0.2 s replaces it). |
| Light-band sweep across the frame (topic change, long-form) | whoosh | sweep time −0.05 | 12 sweeps in the main video. |
| Title card with glass icon badge | glass | scene start +0.15 | The badge landing. |
| Big-word card | whoosh on the first line's word reveal; glass when the pill/label lands | first line start; pill time | Hero claims also get a hand-placed impact (5.2). |
| Logo tiles appear | pop | each logo +0.05 | One pop per logo. |
| Number count-up (stat card) | glass when the number pill lands (+0.30); 3 ticks across the first half of the count (count start, +¼, +½ of count duration); pop at 95 % of the count | as stated | The pop marks the final number. |
| Chat window: user prompt types out | type | typing start, trimmed to the typing duration + 0.05 s | Main video adds a 0.12 s fade-out to the trimmed typing. |
| Chat window: AI reply starts | shimmer | first reply bubble only | Later replies are silent. |
| Search bar | whoosh when the bar enters (+0.05); type for the query; pop per result card | as stated | |
| List, grid, steps, compare, devices items | pop | each item as it lands (compare +0.10, flow nodes +0.15) | One pop per item. |
| Flow diagram centre | glass | +0.20 | |
| Document assembles from files | pop on the first file; whoosh when the document forms | as stated | |
| Devices card | whoosh at +0.10, pop per device | as stated | |
| Phone notification appears | notif | each notification | |
| Overlay chip (small floating label) | pop by default; can be overridden to glass, glitch or notif to match meaning | chip start +0.02 | See 5.2 for the overrides we used. |
| Lower third | swipe | +0.02 | |
| Fast punch-in camera zoom (≥1.1×, ≤0.3 s) on an emphasised phrase | whip | zoom start (+0.05 when the zoom has a duration) | 14 of 18 such zooms in the main video have one. |

### 5.2 Hand-placed accents [VERIFIED]

These are added by hand on top of the automatic rules, for story beats rather than graphics.

| Story beat | Family | How we placed it | Example |
|---|---|---|---|
| Video's very first frame (cold open) | impact | at 0.00 | Main video opening. A shimmer was also cued at 0.05 s, but the one-sound-per-moment rule removed it, so only the impact plays. |
| Hero claim / chapter word | impact | on the hero word's reveal | "স্বর্ণযুগ" (main 532.5 s), "Claude এডিট করেছে" (main 595.3 s), "Claude কে স্কিল শেখানো যায়" (main 662.8 s) |
| Build into a hero claim | riser | climax on the first line of the card, impact follows on the hero word | Main: riser 530.3 → impact 532.5; riser 594.4 → impact 595.3. Reel 04: riser 532.55 → impact 532.82 (source clock) |
| Tension before a number reveal | riser | climax on the number card | Main 44.6 s, into the "$20" stat |
| Something negative, broken or "wrong" | glitch | on the word or chip | "ওভার বায়াসড" (main 26.35 s), chip "শুধু মোবাইল? ব্যাড লাক!" (main 193.55 s), out-of-stock shop card (Reel 05) |
| Delivery, message, "it arrived" | notif | on the word or chip | Chip "২ দিন পরে — দরজায় ডেলিভারি" (main 494.6 s), Reel 05 hook "দরজায় চলে আসছে" |
| Short spoken greeting with a hard punch-in | pop | on the punch | "হ্যালো!" (main 9.52 s) |
| A recommendation or "this is the answer" reveal | shimmer | on the logo or answer | Claude logo, "আমার রেকমেন্ডেশন" (main 747.9 s) |
| Comedic snap zoom | fun | on the snap | "আমি কিন্তু রাগ করব না" (main 78.56 s). Used once in all six edits. |
| Music drop in a Short | impact | exactly on the drop | Reel 05: impact on "Claude একদম নাই করে দিয়েছে", where the music's bass drops |
| Transition into a bright "reset" (white bloom between intro and body) | suck, then shimmer | suck when the screen is fully white; shimmer as the white clears (+0.05) | Main video at the intro → body join |

### 5.3 Events that stay silent [VERIFIED]

Our edits deliberately leave these without SFX:

- Caption changes, caption word reveals and the green emphasis box wipe.
- Exits of every kind: scene exits, panel slide-outs, B-roll exits, chip exits.
- Reel reframes between full-frame and stacked layout (camera moves with the panel; the panel's own swipe covers it).
- Slow camera creeps and push-ins (durations above 0.3 s), and every zoom-out back to 1.0×.
- Items inside a scene after the first, when the scene type says "first only" (chat replies, document files).
- Static screenshots once they are on screen.

The reference video analysis (`SFX_ROOT/REFERENCE_SOUND_ANALYSIS.md`) found the same pattern in our style reference: captions, gestures, small reframes and routine jump cuts in long-form are left silent.

---

## 6. Timing, levels and mixing

### 6.1 How a file is measured [VERIFIED]

Each file has two numbers that drive placement and volume:

- **Level:** decode to mono, 48 kHz; compute the RMS of every 100 ms window (sliding); take the loudest window; convert to dBFS.
- **Sync point:** the centre time of that loudest window.

This reproduces our stored metadata to within 0.06 dB (level) and 0.02 s (sync point). Section 13.1 has the code. Use it for any new file.

### 6.2 Timing formula [VERIFIED]

For an event at time `t` (the frame where the visual thing happens):

```
clip_start = t − sync_point + 1/30
```

The extra 1/30 s (one frame at 30 fps) makes the hit land one frame **after** the picture changes. Sound that arrives a frame late feels caused by the picture; sound that arrives early feels wrong.

Exceptions and edge cases:

| Case | Rule |
|---|---|
| Risers and suck/reverse sounds (long-form) | `clip_start = t − sync_point` (no extra frame), so the climax lands exactly on the event. Our Reels used the standard formula for every family. |
| `clip_start` would be before 0 | Start at 0 and skip into the file by the missing amount (media offset). |
| Clip would run past the end of the video | Cut it at the video's end. |
| Typing | Trim to the typing animation's duration + 0.05 s. The main video added a 0.12 s fade-out; the Reels did not. |
| Everything else | Play the whole file. No fade-in, no fade-out. |

We never changed playback speed, pitch or stereo position of an SFX [VERIFIED: no such setting exists in any edit].

### 6.3 Volume formula [VERIFIED]

```
gain        = 10 ^ ((family_target_dB − file_level_dB) / 20)
clip_volume = gain × MASTER
```

- `family_target_dB` comes from Section 4.1.
- `file_level_dB` comes from Section 9 (or from measuring a new file, Section 6.1).
- `MASTER` is the volume we apply to the voice in that edit: **1.0** in the main video, **1.12** in Reels 01, 02, 03 and 05, **1.25** in Reel 04. Raising the voice raises every SFX by the same amount, so the balance never changes.

Precomputed gains for every file are in Section 9. In an editor that uses dB: `clip_dB = 20 × log10(gain × MASTER)`.

### 6.4 One sound per moment (thinning) [VERIFIED]

After you have the full cue list, thin it:

1. Sort cues by time.
2. For each cue, look at cues already kept within **0.2 s** (within **0.08 s** for ticks).
3. If any kept cue in that window has **equal or higher priority** (Section 4.1), drop the new cue.
4. Ticks are dropped whenever anything already sits within 0.08 s.
5. Otherwise keep the new cue and remove the lower-priority cues it clashes with.

This is why a scene entry whoosh and a panel swipe never stack, and why an impact always wins over a pop on the same beat.

Cues that are **more than 0.2 s apart are both kept.** That is how layering works in our style (6.7).

### 6.5 Rotation [VERIFIED]

Each family has a fixed list of takes (Section 9). Every time a family is used, take the **next** file in its list and wrap around at the end. The counter runs across the whole edit. Consequences:

- Two consecutive pops are never the same file (pop has 4 takes).
- Usage stays even: the four pops were used 27, 27, 23 and 21 times.

Do not pick "the best one" every time. Repetition of an identical file is the most noticeable mistake in SFX work.

### 6.6 Music balance [VERIFIED]

| Edit | Music | Clip volume | Fades | EQ on the music | Ducking |
|---|---|---|---|---|---|
| Main video (13 min) | Intro: "Deep Techno" (Mixkit). Body: "Beauty Flow" and "Limit 70" (Kevin MacLeod) | intro 0.06, body 0.09 | intro out 1.1 s; body in 3.0 s / out 3.0–3.5 s | high-pass 45 Hz; −4.5 dB at 2.6 kHz (Q 0.8); −2 dB at 400 Hz (Q 0.9) | none; the bed is simply low |
| Reels 01–04 | "Deep Techno", starting 8 s into the track | 0.06 × MASTER | in 0.3 s; out 1.2 s (Reel 04: 2.2 s) | high-pass 45 Hz; −4.5 dB at 2.6 kHz | none |
| Reel 05 | "Autofahren" (Mixkit), drop aligned to a story beat | 0.33 × MASTER before the drop; ducks to 56 % under speech after it | in 0.4 s; out 2.4 s | high-pass 40 Hz; −5 dB at 2.6 kHz (Q 0.8); −2 dB at 180 Hz | volume automation: 0.18 s attack, 0.12 s hold, 0.38 s release around speech |

Rules that follow from this:

- **SFX levels do not change with the music.** They are set relative to the voice only.
- **The music is EQ'd out of the voice band (2.6 kHz cut).** SFX are not EQ'd; their levels already keep them clear.
- **Music fades out at the end; SFX never run past the last frame.**
- The style reference keeps music 14–18 dB under the voice (from `REFERENCE_SOUND_ANALYSIS.md`). Our Reel 05 bed sat about 13 dB under speech and about 8 dB under in gaps.

### 6.7 Layering [VERIFIED]

We layer only in these combinations, always with at least 0.2 s between the two sounds so both survive thinning:

| Layer | Spacing we used | Purpose |
|---|---|---|
| riser → impact | 0.27 s (Reel 04), 0.9 s and 2.2 s (main) | Build, then payoff on the hero word |
| suck → shimmer | 0.95 s (suck on full white, shimmer as it clears) | Reset between intro and body |
| glass → ticks → pop | stat card: glass at 0.30, ticks over the first half of the count, pop at 95 % | One readable "count and land" phrase |
| whoosh (bar) → type → pops | search card | Enter, type, results |
| type → shimmer | chat card | Prompt, then AI answers |

Everything else is a single sound.

### 6.8 Track lanes [VERIFIED]

When two SFX overlap in time, put the second on a new track. Reuse the lowest track that is free at the clip's start. Our edits never needed more than 2–3 SFX tracks. The voice and the music each sit on their own track.

### 6.9 Final loudness [VERIFIED: measured on the finished files]

| Deliverable | Integrated loudness | True peak |
|---|---|---|
| Main video, v1 / v2 | −16.2 / −16.0 LUFS | −1.7 / −4.2 dBFS |
| Reel 01 | −14.2 LUFS | −3.6 dBFS |
| Reel 02 | −14.8 LUFS | −3.7 dBFS |
| Reel 03 | −14.0 LUFS | −2.2 dBFS |
| Reel 04 | −14.3 LUFS | −2.3 dBFS |
| Reel 05 | −14.8 LUFS | −2.1 dBFS |

Targets that follow from this: **long-form about −16 LUFS; Shorts/Reels −14 to −15 LUFS; true peak no higher than −1 dBFS.** Reach the Shorts target by raising MASTER (voice and SFX together), never by raising SFX alone.

---

## 7. Density, spacing and restraint

### 7.1 Measured density [VERIFIED]

| Edit | Length | SFX placed | Per minute |
|---|---:|---:|---:|
| Main video | 13:12 | 198 | 15.0 |
| Reel 01 | 1:09 | 12 | 10.4 |
| Reel 02 | 1:51 | 33 | 17.8 |
| Reel 03 | 1:14 | 29 | 23.4 |
| Reel 04 | 1:30 | 34 | 22.6 |
| Reel 05 | 2:07 | 39 | 18.5 |

Family mix in the main video: whoosh 55, pop 55, swipe 21, whip 13, glass 12, tick 11, type 7, notif 7, shimmer 6, impact 5, riser 3, fun 1, suck 1, glitch 1.

### 7.2 Restraint rules

- **[VERIFIED] Big sounds are rare.** In 13 minutes the main video used 5 impacts, 3 risers, 1 glitch, 1 suck and 1 fun sting. In a Short, the most we have used is 3 impacts and 1 riser (Reel 04).
- **[VERIFIED] Most sounds are small.** Whoosh, swipe and pop make up about two thirds of all placements.
- **[VERIFIED] Click, camera shutter and the second suck take have never been used.** They exist for screenshots and cursor clicks; we have not shown those yet.
- **[RECOMMENDED] Long-form density:** 12–18 SFX per minute overall; up to about 20 per minute in the first 45 seconds, then one meaningful sound every 4–7 seconds in the body. (The reference video measured 20–23 per minute in its intro and 10–13 in the body.)
- **[RECOMMENDED] Shorts density:** 15–24 per minute. Above 25 per minute it starts to sound busy.
- **[RECOMMENDED] Never more than 3 sounds in any 1-second window,** and no more than 2 impacts in any 30-second window.
- **[RECOMMENDED] If a graphic has more than 6 items, pop the first 4 and let the rest land silently** (the reference does the same with cascades).

---

## 8. Situation guidelines

Each subsection says what we do [VERIFIED] and, where our edits have no precedent, what to do [RECOMMENDED].

### 8.1 Text and caption animations
- **[VERIFIED]** Spoken captions (lead line, green punch box, tail) are silent, including the punch-word box wipe.
- **[VERIFIED]** Hero titles inside graphic cards follow the card rules (title → glass; big word → whoosh on line 1, glass on the pill, impact if it is the hero claim).
- **[VERIFIED]** Hook titles in Shorts use the panel or B-roll they sit on for sound; the hook gets a hand-placed accent only if the beat earns it (Reel 04: impacts; Reel 05: notif on "দরজায় চলে আসছে").
- **[RECOMMENDED]** Kinetic text that appears word by word gets at most one sound, on the first word.

### 8.2 B-roll transitions and camera movement
- **[VERIFIED]** B-roll entry: whoosh at the start. Exit: silent.
- **[VERIFIED]** The slow push-in on B-roll (Ken Burns style) is silent.
- **[VERIFIED]** In Shorts, a hard cut between source segments gets a whoosh exactly on the cut.
- **[RECOMMENDED]** Back-to-back B-roll clips: whoosh on the first entry only. If the second clip is a new location or idea, use a swipe on it.

### 8.3 Motion graphics and animated elements
- **[VERIFIED]** Every item that lands gets one pop; the container's entry gets a whoosh (full screen) or swipe (panel).
- **[VERIFIED]** Glass/liquid UI elements (badges, pills, number pill, flow centre) get glass instead of pop.
- **[VERIFIED]** Phone notifications get notif. Typing gets type. The first AI reply gets shimmer.
- **[RECOMMENDED]** Cursor clicks on an on-screen button: click family (never used yet). Screenshots: shutter family (never used yet).

### 8.4 Zoom-ins, zoom-outs and speed ramps
- **[VERIFIED]** Fast punch-in on an emphasised phrase (≥1.1×, ≤0.3 s): whip at the zoom start (+0.05 s when the zoom has a duration).
- **[VERIFIED]** Slow push-ins, creeps and every zoom-out: silent.
- **[VERIFIED]** Comedic snap zoom: fun sting. Once per video at most.
- **[RECOMMENDED]** Speed ramps (never used in our edits): one whip at the ramp's fastest point if the ramp is under 0.5 s; silent if it is longer. Never put a riser under a speed ramp.

### 8.5 Scene changes and cinematic transitions
- **[VERIFIED]** Topic sweep (light band) in long-form: whoosh at sweep −0.05 s.
- **[VERIFIED]** Intro-to-body reset through white: suck on full white, shimmer as it clears.
- **[VERIFIED]** Chapter or hero cards: riser into the card, impact on the hero word.
- **[RECOMMENDED]** A chapter change without a hero card: one whoosh, no impact.

### 8.6 Visual reveals, highlights and emphasis
- **[VERIFIED]** Number reveals: glass, ticks, pop (stat rule). Tension before a big number: riser.
- **[VERIFIED]** The "answer" or recommendation: shimmer. Negative or broken: glitch. Arrival/delivery: notif.
- **[RECOMMENDED]** Highlight boxes or underlines drawn over existing content: silent unless they are the main point of the beat, then one pop.

### 8.7 Background music and SFX balancing
- **[VERIFIED]** See Section 6.6. SFX levels follow the voice, not the music.
- **[VERIFIED]** When a Short's music has a drop, align a story beat to it and put an impact exactly on the drop (Reel 05).
- **[RECOMMENDED]** If the music is ducked with automation, keep SFX outside the duck: do not duck SFX.

### 8.8 Layering multiple sound effects
- **[VERIFIED]** Only the combinations in Section 6.7. Keep 0.2 s or more between layered sounds.
- **[RECOMMENDED]** Never layer two sounds from the same family on one event.

### 8.9 Keeping levels consistent
- **[VERIFIED]** Every file is level-matched to its family target (Section 6.3), so swapping takes never changes loudness.
- **[VERIFIED]** One MASTER for voice and SFX together.
- **[RECOMMENDED]** After a render, spot-check three moments: a pop under speech, the loudest impact, and a whoosh in a pause. The voice must stay clearly on top in all three.

### 8.10 Avoiding excessive or repetitive SFX
- **[VERIFIED]** Thinning (6.4) and rotation (6.5) on every edit.
- **[VERIFIED]** Ordinary caption changes, exits and slow camera moves are silent.
- **[RECOMMENDED]** If the same family fires more than 4 times in 10 seconds, drop every second one.

---

## 9. SFX reference database

One table per family, in rotation order. Columns:

- **Rel. path:** relative to `SFX_ROOT` (extras show their original project path; see 2.2).
- **Len:** file duration (s). **SR/Ch:** sample rate / channels.
- **Level:** loudest 100 ms RMS (dBFS). **Sync:** sync point (s). **Gain:** precomputed for MASTER = 1.0. **Peak:** sample peak (dBFS).
- **Used:** placements across the six finished edits.
- **Character:** from `SFX_CATALOGUE.md` (spectral description and original title). The author of this guide could not listen to the files (Section 15).

### 9.1 impact: Impact / hit  (target -25 dB, priority 1)

Our loudest and rarest sound: short low hits.

- **When:** [VERIFIED] The cold open's first frame, hero claims, the main subject's logo ("২ নম্বর টুল" → Claude), a Short's music drop.
- **Where:** [VERIFIED] On the hero word's reveal or exactly on the drop.
- **How:** [VERIFIED] Full file, no fades. Highest priority: it wins every collision.
- **Why:** It marks the 3–5 moments the viewer must remember.
- **Avoid:** [VERIFIED by restraint] 5 in 13 minutes; at most 3 in a Short. [RECOMMENDED] Two impacts within 30 s.
- **Combines with:** [VERIFIED] After a riser.

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `impact_hit_dia-s15-warped-bass-hits-1_03.mp3` | `09_impact_hit/impact_hit_dia-s15-warped-bass-hits-1_03.mp3` | 0.37 | 44.1k/2 | -9.5 | 0.08 | 0.168 | -1.3 | 6 | neutral low cinematic impact; stereo; source title “DIA S15 Warped Bass - Hits (1).wav” |
| 2 | `impact_hit_super-low-bass-hit-kick-drum-wav_02.mp3` | `09_impact_hit/impact_hit_super-low-bass-hit-kick-drum-wav_02.mp3` | 0.33 | 48k/2 | -0.1 | 0.06 | 0.057 | -0.3 | 3 | dark low cinematic impact; stereo; source title “super low bass hit kick drum wAv” |
| – | `impact_hit_deep-cinematic-impact_01.mp3` | `09_impact_hit/impact_hit_deep-cinematic-impact_01.mp3` | 2.00 | 44.1k/2 | -6.7 | 0.06 | 0.122 | -0.3 | not active | dark low cinematic impact; stereo; source title “Deep Cinematic Impact” |

### 9.2 riser: Riser  (target -27 dB, priority 2)

1.8–2 s builds into a payoff.

- **When:** [VERIFIED] Into a hero claim card ("স্বর্ণযুগ", "Claude এডিট করেছে") and into a big number reveal ("$20"). 3 in the main video, 1 in Reel 04.
- **Where:** [VERIFIED] Climax on the first line of the card or on the number card. Long-form places the climax exactly on the event; Reels used the standard +1 frame.
- **How:** [VERIFIED] Full file, no fades.
- **Why:** It creates expectation so the payoff lands harder.
- **Avoid:** [VERIFIED by restraint] Never more than 3 per long video or 1 per Short so far. [RECOMMENDED] A riser without a payoff; risers under speech-dense passages.
- **Combines with:** [VERIFIED] Riser → impact (0.27–2.2 s later).

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `riser_brush-rising-woosh-muffle-000212_03.mp3` | `08_riser/riser_brush-rising-woosh-muffle-000212_03.mp3` | 1.77 | 48k/1 | -13.1 | 1.08 | 0.201 | -3.3 | 2 | dark ascending transition build; mono; source title “brush-rising-woosh-muffle-000212_0029S3_D 057-062 069-100 003-007.wav” |
| 2 | `riser_energy-riser_01.mp3` | `08_riser/riser_energy-riser_01.mp3` | 1.93 | 48k/2 | -2.7 | 0.81 | 0.061 | -0.1 | 1 | dark ascending transition build; stereo; source title “Energy Riser” |
| 3 | `riser_riser_02.mp3` | `08_riser/riser_riser_02.mp3` | 2.00 | 44.1k/2 | -11.7 | 1.94 | 0.172 | -0.3 | 1 | neutral ascending transition build; stereo; source title “Riser” |
| – | `riser_whoosh_04.mp3` | `08_riser/riser_whoosh_04.mp3` | 3.62 | 44.1k/2 | -6.6 | 0.89 | 0.095 | -0.0 | not active | neutral ascending transition build; stereo; source title “Whoosh.wav” |

### 9.3 fun: Fun stings  (target -30 dB, priority 3)

Short comedic stings.

- **When:** [VERIFIED] Once: a comedic snap zoom on "আমি কিন্তু রাগ করব না".
- **Where:** [VERIFIED] On the snap.
- **How:** [VERIFIED] Full file, no fades. Priority 3, so it beats whips on the same zoom.
- **Why:** It signals a joke so the audience knows it is safe to laugh.
- **Avoid:** [RECOMMENDED] More than one per video; serious or sponsored segments.
- **Combines with:** [VERIFIED] Alone.

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `fun_double_blink.mp3` | `work/sfx_fun/fun_double_blink.mp3 (extra)` | 1.66 | 44.1k/2 | -23.2 | 0.28 | 0.456 | -12.3 | 1 | no description recorded (name only) |
| 2 | `fun_xylo_sting.mp3` | `work/sfx_fun/fun_xylo_sting.mp3 (extra)` | 1.90 | 44.1k/2 | -30.8 | 0.64 | 1.101 | -19.1 | 0 | no description recorded (name only) |
| 3 | `fun_cute_bounce.mp3` | `work/sfx_fun/fun_cute_bounce.mp3 (extra)` | 0.34 | 44.1k/1 | -4.7 | 0.05 | 0.055 | -2.8 | 0 | no description recorded (name only) |
| – | `fun_mild_surprise.mp3` | `work/sfx_fun/fun_mild_surprise.mp3 (extra)` | 3.65 | 44.1k/2 | -17.0 | 0.27 | 0.224 | -10.5 | not active | no description recorded (name only) |

### 9.4 whip: Fast whip whoosh  (target -29 dB, priority 4)

A tight, fast swish for punch-in zooms.

- **When:** [VERIFIED] A fast punch-in zoom (≥1.1×, ≤0.3 s) on an emphasised phrase. Long-form only so far (13 uses, all in the main video).
- **Where:** [VERIFIED] At the zoom start; +0.05 s when the zoom has a duration.
- **How:** [VERIFIED] Full file, no fades.
- **Why:** It gives the zoom physical speed and marks the phrase as important.
- **Avoid:** [VERIFIED] Slow push-ins and zoom-outs. [RECOMMENDED] More than one whip per 20 s; whips on every punch-in (we left 4 of 18 silent).
- **Combines with:** [VERIFIED] Glitch 0.15 s later when the phrase is negative ("ওভার বায়াসড").

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `whoosh_fast_whip_clean-fast-swoosh_01.mp3` | `02_whoosh_fast_whip/whoosh_fast_whip_clean-fast-swoosh_01.mp3` | 0.92 | 48k/2 | -10.6 | 0.31 | 0.121 | -1.1 | 4 | neutral tight fast whip; stereo; source title “Clean fast Swoosh.aiff” |
| 2 | `whoosh_fast_whip_whip-10_04.mp3` | `02_whoosh_fast_whip/whoosh_fast_whip_whip-10_04.mp3` | 0.43 | 48k/1 | -15.7 | 0.11 | 0.216 | -1.3 | 3 | dark tight fast whip; mono; source title “Whip 10” |
| 3 | `whoosh_fast_whip_whip-8_02.mp3` | `02_whoosh_fast_whip/whoosh_fast_whip_whip-8_02.mp3` | 0.64 | 48k/1 | -18.4 | 0.20 | 0.296 | -2.8 | 3 | neutral tight fast whip; mono; source title “Whip 8” |
| 4 | `whoosh_fast_whip_whip-9_03.mp3` | `02_whoosh_fast_whip/whoosh_fast_whip_whip-9_03.mp3` | 0.54 | 48k/1 | -17.0 | 0.23 | 0.252 | -1.9 | 3 | neutral tight fast whip; mono; source title “Whip 9” |

### 9.5 suck: Reverse / suck  (target -29 dB, priority 5)

Reverse swells that pull into a cut.

- **When:** [VERIFIED] Once: when the intro pushes into full white before the main video.
- **Where:** [VERIFIED] Climax exactly when the screen is fully white.
- **How:** [VERIFIED] Long-form timing exception: climax on the event, no extra frame.
- **Why:** It pulls the viewer through a reset and makes the cut feel intentional.
- **Avoid:** [RECOMMENDED] Ordinary cuts; more than once per video.
- **Combines with:** [VERIFIED] suck → shimmer 0.95 s later.

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `reverse_suck_backwards-whoosh_02.mp3` | `14_reverse_suck/reverse_suck_backwards-whoosh_02.mp3` | 0.66 | 44.1k/1 | -23.9 | 0.49 | 0.558 | -14.7 | 1 | dark reverse suction/swell; mono; source title “Backwards Whoosh” |
| 2 | `reverse_suck_reverse-cymbal_05.mp3` | `14_reverse_suck/reverse_suck_reverse-cymbal_05.mp3` | 2.00 | 48k/1 | -24.1 | 0.24 | 0.568 | -11.5 | 0 | neutral reverse suction/swell; mono; source title “reverse cymbal.wav” |
| – | `reverse_suck_sfx-weird-watery-sucking-sound_03.mp3` | `14_reverse_suck/reverse_suck_sfx-weird-watery-sucking-sound_03.mp3` | 2.00 | 44.1k/2 | -20.0 | 0.74 | 0.355 | -6.5 | not active | bright reverse suction/swell; stereo; source title “[SFX] weird watery 'sucking' sound” |

### 9.6 notif: Notification  (target -32 dB, priority 6)

Subtle message pings.

- **When:** [VERIFIED] Phone notifications in a phone card; a delivery/arrival chip; a Short's hook about something arriving.
- **Where:** [VERIFIED] On each notification's appearance.
- **How:** [VERIFIED] Full file, no fades.
- **Why:** Viewers know this sound from their own phones; it says "message received" with no explanation.
- **Avoid:** [RECOMMENDED] Non-message moments; more than 3 in a row.
- **Combines with:** [VERIFIED] Usually alone.

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `notification_chime-notification_04.mp3` | `11_notification/notification_chime-notification_04.mp3` | 0.32 | 44.1k/2 | -11.8 | 0.05 | 0.098 | -4.5 | 6 | bright subtle UI notification tone; stereo; source title “Chime Notification” |
| 2 | `notification_notification-sound_02.mp3` | `11_notification/notification_notification-sound_02.mp3` | 0.41 | 48k/2 | -26.4 | 0.05 | 0.526 | -23.2 | 4 | dark subtle UI notification tone; stereo; source title “Notification Sound” |
| 3 | `notification_notification-sound_03.mp3` | `11_notification/notification_notification-sound_03.mp3` | 0.69 | 44.1k/2 | -13.8 | 0.09 | 0.123 | -7.7 | 4 | dark subtle UI notification tone; stereo; source title “Notification Sound” |

### 9.7 whoosh: Soft whoosh  (target -31 dB, priority 7)

Our main transition sound: airy, soft, short.

- **When:** [VERIFIED] A full-screen graphic or B-roll enters; a hard cut between source segments in a Short; a long-form topic sweep; the first line of a big-word card; a search bar or document assembling.
- **Where:** [VERIFIED] On the entry frame (+0.00), on the cut, or 0.05 s before the sweep's midpoint. Never on exits.
- **How:** [VERIFIED] Full file, no fades, gain from the table × MASTER, standard timing formula.
- **Why:** It tells the viewer "the picture is changing" without drawing attention to itself.
- **Avoid:** [VERIFIED] Exits, slow camera moves, caption changes. [RECOMMENDED] Two whooshes less than 1 s apart: keep the first.
- **Combines with:** [VERIFIED] Followed by pops as items land; whoosh (search bar) → type → pops.

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `whoosh_soft_digital-whoosh-soft_02.mp3` | `01_whoosh_soft/whoosh_soft_digital-whoosh-soft_02.mp3` | 0.95 | 44.1k/2 | -15.2 | 0.44 | 0.163 | -5.3 | 27 | dark airy soft sweep; stereo; source title “digital_whoosh_soft.wav” |
| 2 | `whoosh_soft_02.wav` | `work/sfx/whoosh_soft_02.wav (extra)` | 1.39 | 44.1k/2 | -11.2 | 0.15 | 0.103 | -1.0 | 23 | Mixkit "Short wind swoosh" |
| 3 | `whoosh_soft_04.wav` | `work/sfx/whoosh_soft_04.wav (extra)` | 1.10 | 44.1k/2 | -11.3 | 0.09 | 0.103 | -1.0 | 22 | Mixkit "Quick swoosh accent" |
| – | `whoosh_soft_swing-1-5_01.mp3` | `01_whoosh_soft/whoosh_soft_swing-1-5_01.mp3` | 0.91 | 48k/2 | -41.0 | 0.09 | 3.162 | -28.6 | not active | neutral airy soft sweep; stereo; source title “Swing 1_5” |
| – | `whoosh_soft_whoosh-soft_03.mp3` | `01_whoosh_soft/whoosh_soft_whoosh-soft_03.mp3` | 0.37 | 44.1k/1 | -31.1 | 0.21 | 1.012 | -20.3 | not active | dark airy soft sweep; mono; source title “whoosh.soft.wav” |

### 9.8 swipe: Swipe / scroll  (target -32 dB, priority 8)

Light air movement for panels sliding in.

- **When:** [VERIFIED] A side panel slides in (long-form split screen) or a bottom panel slides up (Shorts); a lower third enters.
- **Where:** [VERIFIED] Panel start +0.05 s; lower third +0.02 s.
- **How:** [VERIFIED] Full file, no fades.
- **Why:** It matches the direction-less slide of a panel better than a full whoosh.
- **Avoid:** [VERIFIED] Panels that cross-fade from a previous panel on the same side; the panel already on screen at frame 0; exits.
- **Combines with:** [VERIFIED] Followed by pops for the panel's items.

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `swipe_scroll_whip01_03.mp3` | `12_swipe_scroll/swipe_scroll_whip01_03.mp3` | 0.78 | 44.1k/2 | -12.5 | 0.17 | 0.106 | -1.7 | 28 | neutral light swipe air movement; stereo; source title “whip01.wav” |
| 2 | `swipe_scroll_whip02_02.mp3` | `12_swipe_scroll/swipe_scroll_whip02_02.mp3` | 0.67 | 44.1k/2 | -11.3 | 0.09 | 0.092 | -1.5 | 27 | neutral light swipe air movement; stereo; source title “whip02.wav” |
| 3 | `swipe_scroll_whips04_04.mp3` | `12_swipe_scroll/swipe_scroll_whips04_04.mp3` | 0.59 | 44.1k/2 | -18.3 | 0.10 | 0.207 | -8.5 | 25 | neutral light swipe air movement; stereo; source title “whips04.wav” |
| – | `swipe_scroll_sfx-whoosh-high-1-12_01.mp3` | `12_swipe_scroll/swipe_scroll_sfx-whoosh-high-1-12_01.mp3` | 0.50 | 48k/1 | -35.3 | 0.09 | 1.462 | -22.1 | not active | neutral light swipe air movement; mono; source title “Sfx - Whoosh High 1 (12).wav” |

### 9.9 type: Typing keys  (target -36 dB, priority 9)

Mechanical keyboard bursts for typed prompts and search queries.

- **When:** [VERIFIED] A chat prompt or search query types out on screen.
- **Where:** [VERIFIED] From the first typed character.
- **How:** [VERIFIED] Trim to the typing animation's duration + 0.05 s. Long-form adds a 0.12 s fade-out; Reels did not.
- **Why:** Hearing the typing sells that a real person or AI is entering the text.
- **Avoid:** [RECOMMENDED] Typing under real screen recordings that already have keyboard sound; typing longer than about 2.5 s.
- **Combines with:** [VERIFIED] Whoosh (bar) → type → pops (results); type → shimmer (AI reply).

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `typing_keys_mech-keyboard-01_02.mp3` | `07_typing_keys/typing_keys_mech-keyboard-01_02.mp3` | 1.28 | 48k/2 | -17.7 | 0.06 | 0.122 | -0.5 | 9 | neutral short mechanical typing burst; stereo; source title “MECH-KEYBOARD-01.wav” |
| 2 | `typing_keys_mech-keyboard-02_03.mp3` | `07_typing_keys/typing_keys_mech-keyboard-02_03.mp3` | 1.28 | 48k/2 | -18.1 | 0.05 | 0.127 | -0.9 | 4 | neutral short mechanical typing burst; stereo; source title “MECH-KEYBOARD-02.wav” |
| – | `typing_keys_keyboard-computer-mechanical-typ_04.mp3` | `07_typing_keys/typing_keys_keyboard-computer-mechanical-typ_04.mp3` | 2.39 | 48k/1 | -21.1 | 0.70 | 0.180 | -4.0 | not active | bright short mechanical typing burst; mono; source title “Keyboard, computer, mechanical, typing, quickly, rapidly, keys, press, button, click, tap, repeatedly, spacebar, delete_96Khz_Mono_ZoomH4n_NT5.wav” |

### 9.10 pop: UI pop  (target -33 dB, priority 10)

Rounded, short landings for cards, chips, logos and list items.

- **When:** [VERIFIED] Every list, grid, step, compare, device or result item that lands; logo tiles; the final number of a count-up; overlay chips (default).
- **Where:** [VERIFIED] On each item's landing (+0.00 to +0.15 depending on scene type; see 5.1).
- **How:** [VERIFIED] Full file, no fades. The four takes rotate.
- **Why:** Each landing feels tactile, which keeps lists readable and rhythmic.
- **Avoid:** [RECOMMENDED] More than 4 pops in one cascade (let the rest land silently); pops on caption words.
- **Combines with:** [VERIFIED] After a whoosh or swipe entry; closes the stat card's tick run.

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `pop_ui_bop-sound-effect-button_04.mp3` | `03_pop_ui/pop_ui_bop-sound-effect-button_04.mp3` | 0.17 | 44.1k/2 | -19.5 | 0.05 | 0.211 | -14.0 | 27 | dark rounded UI pop; stereo; source title “bop sound effect button” |
| 2 | `pop_ui_click-pop-two-part_01.mp3` | `03_pop_ui/pop_ui_click-pop-two-part_01.mp3` | 0.50 | 44.1k/2 | -26.3 | 0.05 | 0.461 | -9.3 | 27 | neutral rounded UI pop; stereo; source title “Click Pop - two part” |
| 3 | `pop_ui_the-best-bubble-pop-sound-for-ga_03.mp3` | `03_pop_ui/pop_ui_the-best-bubble-pop-sound-for-ga_03.mp3` | 0.31 | 44.1k/1 | -13.3 | 0.09 | 0.104 | -4.2 | 23 | neutral rounded UI pop; mono; source title “The Best Bubble Pop Sound For Game and UI” |
| 4 | `pop_ui_ui-series-hollow-pop_02.mp3` | `03_pop_ui/pop_ui_ui-series-hollow-pop_02.mp3` | 0.51 | 44.1k/2 | -14.5 | 0.05 | 0.119 | -1.6 | 21 | neutral rounded UI pop; stereo; source title “UI Series: Hollow pop” |

### 9.11 glass: Glass / liquid  (target -33 dB, priority 11)

Rounded bubble sounds for our Liquid Glass UI elements.

- **When:** [VERIFIED] A title card's glass badge (+0.15), a big-word pill, a stat card's number pill (+0.30), a flow diagram's centre (+0.20), and chips that are glass objects ("ফ্রি প্ল্যান", "একটা PC").
- **Where:** [VERIFIED] On the glass element's landing.
- **How:** [VERIFIED] Full file, no fades. Note: `glass_liquid_the-best-bubble-pop-sound-for-ga_02.mp3` is byte-identical to the pop take `pop_ui_the-best-bubble-pop-sound-for-ga_03.mp3` (same Freesound source).
- **Why:** It ties the sound to the visual material: glass looks soft, so it sounds soft.
- **Avoid:** [RECOMMENDED] Non-glass elements; bell-like chimes.
- **Combines with:** [VERIFIED] Glass → ticks → pop in the stat card.

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `glass_liquid_sci-fi-bubble-pop_04.mp3` | `05_glass_liquid/glass_liquid_sci-fi-bubble-pop_04.mp3` | 0.49 | 44.1k/2 | -20.8 | 0.26 | 0.245 | -8.5 | 8 | dark glassy liquid bubble pop; stereo; source title “Sci-Fi Bubble Pop” |
| 2 | `glass_liquid_the-best-bubble-pop-sound-for-ga_02.mp3` | `05_glass_liquid/glass_liquid_the-best-bubble-pop-sound-for-ga_02.mp3` | 0.31 | 44.1k/1 | -13.3 | 0.09 | 0.104 | -4.2 | 6 | neutral glassy liquid bubble pop; mono; source title “The Best Bubble Pop Sound For Game and UI” |
| – | `glass_liquid_soap-bubble-pop-mouth-perc_01.mp3` | `05_glass_liquid/glass_liquid_soap-bubble-pop-mouth-perc_01.mp3` | 0.75 | 48k/2 | -34.4 | 0.07 | 1.175 | -23.5 | not active | neutral glassy liquid bubble pop; stereo; source title “Soap bubble pop - Mouth perc.wav” |

### 9.12 click: Click / tap  (target -34 dB, priority 12)

Very short tactile clicks.

- **When:** [RECOMMENDED] A cursor click or a button press shown on screen. Never used in our edits yet.
- **Where:** [RECOMMENDED] On the frame the button visibly depresses.
- **How:** [RECOMMENDED] Full file, standard timing, family target −34 dB.
- **Why:** A click confirms an on-screen action; it is quieter and drier than a pop.
- **Avoid:** [RECOMMENDED] Using clicks for item landings (that is the pop's job).
- **Combines with:** [RECOMMENDED] Click on the button, then a pop or whoosh for what opens.

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `click_tap_lego-click-short_02.mp3` | `04_click_tap/click_tap_lego-click-short_02.mp3` | 0.18 | 48k/2 | -29.8 | 0.05 | 0.618 | -5.5 | 0 | bright short tactile UI click; stereo; source title “Lego Click (short)” |
| 2 | `click_tap_menu-fx-03-descending_04.mp3` | `04_click_tap/click_tap_menu-fx-03-descending_04.mp3` | 0.24 | 44.1k/1 | -19.9 | 0.07 | 0.196 | -10.4 | 0 | dark short tactile UI click; mono; source title “Menu FX 03 (descending).wav” |
| 3 | `click_tap_snap-click-07_01.mp3` | `04_click_tap/click_tap_snap-click-07_01.mp3` | 0.21 | 48k/2 | -10.9 | 0.05 | 0.070 | -7.5 | 0 | dark short tactile UI click; stereo; source title “Snap Click 07.wav” |
| – | `click_tap_ui-click_03.mp3` | `04_click_tap/click_tap_ui-click_03.mp3` | 0.60 | 44.1k/2 | -45.5 | 0.26 | 3.758 | -24.8 | not active | neutral short tactile UI click; stereo; source title “UI click” |

### 9.13 tick: Counter tick  (target -35 dB, priority 13)

Tiny precise ticks for count-ups.

- **When:** [VERIFIED] Number count-ups: three ticks across the first half of the count.
- **Where:** [VERIFIED] Count start, +¼ and +½ of the count duration.
- **How:** [VERIFIED] Full file. Ticks are thinned within 0.08 s and always yield to other cues.
- **Why:** It makes a counting number feel mechanical and precise.
- **Avoid:** [RECOMMENDED] Ticking through the whole count (it becomes a buzz); ticks outside numbers.
- **Combines with:** [VERIFIED] Glass before, pop at 95 % of the count.

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `tick_counter_sfx-ambiance-clock-tick_01.mp3` | `06_tick_counter/tick_counter_sfx-ambiance-clock-tick_01.mp3` | 0.11 | 48k/2 | -26.4 | 0.05 | 0.373 | -13.3 | 8 | dark precise digital/mechanical tick; stereo; source title “SFX Ambiance: Clock Tick” |
| 2 | `tick_counter_soft-ui-digital-tick_04.mp3` | `06_tick_counter/tick_counter_soft-ui-digital-tick_04.mp3` | 0.24 | 44.1k/1 | -28.2 | 0.05 | 0.455 | -12.0 | 6 | bright precise digital/mechanical tick; mono; source title “Soft UI Button Click” |
| – | `tick_counter_mab-clock-tick-1-20080713_02.mp3` | `06_tick_counter/tick_counter_mab-clock-tick-1-20080713_02.mp3` | 0.25 | 48k/1 | -22.4 | 0.13 | 0.234 | -0.4 | not active | bright precise digital/mechanical tick; mono; source title “mab-clock-tick-1-20080713.wav” |

### 9.14 shimmer: Shimmer / sparkle  (target -33 dB, priority 14)

Soft bright shimmer for "AI magic" and answers.

- **When:** [VERIFIED] The first AI reply in a chat card; the recommendation reveal; the white bloom clearing into the main video.
- **Where:** [VERIFIED] On the reply's first word, the logo, or the bloom clearing (+0.05 s).
- **How:** [VERIFIED] Full file, no fades.
- **Why:** It sounds like "done for you", which is the core promise of our AI content.
- **Avoid:** [RECOMMENDED] Every AI mention; shimmer on top of an impact (thinning removes it anyway).
- **Combines with:** [VERIFIED] type → shimmer; suck → shimmer.

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `shimmer_sparkle_fantasy-ui-button-3_03.mp3` | `13_shimmer_sparkle/shimmer_sparkle_fantasy-ui-button-3_03.mp3` | 1.26 | 44.1k/2 | -20.3 | 0.62 | 0.231 | -6.9 | 6 | bright soft shimmering transition; stereo; source title “Fantasy_ui_Button_3.wav” |
| 2 | `shimmer_sparkle_transition-action-jump-pitch-shi_01.mp3` | `13_shimmer_sparkle/shimmer_sparkle_transition-action-jump-pitch-shi_01.mp3` | 1.32 | 44.1k/2 | -12.7 | 0.13 | 0.096 | -0.3 | 2 | neutral soft shimmering transition; stereo; source title “Transition,action,jump,pitch-shift,short,shimmer,whoosh,positive,soft.wav” |
| 3 | `shimmer_sparkle_transition-action-jump-pitch-shi_02.mp3` | `13_shimmer_sparkle/shimmer_sparkle_transition-action-jump-pitch-shi_02.mp3` | 1.15 | 44.1k/2 | -12.1 | 0.15 | 0.090 | -0.3 | 2 | bright soft shimmering transition; stereo; source title “Transition,action,jump,pitch-shift,short,shimmer,whoosh,positive_r8bp.wav” |

### 9.15 glitch: Digital glitch  (target -33 dB, priority 15)

Short static stutters.

- **When:** [VERIFIED] Something negative, broken or wrong: "ওভার বায়াসড", "শুধু মোবাইল? ব্যাড লাক!", an out-of-stock shop card.
- **Where:** [VERIFIED] On the word or on the chip/card landing.
- **How:** [VERIFIED] Full file, no fades. Lowest priority but one: anything else on the beat wins.
- **Why:** It gives the "error" feeling a sound, which reads instantly in a tech video.
- **Avoid:** [RECOMMENDED] Positive beats; generic transitions; more than one per 2 minutes.
- **Combines with:** [VERIFIED] After a whip on the same phrase.

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `glitch_digital_glitch-corruption_03.mp3` | `10_glitch_digital/glitch_digital_glitch-corruption_03.mp3` | 1.34 | 44.1k/2 | -16.2 | 0.97 | 0.145 | -0.2 | 2 | neutral brief digital stutter/static; stereo; source title “Glitch Corruption” |
| 2 | `glitch_digital_interference_01.mp3` | `10_glitch_digital/glitch_digital_interference_01.mp3` | 0.60 | 48k/2 | -21.4 | 0.18 | 0.262 | -5.9 | 0 | neutral brief digital stutter/static; stereo; source title “interference.aif” |
| 3 | `glitch_digital_static-glitch_02.mp3` | `10_glitch_digital/glitch_digital_static-glitch_02.mp3` | 0.36 | 48k/2 | -13.4 | 0.13 | 0.105 | -0.2 | 0 | neutral brief digital stutter/static; stereo; source title “static_glitch.aif” |

### 9.16 shutter: Camera shutter  (target -31 dB, priority 16)

Mechanical shutter clicks.

- **When:** [RECOMMENDED] A screenshot or a frozen "snap" frame. Never used in our edits yet.
- **Where:** [RECOMMENDED] On the freeze or flash frame.
- **How:** [RECOMMENDED] Full file, standard timing, family target −31 dB.
- **Why:** It names the action ("captured") instantly.
- **Avoid:** [RECOMMENDED] Anything that is not a capture.
- **Combines with:** [RECOMMENDED] Alone, or followed by a pop when the screenshot lands as a card.

Rotation order (active takes):

| # | File | Rel. path | Len | SR/Ch | Level | Sync | Gain | Peak | Used | Character |
|---:|---|---|---:|---|---:|---:|---:|---:|---:|---|
| 1 | `camera_shutter_camera-shutter-analogue-film-slr_02.mp3` | `15_camera_shutter/camera_shutter_camera-shutter-analogue-film-slr_02.mp3` | 0.67 | 48k/2 | -17.3 | 0.42 | 0.206 | -0.4 | 0 | bright mechanical camera shutter; stereo; source title “Camera shutter analogue film SLR 1/4 01” |
| 2 | `camera_shutter_camera-shutter-analogue-film-slr_04.mp3` | `15_camera_shutter/camera_shutter_camera-shutter-analogue-film-slr_04.mp3` | 0.63 | 48k/2 | -17.9 | 0.42 | 0.221 | -0.7 | 0 | bright mechanical camera shutter; stereo; source title “Camera shutter analogue film SLR 1/4 02” |
| 3 | `camera_shutter_shutter_03.mp3` | `15_camera_shutter/camera_shutter_shutter_03.mp3` | 0.64 | 48k/2 | -22.6 | 0.17 | 0.382 | -5.5 | 0 | bright mechanical camera shutter; stereo; source title “Shutter” |
| – | `camera_shutter_taking-photo-with-camera_01.mp3` | `15_camera_shutter/camera_shutter_taking-photo-with-camera_01.mp3` | 0.77 | 44.1k/2 | -36.8 | 0.32 | 1.950 | -15.7 | not active | bright mechanical camera shutter; stereo; source title “Taking Photo with Camera” |


---

## 10. Real examples from our projects

### 10.1 Main video: "কেন আপনার খাবারের খরচ কমিয়ে হলেও Claude Pro কেনা উচিত!" (13:12, 16:9)

All times are on the source clock; the film adds a 1.5 s pause at 79.97 s.

| Time (s) | What is on screen / said | SFX | Why |
|---:|---|---|---|
| 0.00 | Cold open, slow pull-out, hero caption "একদিন বসে বসে ভাবতেছিলাম" | impact | Strong first frame (the shimmer cued 0.05 s later was thinned out) |
| 9.52 | Hard punch-in on "হ্যালো!" | pop | Small, friendly accent |
| 26.20 | Punch-in on "ওভার বায়াসড" | whip | Emphasis zoom |
| 26.35 | Same phrase | glitch | Something is "off" |
| 40.50 | Chip "ফ্রি প্ল্যান · লিমিটেড ফিচার" | glass (chip override) | Glass UI element |
| 44.60 | Tension push into the "$20" stat | riser | Build to a number |
| 44.55–49.0 | Stat card counts to $20 | glass, ticks, pop | Stat rule |
| 52.10 | Claude logo lands in "২ নম্বর টুল" | impact | The video's main subject |
| 78.56 | Snap zoom on "আমি কিন্তু রাগ করব না" | fun (fun_double_blink) | Comedic beat |
| 193.55 | Chip "শুধু মোবাইল? ব্যাড লাক!" | glitch (chip override) | Negative beat |
| 494.60 | Chip "২ দিন পরে — দরজায় ডেলিভারি" | notif (chip override) | Arrival |
| 530.30 → 532.50 | Big word "এখন কনটেন্ট ক্রিয়েশনের / স্বর্ণযুগ" | riser → impact | Chapter hero claim |
| 594.40 → 595.30 | Big word "এই ভিডিওটা কিন্তু / Claude এডিট করেছে" | riser → impact | Hero claim |
| 662.80 | Big word "Claude কে স্কিল শেখানো যায়" | impact | "Mic drop" moment |
| 747.90 | Logo card "আমার রেকমেন্ডেশন" → Claude | shimmer | The answer |

Totals for the whole main video, including the accents above: 55 whooshes (scene entries, B-roll, 12 sweeps), 55 pops (items), 21 swipes (panels), 13 whips (punch-ins), 12 glass, 11 ticks, 7 typing, 7 notifications, 6 shimmers, 5 impacts, 3 risers, 1 fun, 1 suck, 1 glitch.

### 10.2 Shorts / Reels (9:16, stacked layout: speaker on top, panel below)

| Reel | Hand-placed accents | Automatic pattern |
|---|---|---|
| Reel 01 (1:09) | none | 5 swipes, 3 whooshes, 2 pops, 1 type, 1 shimmer |
| Reel 02 (1:51) | none | 15 swipes, 11 pops, 4 whooshes, 3 notifs |
| Reel 03 (1:14) | none | 12 swipes, 10 pops, 3 ticks, glass, whoosh, type, shimmer |
| Reel 04 (1:30) | riser + impact into "golden age"; impacts on both "Claude edited this" beats | 14 swipes, 6 pops, 4 whooshes, 3 notifs, glass, type, shimmer |
| Reel 05 (2:07) | notif on the hook "দরজায় চলে আসছে" (0.06 s); impact on the music drop (13.0 s); glitch on the out-of-stock shop card (100.5 s) | 14 pops, 13 swipes, 5 whooshes, 3 types, shimmer |

In every Reel, each seam between source segments has a whoosh, and each new bottom panel has a swipe.

---

## 11. Step-by-step workflow for a new edit

### 11.1 Before placing sounds

1. Read this guide fully.
2. Get `SFX_ROOT` (and any extras folder) from the user. Run the check in 2.4.
3. Load the reference data for the active set (Section 9, or re-measure with Section 13.1 if files changed).
4. Confirm with the user, if not obvious: long-form or Short? Which music track? Voice MASTER?

### 11.2 Building the cue list

1. **List visual events** with timestamps (graphics in/out, items landing, counts, typing, notifications, cuts, B-roll, punch zooms, hero cards).
2. **Map events to families** with Section 5.1. Unlisted events stay silent (5.3).
3. **Add hand-placed accents** only for beats that match Section 5.2. Ask yourself: is this one of the 3–5 biggest moments of the video? If not, no impact.
4. **Compute clip start, duration and volume** with 6.2 and 6.3.
5. **Thin** with 6.4. **Rotate** with 6.5. **Assign tracks** with 6.8.
6. **Check density** against Section 7. If over, remove low-priority cues first (shutter, glitch, shimmer, tick, click, glass, pop), never the impacts on hero beats.

### 11.3 QA checklist (after rendering)

- [ ] Every SFX file used exists and matched its checksum.
- [ ] No SFX within 0.2 s of another, except the layer pairs in 6.7.
- [ ] No sound on caption changes, exits or slow camera moves.
- [ ] Impacts: count them. Long-form ≤ 1 per 2 minutes on average; Shorts ≤ 3.
- [ ] Rotation: no family plays the same file twice in a row.
- [ ] Loudness: long-form about −16 LUFS, Shorts −14 to −15 LUFS; true peak ≤ −1 dBFS. Measure with
      `ffmpeg -i OUT.mp4 -map 0:a -af ebur128=peak=true -f null -` and read the `I:` and `Peak:` summary lines.
- [ ] Listen-through (or ask the user to listen) at three moments: a pop under speech, the loudest impact, a whoosh in a pause. The voice must stay on top.
- [ ] Report to the user: SFX count, per-family counts, loudness, any recommendations applied, any missing files.

---

## 12. Fallback rules

### 12.1 A specific file is missing

Skip it in the rotation and use the family's remaining takes. Tell the user.

### 12.2 A whole family is missing

| Missing family | Use instead | Notes |
|---|---|---|
| whoosh | swipe | Same role, lighter. |
| swipe | whoosh | |
| whip | whoosh | Place on the zoom start. |
| pop | glass, then click | |
| glass | pop | |
| click | pop (quietest take: `pop_ui_bop-sound-effect-button_04.mp3`) | |
| tick | click; if that is missing too, no ticks (keep the final pop) | |
| type | no sound | Do not fake typing with clicks. |
| notif | pop | |
| shimmer | glass | Or no sound. |
| glitch | no sound | Never substitute another family. |
| riser | no sound | Keep the impact on its own. |
| impact | no sound | Never replace an impact with a pop or whoosh. |
| suck | whoosh | Or no sound. |
| shutter | click | |
| fun | no sound | Comedy stings are optional. |

Apply the replacement family's own level target and rotation.

### 12.3 The whole library is missing

Do not download, generate or borrow sounds. Produce the cue list (time, family, intended file) so the user can apply it later, and tell the user the library could not be found.

### 12.4 The user adds new SFX files

1. Ask which family each file belongs to (or propose one and confirm).
2. Measure level and sync point with Section 13.1.
3. Compute `gain = 10^((family_target − level)/20)`.
4. Record source and licence. Only use files licensed for monetised commercial use.
5. Append the file to the end of its family's rotation list.

---

## 13. Reference implementation (portable Python)

These functions reproduce our placement logic. They need Python 3, numpy and ffmpeg on PATH. They output a cue sheet that any editor can use.

### 13.1 Measure a file

```python
import subprocess, numpy as np

def measure(path):
    """Level (dBFS, loudest 100 ms RMS, mono 48 kHz) and sync point (s), as used in this guide."""
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "48000",
                          "-f", "f32le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    n = 4800                                            # 100 ms at 48 kHz
    if len(x) < n:
        e = np.array([np.mean(x ** 2)]); half = len(x) / 2
    else:
        e = np.convolve(x ** 2, np.ones(n) / n, mode="valid"); half = n / 2
    level = float(10 * np.log10(e.max() + 1e-12))
    sync = (int(np.argmax(e)) + half) / 48000
    dur = len(x) / 48000
    return round(level, 1), round(sync, 3), round(dur, 3)
```

### 13.2 Build the SFX track

```python
TARGET = {"impact": -25, "riser": -27, "whip": -29, "suck": -29, "fun": -30, "whoosh": -31,
          "shutter": -31, "notif": -32, "swipe": -32, "pop": -33, "glass": -33, "glitch": -33,
          "shimmer": -33, "click": -34, "tick": -35, "type": -36}
PRIORITY = ["impact", "riser", "fun", "whip", "suck", "notif", "whoosh", "swipe", "type", "pop",
            "glass", "click", "tick", "shimmer", "glitch", "shutter"]
FPS = 30

# FAMILIES: family -> ordered list of filenames (rotation order, Section 9)
# INFO: filename -> {"level": dB, "sync": s, "dur": s}   (Section 9 or measure())

def thin(cues):
    """cues: list of (t, family) or (t, "type:<seconds>"). One sound per moment."""
    rank = {f: i for i, f in enumerate(PRIORITY)}
    kept = []
    for t, cat in sorted(cues):
        fam = cat.split(":")[0]
        window = 0.08 if fam == "tick" else 0.2
        clash = [k for k in kept if abs(k[0] - t) < window]
        if any(rank[k[1].split(":")[0]] <= rank[fam] or fam == "tick" for k in clash):
            continue
        kept = [k for k in kept if k not in clash] + [(t, cat)]
    return sorted(kept)

def place(cues, FAMILIES, INFO, video_dur, master=1.0, long_form=True):
    rot, lanes, out = {}, [], []
    for t, cat in thin(cues):
        trim = None
        if cat.startswith("type:"):
            trim, cat = float(cat.split(":")[1]), "type"
        files = FAMILIES[cat]
        i = rot.get(cat, 0); rot[cat] = i + 1
        f = files[i % len(files)]
        info = INFO[f]
        start = t - info["sync"] + (0 if (long_form and cat in ("riser", "suck")) else 1 / FPS)
        offset = 0.0
        if start < 0:
            offset, start = -start, 0.0
        dur = info["dur"] - offset
        if trim is not None:
            dur = min(dur, trim + 0.05)
        dur = min(dur, video_dur - start)
        if dur <= 0.02:
            continue
        gain = 10 ** ((TARGET[cat] - info["level"]) / 20)
        lane = next((k for k, end in enumerate(lanes) if end <= start), None)
        if lane is None:
            lanes.append(0.0); lane = len(lanes) - 1
        lanes[lane] = start + dur
        out.append(dict(file=f, family=cat, start=round(start, 3), media_offset=round(offset, 3),
                        duration=round(dur, 3), volume=round(gain * master, 3),
                        fade_out=0.12 if (trim is not None and long_form) else 0.0, track=lane))
    return out
```

### 13.3 Using the cue sheet in other editors

| Field | Premiere Pro | DaVinci Resolve | CapCut |
|---|---|---|---|
| `start` | clip in-point on the timeline | clip start | clip start |
| `media_offset` | source in-point | source in | trim the head |
| `duration` | clip length | clip length | trim the tail |
| `volume` | Clip Volume in dB = `20·log10(volume)` | Clip Volume in dB, same formula | Volume % = `volume × 100` (approximately; CapCut's scale is not strictly linear, so check by ear) |
| `fade_out` | Constant Power fade of that length | Fade handle | Fade out |
| `track` | Audio track A(3 + track) | Audio track A(3 + track) | Separate audio layer |

Keep the voice on its own track at `master`, and the music on its own track below the SFX.

---

## 14. Licensing and credits

**[VERIFIED]** from `SFX_CATALOGUE.md`, `work/audio_sources.md` and `deliverables/CREDITS_FOR_DESCRIPTION.md` on the original machine:

- **Active set needs no SFX credit.** It uses only CC0 files from `SFX_ROOT`, two Mixkit WAVs (Mixkit Sound Effects Free License: commercial use allowed, no attribution) and the CC0 fun stings.
- **Five library files are CC BY and are not in the active set.** If the user approves using one, paste its credit into the video description:
  - "whoosh.soft.wav" by junggle — CC BY 4.0 — https://freesound.org/people/junggle/sounds/73263
  - "mab-clock-tick-1-20080713.wav" by mab — CC BY 3.0 — https://freesound.org/people/mab/sounds/57211
  - "Keyboard, computer, mechanical, typing, quickly, rapidly, keys, press, button, click, tap, repeatedly, spacebar, delete_96Khz_Mono_ZoomH4n_NT5.wav" by MattRuthSound — CC BY 4.0 — https://freesound.org/people/MattRuthSound/sounds/561688
  - "Whoosh.wav" by hgavin — CC BY 3.0 — https://freesound.org/people/hgavin/sounds/14910
  - "Deep Cinematic Impact" by MeijstroAudio — CC BY 4.0 — https://freesound.org/people/MeijstroAudio/sounds/377303
- **Music credits** depend on the track. Kevin MacLeod tracks (CC BY 4.0) need the credit line; Mixkit tracks do not.
- **Never use** NonCommercial, ShareAlike, NoDerivatives, personal-use-only or unknown-licence sounds. Our videos are monetised on YouTube, Facebook and Instagram.

---

## 15. Known gaps and unverified items

These could not be verified. Do not treat them as rules.

1. **No one has listened to the files while writing this guide.** Sound descriptions come from `SFX_CATALOGUE.md` (automatic spectral descriptions plus original titles) and from measurements. Listen before relying on a description for a delicate moment.
2. **Why six library files were left out of the active set is not recorded:** `whoosh_soft_swing-1-5_01.mp3`, `click_tap_ui-click_03.mp3`, `glass_liquid_soap-bubble-pop-mouth-perc_01.mp3`, `swipe_scroll_sfx-whoosh-high-1-12_01.mp3`, `reverse_suck_sfx-weird-watery-sucking-sound_03.mp3` and `camera_shutter_taking-photo-with-camera_01.mp3`. Observation only: four of them (`swing-1-5`, `ui-click`, `soap-bubble`, `whoosh-high`) have sample peaks between −22 and −29 dBFS, far quieter than the rest of the library.
3. **Why the family targets have their exact values is not recorded.** The values themselves are verified: they are reproduced exactly from the stored gains of all 45 active files.
4. **The original script that produced the stored levels and gains is not in the project.** The method in Section 6.1 reproduces its numbers to within 0.06 dB and 0.02 s.
5. **Source pages for the fun stings were not saved.** Our credits file says they are CC0 sounds from Freesound by the users nomiqbomi and Hemplock. Confirm before using them in new work.
6. **Four of the 18 fast punch-in zooms in the main video have no whip.** The reason was not recorded.
7. **Speed ramps, cursor clicks, screenshots and on-screen keyboard shortcuts have never been sound-designed in our edits.** Rules for them in this guide are [RECOMMENDED].
8. **The density targets marked [RECOMMENDED] in Section 7.2** are derived from our measured numbers and the reference analysis, not from a preference the user has stated.

---

## 16. Appendix A: legacy library (not part of the active workflow)

Before the current library was built, the first draft of the main video used an earlier set of 60 files from Mixkit, Freesound and Kenney. It lived at `work/sfx/` (copied to `edit/assets/sfx/`) on the original machine. Only two of its files are still active (`whoosh_soft_02.wav`, `whoosh_soft_04.wav`, see 2.2). The rest were superseded and are **not** used. They are listed for completeness; do not use them without the user's approval.

| File | Len (s) | Source title | Status |
|---|---:|---|---|
| `bassdrop_sub_01.mp3` | 2.42 | Sine Bass Drop — josheb_policarpio (Freesound #612930) | Legacy, not used |
| `bassdrop_sub_02.mp3` | 2.19 | Sub Rush 3 — JarredGibb (Freesound #263893) | Legacy, not used |
| `bassdrop_sub_03.mp3` | 4.80 | Bass Drop — qubodup (Freesound #212768) | Legacy, not used |
| `camera_shutter_01.wav` | 1.51 | Camera digital shutter — Mixkit | Legacy, not used |
| `camera_shutter_02.wav` | 0.35 | Camera shutter click — Mixkit | Legacy, not used |
| `click_ui_kenney_01.ogg` | 0.04 | select_002.ogg, Interface Sounds 1.0 — Kenney | Legacy, not used |
| `click_ui_soft_01.wav` | 0.20 | Cool interface click tone — Mixkit | Legacy, not used |
| `click_ui_soft_02.wav` | 1.10 | Select click — Mixkit | Legacy, not used |
| `click_ui_soft_03.wav` | 0.50 | Modern technology select — Mixkit | Legacy, not used |
| `glass_tap_01.mp3` | 0.49 | Glass Tap — zembacraftworks (Freesound #427389) | Legacy, not used |
| `glass_tap_02.mp3` | 0.51 | Glass Tap 2 — CJspellsfish (Freesound #668383) | Legacy, not used |
| `glass_tap_screen_03.mp3` | 0.60 | Knocking On Screen, 01.wav — MATRIXXX_ (Freesound #368680) | Legacy, not used |
| `glass_ui_kenney_01.ogg` | 0.28 | glass_001.ogg, Interface Sounds 1.0 — Kenney | Legacy, not used |
| `glass_ui_kenney_02.ogg` | 0.69 | glass_004.ogg, Interface Sounds 1.0 — Kenney | Legacy, not used |
| `glitch_digital_01.wav` | 1.07 | Digital glitch break — Mixkit | Legacy, not used |
| `glitch_digital_02.wav` | 1.72 | Small sci fi glitch — Mixkit | Legacy, not used |
| `glitch_digital_03.wav` | 2.04 | Virtual quick glitch — Mixkit | Legacy, not used |
| `impact_hit_01.wav` | 1.22 | Quick zoom impact — Mixkit | Legacy, not used |
| `impact_hit_02.mp3` | 4.08 | Cinematic whoosh deep impact — Mixkit | Legacy, not used |
| `impact_hit_03.wav` | 5.99 | Movie impact intro presentation — Mixkit | Legacy, not used |
| `keyboard_typing_01.wav` | 2.13 | Electronic typing — Mixkit | Legacy, not used |
| `keyboard_typing_02.wav` | 10.54 | Hard laptop keyboard typing — Mixkit | Legacy, not used |
| `liquid_ui_01.wav` | 0.92 | Water sci fi bleep — Mixkit | Legacy, not used |
| `liquid_ui_02.wav` | 1.05 | Liquid bubble — Mixkit | Legacy, not used |
| `mouse_click_01.wav` | 1.04 | Clear mouse clicks — Mixkit | Legacy, not used |
| `mouse_click_02.wav` | 1.38 | Mouse click close — Mixkit | Legacy, not used |
| `mouse_click_03.wav` | 0.47 | Fast double click on mouse — Mixkit | Legacy, not used |
| `notification_ping_01.wav` | 1.29 | Digital quick tone — Mixkit | Legacy, not used |
| `notification_ping_02.wav` | 1.30 | Confirmation tone — Mixkit | Legacy, not used |
| `notification_ping_03.wav` | 1.72 | Interface hint notification — Mixkit | Legacy, not used |
| `pop_ui_01.wav` | 0.38 | Bubble pop up alert notification — Mixkit | Legacy, not used |
| `pop_ui_02.mp3` | 1.07 | Message pop alert — Mixkit | Legacy, not used |
| `pop_ui_03.wav` | 0.30 | Dry pop up notification alert — Mixkit | Legacy, not used |
| `pop_ui_04.wav` | 0.18 | Explainer video pops whoosh light pop — Mixkit | Legacy, not used |
| `reverse_cymbal_01.mp3` | 2.00 | reverse cymbal.wav — John Rayson (Freesound #23127) | Legacy, not used |
| `reverse_cymbal_02.mp3` | 2.78 | Reversed Crash Cymbal — TheEndOfACycle (Freesound #674291) | Legacy, not used |
| `reverse_cymbal_03.mp3` | 3.16 | cymbal-reversed-glassy-resonance.wav — burnttoys (Freesound #9523) | Legacy, not used |
| `riser_tech_01.wav` | 2.58 | Cinematic trailer riser — Mixkit | Legacy, not used |
| `riser_tech_02.mp3` | 6.56 | Short space stutter intro riser — Mixkit | Legacy, not used |
| `riser_tech_03.mp3` | 2.00 | Riser — Rizzard (Freesound #561207) | Legacy, not used |
| `riser_tech_04.mp3` | 1.93 | Energy Riser — magnuswaker (Freesound #522095) | Legacy, not used |
| `sparkle_shimmer_01.wav` | 2.33 | Magic sparkle touch — Mixkit | Legacy, not used |
| `sparkle_shimmer_02.wav` | 3.00 | Sweeping sparkle presentation intro — Mixkit | Legacy, not used |
| `suckin_vacuum_01.wav` | 2.26 | Vacuum swoosh transition — Mixkit | Legacy, not used |
| `suckin_vacuum_02.wav` | 1.27 | Air zoom vacuum — Mixkit | Legacy, not used |
| `swipe_ui_01.wav` | 1.06 | Fast swipe zoom — Mixkit | Legacy, not used |
| `swipe_ui_02.wav` | 1.65 | Technology transition slide — Mixkit | Legacy, not used |
| `swipe_ui_03.wav` | 0.95 | Futuristic metal transition sweep — Mixkit | Legacy, not used |
| `tick_counter_01.wav` | 1.84 | Arcade retro scoring counter — Mixkit | Legacy, not used |
| `tick_counter_02.wav` | 9.93 | Electric ticking counter — Mixkit | Legacy, not used |
| `tick_ui_kenney_01.ogg` | 0.04 | tick_001.ogg, Interface Sounds 1.0 — Kenney | Legacy, not used |
| `tick_ui_kenney_02.ogg` | 0.02 | tick_002.ogg, Interface Sounds 1.0 — Kenney | Legacy, not used |
| `whoosh_soft_01.wav` | 2.32 | Air woosh — Mixkit | Legacy, not used |
| `whoosh_soft_02.wav` | 1.39 | Short wind swoosh — Mixkit | Active (see 2.2) |
| `whoosh_soft_03.wav` | 1.32 | Cinematic transition wind swoosh — Mixkit | Legacy, not used |
| `whoosh_soft_04.wav` | 1.10 | Quick swoosh accent — Mixkit | Active (see 2.2) |
| `whoosh_whip_01.wav` | 1.76 | Fast whoosh transition — Mixkit | Legacy, not used |
| `whoosh_whip_02.wav` | 1.33 | Cinematic whoosh fast transition — Mixkit | Legacy, not used |
| `whoosh_whip_03.wav` | 0.86 | Fast air sweep transition — Mixkit | Legacy, not used |
| `whoosh_whip_04.wav` | 0.57 | Fast transitions swoosh — Mixkit | Legacy, not used |

---

## 17. Appendix B: full checksum manifest

MD5 checksums of every file this guide references, measured on 31 October 2026. Use them with Section 2.3–2.4.

| File | Rel. path | MD5 |
|---|---|---|
| `whoosh_soft_digital-whoosh-soft_02.mp3` | `01_whoosh_soft/whoosh_soft_digital-whoosh-soft_02.mp3` | `b4afe3c92a350575bc129f97bd3eaa62` |
| `whoosh_soft_swing-1-5_01.mp3` | `01_whoosh_soft/whoosh_soft_swing-1-5_01.mp3` | `35ae4c786cbc136c555b39f518e0041f` |
| `whoosh_soft_whoosh-soft_03.mp3` | `01_whoosh_soft/whoosh_soft_whoosh-soft_03.mp3` | `81caef265e60a53d7c21adff2de280ae` |
| `whoosh_fast_whip_clean-fast-swoosh_01.mp3` | `02_whoosh_fast_whip/whoosh_fast_whip_clean-fast-swoosh_01.mp3` | `dd1467f64e834cc215071df28d8cc693` |
| `whoosh_fast_whip_whip-10_04.mp3` | `02_whoosh_fast_whip/whoosh_fast_whip_whip-10_04.mp3` | `2df86d41f98d8a3c222c4c274b6a7e0c` |
| `whoosh_fast_whip_whip-8_02.mp3` | `02_whoosh_fast_whip/whoosh_fast_whip_whip-8_02.mp3` | `59d841d3c03add4d29f1796c9a05ef7d` |
| `whoosh_fast_whip_whip-9_03.mp3` | `02_whoosh_fast_whip/whoosh_fast_whip_whip-9_03.mp3` | `0fe32340cd56bc188db3ddffedae9e7d` |
| `pop_ui_bop-sound-effect-button_04.mp3` | `03_pop_ui/pop_ui_bop-sound-effect-button_04.mp3` | `ceea4f42ccfd173c628b52f817568817` |
| `pop_ui_click-pop-two-part_01.mp3` | `03_pop_ui/pop_ui_click-pop-two-part_01.mp3` | `e893eba58846b0cf4e9edb0252038043` |
| `pop_ui_the-best-bubble-pop-sound-for-ga_03.mp3` | `03_pop_ui/pop_ui_the-best-bubble-pop-sound-for-ga_03.mp3` | `a0aacd980e638b0e63405f9b170c7ec9` |
| `pop_ui_ui-series-hollow-pop_02.mp3` | `03_pop_ui/pop_ui_ui-series-hollow-pop_02.mp3` | `84f83efe13c2f666f79ce5cac7be17ed` |
| `click_tap_lego-click-short_02.mp3` | `04_click_tap/click_tap_lego-click-short_02.mp3` | `a50330028a3c048d78b8093e5536250c` |
| `click_tap_menu-fx-03-descending_04.mp3` | `04_click_tap/click_tap_menu-fx-03-descending_04.mp3` | `6e072a6bb1b68d29ab82e8bbab2fa9e4` |
| `click_tap_snap-click-07_01.mp3` | `04_click_tap/click_tap_snap-click-07_01.mp3` | `6e33b59f838ac1f78aab2c327e4614e8` |
| `click_tap_ui-click_03.mp3` | `04_click_tap/click_tap_ui-click_03.mp3` | `81779696d268ae55fa76cc6fae61cae3` |
| `glass_liquid_sci-fi-bubble-pop_04.mp3` | `05_glass_liquid/glass_liquid_sci-fi-bubble-pop_04.mp3` | `477219c9f4f30bb0641847e2af473d0f` |
| `glass_liquid_soap-bubble-pop-mouth-perc_01.mp3` | `05_glass_liquid/glass_liquid_soap-bubble-pop-mouth-perc_01.mp3` | `ab90327eca84710a0d24875c814e3398` |
| `glass_liquid_the-best-bubble-pop-sound-for-ga_02.mp3` | `05_glass_liquid/glass_liquid_the-best-bubble-pop-sound-for-ga_02.mp3` | `a0aacd980e638b0e63405f9b170c7ec9` |
| `tick_counter_mab-clock-tick-1-20080713_02.mp3` | `06_tick_counter/tick_counter_mab-clock-tick-1-20080713_02.mp3` | `f5e9ffc7049d5f13600591bf0e17965b` |
| `tick_counter_sfx-ambiance-clock-tick_01.mp3` | `06_tick_counter/tick_counter_sfx-ambiance-clock-tick_01.mp3` | `8320b7d1869b566252a051f73509bc34` |
| `tick_counter_soft-ui-digital-tick_04.mp3` | `06_tick_counter/tick_counter_soft-ui-digital-tick_04.mp3` | `ce2ebd737bac3df7ebacaa7729d030e5` |
| `typing_keys_keyboard-computer-mechanical-typ_04.mp3` | `07_typing_keys/typing_keys_keyboard-computer-mechanical-typ_04.mp3` | `10f067577f6c9898675a6a65d549e3da` |
| `typing_keys_mech-keyboard-01_02.mp3` | `07_typing_keys/typing_keys_mech-keyboard-01_02.mp3` | `a3c51ce4fbbce0a88e4e6ab4da4942f8` |
| `typing_keys_mech-keyboard-02_03.mp3` | `07_typing_keys/typing_keys_mech-keyboard-02_03.mp3` | `b8d74b820939b7108a3dfdaadf75b114` |
| `riser_brush-rising-woosh-muffle-000212_03.mp3` | `08_riser/riser_brush-rising-woosh-muffle-000212_03.mp3` | `477735a956d87fccf5905ed78a212ca0` |
| `riser_energy-riser_01.mp3` | `08_riser/riser_energy-riser_01.mp3` | `7be97b89bc9f25ec0d66e97361fb9e3f` |
| `riser_riser_02.mp3` | `08_riser/riser_riser_02.mp3` | `13146f8aa3d8dd8a627403d0cfae865f` |
| `riser_whoosh_04.mp3` | `08_riser/riser_whoosh_04.mp3` | `56416e83afb708bfe7560460b1e51e6c` |
| `impact_hit_deep-cinematic-impact_01.mp3` | `09_impact_hit/impact_hit_deep-cinematic-impact_01.mp3` | `7208b6f26f91e32df262440b91e509a3` |
| `impact_hit_dia-s15-warped-bass-hits-1_03.mp3` | `09_impact_hit/impact_hit_dia-s15-warped-bass-hits-1_03.mp3` | `8e40ed24925d765bde40f62098771be9` |
| `impact_hit_super-low-bass-hit-kick-drum-wav_02.mp3` | `09_impact_hit/impact_hit_super-low-bass-hit-kick-drum-wav_02.mp3` | `048172ff677aff92322e470750d44d5c` |
| `glitch_digital_glitch-corruption_03.mp3` | `10_glitch_digital/glitch_digital_glitch-corruption_03.mp3` | `2ed49d25cd3ff816801a505cc19ca199` |
| `glitch_digital_interference_01.mp3` | `10_glitch_digital/glitch_digital_interference_01.mp3` | `6f21bb38a0aa8253c9f35314aec7ef4d` |
| `glitch_digital_static-glitch_02.mp3` | `10_glitch_digital/glitch_digital_static-glitch_02.mp3` | `e4a5d86dae693fe284b234f58c70432f` |
| `notification_chime-notification_04.mp3` | `11_notification/notification_chime-notification_04.mp3` | `68f9c5e8f246a3465b23ceda5de166a4` |
| `notification_notification-sound_02.mp3` | `11_notification/notification_notification-sound_02.mp3` | `580c64e4bed11173ba0104b5b4ccf9bb` |
| `notification_notification-sound_03.mp3` | `11_notification/notification_notification-sound_03.mp3` | `75902399e68a14f3cf487a666baebb06` |
| `swipe_scroll_sfx-whoosh-high-1-12_01.mp3` | `12_swipe_scroll/swipe_scroll_sfx-whoosh-high-1-12_01.mp3` | `26f205061082859c4ecd8c23ebb924e8` |
| `swipe_scroll_whip01_03.mp3` | `12_swipe_scroll/swipe_scroll_whip01_03.mp3` | `926f5584176bb93ab5cd9d6466c2f6d1` |
| `swipe_scroll_whip02_02.mp3` | `12_swipe_scroll/swipe_scroll_whip02_02.mp3` | `ab53e514a653c3510976a96fa603ae62` |
| `swipe_scroll_whips04_04.mp3` | `12_swipe_scroll/swipe_scroll_whips04_04.mp3` | `59f341090ddef02d186cc1a6dc708cda` |
| `shimmer_sparkle_fantasy-ui-button-3_03.mp3` | `13_shimmer_sparkle/shimmer_sparkle_fantasy-ui-button-3_03.mp3` | `acb60b776ef1d9d35c474ae5866eb985` |
| `shimmer_sparkle_transition-action-jump-pitch-shi_01.mp3` | `13_shimmer_sparkle/shimmer_sparkle_transition-action-jump-pitch-shi_01.mp3` | `24cde79cb5e123174d76fa52b0ed0d55` |
| `shimmer_sparkle_transition-action-jump-pitch-shi_02.mp3` | `13_shimmer_sparkle/shimmer_sparkle_transition-action-jump-pitch-shi_02.mp3` | `8aa80691802ec33249e0fdea091d411e` |
| `reverse_suck_backwards-whoosh_02.mp3` | `14_reverse_suck/reverse_suck_backwards-whoosh_02.mp3` | `7fc6e5a841af00d294138a3459d3d2ed` |
| `reverse_suck_reverse-cymbal_05.mp3` | `14_reverse_suck/reverse_suck_reverse-cymbal_05.mp3` | `d96eb7ac6b52c615dc450fab976ba4a9` |
| `reverse_suck_sfx-weird-watery-sucking-sound_03.mp3` | `14_reverse_suck/reverse_suck_sfx-weird-watery-sucking-sound_03.mp3` | `4b7c089d7c5dbd65f4f636e1d259daea` |
| `camera_shutter_camera-shutter-analogue-film-slr_02.mp3` | `15_camera_shutter/camera_shutter_camera-shutter-analogue-film-slr_02.mp3` | `de0277b9b3271d2a457e6e13ecc25d0a` |
| `camera_shutter_camera-shutter-analogue-film-slr_04.mp3` | `15_camera_shutter/camera_shutter_camera-shutter-analogue-film-slr_04.mp3` | `143c36a24f6e0c48346d0739ff67b5a5` |
| `camera_shutter_shutter_03.mp3` | `15_camera_shutter/camera_shutter_shutter_03.mp3` | `c6b2c75d46eec4af4b5314eaa490ea37` |
| `camera_shutter_taking-photo-with-camera_01.mp3` | `15_camera_shutter/camera_shutter_taking-photo-with-camera_01.mp3` | `bb5fc0da39ca642454c9ab6d6bbb0baf` |
| `fun_cute_bounce.mp3` | `work/sfx_fun/fun_cute_bounce.mp3 (extra)` | `5b6caf0d7ce67043b3ad628be029cfba` |
| `fun_double_blink.mp3` | `work/sfx_fun/fun_double_blink.mp3 (extra)` | `dec54b7ea883ac9e97a644a8893c836c` |
| `fun_mild_surprise.mp3` | `work/sfx_fun/fun_mild_surprise.mp3 (extra)` | `4a72057b0e5858a887a229b9bf3ef773` |
| `fun_xylo_sting.mp3` | `work/sfx_fun/fun_xylo_sting.mp3 (extra)` | `77aa74a316ebb6e82573f6eb95a5f295` |
| `whoosh_soft_02.wav` | `work/sfx/whoosh_soft_02.wav (extra)` | `9f05710d4ec2f3111f980134397e2d27` |
| `whoosh_soft_04.wav` | `work/sfx/whoosh_soft_04.wav (extra)` | `286e01e802ccf40d3de652dd947b7752` |

---

*End of guide. If anything here conflicts with a direct instruction from the user, the user's instruction wins; note the change so this guide can be updated.*
