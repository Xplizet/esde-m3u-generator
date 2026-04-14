"""
Verification script for multi-disc detection logic in m3u_generator.py.

Builds a temp directory with synthetic filenames covering:
  - Standard Disc/CD/Disk/Diskette keyword patterns (regression checks)
  - Bare (N) chdman-style patterns (the new feature, GitHub issue #4)
  - False positives that must NOT trigger (Rev/Beta/Track/version/year/region)
  - Edge cases (lone bare-N file, mixed regions, out-of-order discs)

Asserts expected groupings for both find_multidisc_games (folder scan)
and find_multidisc_games_from_files (file-list scan).

Usage: python verify_detection.py
Exits 0 on success, 1 on any failure.
"""
import sys
import shutil
import tempfile
from pathlib import Path

from PyQt5.QtWidgets import QApplication
_app = QApplication.instance() or QApplication(sys.argv)

from m3u_generator import ScanWorker
import m3u_generator_cli


# Each scenario lives in its own subfolder for isolated folder-scan testing.
# Base names are unique across scenarios so file-list mode doesn't collide.
SCENARIOS = [
    # ===== SHOULD DETECT: keyword path (regression checks) =====
    {
        "subfolder": "FF7",
        "files": [
            "Final Fantasy VII (Disc 1).chd",
            "Final Fantasy VII (Disc 2).chd",
            "Final Fantasy VII (Disc 3).chd",
        ],
        "expected": {
            "Final Fantasy VII": [
                "Final Fantasy VII (Disc 1).chd",
                "Final Fantasy VII (Disc 2).chd",
                "Final Fantasy VII (Disc 3).chd",
            ]
        },
    },
    {
        "subfolder": "FF8",
        "files": [
            "Final Fantasy VIII (USA) (Disc 1).chd",
            "Final Fantasy VIII (USA) (Disc 2).chd",
            "Final Fantasy VIII (USA) (Disc 3).chd",
            "Final Fantasy VIII (USA) (Disc 4).chd",
        ],
        "expected": {
            "Final Fantasy VIII (USA)": [
                "Final Fantasy VIII (USA) (Disc 1).chd",
                "Final Fantasy VIII (USA) (Disc 2).chd",
                "Final Fantasy VIII (USA) (Disc 3).chd",
                "Final Fantasy VIII (USA) (Disc 4).chd",
            ]
        },
    },
    {
        "subfolder": "ChronoCross",
        "files": ["Chrono Cross CD1.chd", "Chrono Cross CD2.chd"],
        "expected": {
            "Chrono Cross": ["Chrono Cross CD1.chd", "Chrono Cross CD2.chd"]
        },
    },
    {
        "subfolder": "MetalGearHyphen",
        "files": ["Metal Gear Solid-disc1.chd", "Metal Gear Solid-disc2.chd"],
        "expected": {
            "Metal Gear Solid": [
                "Metal Gear Solid-disc1.chd",
                "Metal Gear Solid-disc2.chd",
            ]
        },
    },
    {
        "subfolder": "LemmingsDisks",
        "files": [
            "Lemmings[Diskette3].adf",
            "Lemmings[Diskette4].adf",
            "Lemmings[Diskette5].adf",
        ],
        "expected": {
            "Lemmings": [
                "Lemmings[Diskette3].adf",
                "Lemmings[Diskette4].adf",
                "Lemmings[Diskette5].adf",
            ]
        },
    },
    {
        "subfolder": "RivenCD",
        "files": ["Riven CD 1.chd", "Riven CD 2.chd"],
        "expected": {"Riven": ["Riven CD 1.chd", "Riven CD 2.chd"]},
    },
    # ===== SHOULD DETECT: new bare (N) pattern =====
    {
        "subfolder": "Castlevania",
        "files": [
            "Castlevania (USA) (1).chd",
            "Castlevania (USA) (2).chd",
            "Castlevania (USA) (3).chd",
            "Castlevania (USA) (4).chd",
        ],
        "expected": {
            "Castlevania (USA)": [
                "Castlevania (USA) (1).chd",
                "Castlevania (USA) (2).chd",
                "Castlevania (USA) (3).chd",
                "Castlevania (USA) (4).chd",
            ]
        },
    },
    {
        "subfolder": "CoolGame",
        "files": ["Cool Game (1).chd", "Cool Game (2).chd"],
        "expected": {"Cool Game": ["Cool Game (1).chd", "Cool Game (2).chd"]},
    },
    {
        "subfolder": "SimCity",
        "files": [
            "Sim City 2000 (Japan) (1).iso",
            "Sim City 2000 (Japan) (2).iso",
            "Sim City 2000 (Japan) (3).iso",
        ],
        "expected": {
            "Sim City 2000 (Japan)": [
                "Sim City 2000 (Japan) (1).iso",
                "Sim City 2000 (Japan) (2).iso",
                "Sim City 2000 (Japan) (3).iso",
            ]
        },
    },
    # Bare (N) discs added in non-sorted order, verify extract_disc_number works
    {
        "subfolder": "WildGame",
        "files": [
            "Wild Game (USA) (3).chd",
            "Wild Game (USA) (1).chd",
            "Wild Game (USA) (2).chd",
        ],
        "expected": {
            "Wild Game (USA)": [
                "Wild Game (USA) (1).chd",
                "Wild Game (USA) (2).chd",
                "Wild Game (USA) (3).chd",
            ]
        },
    },
    # ===== SHOULD NOT DETECT: false positives that must be rejected =====
    {
        "subfolder": "LoneBare",
        "files": ["Lone Game (USA) (1).chd"],  # only 1 file → not multi-disc
        "expected": {},
    },
    {
        "subfolder": "RevisionPair",
        "files": [
            "Tekken 3 (USA) (Rev 1).chd",
            "Tekken 3 (USA) (Rev 2).chd",
        ],
        "expected": {},
    },
    {
        "subfolder": "BetaPair",
        "files": [
            "Beta Title (Beta 1).chd",
            "Beta Title (Beta 2).chd",
        ],
        "expected": {},
    },
    {
        "subfolder": "TrackPair",
        "files": [
            "Track Game (Track 01).chd",
            "Track Game (Track 02).chd",
        ],
        "expected": {},
    },
    {
        "subfolder": "VersionPair",
        "files": [
            "Versioned (USA) (v1.0).chd",
            "Versioned (USA) (v1.1).chd",
        ],
        "expected": {},
    },
    {
        "subfolder": "YearPair",
        "files": [
            "Annual Sports (USA) (1996).chd",
            "Annual Sports (USA) (1997).chd",
        ],
        "expected": {},
    },
    {
        "subfolder": "RegionList",
        "files": [
            "Multi Lang Title (En,Fr,Es).chd",
            "Multi Lang Title (De,It,Pt).chd",
        ],
        "expected": {},
    },
    {
        "subfolder": "Standalone",
        "files": ["Standalone Game.chd", "Another Game.chd"],
        "expected": {},
    },
    {
        "subfolder": "RegionOnly",
        "files": ["Cartridge Game (USA).chd", "Cartridge Game (Japan).chd"],
        "expected": {},
    },
    {
        "subfolder": "DemoPair",
        "files": [
            "Preview Game (USA) (Demo 1).chd",
            "Preview Game (USA) (Demo 2).chd",
        ],
        "expected": {},
    },
    # ===== Edge case (mixed): two USA bare discs detect, lone Japan bare doesn't =====
    {
        "subfolder": "MegaManMixed",
        "files": [
            "Mega Man X4 (USA) (1).chd",
            "Mega Man X4 (USA) (2).chd",
            "Mega Man X4 (Japan) (1).chd",
        ],
        "expected": {
            "Mega Man X4 (USA)": [
                "Mega Man X4 (USA) (1).chd",
                "Mega Man X4 (USA) (2).chd",
            ]
        },
    },
]


