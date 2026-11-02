"""Verify the caption fonts: manifest files intact (sha256) and fonts visible to the OS.

Usage: python Scripts/verify_fonts.py
Needs: pip install fonttools   (only for reading the library; OS lookup uses PowerShell / fc-list / system_profiler)
Exit code 1 if a required family/weight is missing. Opekkha (not redistributable) is reported separately.
"""
import hashlib, json, os, platform, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
man = json.load(open(os.path.join(ROOT, "Font_Manifest", "font_manifest.json"), encoding="utf-8"))


def installed_names():
    s = platform.system()
    if s == "Windows":
        ps = ("Add-Type -AssemblyName PresentationCore;"
              "[System.Windows.Media.Fonts]::SystemFontFamilies | ForEach-Object { $_.Source };"
              "Get-ItemProperty 'HKCU:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Fonts' | "
              "Get-Member -MemberType NoteProperty | ForEach-Object Name")
        return subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True).stdout
    if s == "Darwin":
        return subprocess.run(["system_profiler", "SPFontsDataType"], capture_output=True, text=True).stdout
    return subprocess.run(["fc-list", ":", "family", "style", "file"], capture_output=True, text=True).stdout


bad = 0
for f in man["fonts"]:
    p = os.path.join(ROOT, f["file"])
    ok = os.path.exists(p) and hashlib.sha256(open(p, "rb").read()).hexdigest() == f["sha256"]
    if not ok:
        print("CORRUPT/MISSING in library:", f["file"]); bad = 1

names = installed_names().lower()
required = [f for f in man["fonts"] if "Legacy_v1_" not in f["file"]]
for f in required:
    fam = f["family"].lower()
    hit = fam in names
    print(("OK      " if hit else "MISSING ") + f"{f['family']} {f['subfamily']}")
    bad |= (not hit)
print("\nOpekkha (FN Shorif Opekkha Unicode): ", "found" if "opekkha" in names else "NOT installed - see guide section 5 (licence-restricted, install from FontBD)")
sys.exit(bad)
