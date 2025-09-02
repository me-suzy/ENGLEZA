@echo off
setlocal enabledelayedexpansion

echo Pornirea scripturilor Python...

set PYTHON_PATH=c:\Users\necul\AppData\Local\Programs\Python\Python312\pythonw.exe
set LOG_FILE=errors.log

if exist %LOG_FILE% del %LOG_FILE%

set SCRIPTS[0]=e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 18\ENGLEZA\Parsing WEBSITE - EN.py
set SCRIPTS[1]=e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 4 internet\replace_nbsp_cu_un_singur_spatiu_in_tagurile.py
set SCRIPTS[2]=e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 4 internet\Sterge spatiile goale duble din tagurile (varianta FINALA).py
set SCRIPTS[3]=e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 9 (2022) (EMAIL)\BEBE-PARSING-Python (FARA SUBFOLDER).py
set SCRIPTS[4]=e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\Schimba tagurile p class text obisnuit2 in H2 si H3.py
set SCRIPTS[5]=e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\inlocuieste-fisiere-gata-design-categorii.py
set SCRIPTS[6]=e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\Inlocuieste fiecare icon-facebook jpg cu imaginea nou creata.py

set /a count=0
set /a total=7
set /a errors=0

for /L %%i in (0,1,6) do (
    echo Rulare script !count! din %total%: !SCRIPTS[%%i]!
    %PYTHON_PATH% "!SCRIPTS[%%i]!" 2>> %LOG_FILE%
    if !ERRORLEVEL! NEQ 0 (
        echo Eroare la rularea scriptului !SCRIPTS[%%i]! >> %LOG_FILE%
        echo Eroare la rularea scriptului !SCRIPTS[%%i]!
        set /a errors+=1
    ) else (
        echo Script finalizat cu succes: !SCRIPTS[%%i]!
    )
    set /a count+=1
)

echo.
echo Toate scripturile au fost rulate.
echo Total scripturi: %total%
echo Scripturi cu erori: %errors%
echo Scripturi rulate cu succes: %count%

if %errors% GTR 0 (
    echo ATENȚIE: Au apărut erori la rularea unor scripturi! Verificați %LOG_FILE% pentru detalii.
) else (
    echo Toate scripturile au rulat cu succes!
)

echo.
echo Testare separată a ultimelor două scripturi:
%PYTHON_PATH% "!SCRIPTS[5]!" 2>> %LOG_FILE%
if !ERRORLEVEL! NEQ 0 (
    echo Eroare la rularea separată a scriptului !SCRIPTS[5]! >> %LOG_FILE%
    echo Eroare la rularea separată a scriptului !SCRIPTS[5]!
) else (
    echo Script !SCRIPTS[5]! rulat separat cu succes.
)

%PYTHON_PATH% "!SCRIPTS[6]!" 2>> %LOG_FILE%
if !ERRORLEVEL! NEQ 0 (
    echo Eroare la rularea separată a scriptului !SCRIPTS[6]! >> %LOG_FILE%
    echo Eroare la rularea separată a scriptului !SCRIPTS[6]!
) else (
    echo Script !SCRIPTS[6]! rulat separat cu succes.
)

pause
