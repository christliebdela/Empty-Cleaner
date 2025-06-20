# Empty Cleaner - Build and Installer Generator

Write-Host "=============================================="
Write-Host "Empty Cleaner - Build and Installer Generator"
Write-Host "=============================================="
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version
    Write-Host "Found Python: $pythonVersion"
} catch {
    Write-Host "Error: Python is not installed or not in the PATH."
    Write-Host "Please install Python from https://www.python.org/downloads/"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "1. Installing required packages..."
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to install required packages."
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "2. Building executable..."
python build_installer.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Failed to build the executable."
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "3. Checking for NSIS installer..."
try {
    $nsisVersion = & makensis /VERSION
    Write-Host "Found NSIS: $nsisVersion"
    Write-Host "Creating installer..."
    & makensis installer.nsi
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to create the installer."
        Read-Host "Press Enter to exit"
        exit 1
    }
    Write-Host ""
    Write-Host "Installer has been created successfully: EmptyCleanerSetup.exe"
} catch {
    Write-Host "NSIS not found. Cannot create installer automatically."
    Write-Host ""
    Write-Host "To create an installer:"
    Write-Host "1. Download and install NSIS from https://nsis.sourceforge.io/Download"
    Write-Host "2. Run: makensis installer.nsi"
    Write-Host ""
    Write-Host "Executable has been created in the 'dist' folder."
}

Write-Host ""
Write-Host "Build process completed!"
Write-Host ""
Read-Host "Press Enter to exit"
