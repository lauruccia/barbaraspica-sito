@echo off
chcp 65001 >nul 2>&1
title Anteprima sito Barbara Spica
cd /d "%~dp0"

echo.
echo  Sito Barbara Spica - Anteprima locale
echo  =====================================
echo.
echo  Apertura browser su http://localhost:8000
echo  (premi CTRL+C per fermare il server)
echo.

where php >nul 2>nul
if not errorlevel 1 (
  start "" http://localhost:8000
  php -S localhost:8000 -t "%~dp0"
  goto :end
)

where python >nul 2>nul
if not errorlevel 1 (
  start "" http://localhost:8000
  python -m http.server 8000
  goto :end
)

where npx >nul 2>nul
if not errorlevel 1 (
  start "" http://localhost:8000
  npx --yes serve -l 8000 .
  goto :end
)

echo.
echo  ERRORE: nessuno tra PHP, Python o Node e' installato.
echo  Installa PHP da https://windows.php.net/download
echo  oppure Python da https://www.python.org/downloads/
echo.
pause
:end
