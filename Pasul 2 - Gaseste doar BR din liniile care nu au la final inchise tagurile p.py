import os
import re

def find_and_modify_tags(directory):
    # Lista de fișiere de exclus
    excluded_files = [
        'aforisme-si-pareri-bine-slefuite-III.html',
        'aforisme-si-pareri-bine-slefuite-II.html',
        'aforisme-si-pareri-bine-slefuite.html',
        'cartea-cartilor.html',
        'cartea-creatiei.html',
        'cartea-de-nisip.html',
        'ganduri-din-colturile-memoriei-III.html',
        'imagini-din-muzeul-mitropolitan-iasi.html',
        'ganduri-din-colturile-memoriei-II.html',
        'ganduri-din-colturile-memoriei.html',
        'python-scripts-examples.html'
    ]

    # Regex pattern pentru a găsi liniile cu taguri <p> neînchise
    unclosed_p_pattern = re.compile(r'<p class="text_obisnuit(?:2)?">(?:(?!</p>).)*$')

    # Regex pattern pentru a găsi structura specifică de Leadership
    leadership_pattern = re.compile(r'<p class="text_obisnuit"><span class="text_obisnuit2">Leadership:')

    # Regex pattern pentru a înlocui structura găsită cu cea corectată și să evite dublarea </p>
    replace_leadership_pattern = re.compile(r'<p class="text_obisnuit"><span class="text_obisnuit2">(Leadership:.*?)</span></p>', re.DOTALL)

    # Regex pattern pentru a elimina tagurile <span> și </span> din orice linie ce conține <p class="text_obisnuit2">
    span_cleanup_pattern = re.compile(r'</?span.*?>')

    # Pas 1: Găsește și curăță tagurile <span> din tagurile match case <p class="text_obisnuit"><span class="text_obisnuit2">.*?</p>
    general_cleanup_pattern = re.compile(r'<p class="text_obisnuit"><span class="text_obisnuit2">(.*?)</p>', re.DOTALL)

    # Pas 2: Înlocuiește <p class="text_obisnuit"><span class="text_obisnuit2"> cu <p class="text_obisnuit2">
    replace_general_pattern = re.compile(r'<p class="text_obisnuit"><span class="text_obisnuit2">')

    for filename in os.listdir(directory):
        if filename.endswith('.html') and filename not in excluded_files:
            file_path = os.path.join(directory, filename)
            unclosed_lines = []
            leadership_lines = []

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.readlines()

            modified_content = []

            for line_num, line in enumerate(content, 1):
                stripped_line = line.strip()

                # Căutare de linii cu taguri <p> neînchise
                if unclosed_p_pattern.search(stripped_line):
                    unclosed_lines.append((line_num, stripped_line))
                # Căutare de linii cu Leadership
                if leadership_pattern.search(stripped_line):
                    leadership_lines.append((line_num, stripped_line))

                # Pas 1: Curăță tagurile <span> din tagurile specificate
                modified_line = general_cleanup_pattern.sub(lambda match: f'<p class="text_obisnuit">{span_cleanup_pattern.sub("", match.group(1))}</p>', line)

                # Pas 2: Înlocuiește <p class="text_obisnuit"><span class="text_obisnuit2"> cu <p class="text_obisnuit2">
                modified_line = replace_general_pattern.sub('<p class="text_obisnuit2">', modified_line)

                # Modificarea conținutului pentru Leadership, prevenind dublarea </p>
                modified_line = replace_leadership_pattern.sub(r'<p class="text_obisnuit2">\1</p>', modified_line)

                modified_content.append(modified_line)

            # Afișare rezultate
            if unclosed_lines or leadership_lines:
                print(f"\nFișierul: {filename}")
                if unclosed_lines:
                    print("  Linii cu taguri <p> neînchise:")
                    for line_num, line_content in unclosed_lines:
                        print(f"    Linia {line_num}: {line_content}")
                if leadership_lines:
                    print("  Linii care conțin Leadership:")
                    for line_num, line_content in leadership_lines:
                        print(f"    Linia {line_num}: {line_content}")

            # Scrie conținutul modificat înapoi în fișier
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(modified_content)

# Specificați directorul cu fișierele HTML
directory = r'e:\Carte\BB\17 - Site Leadership\Principal\ro'
find_and_modify_tags(directory)