def make_test_tree(root: Path):
    for scenario in SCENARIOS:
        sub = root / scenario["subfolder"]
        sub.mkdir(parents=True, exist_ok=True)
        for fn in scenario["files"]:
            (sub / fn).write_bytes(b"")


def test_folder_scan(root: Path):
    """find_multidisc_games keys by subfolder/basename, strict equality test."""
    worker = ScanWorker(folder_path=str(root))
    games = worker.find_multidisc_games(str(root))

    failures = []
    expected_total = {}
    for scenario in SCENARIOS:
        for base, files in scenario["expected"].items():
            key = f"{scenario['subfolder']}/{base}"
            expected_total[key] = files

    for key, expected_files in expected_total.items():
        if key not in games:
            failures.append(f"MISSING expected group: {key!r}")
            continue
        actual_files = [fn for fn, _ in games[key]]
        if actual_files != expected_files:
            failures.append(
                f"WRONG ORDER/CONTENT for {key!r}\n"
                f"     expected: {expected_files}\n"
                f"     got:      {actual_files}"
            )

    for key in games:
        if key not in expected_total:
            actual_files = [fn for fn, _ in games[key]]
            failures.append(f"UNEXPECTED group (false positive): {key!r} -> {actual_files}")

    return failures, games


def test_cli_scan(root: Path):
    """m3u_generator_cli.find_multidisc_games, keys by subfolder/basename."""
    games = m3u_generator_cli.find_multidisc_games(str(root))

    failures = []
    expected_total = {}
    for scenario in SCENARIOS:
        for base, files in scenario["expected"].items():
            key = f"{scenario['subfolder']}/{base}"
            expected_total[key] = files

    for key, expected_files in expected_total.items():
        if key not in games:
            failures.append(f"MISSING expected group: {key!r}")
            continue
        actual_files = [fn for fn, _ in games[key]]
        if actual_files != expected_files:
            failures.append(
                f"WRONG ORDER/CONTENT for {key!r}\n"
                f"     expected: {expected_files}\n"
                f"     got:      {actual_files}"
            )

    for key in games:
        if key not in expected_total:
            actual_files = [fn for fn, _ in games[key]]
            failures.append(f"UNEXPECTED group (false positive): {key!r} -> {actual_files}")

    return failures, games


