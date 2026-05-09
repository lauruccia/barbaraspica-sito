@echo off
chcp 65001 >nul 2>&1
title Inizializza Git per il sito
cd /d "%~dp0"

echo.
echo  Inizializzazione Git per il sito Barbara Spica
echo  ==============================================
echo.

where git >nul 2>nul
if errorlevel 1 (
  echo  ERRORE: Git non e' installato.
  echo  Scaricalo da https://git-scm.com/download/win
  pause
  exit /b 1
)

if exist ".git\" (
  echo  Git e' gia' inizializzato in questa cartella.
  echo  Per ri-inizializzare elimina la cartella .git e riprova.
  pause
  exit /b 0
)

echo.
echo  Step 1/6: git init
git init

echo.
echo  Step 2/6: configurazione utente
git config user.name "Laura"
git config user.email "gruppokosmos00@gmail.com"

echo.
echo  Step 3/6: aggiungo remote GitHub
git remote add origin https://github.com/lauruccia/barbaraspica-sito.git

echo.
echo  Step 4/6: imposto branch main
git branch -M main

echo.
echo  Step 5/6: aggiungo i file
git add .

echo.
echo  Step 6/6: primo commit
git commit -m "feat: sito vetrina iniziale"

echo.
echo  ==============================================
echo   Repository pronto.
echo  ==============================================
echo.
echo  PROSSIMO PASSO: per pubblicare su GitHub esegui:
echo.
echo      git push -u origin main
echo.
echo  Ti chiedera' username (lauruccia) e Personal Access Token come password.
echo  Crea il token su: https://github.com/settings/tokens (scope: repo)
echo.
pause
