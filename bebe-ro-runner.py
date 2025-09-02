import subprocess
import os

# Lista de scripturi de rulat
scripts = [
    r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 18\Parsing WEBSITE - FINAL.py",    
    r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 4 internet\replace_nbsp_cu_un_singur_spatiu_in_tagurile.py",    
    r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 4 internet\Sterge spatiile goale duble din tagurile (varianta FINALA).py",    
    r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 9 (2022) (EMAIL)\BEBE-PARSING-Python (FARA SUBFOLDER).py",    
    r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\Schimba tagurile p class text obisnuit2 in H2 si H3.py",
    r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\inlocuieste-fisiere-gata-design-categorii.py"
    r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\Inlocuieste fiecare icon-facebook jpg cu imaginea nou creata.py" 

]

# Directorul Python
pythonw_path = r"c:\Users\necul\AppData\Local\Programs\Python\Python312\pythonw.exe"

# Fișierul jurnal
log_file_path = r"log.txt"

with open(log_file_path, "w", encoding="utf-8") as log_file:
    for script in scripts:
        try:
            result = subprocess.run([pythonw_path, script], capture_output=True, text=True)
            log_file.write(f"Script: {script}\n")
            log_file.write(f"Return Code: {result.returncode}\n")
            log_file.write(f"Output: {result.stdout}\n")
            log_file.write(f"Errors: {result.stderr}\n")
            log_file.write("-" * 80 + "\n")
            if result.returncode != 0:
                print(f"Script {script} a întâmpinat o eroare. Verificați jurnalul pentru detalii.")
        except Exception as e:
            log_file.write(f"Script: {script}\n")
            log_file.write(f"Exception: {str(e)}\n")
            log_file.write("-" * 80 + "\n")
            print(f"Eroare la rularea scriptului {script}. Verificați jurnalul pentru detalii.")

print("Toate fișierele py au fost rulate și finalizate.")
