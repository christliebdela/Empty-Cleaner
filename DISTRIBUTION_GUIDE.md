# EmptyCleaner Distribution Guide

This directory (`EmptyCleaner-Release`) contains the complete distribution package for Empty Cleaner.

## Directory Structure

- `portable/` - Contains the standalone executable that can be run without installation
- `source/` - Contains the complete source code of the application
- `docs/` - Contains documentation files (README, INSTALL guide, LICENSE)
- `EmptyCleanerSetup.exe` - Windows installer with Start Menu integration
- `installer.nsi` - NSIS installer script used to create the installer
- `INSTALLATION_GUIDE.txt` - Simple text instructions for end users

## How to Use This Distribution

### For End Users

1. **Portable Version:**
   - Navigate to the `portable` folder and run `Empty Cleaner.exe`
   - No installation required
   - Can be copied to any location or USB drive

2. **Installer Version:**
   - Run `EmptyCleanerSetup.exe` in the root of this folder
   - Follow the installation wizard
   - The application will be installed with Start Menu shortcuts
   - Can be uninstalled through Windows Control Panel

### For Developers

1. **Source Code:**
   - The `source` folder contains all the code needed to build the application
   - See `README.md` in the source folder for development instructions

2. **Building a New Installer:**
   - Ensure NSIS is installed ([https://nsis.sourceforge.io/Download](https://nsis.sourceforge.io/Download))
   - Use the `installer.nsi` script to create a new installer
   - Run `makensis installer.nsi` from the command line

## Distribution Tips

1. You can share the entire `EmptyCleaner-Release` folder with users
2. Or create a ZIP file of this folder for easier distribution
3. You can also share just the installer or the portable executable

## Support

For support or to report issues, please refer to the project repository or contact information
in the documentation.
