@echo off
REM oea-framework-paper - bootstrap (Windows)
REM Usage: scripts\setup.cmd [--experiments]
REM   --experiments  also install torch + transformers for real_lm_experiment.py
setlocal

set "PROJECT_ROOT=%~dp0.."
set "VENV_DIR=%PROJECT_ROOT%\.venv"
set WITH_EXPERIMENTS=0
for %%A in (%*) do if /I "%%A"=="--experiments" set WITH_EXPERIMENTS=1

echo oea-framework-paper setup (Windows)

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python 3.10+ not found. Download from https://python.org
    exit /b 1
)

if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
)

call "%VENV_DIR%\Scripts\activate.bat"

echo Installing core dependencies...
python -m pip install --upgrade pip -q
python -m pip install -r "%PROJECT_ROOT%\requirements.txt" -q
python -m pip install pytest -q

if "%WITH_EXPERIMENTS%"=="1" (
    echo Installing experiment dependencies ^(requires ~2 GB: torch + transformers^)...
    python -m pip install -r "%PROJECT_ROOT%\requirements-experiments.txt" --extra-index-url https://download.pytorch.org/whl/cpu -q
    echo Experiment dependencies installed.
)

echo.
echo Setup complete. Environment active in this shell.
echo.
echo Run experiments:
echo   scripts\run-experiments.cmd              ^(pilot + credibility suite^)
echo   scripts\run-experiments.cmd --all        ^(includes real LLM, ~3 min^)
echo   python experiments\real_lm_experiment.py ^(real LLM only^)
