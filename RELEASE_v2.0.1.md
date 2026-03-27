# ES-DE Multi-Disc M3U Generator v2.0.1

## Bug Fixes

### Fixed game names being truncated when region tags are present

File names with parenthesized region tags (e.g., `(USA)`, `(Europe)`, `(Japan)`) were being cut short, resulting in incorrect folder and M3U names.

**Before:**
```
Final Fantasy VII (USA) (Disc 1).chd  ->  "Final Fantasy VII (USA.m3u"
Resident Evil 2 (USA) [CD1].cue      ->  "Resident Evil 2 (USA.m3u"
```

**After:**
```
Final Fantasy VII (USA) (Disc 1).chd  ->  "Final Fantasy VII (USA).m3u"
Resident Evil 2 (USA) [CD1].cue      ->  "Resident Evil 2 (USA).m3u"
```

### Fixed subfolder preservation for multi-disc games

When scanning a root folder containing subfolders (e.g., `PSX/`, `Saturn/`), all M3U folders were incorrectly created at the root level. They are now created in the correct subfolder alongside the original disc files.

**Before:**
```
ROMs/
  PSX/
  Resident Evil 2 (USA).m3u/    <-- wrong, pulled up to root
```

**After:**
```
ROMs/
  PSX/
    Resident Evil 2 (USA).m3u/  <-- correct, stays in PSX/
```

## Download

Download `ESDE_M3U_Generator_2.0.1.exe` below -- no Python installation required.
