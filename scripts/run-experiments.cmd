@echo off
REM oea-framework-paper - run experiments (Windows)
REM Usage: scripts\run-experiments.cmd [--all]
REM   --all  also run real LLM experiment (requires --experiments setup, ~3 min)
setlocal

set "PROJECT_ROOT=%~dp0.."
set RUN_ALL=0
for %%A in (%*) do if /I "%%A"=="--all" set RUN_ALL=1

set "VENV=%PROJECT_ROOT%\.venv"
if exist "%VENV%\Scripts\activate.bat" call "%VENV%\Scripts\activate.bat"

cd /d "%PROJECT_ROOT%"

echo === [1/3] Pilot experiment (run_experiments.py) ===
python experiments\run_experiments.py
if %ERRORLEVEL% neq 0 ( echo FAILED & exit /b 1 )
echo Pilot done. Results in results\

echo.
echo === [2/3] Credibility suite - fast validation ===
python -c "from experiments.credibility_suite import load_plan, run_suite; from pathlib import Path; plan = load_plan(Path('experiments/config/credibility_plan_fast.json')); run_suite(plan); print('Fast credibility suite done.')"
if %ERRORLEVEL% neq 0 ( echo FAILED & exit /b 1 )

echo.
if "%RUN_ALL%"=="1" (
    echo === [3/3] Real LLM experiment ^(distilgpt2, ~3 min^) ===
    python experiments\real_lm_experiment.py
    if %ERRORLEVEL% neq 0 ( echo FAILED & exit /b 1 )
    echo Real LLM done. Results in results\real_lm\
) else (
    echo === [3/3] Real LLM experiment - SKIPPED ^(pass --all to enable^) ===
)

echo.
echo All experiments complete.
echo Results:
echo   results\recursive_stability_runs.csv
echo   results\epistemic_friction_runs.csv
echo   results\summary_metrics.json
echo   results\credibility\  ^(full credibility suite - run manually^)
echo   results\real_lm\      ^(real LLM - if --all was used^)
