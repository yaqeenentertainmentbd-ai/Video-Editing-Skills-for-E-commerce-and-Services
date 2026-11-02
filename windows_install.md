# Windows install (10 1809+ / 11)

Run from the library root. Nothing is downloaded; only `Fonts\**\*.ttf` is copied.

## Without admin (per user, recommended)
```powershell
powershell -ExecutionPolicy Bypass -File Scripts\install_fonts.ps1
```
Copies to `%LOCALAPPDATA%\Microsoft\Windows\Fonts` and registers under `HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts`.
Add `-IncludeLegacy` for the v1 fonts (Anek Bangla, Tiro Bangla, Noto Sans Bengali).

## With admin (all users)
Open an elevated PowerShell, then `Scripts\install_fonts.ps1 -AllUsers`. Do not bypass UAC; if not elevated, use the per-user mode.

## Opekkha (not in the library)
Download from FontBD (https://fontbd.com), install by right-click -> "Install for all users" or per-user. Family name must read `FN Shorif Opekkha Unicode`.
If the user keeps a private copy, the originals are listed in the guide, section 5.

## Check already installed
```powershell
Add-Type -AssemblyName PresentationCore
[Windows.Media.Fonts]::SystemFontFamilies | Where-Object Source -match 'Poppins|Hind Siliguri|Montserrat|Instrument Serif|Abu Sayed|Opekkha' | Select Source
python Scripts\verify_fonts.py
```
Missing weights: verify_fonts prints one MISSING line per family/weight. Re-run the installer.

## Duplicates / conflicts
The installer refuses to overwrite a same-named file with different content and warns. Check both `C:\Windows\Fonts` and `%LOCALAPPDATA%\Microsoft\Windows\Fonts`. Remove the older copy in Settings -> Personalization -> Fonts, then reinstall. Google Fonts "Poppins" static files and these are the same version (4.004).

## Refresh / restart
Windows has no manual font cache step for per-user installs. Fully quit and relaunch Premiere Pro, After Effects, DaVinci Resolve, CapCut, and any open Chrome used for HyperFrames renders. If an app still misses the font, sign out and in. Last resort: stop service `FontCache`, delete `C:\Windows\ServiceProfiles\LocalService\AppData\Local\FontCache\*` (admin), restart the service.

## Verify inside apps
Premiere: Essential Graphics / Text tool font list; After Effects: Character panel; Resolve: Text+ font dropdown; CapCut: Text -> Font. Type a Bangla sample and Latin sample; both must render without boxes. HyperFrames: run the lint/render and check logs for `font` warnings (fonts load from `assets/fonts` by @font-face, so system install is not required there).
