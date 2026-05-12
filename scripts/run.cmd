@echo off
REM oea-framework-paper — Windows Run
setlocal

set "PROJECT_ROOT=%~dp0.."
set "VENV_DIR=%PROJECT_ROOT%\.venv"

if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found. Run scripts\setup.cmd first.
    exit /b 1
)

call "%VENV_DIR%\Scripts\activate.bat"
oea_framework_paper %*
