import concurrent.futures
import subprocess
import os
import shutil

def overwrite_html_files():
    source_folder = r"c:\Folder1\fisiere_html"
    destination_folder = r"c:\Folder1\fisiere_gata"

    if not os.path.exists(source_folder):
        print(f"Source folder {source_folder} does not exist.")
        return

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for filename in os.listdir(source_folder):
        if filename.endswith(".html"):
            source_file = os.path.join(source_folder, filename)
            destination_file = os.path.join(destination_folder, filename)
            shutil.copy2(source_file, destination_file)
            print(f"Copied {filename} to {destination_folder}")

def run_script(script_path):
    try:
        result = subprocess.run(["python", script_path], capture_output=True, text=True, check=True)
        print(f"Script {os.path.basename(script_path)} executed successfully.")
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing {os.path.basename(script_path)}:")
        print(e.stderr)
        return False

if __name__ == "__main__":
    print("Overwriting HTML files...")
    overwrite_html_files()
    print("HTML files overwritten.")

    script_paths = [
        r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 18\Parsing WEBSITE - FINAL.py",
        r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 4 internet\replace_nbsp_cu_un_singur_spatiu_in_tagurile.py",
        r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 4 internet\Sterge spatiile goale duble din tagurile (varianta FINALA).py",
        r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\Sedinta 9 (2022) (EMAIL)\BEBE-PARSING-Python (FARA SUBFOLDER).py",
        r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\Schimba tagurile p class text obisnuit2 in H2 si H3.py",
        r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\inlocuieste-fisiere-gata-design-categorii.py",
        r"e:\Carte\BB\17 - Site Leadership\alte\Ionel Balauta\Aryeht\Task 1 - Traduce tot site-ul\Doar Google Web\Andreea\Meditatii\2023\Inlocuieste fiecare icon-facebook jpg cu imaginea nou creata.py"
    ]

    results = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        future_to_script = {executor.submit(run_script, script_path): script_path for script_path in script_paths}
        for future in concurrent.futures.as_completed(future_to_script):
            script_path = future_to_script[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as exc:
                print(f"Script {os.path.basename(script_path)} generated an exception: {exc}")

    successful = sum(results)
    total = len(script_paths)
    print(f"{successful} out of {total} scripts executed successfully.")
