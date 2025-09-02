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

def run_script(script_path):
    print(f"Rularea scriptului: {script_path}")
    try:
        # Verifică existența scriptului
        if not os.path.isfile(script_path):
            print(f"Scriptul {script_path} nu există.")
            return
        
        result = subprocess.run(['python', script_path], check=True, capture_output=True, text=True)
        with open('script_output.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"Script rulat cu succes: {os.path.basename(script_path)}\n")
            log_file.write(f"Output:\n{result.stdout}\n")
            log_file.write(f"Errors:\n{result.stderr}\n")
        print(f"Scriptul {os.path.basename(script_path)} a fost rulat cu succes.")
    except subprocess.CalledProcessError as e:
        with open('script_output.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"Eroare la rularea scriptului {os.path.basename(script_path)}: {e}\n")
            log_file.write(f"Output:\n{e.stdout}\n")
            log_file.write(f"Errors:\n{e.stderr}\n")
        print(f"Eroare la rularea scriptului {os.path.basename(script_path)}. Verifică script_output.log pentru detalii.")
    except Exception as e:
        with open('script_output.log', 'a', encoding='utf-8') as log_file:
            log_file.write(f"Eroare neașteptată la rularea scriptului {os.path.basename(script_path)}: {e}\n")
        print(f"Eroare neașteptată la rularea scriptului {os.path.basename(script_path)}. Verifică script_output.log pentru detalii.")

def main():
    for script in scripts:
        run_script(script)

    print("Toate fișierele py au fost rulate și finalizate.")
    input("Apăsați Enter pentru a închide această fereastră...")

if __name__ == "__main__":
    main()
