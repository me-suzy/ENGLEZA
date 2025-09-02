import os
import regex as re

def process_file_content(content):
    lines = content.split('\n')
    processed_lines = []

    for line in lines:
        # Păstrăm spațiile inițiale ale fiecărei linii
        leading_spaces = re.match(r'^\s*', line).group()

        stripped_line = line.strip()

        # Păstrăm liniile cu <br><br> neschimbate
        if '<br><br>' in stripped_line:
            processed_lines.append(line)
            continue

        # Procesăm doar liniile care conțin taguri <p>
        if '<p class="text_obisnuit"' in stripped_line or '<p class="text_obisnuit2"' in stripped_line:
            # Înlocuim <br> la sfârșitul liniei cu </p>
            stripped_line = re.sub(r'(<p class="text_obisnuit2?">.*?)<br>\s*$', r'\1</p>', stripped_line)

            # Eliminăm spațiile inutile de la început
            stripped_line = re.sub(r'^\s*(<p class="text_obisnuit2?">)', r'\1', stripped_line)

            # Eliminăm </p> dublu
            stripped_line = re.sub(r'(<p class="text_obisnuit2?">.*?</p>)\s*</p>\s*', r'\1', stripped_line)

        # Adăugăm spațiile inițiale înapoi
        processed_lines.append(leading_spaces + stripped_line)

    content = '\n'.join(processed_lines)

    # Adăugăm spații între paragrafe
    # content = re.sub(r'(</p>)\s*(<p class="text_obisnuit">)', r'\1\n\n\2', content)
    content = re.sub(r'</span> </span>', r'</span> ', content)
    content = re.sub(r'<strong>|</strong>', r' ', content)

    # Eliminăm liniile care conțin doar </p>
    content = re.sub(r'^\s*</p>\s*$', '', content, flags=re.MULTILINE)

    return content

def process_html_files(directory):
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

    for filename in os.listdir(directory):
        if filename.endswith('.html') and filename not in excluded_files:
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            processed_content = process_file_content(content)

            if content != processed_content:
                print(f"\nModificări în fișierul: {filename}")
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(processed_content)

            # Verificăm dacă mai există linii cu <br><br> după procesare
            if '<br><br>' in processed_content:
                print(f"\nLinia <br><br> păstrată în fișierul: {filename}")

# Specificați directorul cu fișierele HTML
directory = r'e:\Carte\BB\17 - Site Leadership\Principal\ro'
process_html_files(directory)
