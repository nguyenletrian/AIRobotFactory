@echo off
setlocal
cd /d "%~dp0"
rem Isolated simulation-only setup: does not connect to motors, printers or Bridge.
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" "scripts\bootstrap.py" %*
  goto result
)
where py >nul 2>nul
if not errorlevel 1 (
  rem Prefer Python 3.12 but handle systems with 3.13 or 3.14 as the global default.
  for %%V in (3.12 3.13 3.11 3.10) do (
    py -%%V -c "import sys; assert sys.maxsize>2**32" >nul 2>nul
    if not errorlevel 1 (
      py -%%V "scripts\bootstrap.py" %*
      goto result
    )
  )
)
where python >nul 2>nul
if errorlevel 1 goto missing
python "scripts\bootstrap.py" %*
goto result
:missing
echo [AIRobotFactory] Python 3.10-3.13 64-bit missing. Install Python 3.12 and rerun.
pause
exit /b 1
:result
if errorlevel 1 (
  echo [AIRobotFactory] Setup FAILED; see the error above.
  pause
  exit /b 1
)
echo [AIRobotFactory] Simulation ready.
exit /b 0
