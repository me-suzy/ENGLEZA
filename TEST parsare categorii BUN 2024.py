import os
import re

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def write_to_file(text, file_path):
    with open(file_path, 'wb') as f:
        f.write(text.encode('utf8', 'ignore'))

def copiaza_continut_html(cale_fisier_html, cale_fisiere_gata):
    # Citim fișierul HTML sursă
    text_html = read_text_from_file(cale_fisier_html)

    # Regex pentru a extrage elementele <li>
    elemente_lista_pattern = re.compile(r'<li><a href="(.*?)" title="(.*?)">(.*?) \((.*?)\)</a></li>')
    elemente_lista = re.findall(elemente_lista_pattern, text_html)

    # Citim template-ul
    template_category = read_text_from_file('C:\\Folder1\\category-name.txt')

    # Pentru fiecare element <li>, înlocuim valorile în template
    final_text = ''
    for i in range(len(elemente_lista)):
        # Inlocuire in template
        new_template_category = template_category.replace("smth1", elemente_lista[i][0])  # URL
        new_template_category = new_template_category.replace("smth2", elemente_lista[i][1])  # Titlu
        new_template_category = new_template_category.replace("smth3", elemente_lista[i][2])  # Text
        new_template_category = new_template_category.replace("smth4", elemente_lista[i][3])  # Span

        # Adăugăm la final textul modificat
        final_text += new_template_category + '\n'

        # Debug pentru verificare
        print(f"Rezultat după înlocuire pentru element {i}:")
        print(new_template_category)

    # Scriem rezultatul final în fișierul de ieșire
    file_path = cale_fisiere_gata + "\\" + os.path.basename(cale_fisier_html)
    write_to_file(final_text, file_path)
    print("Scriere efectuată cu succes.")

# Testare simplă
copiaza_continut_html("C:\\Folder1\\fisiere_html\\index.html", "C:\\Folder1\\fisiere_gata")
