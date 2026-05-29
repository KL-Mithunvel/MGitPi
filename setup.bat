@echo off
setlocal enabledelayedexpansion
title MGitPi Setup — Windows

echo.
echo ============================================================
echo         MGitPi Setup — Windows Edition
echo ============================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "SECRETS_DIR=%SCRIPT_DIR%secrets"
set "SECRETS_FILE=%SECRETS_DIR%\credentials.env"
set "EXAMPLE_FILE=%SCRIPT_DIR%secrets.example\credentials.env"

:: ── 1. Python ────────────────────────────────────────────────────────────────
echo [INFO] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ ERR] Python not found. Download Python 3.10+ from https://python.org
    pause & exit /b 1
)
for /f "tokens=2" %%v in ('python --version 2^>^&1') do set PY_VER=%%v
echo [ OK ] Python %PY_VER%

:: ── 2. Git ───────────────────────────────────────────────────────────────────
echo [INFO] Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo [ ERR] Git not found. Download from https://git-scm.com
    pause & exit /b 1
)
for /f "tokens=3" %%v in ('git --version') do set GIT_VER=%%v
echo [ OK ] Git %GIT_VER%

:: ── 3. Dev dependencies ──────────────────────────────────────────────────────
echo [INFO] Installing pytest...
python -m pip install -r "%SCRIPT_DIR%requirements-dev.txt" -q
if errorlevel 1 (
    echo [WARN] Could not install pytest ^(non-fatal^)
) else (
    echo [ OK ] pytest installed
)

:: ── 4. MGitPi data directory ─────────────────────────────────────────────────
if not exist "%USERPROFILE%\.mgitpi" mkdir "%USERPROFILE%\.mgitpi"
echo [ OK ] Data directory: %USERPROFILE%\.mgitpi

:: ── 5. Credentials ───────────────────────────────────────────────────────────
if not exist "%SECRETS_FILE%" (
    echo [WARN] No credentials file found.
    if not exist "%SECRETS_DIR%" mkdir "%SECRETS_DIR%"
    copy "%EXAMPLE_FILE%" "%SECRETS_FILE%" >nul
    echo [INFO] Template copied to secrets\credentials.env
    echo        Edit it with your SSH details, then re-run setup.bat
    pause & exit /b 0
)

:: Load key=value pairs from credentials.env (skip comments and blanks)
for /f "usebackq tokens=1,* delims==" %%a in ("%SECRETS_FILE%") do (
    set "LINE=%%a"
    if not "!LINE:~0,1!" == "#" (
        if not "%%a" == "" set "%%a=%%b"
    )
)
echo [ OK ] Credentials loaded

:: ── 6. SSH key ───────────────────────────────────────────────────────────────
echo [INFO] Setting up SSH...
if not exist "%USERPROFILE%\.ssh" mkdir "%USERPROFILE%\.ssh"

:: Copy key from secrets/ if present
if exist "%SECRETS_DIR%\id_ed25519" (
    copy /y "%SECRETS_DIR%\id_ed25519"     "%USERPROFILE%\.ssh\id_ed25519"     >nul
    if exist "%SECRETS_DIR%\id_ed25519.pub" (
        copy /y "%SECRETS_DIR%\id_ed25519.pub" "%USERPROFILE%\.ssh\id_ed25519.pub" >nul
    )
    echo [ OK ] SSH key installed to %%USERPROFILE%%\.ssh\
)

:: Generate key if still missing (requires Git Bash's ssh-keygen in PATH)
set "KEY_PATH=%USERPROFILE%\.ssh\id_ed25519"
if not exist "%KEY_PATH%" (
    echo [INFO] Generating new SSH key...
    set "EMAIL=%GITHUB_USERNAME%@mgitpi"
    if defined SSH_PASSPHRASE (
        ssh-keygen -t ed25519 -C "%EMAIL%" -f "%KEY_PATH%" -N "%SSH_PASSPHRASE%" -q
    ) else (
        ssh-keygen -t ed25519 -C "%EMAIL%" -f "%KEY_PATH%" -N "" -q
    )
    echo [ OK ] SSH key generated: %KEY_PATH%
    echo.
    echo [INFO] Add this public key to GitHub ^(Settings ^> SSH Keys^):
    type "%KEY_PATH%.pub"
    echo.
    pause
)
echo [ OK ] SSH key: %KEY_PATH%

:: ── 7. Start ssh-agent and add key ───────────────────────────────────────────
echo [INFO] Starting ssh-agent...
for /f "tokens=*" %%i in ('ssh-agent -s 2^>nul') do (
    set "AGENT_LINE=%%i"
    if "!AGENT_LINE:~0,12!" == "SSH_AUTH_SOCK" (
        for /f "tokens=1,2 delims==;" %%a in ("!AGENT_LINE!") do set "%%a=%%b"
    )
    if "!AGENT_LINE:~0,12!" == "SSH_AGENT_PI" (
        for /f "tokens=1,2 delims==;" %%a in ("!AGENT_LINE!") do set "%%a=%%b"
    )
)
ssh-add "%KEY_PATH%" >nul 2>&1
echo [ OK ] Key loaded into ssh-agent

:: ── 8. Test SSH connection ────────────────────────────────────────────────────
set "HOST=%GITHUB_HOST%"
if "%HOST%"=="" set "HOST=github.com"
echo [INFO] Testing SSH connection to %HOST%...
ssh -T git@%HOST% -o StrictHostKeyChecking=no -o ConnectTimeout=8 -o BatchMode=yes 2>&1 | findstr /i "success Hi welcome" >nul
if %errorlevel% == 0 (
    echo [ OK ] SSH connection to %HOST% — authenticated
) else (
    echo [WARN] SSH test inconclusive — ensure your public key is added to %HOST%
)

:: ── Done ─────────────────────────────────────────────────────────────────────
echo.
echo ============================================================
echo   Setup complete!
echo   Run the app : python main.py
echo   Run tests   : python -m pytest tests\ -v
echo ============================================================
echo.
pause
endlocal
