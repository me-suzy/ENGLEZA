import os
import re

from datetime import datetime

def extract_date(content):
    date_match = re.search(r'On (\w+ \d+, \d{4})', content)
    if date_match:
        date_str = date_match.group(1)
        try:
            date_obj = datetime.strptime(date_str, '%B %d, %Y')
            return date_obj.strftime('%Y-%m-%d')
        except ValueError:
            print(f"Eroare la parsarea datei: {date_str}")
            return None
    return None

def update_html_file(file_path, output_dir):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        published_date = extract_date(content)

        if published_date:
            # Adăugare meta pentru data publicării
            content = re.sub(
                r'(<!--STARTDATES-->)',
                f'\\1\n                                    <meta itemprop="datePublished" content="{published_date}">',
                content
            )
        else:
            print(f"Nu s-a putut extrage data pentru fișierul: {file_path}")

        # Corectare pentru primul replace
        content = re.sub(
            r'(<div class="news_desc" itemscope itemtype="https://schema.org/Product">)',
            '                            <div class="news_desc" itemscope itemtype="https://schema.org/BlogPosting">\n'
            '                            <article>\n'
            '                                <header>',
            content
        )


        # Adăugare itemprop="author"
        '''
        content = re.sub(
            r'(by Neculai Fantanaru</a>)',
            r'by <span itemprop="author">Neculai Fantanaru</span></a>',
            content
        )
        '''

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

        output_path = os.path.join(output_dir, os.path.basename(file_path))
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Fișierul {os.path.basename(file_path)} a fost actualizat cu succes.")
    except Exception as e:
        print(f"Eroare la procesarea fișierului {file_path}: {str(e)}")

# Definirea directoarelor de intrare și ieșire
input_dir = 'd:\\4'
output_dir = 'd:\\4\\Output'

# Crearea directorului de ieșire dacă nu există
if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"Directorul de ieșire {output_dir} a fost creat.")

# Procesare toate fișierele HTML din directorul de intrare
for filename in os.listdir(input_dir):
    if filename.endswith('.html'):
        file_path = os.path.join(input_dir, filename)
        update_html_file(file_path, output_dir)

print("Procesarea fișierelor HTML s-a încheiat. Fișierele actualizate se află în", output_dir)