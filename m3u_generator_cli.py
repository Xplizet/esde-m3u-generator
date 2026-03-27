#!/usr/bin/env python3
"""
ES-DE Multi-Disc M3U Generator — CLI version
Standalone script with no PyQt5 dependency.
"""

import sys
import os
import re
import argparse
from pathlib import Path

DISC_PATTERN = re.compile(
    r'(?i)(?P<basename>.*?)'
    r'[\s\-_]*[\(\[]*'
    r'(disc|cd|disk|diskette)[\s\-_]*'
    r'(?P<discnum>\d+)'
    r'[\s\-_]*[\)\]]*'
    r'(?:[^\w\d]|$)'
)


def extract_disc_number(filename):
    match = re.search(r'(?i)(disc|cd|disk|diskette)[\s\-_]*([0-9]+)', filename)
    if match:
        return int(match.group(2))
    return 0


def find_multidisc_games(folder):
    games = {}
    for file_path in Path(folder).rglob('*'):
        if file_path.is_file():
            filename = file_path.name
            match = DISC_PATTERN.search(filename)
            if match:
                base_name = match.group('basename').strip(' -_')
                if not base_name:
                    base_name = filename
                rel_parent = file_path.parent.relative_to(folder)
                if str(rel_parent) != '.':
                    game_key = f"{rel_parent.as_posix()}/{base_name}"
                else:
                    game_key = base_name
                if game_key not in games:
                    games[game_key] = []
                games[game_key].append((filename, file_path))
    for game_name in games:
        games[game_name].sort(key=lambda x: extract_disc_number(x[0]))
    return games


def generate(folder, games):
    created_folders = []
    moved_count = 0

    for game_name, discs in games.items():
        if '/' in game_name:
            subfolder_path, base_game_name = game_name.rsplit('/', 1)
            target_folder = Path(folder) / subfolder_path
        else:
            base_game_name = game_name
            target_folder = Path(folder)

        folder_name = f"{base_game_name}.m3u"
        game_folder = target_folder / folder_name
        game_folder.mkdir(parents=True, exist_ok=True)

        for disc_filename, disc_path in discs:
            new_disc_path = game_folder / disc_filename
            disc_path.rename(new_disc_path)
            moved_count += 1

        m3u_path = game_folder / folder_name
        with open(m3u_path, 'w', encoding='utf-8') as f:
            for disc_filename, _ in discs:
                f.write(f"{disc_filename}\n")

        rel_name = f"{subfolder_path}/{folder_name}" if '/' in game_name else folder_name
        created_folders.append(rel_name)
        print(f"  Created: {rel_name}")

    return created_folders, moved_count


def main():
    parser = argparse.ArgumentParser(
        prog="m3u_generator_cli",
        description="ES-DE Multi-Disc M3U Generator (CLI) - create .m3u folders for multi-disc games"
    )
    parser.add_argument("folder", help="Path to the games/ROMs folder to scan")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation prompt")
    args = parser.parse_args()

    folder = os.path.abspath(args.folder)
    if not os.path.isdir(folder):
        print(f"Error: '{folder}' is not a valid directory.")
        sys.exit(1)

    print(f"Scanning '{folder}' for multi-disc games...")
    games = find_multidisc_games(folder)

    if not games:
        print("No multi-disc games found.")
        sys.exit(0)

    print(f"\nFound {len(games)} multi-disc game(s):\n")
    for i, (name, discs) in enumerate(sorted(games.items()), 1):
        print(f"  {i}. {name} ({len(discs)} discs)")
        for disc_filename, _ in discs:
            print(f"       - {disc_filename}")

    print(f"\nThis will create {len(games)} .m3u folder(s) and move disc files into them.")

    if not args.yes:
        try:
            answer = input("\nProceed? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            sys.exit(0)
        if answer not in ('y', 'yes'):
            print("Aborted.")
            sys.exit(0)

    print()
    created_folders, moved_count = generate(folder, games)
    print(f"\nDone! Created {len(created_folders)} folder(s), moved {moved_count} file(s).")


if __name__ == "__main__":
    main()
