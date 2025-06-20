# Empty Cleaner

A modern, user-friendly tool  that scans your chosen directory for empty files and folders, and helps you clean them up safely by sending them to the recycle bin.

## Features

- **Scan for Empty Files and Folders**: Find all empty files and folders in the selected directory.
- **Move to Recycle Bin**: Send empty items to the recycle bin with confirmation.
- **Empty Recycle Bin**: Permanently remove all items from your recycle bin.
- **Light/Dark Mode Toggle**: Switch between light and dark themes as per your preference.

## Installation

1. Make sure you have Python 3.6+ installed on your system.
2. Clone or download this repository.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

Alternatively, use the included setup.bat file on Windows:

```batch
setup.bat
```

## Usage

Run the application using one of the following methods:

### Using Command Prompt

```batch
run.bat
```

### Using PowerShell

```powershell
.\run.ps1
```

### Direct Python execution

```bash
python empty_cleaner.py
```

### Steps to use

1. Click the "Browse" button to select a directory to scan.
2. Click "Scan Directory" to find empty items.
3. Review the list of empty files and folders in the tabbed results panel.
4. Click "Move to Recycle Bin" to safely send the items to the recycle bin.
5. Use "Empty Recycle Bin" to permanently delete items in the recycle bin if needed.
6. Use the appearance mode selector to switch between Dark, Light, and System themes.

## Notes

- All deletions are sent to the recycle bin using the send2trash library, making them recoverable unless you empty the bin.
- The application runs on Windows and requires the customtkinter, winshell, and send2trash packages.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
