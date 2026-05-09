@echo off
chcp 65001 >nul 2>&1
title Nuovo articolo blog
cd /d "%~dp0"

echo.
echo  Nuovo articolo blog
echo  ===================
echo.

set /p NOMEFILE=Nome file (es. autismo-segnali-precoci): 

if "%NOMEFILE%"=="" (
  echo  Annullato.
  pause
  exit /b
)

set FILEPATH=_articles\%NOMEFILE%.md

if exist "%FILEPATH%" (
  echo.
  echo  ATTENZIONE: il file %FILEPATH% esiste gia'.
  set /p OVER=Sovrascrivere [s/N]? 
  if /i not "%OVER%"=="s" exit /b
)

copy /Y "_articles\_TEMPLATE.md" "%FILEPATH%" >nul

echo.
echo  Creato: %FILEPATH%
echo.
echo  Apro l'editor (Notepad)...
start "" notepad "%FILEPATH%"
echo.
echo  Quando hai finito di scrivere e SALVATO il file (Ctrl+S),
echo  lancia "pubblica-articoli.bat" per generare l'HTML.
echo.
pause
