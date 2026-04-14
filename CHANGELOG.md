# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.3] - 2026-04-14
### Added
- Multi-disc detection now recognizes bare-numbered filenames like `Game (USA) (1).chd`, `Game (USA) (2).chd`, etc. (#4)
- Verification script (`verify_detection.py`) covering both keyword and bare-number patterns plus common false-positive cases

### Fixed
- Files using bare `(N)` numbering are now grouped and processed correctly. Detection requires 2+ sibling files sharing the same base name, so single-file disambiguators (`Game (Rev 1).chd`, `Game (1996).chd`, lone `Game (1).chd`) are not misidentified as multi-disc games.

## [2.0.2] - 2026-03-27
### Added
- CLI mode for headless/SSH usage (standalone executable, no PyQt5 dependency)
- Build script now produces both GUI and CLI executables

### Fixed
- Fixed cross-device file move error (`[WinError 17]`) when running under Wine on Linux (#2)

## [2.0.1] - 2026-03-27
### Fixed
- Fixed multi-disc detection truncating game names with parenthesized region tags (e.g., "Final Fantasy VII (USA) (Disc 1).chd" was incorrectly parsed as "Final Fantasy VII (USA")
- Fixed subfolder preservation: M3U folders are now created in the correct subfolder instead of the root scan directory

## [2.0.0] - 2024-06-09
### Added
- Brand new PyQt5-based GUI with modern dark and light themes
- Drag-and-drop support for both files and folders
- Flexible multi-disc detection supporting a wide range of naming patterns (Disc, CD, Disk, Diskette, with/without spaces, parentheses, brackets, hyphens, underscores, region tags, etc.)
- Professional interface with styled status bar, scrollbars, and resizable columns

### Changed
- Improved error handling and user feedback
- Faster, more robust background scanning
- Updated documentation and release notes

### Removed
- All test/demo UI and legacy code

### Fixed
- Issues with horizontal scroll bars and column resizing
- Grouping and detection for all common and tricky multi-disc naming conventions

## [Unreleased]

### Added
- New PyQt5-based GUI: `m3u_generator.py` with modern dark and light theme support
- Theme switcher in the menu (View → Theme)
- Professional dark theme styling for all widgets, headers, and scroll bars
- Horizontal and vertical scroll bars for the multi-disc games list, styled for both themes
- Interactive column resizing for long game and folder names
- **Flexible multi-disc detection:** Now supports a wide range of disc naming patterns, including `Disc`, `CD`, `Disk`, `Diskette`, with or without parentheses, brackets, spaces, hyphens, underscores, etc. (e.g., `Game Disc1`, `Game (CD 2)`, `Game-disk3`, `Game_cd4`, `Game[Diskette5]`)

### Changed
- Replaced tkinter interface with PyQt5 for a more modern, responsive, and visually appealing UI
- Improved column width handling: "Selected" column is now wide enough for the full title
- "Game Name" and "Folder Name" columns are now resizable and support horizontal scrolling
- Status bar and progress bar now use PyQt5 widgets and styling
- Grouped sections for better organization (folder selection, results, etc.)
- Updated requirements.txt to include PyQt5
- **Improved grouping logic:** Discs with different keywords (disc, cd, disk, etc.) and separators are now grouped as the same game if the base name matches

### Fixed
- Fixed issue where horizontal scroll bar would not appear for long game or folder names
- Fixed style/layout issues caused by forced widget widths
- Fixed header visibility and readability in dark theme
- Fixed checkboxes and selection logic for the new tree widget

## [1.1.0] - 2025-07-06

### Added
- **Subfolder preservation**: M3U folders are now created in the same subfolder where multidisc games are detected, rather than moving everything to the selected root folder
- Enhanced UI display showing which subfolder each multidisc game is located in
- Improved folder structure handling for better organization

### Changed
- Modified `find_multidisc_games()` to use subfolder paths as part of game keys
- Updated `generate_esde_folders()` to create M3U folders in their original subfolder locations
- Enhanced `_update_results()` to display subfolder information in the UI
- Updated documentation with new folder structure examples

### Fixed
- Resolved issue where all multidisc games were being moved to the selected root folder regardless of their original subfolder location

## [1.0.0] - 2025-07-03

### Added
- Initial release of ES-DE Multi-Disc M3U Generator
- GUI application for creating ES-DE compatible multi-disc game folders
- Automatic detection of multi-disc games using "(Disc X)" naming pattern
- Recursive folder scanning through all subfolders
- Checkbox selection interface for choosing which games to process
- "Select All" and "Select None" buttons for easy selection
- Progress indication and status bar
- Support for all file extensions
- Automatic disc sorting by disc number
- M3U file generation with proper disc order
- Standalone executable build support
- Comprehensive documentation and examples

### Features
- Clean, modern GUI with auto-hiding scrollbars
- No duplicate entries in ES-DE, proper disc switching
- Works with any file extension
- Safe to run multiple times (won't duplicate folders)
- No Python knowledge required for the .exe version 