def test_file_list_scan(root: Path):
    """find_multidisc_games_from_files keys by basename only (no subfolder context).

    Since our scenario base names are unique, we can do strict equality.
    """
    all_files = [str(p) for p in root.rglob("*") if p.is_file()]
    worker = ScanWorker(file_paths=all_files)
    games = worker.find_multidisc_games_from_files(all_files)

    failures = []
    expected_total = {}
    for scenario in SCENARIOS:
        for base, files in scenario["expected"].items():
            expected_total[base] = files

    for base, expected_files in expected_total.items():
        if base not in games:
            failures.append(f"MISSING expected group: {base!r}")
            continue
        actual_files = [fn for fn, _ in games[base]]
        if actual_files != expected_files:
            failures.append(
                f"WRONG ORDER/CONTENT for {base!r}\n"
                f"     expected: {expected_files}\n"
                f"     got:      {actual_files}"
            )

    for base in games:
        if base not in expected_total:
            actual_files = [fn for fn, _ in games[base]]
            failures.append(f"UNEXPECTED group (false positive): {base!r} -> {actual_files}")

    return failures, games


def main():
    tmpdir = Path(tempfile.mkdtemp(prefix="m3u_verify_"))
    try:
        print(f"Test root: {tmpdir}")
        make_test_tree(tmpdir)
        total_files = sum(len(s["files"]) for s in SCENARIOS)
        print(f"Created {total_files} files across {len(SCENARIOS)} scenarios\n")

        print("=" * 72)
        print("TEST 1: folder scan via find_multidisc_games")
        print("=" * 72)
        folder_failures, folder_games = test_folder_scan(tmpdir)
        if folder_failures:
            print(f"FAIL ({len(folder_failures)} failure(s)):")
            for f in folder_failures:
                print(f"  - {f}")
        else:
            print(f"PASS: {len(folder_games)} expected group(s) detected, no false positives")

        print()
        print("=" * 72)
        print("TEST 2: file-list scan via find_multidisc_games_from_files")
        print("=" * 72)
        file_failures, file_games = test_file_list_scan(tmpdir)
        if file_failures:
            print(f"FAIL ({len(file_failures)} failure(s)):")
            for f in file_failures:
                print(f"  - {f}")
        else:
            print(f"PASS: {len(file_games)} expected group(s) detected, no false positives")

        print()
        print("=" * 72)
        print("TEST 3: CLI module scan via m3u_generator_cli.find_multidisc_games")
        print("=" * 72)
        cli_failures, cli_games = test_cli_scan(tmpdir)
        if cli_failures:
            print(f"FAIL ({len(cli_failures)} failure(s)):")
            for f in cli_failures:
                print(f"  - {f}")
        else:
            print(f"PASS: {len(cli_games)} expected group(s) detected, no false positives")

        print()
        total_failures = len(folder_failures) + len(file_failures) + len(cli_failures)
        if total_failures:
            print("=" * 72)
            print(f"OVERALL: FAIL ({total_failures} total failure(s))")
            print("=" * 72)
            sys.exit(1)
        else:
            print("=" * 72)
            print("OVERALL: ALL TESTS PASSED")
            print("=" * 72)
            sys.exit(0)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    main()
