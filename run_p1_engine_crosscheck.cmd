@echo off
setlocal
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "PYTHONPATH=%~dp0src;%~dp0..\YOLO-Master-E3-P0\src"
set "E3_PYTHON=%~dp0..\YOLO-Master-baseline\.venv\Scripts\python.exe"
if not exist "%E3_PYTHON%" (
  echo ERROR: project-local Python not found: "%E3_PYTHON%"
  exit /b 1
)
if not exist "%~dp0..\YOLO-Master-E3-P0\src\e3_p0" (
  echo ERROR: sibling P0 repository not found: "%~dp0..\YOLO-Master-E3-P0"
  exit /b 1
)
if not defined E3_P1_RUN_ID (
  for /f %%I in ('powershell -NoProfile -Command "Get-Date -Format yyyyMMdd-HHmmss-fff"') do set "E3_P1_RUN_ID=repro-engine-%%I"
)
echo P1 engine cross-check run id: %E3_P1_RUN_ID%
"%E3_PYTHON%" -m e3_p1.engine_crosscheck --config "%~dp0configs\p1_engine_crosscheck.yaml" --run-id "%E3_P1_RUN_ID%" --no-update-latest
exit /b %ERRORLEVEL%
