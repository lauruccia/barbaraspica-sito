@echo off
chcp 65001 >nul 2>&1
title Pubblica articoli blog
cd /d "%~dp0"

echo.
echo  Pubblica articoli blog
echo  ======================
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo  ERRORE: Python non e' installato.
  echo  Scaricalo da https://www.python.org/downloads/
  pause
  exit /b 1
)

python _tools\build_article.py --all
echo.
python _tools\build_blog_index.py
echo.
python _tools\build_sitemap.py 2>nul
echo.
echo  Fatto. Apri "serve.bat" per vedere l'anteprima.
echo  Per pubblicare online: lancia "carica-online.bat"
echo.
pause
