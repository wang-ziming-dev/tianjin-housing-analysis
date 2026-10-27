@echo off
chcp 65001 >nul
title Jupyter - Data Analysis Project
cd /d "%~dp0"

echo.
echo   ==================================================
echo    Working folder :
echo    %CD%
echo   ==================================================
echo.
echo    A browser tab will open in a few seconds.
echo    KEEP THIS BLACK WINDOW OPEN while you work.
echo    Closing it stops Jupyter.
echo.

where jupyter >nul 2>&1
if errorlevel 1 (
  python -m notebook
) else (
  jupyter notebook
)

echo.
echo   Jupyter has stopped. Press any key to close this window.
pause >nul
