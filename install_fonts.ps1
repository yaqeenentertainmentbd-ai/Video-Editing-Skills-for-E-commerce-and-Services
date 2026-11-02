# Per-user font install for Windows 10 1809+ / Windows 11. No admin needed.
# Usage:  powershell -ExecutionPolicy Bypass -File Scripts\install_fonts.ps1 [-AllUsers] [-IncludeLegacy]
# -AllUsers needs an elevated shell and writes to C:\Windows\Fonts + HKLM.
# Never downloads anything. Only copies .ttf files from ..\Fonts.
param([switch]$AllUsers, [switch]$IncludeLegacy)

$root = Split-Path -Parent $PSScriptRoot
$src  = Join-Path $root 'Fonts'
if ($AllUsers) {
  $dest = Join-Path $env:WINDIR 'Fonts'
  $reg  = 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts'
} else {
  $dest = Join-Path $env:LOCALAPPDATA 'Microsoft\Windows\Fonts'
  $reg  = 'HKCU:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts'
}
New-Item -ItemType Directory -Force -Path $dest | Out-Null

Add-Type -AssemblyName PresentationCore
$files = Get-ChildItem -Path $src -Recurse -Filter *.ttf
if (-not $IncludeLegacy) { $files = $files | Where-Object { $_.FullName -notmatch '\\Legacy_v1_' } }

foreach ($f in $files) {
  $target = Join-Path $dest $f.Name
  if (Test-Path $target) {
    $same = (Get-FileHash $target).Hash -eq (Get-FileHash $f.FullName).Hash
    if ($same) { Write-Host "skip (identical) $($f.Name)"; continue }
    Write-Warning "$($f.Name) exists with DIFFERENT content - not overwriting. Resolve manually."; continue
  }
  Copy-Item $f.FullName $target
  $gf = New-Object System.Windows.Media.GlyphTypeface ([uri]$target)
  $name = ($gf.Win32FaceNames.Values | Select-Object -First 1)
  $fam  = ($gf.Win32FamilyNames.Values | Select-Object -First 1)
  $regName = "$fam $name (TrueType)"
  New-ItemProperty -Path $reg -Name $regName -Value $(if ($AllUsers) { $f.Name } else { $target }) -PropertyType String -Force | Out-Null
  Write-Host "installed $($f.Name) as '$regName'"
}
Write-Host "`nDone. Restart Premiere / After Effects / Resolve / CapCut, then run: python Scripts\verify_fonts.py"
