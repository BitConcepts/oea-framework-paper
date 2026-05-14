@echo off
REM Build the arXiv manuscript PDF
REM Requires MiKTeX or TeX Live with pdflatex and bibtex
setlocal

set "ARXIV_DIR=%~dp0..\arxiv"
pushd "%ARXIV_DIR%"

echo [1/4] pdflatex (pass 1)...
pdflatex -interaction=nonstopmode main.tex >nul 2>&1

echo [2/4] bibtex...
bibtex main >nul 2>&1

echo [3/4] pdflatex (pass 2)...
pdflatex -interaction=nonstopmode main.tex >nul 2>&1

echo [4/4] pdflatex (pass 3)...
pdflatex -interaction=nonstopmode main.tex >nul 2>&1

echo.
echo Done. Output: arxiv\main.pdf
popd
