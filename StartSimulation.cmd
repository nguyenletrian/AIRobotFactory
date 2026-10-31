@echo off
setlocal
cd /d "%~dp0"
rem Simulation-only bootstrap: no administrator rights, device I/O or Bridge mutation.
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" "scripts\bootstrap.py" %*
  goto result
)
where py >nul 2>nul
if not errorlevel 1 (
  py -3.12 -c "import sys; assert sys.maxsize>2**32" >nul 2>nul
  if not errorlevel 1 (
    py -3.12 "scripts\bootstrap.py" %*
    goto result
  )
  py -3 -c "import sys; assert (3,10)<=sys.version_info[:2]<(3,14) and sys.maxsize>2**32" >nul 2>nul
  if not errorlevel 1 (
    py -3 "scripts\bootstrap.py" %*
    goto result
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
