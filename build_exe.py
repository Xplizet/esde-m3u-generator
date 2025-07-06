#!/usr/bin/env python3
"""
Build script for ES-DE Multi-Disc M3U Generator
Creates a standalone executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("Building ES-DE Multi-Disc M3U Generator executable...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"✓ PyInstaller {PyInstaller.__version__} found")
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✓ PyInstaller installed")
    
    # Clean previous builds
    print("Cleaning previous builds...")
    for path in ["build", "dist"]:
        if os.path.exists(path):
            shutil.rmtree(path)
    
    # Extract current version from CHANGELOG.md
    def get_current_version():
        try:
            with open("CHANGELOG.md", "r", encoding="utf-8") as f:
                content = f.read()
                # Find all version entries and get the first non-Unreleased one
                import re
                version_matches = re.findall(r'## \[([^\]]+)\]', content)
                for version in version_matches:
                    if version != "Unreleased":
                        return version
                print("❌ Could not find a valid version in CHANGELOG.md")
                return "v1.1.0"  # Fallback version
        except FileNotFoundError:
            print("❌ CHANGELOG.md not found, using fallback version")
            return "v1.1.0"  # Fallback version
    
    # Build the executable
    print("Building executable...")
    version = get_current_version()
    print(f"✓ Building version: {version}")
    exe_name = f"ESDE_M3U_Generator_{version}"
    
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        f"--name={exe_name}",           # Executable name with version
        "--icon=NONE",                  # No icon for now
        "m3u_generator.py"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Build successful!")
        
        # Check if executable was created
        exe_path = Path(f"dist/{exe_name}.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"✓ Executable created: {exe_path}")
            print(f"✓ Size: {size_mb:.1f} MB")
            print(f"✓ Location: {exe_path.absolute()}")
        else:
            print("❌ Executable not found in dist folder")
            return 1
    else:
        print("❌ Build failed!")
        print("Error output:")
        print(result.stderr)
        return 1
    
    print("\n🎉 Build complete! The executable is ready for distribution.")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 