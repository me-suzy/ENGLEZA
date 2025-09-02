import os
import re

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
        return text

def write_to_file(text, file_path):
    with open(file_path, 'wb') as f:
        f.write(text.encode('utf8', 'ignore'))

def copiaza_continut_html(cale_fisier_html, cale_fisiere_gata):
    text_html = read_text_from_file(cale_fisier_html)
    final_text = ''

    # Extragem secțiunea sidebarNavigation
    sidebar_navigation_pattern = re.compile(r'<ul id="sidebarNavigation">(.*?)</ul>', re.DOTALL)
    navigation_section = re.search(sidebar_navigation_pattern, text_html)

    if navigation_section:
        # Extragem URL-urile și titlurile din secțiunea sidebarNavigation
        elemente_lista_pattern = re.compile(r'<li><a href="(.*?)" title="(.*?)">(.*?) \((.*?)\)</a></li>')
        elemente_lista = re.findall(elemente_lista_pattern, navigation_section.group(1))

        # Citim template-ul pentru categoriile din noul fișier
        template_category = read_text_from_file('C:\\Folder1\\category-name.txt')

        for i in range(len(elemente_lista)):
            # Inlocuire în template pentru fiecare element din lista
            new_template_category = template_category
            new_template_category = new_template_category.replace("smth1", elemente_lista[i][0])  # URL
            new_template_category = new_template_category.replace("smth2", elemente_lista[i][1])  # Titlu
            new_template_category = new_template_category.replace("smth3", elemente_lista[i][2])  # Text
            new_template_category = new_template_category.replace("smth4", elemente_lista[i][3])  # Span

            final_text += new_template_category + '\n'

        # Acum gestionăm secțiunea FLAGS separat
        flags_pattern = re.compile(r'<!-- FLAGS_1 -->(.*?)<!-- FLAGS -->', re.DOTALL)
        flags_section = re.search(flags_pattern, text_html)

        if flags_section:
            links_pattern = re.compile(r'<a href=\"(.*?)\">')
            links = re.findall(links_pattern, flags_section.group(1))

            flags_model_pattern = re.search(flags_pattern, final_text)
            if flags_model_pattern:
                flags_model = flags_model_pattern.group(1)
                links_pattern_model = re.compile(r'<a href=\"(.*?)\">')
                links_model = re.findall(links_pattern_model, flags_model)

                for i in range(len(links)):
                    final_text = final_text.replace(links_model[i], links[i])  # Înlocuim linkurile pentru FLAGS

    # Salvăm fișierul final cu conținutul modificat
    file_path = cale_fisiere_gata + "\\" + os.path.basename(cale_fisier_html)
    write_to_file(final_text, file_path)
    print("Scriere efectuată cu succes.")

def creare_fisiere_html(cale_folder_html, cale_fisiere_gata):
    count = 0

    for f in os.listdir(cale_folder_html):
        if f.endswith('.html'):
            cale_fisier_html = cale_folder_html + "\\" + f
            print("FISIER CURENT: ", cale_fisier_html)
            copiaza_continut_html(cale_fisier_html, cale_fisiere_gata)
            count += 1
    print("Numarul de fisiere modificate: ", count)

def main():
    creare_fisiere_html("C:\\Folder1\\fisiere_html", "C:\\Folder1\\fisiere_gata")

if __name__ == '__main__':
    main()
