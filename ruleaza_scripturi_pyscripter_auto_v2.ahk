#Requires AutoHotkey v2.0

SetWorkingDir A_ScriptDir
SetTitleMatchMode 2
SetWinDelay 100

; Calea către PyScripter
PyScripterPath := "c:\Program Files\PyScripter\PyScripter.exe"

; Lista de scripturi de rulat
scripts := [
    "e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 18\Parsing WEBSITE - FINAL.py",
    "e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 4 internet\replace_nbsp_cu_un_singur_spatiu_in_tagurile.py",
    "e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 4 internet\Sterge spatiile goale duble din tagurile (varianta FINALA).py",
    "e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 9 (2022) (EMAIL)\BEBE-PARSING-Python (FARA SUBFOLDER).py",
    "e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\Schimba tagurile p class text obisnuit2 in H2 si H3.py",
    "e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\Inlocuieste fiecare icon-facebook jpg cu imaginea nou creata.py",
    "e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\inlocuieste-fisiere-gata-design-categorii.py"
]

; Funcție pentru a verifica și activa fereastra PyScripter
ActivatePyScripterWindow(fileName) {
    if WinExist("ahk_exe PyScripter.exe") {
        WinActivate
        WinWaitActive "ahk_exe PyScripter.exe",, 2
        return true
    }
    return false
}

; Deschide toate scripturile
for script in scripts {
    Run PyScripterPath ' "' script '"'
    Sleep 2000  ; Așteaptă mai mult între deschideri
}

; Așteaptă ca toate ferestrele să se deschidă
Sleep 10000

; Rulează scripturile
for script in scripts {
    SplitPath script, &fileName
    if ActivatePyScripterWindow(fileName) {
        ; Încearcă să ruleze scriptul
        Send "^{F9}"  ; Ctrl+F9
        Sleep 1000
        
        ; Verifică dacă scriptul a început să ruleze
        if WinExist("ahk_exe PyScripter.exe") {
            windowText := WinGetText("ahk_exe PyScripter.exe")
            if InStr(windowText, "Running script") {
                MsgBox "Scriptul " fileName " a început să ruleze."
            } else {
                MsgBox "Nu s-a putut confirma rularea scriptului " fileName ". Verificați manual."
            }
        }
        
        Sleep 2000  ; Așteaptă între rulări
    } else {
        MsgBox "Nu s-a putut activa fereastra PyScripter pentru " fileName ". Verificați dacă scriptul s-a deschis corect."
    }
}

MsgBox "Procesul de deschidere și încercare de rulare a scripturilor s-a încheiat. Verificați PyScripter pentru rezultate."