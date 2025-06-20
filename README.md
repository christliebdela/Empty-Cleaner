# Empty Cleaner

A modern, user-friendly tool  that scans your chosen directory for empty files and folders, and helps you clean them up safely by sending them to the recycle bin.

## Features

- **Scan for Empty Files and Folders**: Find all empty files and folders in the selected directory.
- **Move to Recycle Bin**: Send empty items to the recycle bin with confirmation.
- **Empty Recycle Bin**: Permanently remove all items from your recycle bin.
- **Light/Dark Mode Toggle**: Switch between light and dark themes as per your preference.

## Installation

### Option 1: Using the Standalone Executable (Ready to Use)

1. Download the `EmptyCleaner-Latest.zip` file from the latest release.
2. Extract the ZIP file to a location of your choice.
3. Navigate to the `portable` folder and run `Empty Cleaner.exe` directly.
4. No installation needed - you can copy this executable to any location.

### Option 2: Using the Installer (Recommended)

For a more integrated experience with Start menu shortcuts and proper uninstallation:

1. Download the `EmptyCleaner-Latest.zip` file from the latest release.
2. Extract the ZIP file to a location of your choice.
3. Run the `EmptyCleanerSetup.exe` file from the extracted folder.
4. Follow the installation wizard instructions.
5. Launch the application from your Start menu or desktop shortcut.

### Option 3: Building from Source

If you want to modify and rebuild the application:

1. Make sure you have Python 3.6+ installed on your system.
2. Clone or download this repository.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Build your own executable:

```bash
python build_installer.py
```

5. The new executable will be created in the `dist` folder.

## Usage

Run the application using one of the following methods:

### Option 1: Run the Executable (Recommended)

Simply run the executable that's already been created:

```bash
.\dist\Empty Cleaner.exe
```

### Option 2: Using Command Prompt

```batch
run.bat
```

### Option 3: Using PowerShell

```powershell
.\run.ps1
```

### Option 4: Direct Python execution

```bash
python empty_cleaner.py
```

### How to Use the Application

1. Click the "Browse" button to select a directory to scan.
2. Click "Scan Directory" to find empty items.
3. Review the list of empty files and folders in the tabbed results panel.
4. Click "Move to Recycle Bin" to safely send the items to the recycle bin.
5. Use "Empty Recycle Bin" to permanently delete items in the recycle bin if needed.
6. Use the appearance mode selector to switch between Dark, Light, and System themes.

## Building the Installer

To build the executable and installer yourself:

1. Run the automated build script:

```bash
# On Windows with Command Prompt
build_all.bat

# With PowerShell
.\build_all.ps1
```

2. The script will:
   - Install required dependencies
   - Build the standalone executable using PyInstaller
   - Create an installer if NSIS is installed on your system

3. The executable will be in the `dist` folder, and the installer (if created) will be in the root folder named `EmptyCleanerSetup.exe`.

## Notes

- All deletions are sent to the recycle bin using the send2trash library, making them recoverable unless you empty the bin.
- The application runs on Windows and requires the customtkinter, winshell, and send2trash packages.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
