@echo off
chcp 65001 >nul
echo ========================================
echo   Multimodal-Viz EXE Build Script
echo ========================================
echo.

REM Check PyInstaller
where pyinstaller >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] pyinstaller not found. Run: pip install pyinstaller
    pause
    exit /b 1
)

echo [1/3] Cleaning previous build...
if exist build rmdir /s /q build
if exist dist\multimodal-viz rmdir /s /q dist\multimodal-viz

echo [2/3] Building EXE with PyInstaller...
pyinstaller --clean multimodal-viz.spec
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo [3/3] Copying support files...
copy .env.example dist\multimodal-viz\ >nul 2>&1
copy README.txt dist\multimodal-viz\ >nul 2>&1

echo.
echo ========================================
echo   Build complete!
echo   Output: dist\multimodal-viz\
echo ========================================
echo.
echo Files to distribute:
dir /b dist\multimodal-viz\
echo.
echo Zip the folder and share!
pause
