# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2025-07-06

### Added
- **Subfolder preservation**: M3U folders are now created in the same subfolder where multidisc games are detected, rather than moving everything to the root ROMs folder
- Enhanced UI display showing which subfolder each multidisc game is located in
- Improved folder structure handling for better organization

### Changed
- Modified `find_multidisc_games()` to use subfolder paths as part of game keys
- Updated `generate_esde_folders()` to create M3U folders in their original subfolder locations
- Enhanced `_update_results()` to display subfolder information in the UI
- Updated documentation with new folder structure examples

### Fixed
- Resolved issue where all multidisc games were being moved to the root ROMs folder regardless of their original subfolder location

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