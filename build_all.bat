@echo off
echo ==============================================
echo Empty Cleaner - Build and Installer Generator
echo ==============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python is not installed or not in the PATH.
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)
echo Found Python:
python --version

echo.
echo 1. Installing required packages...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to install required packages.
    pause
    exit /b 1
)

echo.
echo 2. Building executable...
python build_installer.py
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to build the executable.
    pause
    exit /b 1
)

echo.
echo 3. Checking for NSIS installer...
makensis /VERSION >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo Found NSIS
    echo Creating installer...
    makensis installer.nsi
    if %ERRORLEVEL% neq 0 (
        echo Error: Failed to create the installer.
        pause
        exit /b 1
    )
    echo.
    echo Installer has been created successfully: EmptyCleanerSetup.exe
) else (
    echo NSIS not found. Cannot create installer automatically.
    echo.
    echo To create an installer:
    echo 1. Download and install NSIS from https://nsis.sourceforge.io/Download
    echo 2. Run: makensis installer.nsi
    echo.
    echo Executable has been created in the 'dist' folder.
)

echo.
echo Build process completed!
echo.
pause
