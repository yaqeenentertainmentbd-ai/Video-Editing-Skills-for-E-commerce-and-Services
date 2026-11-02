# macOS install

```bash
bash Scripts/install_fonts.sh          # per user -> ~/Library/Fonts, no sudo
bash Scripts/install_fonts.sh --legacy # also v1 fonts
```
System-wide (needs admin; only with permission): copy the `.ttf` files to `/Library/Fonts`.
GUI alternative: open a font in Font Book and press Install.

Opekkha is not in the library: download from https://fontbd.com and install via Font Book.

Check installed: `system_profiler SPFontsDataType | grep -iE "Poppins|Hind Siliguri|Montserrat|Instrument Serif|Abu Sayed|Opekkha"` or `python3 Scripts/verify_fonts.py`.
Duplicates: Font Book -> File -> Resolve Duplicates. Font Book also validates (File -> Validate Font).
Cache: `atsutil databases -remove` (then log out and in) only if fonts misbehave. Quit and relaunch editing apps after install.
