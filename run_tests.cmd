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
  echo ERROR: sibling P0 repository not found.
  exit /b 1
)
"%E3_PYTHON%" -m pytest tests -q
if errorlevel 1 exit /b %ERRORLEVEL%
"%E3_PYTHON%" -m ruff check .
exit /b %ERRORLEVEL%
