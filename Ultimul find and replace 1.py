import os
import re
from datetime import datetime

# Dictionar pentru conversia lunilor din română în engleză
months_ro_to_en = {
    "ianuarie": "January", "februarie": "February", "martie": "March", "aprilie": "April",
    "mai": "May", "iunie": "June", "iulie": "July", "august": "August",
    "septembrie": "September", "octombrie": "October", "noiembrie": "November", "decembrie": "December"
}

def extract_date(content):
    date_match = re.search(r'On (\w+ \d+, \d{4})', content)
    if date_match:
        date_str = date_match.group(1)
        for ro_month, en_month in months_ro_to_en.items():
            if ro_month in date_str.lower():
                date_str = date_str.lower().replace(ro_month, en_month.title())
                break
        try:
            date_obj = datetime.strptime(date_str, '%B %d, %Y')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            print(f"Eroare la parsarea datei: {date_str}")
            return None
    else:
        print("Expresia regulată nu a găsit data!")
    return None

def has_existing_structure(content):
    return re.search(r'<article class="blog-box heading-space-half">', content) is not None

def update_html_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if has_existing_structure(content):
            print(f"Fișierul {os.path.basename(file_path)} are deja structura dorită. Nu se face niciun replace.")
            return False

        published_date = extract_date(content)
        if published_date:
            if "<!--STARTDATES-->" in content:
                content = re.sub(
                    r'(<!--STARTDATES-->)',
                    f'\\1\n<meta itemprop="datePublished" content="{published_date}">',
                    content
                )

        # Corectare pentru primul replace
        content = re.sub(
            r'(<div class="news_desc" itemscope itemtype="https://schema.org/Product">)',
            '                            <div class="news_desc" itemscope itemtype="https://schema.org/BlogPosting">\n'
            '                            <article>\n'
            '                                <header>',
            content
        )

        # Adăugare itemprop="image" la imaginea principală
        content = re.sub(
            r'(<img src="[^"]*" alt="[^"]*" class="img-responsive")>',
            r'\1 itemprop="image">',
            content
        )

        # Adăugare div cu itemprop="articleBody"
        content = re.sub(
            r'(<!-- ARTICOL START -->)',
            r'\1\n\n            <div itemprop="articleBody">',
            content
        )

        # Corectare pentru al doilea replace
        content = re.sub(
            r'(<!-- ARTICOL FINAL -->)',
            r'                           </div>\n'
            r'                </article>\n'
            r'       <!-- ARTICOL FINAL -->',
            content
        )

        # Închidere header după metadate
        content = re.sub(
            r'(<!--FINNISHDATES-->.*?</div>)',
            r'\1\n                                </header>',
            content,
            flags=re.DOTALL
        )

        # Eliminare linie specifică
        content = re.sub(
            r'<p align="justify" class="text_obisnuit style3"> </p>\n?',
            '',
            content
        )

        # Eliminare linie specifică
        content = re.sub(
            r'</a></a>',  # Găsește secvența specifică "</a></a>"
            '</a>',       # Înlocuiește cu "</a>"
            content       # Textul sursă în care se face înlocuirea
        )


        # Înlocuire div float-container-stars cu spațiere
        content = re.sub(
            r'<div class="float-container-stars">\s*?'
            r'<div class="float-child">\s*?'
            r'<div class="sharethis-inline-share-buttons"></div>\s*?'
            r'</div>\s*?'
            r'<div class="float-child">\s*?'
            r'<!-- STARS R -->\s*?'
            r'<div\s*?class="rw-ui-container rw-class-\<\?php echo \$rating_class \?\> rw-urid-\<\?php echo \$item_id \?\>">\s*?'
            r'</div>\s*?'
            r'<!-- STARS R2 -->\s*?'
            r'</div>\s*?'
            r'</div>',
            '                                <div style="height: 40px; clear: both; display: block;"></div>',
            content,
            flags=re.DOTALL
        )

        # Eliminare spațiu după ghilimele românești de deschidere
        content = re.sub(
            r'&bdquo; ',
            '„',
            content
        )

        # Eliminare spațiu după ghilimele românești de deschidere
        content = re.sub(
            r'„ ',
            '„',
            content
        )


        # Scriem conținutul modificat înapoi în fișier
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Fișierul {os.path.basename(file_path)} a fost actualizat cu succes.")
        return True
    except Exception as e:
        print(f"Eroare la procesarea fișierului {file_path}: {str(e)}")
        return False

def replace_motto(file_path):
    """Înlocuiește motto-ul românesc cu varianta în engleză."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Verificăm dacă există motto-ul românesc
        if '<p class="motto-subtitle">Totul depinde de cine conduce</p>' in content:
            # Înlocuim motto-ul
            content = content.replace(
                '<p class="motto-subtitle">Totul depinde de cine conduce</p>',
                '<p class="motto-subtitle">Totul depinde de cine conduce</p>'
            )

            # Scriem conținutul actualizat înapoi în fișier
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)

            print(f"Motto-ul a fost actualizat în fișierul {os.path.basename(file_path)}")
            return True
        return False
    except Exception as e:
        print(f"Eroare la înlocuirea motto-ului în fișierul {file_path}: {str(e)}")
        return False

# Definirea directorului de intrare
input_dir = 'c:\\Folder1\\fisiere_gata'

# Liste pentru a ține evidența fișierelor
files_without_replace = []
files_with_existing_structure = []
files_updated = []
files_with_motto_updated = []

# Procesăm toate fișierele HTML din directorul de intrare
for filename in os.listdir(input_dir):
    if filename.endswith('.html'):
        file_path = os.path.join(input_dir, filename)
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        if has_existing_structure(content):
            files_with_existing_structure.append(filename)
        elif update_html_file(file_path):
            files_updated.append(filename)
        else:
            files_without_replace.append(filename)

print("Procesarea fișierelor HTML s-a încheiat.")

# Afișăm rezultatele
if files_updated:
    print("\nFișiere actualizate cu succes:")
    for file in files_updated:
        print(file)

if files_without_replace:
    print("\nFișiere în care nu s-a putut face replace:")
    for file in files_without_replace:
        print(file)

if files_with_existing_structure:
    print("\nFișiere care au deja structura dorită (nu s-a făcut niciun replace):")
    for file in files_with_existing_structure:
        print(file)

# Acum, după ce toate celelalte sarcini au fost rulate,
# realizăm înlocuirea motto-ului în toate fișierele HTML din directorul de intrare
print("\nÎncepem înlocuirea motto-ului...")
for filename in os.listdir(input_dir):
    if filename.endswith('.html'):
        file_path = os.path.join(input_dir, filename)
        if replace_motto(file_path):
            files_with_motto_updated.append(filename)

if files_with_motto_updated:
    print("\nFișiere în care s-a actualizat motto-ul:")
    for file in files_with_motto_updated:
        print(file)
    print(f"\nTotal fișiere cu motto actualizat: {len(files_with_motto_updated)}")
else:
    print("\nNu s-a găsit motto-ul în niciun fișier.")