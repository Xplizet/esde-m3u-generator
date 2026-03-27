# ES-DE Multi-Disc M3U Generator

A modern, user-friendly tool for automatically generating M3U files for multi-disc games, designed for use with ES-DE and similar emulation frontends.

![Screenshot: ES-DE Multi-Disc M3U Generator main window](screenshot.png)
*Modern PyQt5 interface with dark theme, drag-and-drop support, and flexible multi-disc detection*

## Features
- Modern PyQt5 GUI with dark and light theme support
- CLI mode for headless/SSH usage
- Drag-and-drop support for both files and folders
- Flexible multi-disc detection (Disc, CD, Disk, Diskette, with/without spaces, parentheses, brackets, hyphens, underscores, region tags, etc.)
- Clean, professional interface with styled status bar, scrollbars, and resizable columns
- Fast, robust background scanning
- Cross-platform support (Windows, Linux, macOS)

## Installation

### Windows
Download the latest release from the [Releases](https://github.com/Xplizet/esde-m3u-generator/releases) page:
- `ESDE_M3U_Generator_<version>.exe` — GUI version (desktop use)
- `ESDE_M3U_Generator_CLI_<version>.exe` — CLI version (SSH / headless systems)

No Python installation required.

### Linux / macOS
Run from source with Python 3.7+:
```sh
# GUI (requires PyQt5)
pip install -r requirements.txt
python m3u_generator.py

# CLI only (no dependencies beyond Python standard library)
python m3u_generator_cli.py /path/to/roms
```

## Usage

### GUI
1. Launch the app (double-click the exe or run `python m3u_generator.py` with no arguments).
2. Drag and drop your game folders or files onto the window, or use the menu to select a folder.
3. The app will scan for multi-disc games and generate M3U files in the correct subfolders.
4. Toggle between dark and light themes from the menu.

### CLI (for SSH / headless systems)
Using the standalone CLI executable (no Python required):
```sh
ESDE_M3U_Generator_CLI.exe /path/to/roms        # scan, review, confirm
ESDE_M3U_Generator_CLI.exe /path/to/roms -y     # skip confirmation prompt
ESDE_M3U_Generator_CLI.exe --help               # show usage
```

Or from source (no PyQt5 required):
```sh
python m3u_generator_cli.py /path/to/roms
python m3u_generator_cli.py /path/to/roms -y
```

The CLI uses the same detection and generation logic as the GUI. It lists all detected multi-disc games and asks for confirmation before creating folders and moving files.

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

## License
MIT
