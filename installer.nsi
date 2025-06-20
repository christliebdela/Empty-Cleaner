; Empty Cleaner Installer Script
; Created for NSIS (Nullsoft Scriptable Install System)

; Define application constants
!define APPNAME "Empty Cleaner"
!define COMPANYNAME "Christlieb Dela"
!define DESCRIPTION "A utility to find and manage empty files and folders"
!define VERSION "1.0.1"
!define VERSIONWITHBUILD "1.0.1.0"
!define INSTALLSIZE 15000
!define REGPATH_UNINSTSUBKEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"

; Include modern UI
!include "MUI2.nsh"
!include "FileFunc.nsh"

; Set compression
SetCompressor /SOLID lzma

; General settings
Name "${APPNAME}"
OutFile "EmptyCleanerSetup.exe"
InstallDir "$PROGRAMFILES\${APPNAME}"
InstallDirRegKey HKLM "Software\${APPNAME}" ""

; Request application privileges for Windows Vista/7/8/10
RequestExecutionLevel admin

; Interface Configuration
!define MUI_ABORTWARNING
!define MUI_ICON "clean.ico"
!define MUI_UNICON "clean.ico"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Languages
!insertmacro MUI_LANGUAGE "English"

; Install section
Section "Install"
    SetOutPath "$INSTDIR"
    
    ; Add files
    File "dist\${APPNAME}.exe"
    File "clean.ico"
    File "LICENSE"
    File "README.md"
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
    
    ; Start Menu
    CreateDirectory "$SMPROGRAMS\${APPNAME}"
    CreateShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\${APPNAME}.exe" "" "$INSTDIR\clean.ico"
    CreateShortCut "$SMPROGRAMS\${APPNAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe"
    
    ; Desktop shortcut
    CreateShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\${APPNAME}.exe" "" "$INSTDIR\clean.ico"
    
    ; Registry information for add/remove programs
    WriteRegStr HKLM "${REGPATH_UNINSTSUBKEY}" "DisplayName" "${APPNAME}"
    WriteRegStr HKLM "${REGPATH_UNINSTSUBKEY}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
    WriteRegStr HKLM "${REGPATH_UNINSTSUBKEY}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
    WriteRegStr HKLM "${REGPATH_UNINSTSUBKEY}" "InstallLocation" "$\"$INSTDIR$\""
    WriteRegStr HKLM "${REGPATH_UNINSTSUBKEY}" "DisplayIcon" "$\"$INSTDIR\clean.ico$\""
    WriteRegStr HKLM "${REGPATH_UNINSTSUBKEY}" "Publisher" "${COMPANYNAME}"
    WriteRegStr HKLM "${REGPATH_UNINSTSUBKEY}" "DisplayVersion" "${VERSION}"
    WriteRegDWORD HKLM "${REGPATH_UNINSTSUBKEY}" "VersionMajor" 1
    WriteRegDWORD HKLM "${REGPATH_UNINSTSUBKEY}" "VersionMinor" 0
    WriteRegDWORD HKLM "${REGPATH_UNINSTSUBKEY}" "NoModify" 1
    WriteRegDWORD HKLM "${REGPATH_UNINSTSUBKEY}" "NoRepair" 1
    
    ; Calculate and write size info
    ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
    IntFmt $0 "0x%08X" $0
    WriteRegDWORD HKLM "${REGPATH_UNINSTSUBKEY}" "EstimatedSize" "$0"
SectionEnd

; Uninstall section
Section "Uninstall"
    ; Remove files and uninstaller
    Delete "$INSTDIR\${APPNAME}.exe"
    Delete "$INSTDIR\clean.ico"
    Delete "$INSTDIR\LICENSE"
    Delete "$INSTDIR\README.md"
    Delete "$INSTDIR\uninstall.exe"
    
    ; Remove directories
    RMDir "$INSTDIR"
    RMDir /r "$SMPROGRAMS\${APPNAME}"
    
    ; Remove desktop shortcut
    Delete "$DESKTOP\${APPNAME}.lnk"
    
    ; Remove registry keys
    DeleteRegKey HKLM "Software\${APPNAME}"
    DeleteRegKey HKLM "${REGPATH_UNINSTSUBKEY}"
SectionEnd
