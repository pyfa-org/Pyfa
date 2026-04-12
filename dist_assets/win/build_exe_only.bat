@echo off
REM Lightweight Windows build: produces dist\pyfa\pyfa.exe (no Inno Setup installer).
REM Requires: Python 3.11 x64 on PATH, run from repo root OR double-click from Explorer.
REM Optional: Windows 10 SDK UCRT path in pyfa.spec pathex; CROWDIN_API_KEY for progress.json.

setlocal
pushd "%~dp0..\.."

echo === pyfa: install deps + PyInstaller ===
python -m pip install -r requirements.txt
if errorlevel 1 goto :fail
python -m pip install "PyInstaller==6.0.0"
if errorlevel 1 goto :fail

echo === compile_lang ===
python scripts\compile_lang.py
if errorlevel 1 goto :fail

if defined CROWDIN_API_KEY (
  echo === dump_crowdin_progress ===
  python scripts\dump_crowdin_progress.py
  if errorlevel 1 goto :fail
) else (
  echo === skip dump_crowdin_progress (set CROWDIN_API_KEY to update locale\progress.json^) ===
)

echo === db_update ===
python db_update.py
if errorlevel 1 goto :fail

echo === PyInstaller ===
python -m PyInstaller --clean -y pyfa.spec
if errorlevel 1 goto :fail

if exist "dist\pyfa\pyfa.exe" (
  copy /y "dist_assets\win\pyfa.exe.manifest" "dist\pyfa\pyfa.exe.manifest" >nul
)

echo.
echo Build OK. Run:  dist\pyfa\pyfa.exe
popd
endlocal
exit /b 0

:fail
echo Build failed.
popd
endlocal
exit /b 1
