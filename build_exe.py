#!/usr/bin/env python3
"""
Build script for ES-DE Multi-Disc M3U Generator
Creates standalone executables using PyInstaller (GUI + CLI)
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def get_current_version():
    try:
        import re
        with open("CHANGELOG.md", "r", encoding="utf-8") as f:
            content = f.read()
            version_matches = re.findall(r'## \[([^\]]+)\]', content)
            for version in version_matches:
                if version != "Unreleased":
                    return version
            print("Could not find a valid version in CHANGELOG.md")
            return "v1.1.0"
    except FileNotFoundError:
        print("CHANGELOG.md not found, using fallback version")
        return "v1.1.0"


def build_exe(name, script, windowed=False):
    """Build a single executable. Returns True on success."""
    cmd = [
        "pyinstaller",
        "--onefile",
        f"--name={name}",
        "--icon=NONE",
        script
    ]
    if windowed:
        cmd.insert(2, "--windowed")

    print(f"\nBuilding {name}...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"  Build failed!")
        print(result.stderr)
        return False

    exe_path = Path(f"dist/{name}.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"  {exe_path} ({size_mb:.1f} MB)")
        return True
    else:
        print(f"  Executable not found in dist folder")
        return False


def main():
    print("Building ES-DE Multi-Disc M3U Generator...")

    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller installed")

    # Clean previous builds
    print("Cleaning previous builds...")
    for path in ["build", "dist"]:
        if os.path.exists(path):
            shutil.rmtree(path)

    version = get_current_version()
    print(f"Version: {version}")

    gui_name = f"ESDE_M3U_Generator_{version}"
    cli_name = f"ESDE_M3U_Generator_CLI_{version}"

    gui_ok = build_exe(gui_name, "m3u_generator.py", windowed=True)
    cli_ok = build_exe(cli_name, "m3u_generator_cli.py", windowed=False)

    print("\n--- Results ---")
    print(f"  GUI: {'OK' if gui_ok else 'FAILED'} - {gui_name}.exe")
    print(f"  CLI: {'OK' if cli_ok else 'FAILED'} - {cli_name}.exe")

    if gui_ok and cli_ok:
        print("\nBuild complete! Both executables are in dist/")
        return 0
    else:
        print("\nBuild completed with errors.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
