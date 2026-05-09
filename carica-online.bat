@echo off
chcp 65001 >nul 2>&1
title Carica online (GitHub)
cd /d "%~dp0"

echo.
echo  Carica le modifiche su GitHub
echo  =============================
echo.

where git >nul 2>nul
if errorlevel 1 (
  echo  ERRORE: Git non e' installato.
  echo  Scaricalo da https://git-scm.com/download/win
  pause
  exit /b 1
)

where python >nul 2>nul
if not errorlevel 1 (
  echo  Rigenero gli articoli...
  python _tools\build_article.py --all 2>nul
  python _tools\build_blog_index.py 2>nul
  python _tools\build_sitemap.py 2>nul
  echo.
)

set /p MSG=Descrivi in 1 frase cosa hai cambiato (poi INVIO): 
if "%MSG%"=="" set MSG=Aggiornamento contenuti

git add .
git commit -m "%MSG%"
git push origin main

echo.
echo  Modifiche caricate.
echo  Ora vai su cPanel - Git Version Control - Update from Remote - Deploy HEAD Commit
echo.
pause
