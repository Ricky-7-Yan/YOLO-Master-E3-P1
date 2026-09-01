@echo off
setlocal EnableDelayedExpansion
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "PYTHONPATH=%~dp0src;%~dp0..\YOLO-Master-E3-P0\src"
set "E3_PYTHON=%~dp0..\YOLO-Master-baseline\.venv\Scripts\python.exe"
if not exist "%E3_PYTHON%" (
  echo ERROR: project-local Python not found: "%E3_PYTHON%"
  exit /b 1
)
if not defined E3_P1_EVENTS (
  if not exist "%~dp0..\YOLO-Master-E3-P0\artifacts\p0\LATEST.txt" (
    echo ERROR: sibling P0 LATEST.txt not found.
    exit /b 1
  )
  set /p E3_P0_RUN_ID=<"%~dp0..\YOLO-Master-E3-P0\artifacts\p0\LATEST.txt"
  set "E3_P1_EVENTS=%~dp0..\YOLO-Master-E3-P0\artifacts\p0\!E3_P0_RUN_ID!\routing-all.jsonl"
)
"%E3_PYTHON%" -m e3_p1.dashboard --events "%E3_P1_EVENTS%" --host 127.0.0.1 --port 8765 --refresh-ms 1000 --open
exit /b %ERRORLEVEL%
