# ES-DE Multi-Disc M3U Generator

A modern, user-friendly tool for automatically generating M3U files for multi-disc games, designed for use with ES-DE and similar emulation frontends.

![Screenshot: ES-DE Multi-Disc M3U Generator main window](screenshot.png)
*Modern PyQt5 interface with dark theme, drag-and-drop support, and flexible multi-disc detection*

## Features
- Modern PyQt5 GUI with dark and light theme support
- Drag-and-drop support for both files and folders
- Flexible multi-disc detection (Disc, CD, Disk, Diskette, with/without spaces, parentheses, brackets, hyphens, underscores, region tags, etc.)
- Clean, professional interface with styled status bar, scrollbars, and resizable columns
- Fast, robust background scanning

## Installation
- Download the latest release from the [Releases](https://github.com/Xplizet/esde-m3u-generator/releases) page
- Or run from source with Python 3.7+ and PyQt5:
  ```sh
  pip install -r requirements.txt
  python m3u_generator.py
  ```

## Usage
1. Launch the app.
2. Drag and drop your game folders or files onto the window, or use the menu to select a folder.
3. The app will scan for multi-disc games and generate M3U files in the correct subfolders.
4. Toggle between dark and light themes from the menu.

### Example Folder Structure
```
YourGamesRoot/
  Game Title (USA) (Disc 1).cue
  Game Title (USA) (Disc 2).cue
  Another Game (Europe) [CD1].cue
  Another Game (Europe) [CD2].cue
  Subfolder/
    Multi-Disc Game (Disc 1).cue
    Multi-Disc Game (Disc 2).cue
```

After scanning, M3U files will be created in the same folders as the detected games.

## Changelog
See [CHANGELOG.md](CHANGELOG.md) for a full list of changes.

## Release Notes
See [RELEASE_v2.0.0.md](RELEASE_v2.0.0.md) for highlights of the latest version.

## License
MIT
