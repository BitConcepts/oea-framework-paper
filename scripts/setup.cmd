@echo off
REM oea-framework-paper — Windows Setup
REM
REM Usage:
 REM   setup.cmd                  Core dependencies only (numpy, matplotlib, pytest)
 REM   setup.cmd --experiments    + CPU torch + transformers + rouge-score (for real LLM experiments)
 REM   setup.cmd --experiments --cuda  + CUDA 12.1 torch build
setlocal

set "PROJECT_ROOT=%~dp0.."
set "VENV_DIR=%PROJECT_ROOT%\.venv"
set "EXPERIMENTS=0"
set "CUDA=0"

:parse_args
if "%~1"=="--experiments" ( set "EXPERIMENTS=1" & shift & goto parse_args )
if "%~1"=="--cuda"        ( set "CUDA=1"        & shift & goto parse_args )

echo oea-framework-paper setup (Windows)

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python not found. Install Python 3.10+.
    exit /b 1
)

if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
)

call "%VENV_DIR%\Scripts\activate.bat"

echo Installing core dependencies...
pip install "numpy==1.26.4" matplotlib scipy pytest specsmith

if "%EXPERIMENTS%"=="1" (
    echo Installing neural LLM experiment dependencies...
    if "%CUDA%"=="1" (
        echo   [CUDA 12.1 build]
        pip install torch==2.3.1+cu121 --index-url https://download.pytorch.org/whl/cu121
    ) else (
        echo   [CPU build - use --cuda for GPU acceleration]
        pip install torch==2.3.1 --index-url https://download.pytorch.org/whl/cpu
    )
    pip install transformers==4.41.0 rouge-score==0.1.2
    echo Neural dependencies installed.
    echo.
    echo Run GPT-Neo validation:
    echo   GPU:  python experiments\real_lm_experiment.py --model EleutherAI/gpt-neo-125M
    echo   CPU:  python experiments\real_lm_experiment.py --model EleutherAI/gpt-neo-125M --n-seeds 3 --n-iterations 5 --gen-tokens 40
)

echo Setup complete.
