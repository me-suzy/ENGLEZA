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
        'ganduri-din-colturile-memoriei-IV.html',
        'ganduri-din-colturile-memoriei-III.html',
        'ganduri-din-colturile-memoriei-II.html',
        'ganduri-din-colturile-memoriei.html',
        'imagini-din-muzeul-mitropolitan-iasi.html',
        'marturisiri-discrete.html',
        'marturisiri-discrete-II.html',
        'marturisiri-discrete-III.html',
        'marturisiri-discrete-IV.html',
        'marturisiri-discrete-V.html',
        'the-book-of-books.html',
        'the-book-of-creation.html',
        'the-book-of-sand.html',
        'thoughts-in-the-corners-of-memory.html',
        'thoughts-in-the-corners-of-memory-II.html',
        'thoughts-in-the-corners-of-memory-III.html',
        'thoughts-in-the-corners-of-memory-IV.html',
        'citate-celebre-despre-leadership.html',
        'inspirational-leadership-quotes-and-motivational.html'
    ]

    # Regex pattern pentru a găsi liniile cu taguri <p> neînchise
    unclosed_p_pattern = re.compile(r'<p class="text_obisnuit(?:2)?">(?:(?!</p>).)*$')

    # Regex pattern pentru a găsi și înlocui structura specifică de Leadership
    leadership_pattern = re.compile(r'<p class="text_obisnuit"><span class="text_obisnuit2">(Leadership:.*?)</span></p>', re.DOTALL)

    # Regex pattern pentru cazurile cu un singur cuvânt în span la început
    # single_word_span_pattern = re.compile(r'<p class="text_obisnuit"><span class="text_obisnuit2">(\w+)</span>(.*?)</p>', re.DOTALL)

    # Regex pattern pentru a elimina tagurile <span> și </span> din orice linie ce conține <p class="text_obisnuit2">
    span_cleanup_pattern = re.compile(r'</?span.*?>')

    # Pas 1: Găsește și curăță tagurile <span> din tagurile match case <p class="text_obisnuit"><span class="text_obisnuit2">.*?</p>
    general_cleanup_pattern = re.compile(r'<p class="text_obisnuit">(?!<span class="text_obisnuit2">\w+</span>)<span class="text_obisnuit2">(.*?)</span></p>', re.DOTALL)

    # Pas 2: Înlocuiește <p class="text_obisnuit"><span class="text_obisnuit2"> cu <p class="text_obisnuit2">
    replace_general_pattern = re.compile(r'<p class="text_obisnuit"><span class="text_obisnuit2">')

    # Nou pattern pentru a elimina tagurile <strong> și </strong>
    strong_tag_pattern = re.compile(r'<p class="text_obisnuit(?:2)?">.*?</p>', re.DOTALL)

    for filename in os.listdir(directory):
        if filename.endswith('.html') and filename not in excluded_files:
            file_path = os.path.join(directory, filename)
            unclosed_lines = []
            leadership_lines = []

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Aplicăm regex-ul pentru a elimina tagurile <strong> și </strong>
            content = strong_tag_pattern.sub(lambda m: re.sub(r'</?strong>', '', m.group(0)), content)

            # Împărțim conținutul în linii pentru procesarea ulterioară
            content_lines = content.splitlines()

            modified_content = []

            for line_num, line in enumerate(content_lines, 1):
                stripped_line = line.strip()

                # Aplicăm mai întâi regex-ul pentru Leadership
                if leadership_pattern.search(stripped_line):
                    modified_line = leadership_pattern.sub(r'<p class="text_obisnuit2">\1</p>', line)
                    leadership_lines.append((line_num, stripped_line))
                elif single_word_span_pattern.search(stripped_line):
                    # Păstrăm structura pentru cazurile cu un singur cuvânt în span la început
                    modified_line = line
                else:
                    # Dacă nu este o linie de Leadership sau cu span la început, aplicăm celelalte modificări
                    modified_line = general_cleanup_pattern.sub(lambda match: f'<p class="text_obisnuit">{span_cleanup_pattern.sub("", match.group(1))}</p>', line)
                    modified_line = replace_general_pattern.sub('<p class="text_obisnuit2">', modified_line)

                # Verificăm pentru taguri <p> neînchise
                if unclosed_p_pattern.search(stripped_line):
                    unclosed_lines.append((line_num, stripped_line))

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
                file.write('\n'.join(modified_content))

# Specificați directorul cu fișierele HTML
directory = r'd:\55'
find_and_modify_tags(directory)