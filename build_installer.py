import os
import sys
import shutil
import subprocess
from pathlib import Path

# Application info
APP_NAME = "Empty Cleaner"
APP_VERSION = "1.0.1"
MAIN_SCRIPT = "empty_cleaner.py"
ICON_FILE = "clean.ico"

# Get the current directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure the icon file exists
icon_path = os.path.join(base_dir, ICON_FILE)
if not os.path.exists(icon_path):
    print(f"Error: Icon file {ICON_FILE} not found in {base_dir}")
    sys.exit(1)

# Create dist directory if it doesn't exist
dist_dir = os.path.join(base_dir, "dist")
if not os.path.exists(dist_dir):
    os.makedirs(dist_dir)

# Create build directory if it doesn't exist
build_dir = os.path.join(base_dir, "build")
if not os.path.exists(build_dir):
    os.makedirs(build_dir)

# Build command
cmd = [
    "pyinstaller",
    "--name", APP_NAME,
    "--icon", icon_path,
    "--windowed",  # No console window
    "--onefile",   # Single executable file
    "--clean",     # Clean cache before building
    "--add-data", f"{icon_path};.",  # Include the icon file
    os.path.join(base_dir, MAIN_SCRIPT)
]

print("Building executable...")
print(f"Command: {' '.join(cmd)}")

try:
    # Run PyInstaller
    result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    print("Build completed successfully!")
    
    # Location of the executable
    exe_path = os.path.join(dist_dir, f"{APP_NAME}.exe")
    
    if os.path.exists(exe_path):
        print(f"Executable created at: {exe_path}")
    else:
        print(f"Error: Expected executable not found at {exe_path}")
        
except subprocess.CalledProcessError as e:
    print(f"Build failed with error code {e.returncode}")
    print(f"Error output: {e.stderr}")
    sys.exit(1)
