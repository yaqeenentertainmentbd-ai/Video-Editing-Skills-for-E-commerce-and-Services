# Linux install

```bash
bash Scripts/install_fonts.sh          # per user -> ~/.local/share/fonts/video-editing, runs fc-cache
```
System-wide (needs sudo; only with permission): copy to `/usr/local/share/fonts/video-editing/` then `sudo fc-cache -f`.

Check installed: `fc-list | grep -iE "Poppins|Hind Siliguri|Montserrat|Instrument Serif|Abu Sayed|Opekkha"`; weights: `fc-list "Poppins" style`.
Duplicates: `fc-list : family file | sort | uniq -d`; remove the older file and run `fc-cache -f`.
Variable fonts (Montserrat-VF) show as one file with named instances; ffmpeg `drawtext`/libass pick the default instance (Thin), so for FFmpeg use static Montserrat from https://fonts.google.com/specimen/Montserrat instead.
Opekkha: not packaged, download from https://fontbd.com.
Restart editing apps after install.
