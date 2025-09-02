import os
import re

def read_text_from_file(file_path):
    """
    Aceasta functie returneaza continutul unui fisier.
    file_path: calea catre fisierul din care vrei sa citesti
    """
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
        return text

def write_to_file(text, file_path):
    """
    Aceasta functie scrie un text intr-un fisier.
    text: textul pe care vrei sa il scrii
    file_path: calea catre fisierul in care vrei sa scrii
    """
    with open(file_path, 'wb') as f:
        f.write(text.encode('utf8', 'ignore'))

def copiaza_continut_html(cale_fisier_html, cale_fisiere_gata):
    # Citim textul din fisierul HTML
    text_html = read_text_from_file(cale_fisier_html)
    final_text = ''

    # === fisier html vechi articol_categorie ===
    articol_categorie_pattern = re.compile(r'<!-- ARTICOL CATEGORIE START -->([\s\S]*?)<!-- ARTICOL CATEGORIE FINAL -->')
    articol_categorie = re.findall(articol_categorie_pattern, text_html)
    if len(articol_categorie) != 0:
        # === citire fisier model - index2.html ===
        text_html_model = read_text_from_file("e:\\Carte\\BB\\17 - Site Leadership\\alte\\Ionel Balauta\\Aryeht\\Task 1 - Traduce tot site-ul\\Doar Google Web\\Andreea\\Meditatii\\Sedinta 18\\index2.html")
        articol_categorie = articol_categorie[0]

        # Verifică și corectează anumite tag-uri în articol_categorie
        articol_categorie = re.sub(r'<td width="\d+"><span class="den_articol">', '<td><span class="den_articol">', articol_categorie)
        articol_categorie = articol_categorie.replace('<td><p class="den_articol">', '<td><span class="den_articol">')

        # Inlocuirea tag-urilor în articol_categorie
        span_pattern = re.compile(r'<td><span class="den_articol"><a href=\"(.*?)\" class="linkMare">(.*?)</a></span></td>')
        span_nou = '<td><span class="linkMare"><a href="{}" class="linkMare"><span class="den_articol">{}</span></a></span></td>'
        span = re.findall(span_pattern, articol_categorie)
        lista_span_nou = [span_nou.format(s[0], s[1]) for s in span]
        span_pattern_full = re.compile(r'<td><span class="den_articol"><a href=\".*?\" class="linkMare">.*?</a></span></td>')
        span_full = re.findall(span_pattern_full, articol_categorie)
        for original, nou in zip(span_full, lista_span_nou):
            articol_categorie = articol_categorie.replace(original, nou)

        # Extragem informațiile necesare din articol_categorie
        categ_link_title_pattern = re.compile(r'<td><span class="linkMare"><a href="(.*?)" class="linkMare"><span class="den_articol">(.*?)</span></a></span></td>')
        categ_link_title = re.findall(categ_link_title_pattern, articol_categorie)
        print("Total {} ARTICOLE".format(len(categ_link_title)))

        categ_date_link_title_desc_pattern = re.compile(r'<td class="text_dreapta">(.*?)<a href=\"(.*?)\" title=\"(.*?)\" class="external" rel="category tag">(.*?)</a>, by Neculai Fantanaru</td>')
        categ_date_link_title_desc = re.findall(categ_date_link_title_desc_pattern, articol_categorie)

        paragraf_pattern = re.compile(r'<p class="text_obisnuit2"><em>(.*?)</em></p>')
        paragraf = re.findall(paragraf_pattern, articol_categorie)
        print("PARAGRAF", len(paragraf))

        # Extragem butoanele "citește mai departe"
        citeste_buton_pattern = re.compile(r'<div align="right" id="external2"><a href=\"(.*?)\">cite&#351;te mai departe </a>')
        citeste_buton = re.findall(citeste_buton_pattern, articol_categorie)
        read_more_buton_pattern = re.compile(r'<div align="right" id="external2"><a href=\"(.*?)\">read more </a>')
        read_more_buton = re.findall(read_more_buton_pattern, articol_categorie)

        # === Informatii index2 ===
        articol_categorie_index2_pattern = re.compile(r'<!-- ARTICOL START -->([\s\S]*?)<!-- ARTICOL FINAL -->')
        articol_categorie_index2 = re.findall(articol_categorie_index2_pattern, text_html_model)
        if len(articol_categorie_index2) != 0:
            articol_categorie_index2 = articol_categorie_index2[0]
            template_categorie = read_text_from_file("C:\\Folder1\\template_categorie.txt")

            # Extragem elementele din template
            h3_pattern = re.compile(r'<h3 class="font-weight-normal" itemprop="name"><a href=\"(.*?)\" class="color-black">(.*?)</a></h3>')
            h3 = re.findall(h3_pattern, template_categorie)[0]

            dates_section_index2_pattern = re.compile(r'<!--STARTDATES-->([\s\S]*?)<!--FINNISHDATES-->')
            dates_section_index2 = re.findall(dates_section_index2_pattern, template_categorie)[0]

            date_index2_pattern = re.compile(r'<a href="javascript:void\(0\)" class="color-black">(.*?)</a>')
            date_index2 = re.findall(date_index2_pattern, dates_section_index2)[0]

            link_title_desc_index2_pattern = re.compile(r'<a href=\"(.*?)\" title=\"(.*?)\" class="color-green font-weight-600 mx-1" id="hidden">(.*?)</a>')
            link_title_desc_index2 = re.findall(link_title_desc_index2_pattern, dates_section_index2)[0]

            paragraf_index2_pattern = re.compile(r'<p class="mb-35px color-grey line-height-25px">(.*?)</p>')
            paragraf_index2 = re.findall(paragraf_index2_pattern, template_categorie)[0]

            read_more_pattern = re.compile(r'<a href=\"(.*?)\" class="btn-setting color-black btn-hvr-up btn-blue btn-hvr-pink">read more</a>')
            read_more = re.findall(read_more_pattern, template_categorie)[0]

            butoane = citeste_buton if len(citeste_buton) > 0 else read_more_buton
            print("CATEGORIE", len(categ_link_title))

            # Construim noul conținut
            for i in range(len(categ_link_title)):
                new_template = template_categorie
                new_template = new_template.replace(date_index2, categ_date_link_title_desc[i][0].replace(', in', '').strip())
                new_template = new_template.replace(link_title_desc_index2[0], categ_date_link_title_desc[i][1])
                new_template = new_template.replace(link_title_desc_index2[1], categ_date_link_title_desc[i][2])
                new_template = new_template.replace(link_title_desc_index2[2], categ_date_link_title_desc[i][3].lstrip())
                new_template = new_template.replace(paragraf_index2, paragraf[i])
                new_template = new_template.replace(read_more, butoane[i])
                new_template = new_template.replace(h3[0], categ_link_title[i][0])
                new_template = new_template.replace(h3[1], categ_link_title[i][1])
                final_text += new_template + '\n'

            text_html_model = text_html_model.replace(articol_categorie_index2, final_text)
            final_text = text_html_model

            # Schimbare CATEGORIES index2
            lista_pattern = re.compile(r'<ul id="sidebarNavigation">([\s\S]*?)</ul>')
            lista = re.findall(lista_pattern, text_html)
            if len(lista) != 0:
                lista = lista[0]
                elemente_lista_pattern = re.compile(r'<li><a href=\"(.*?)\" title=\"(.*?)\">(.*?) \((.*?)\)</a></li>')
                elemente_lista = re.findall(elemente_lista_pattern, lista)
                if len(elemente_lista) != 0:
                    categories_pattern = re.compile(r'<!-- Categories -->([\s\S]*?)<!-- BOOKS START -->')
                    categories = re.findall(categories_pattern, final_text)
                    if len(categories) != 0:
                        categories = categories[0]
                        template_category = read_text_from_file('C:\\Folder1\\category-name.txt')
                        new_categories_text = ''
                        for elem in elemente_lista:
                            new_template_category = template_category
                            new_template_category = new_template_category.replace('smth1', elem[0])
                            new_template_category = new_template_category.replace('smth2', elem[1])
                            new_template_category = new_template_category.replace('smth3', elem[2])
                            new_template_category = new_template_category.replace('smth4', elem[3])
                            new_categories_text += new_template_category + '\n'
                        final_text = re.sub(categories_pattern, '<!-- Categories -->\n' + new_categories_text + '\n<!-- BOOKS START -->', final_text)
                    else:
                        print("No categories + books start")
                else:
                    print("Niciun element <li>.")
            else:
                print("Tag <ul> gol.")

            # Schimbare LINK-URI FLAGS
            flags_pattern = re.compile(r'<!-- FLAGS_1 -->([\s\S]*?)<!-- FLAGS -->')
            flags = re.findall(flags_pattern, text_html)
            if len(flags) != 0:
                flags = flags[0]
                links_pattern = re.compile(r'<a href=\"(.*?)\">')
                links = re.findall(links_pattern, flags)
                if len(links) != 0:
                    flags_model = re.findall(flags_pattern, final_text)
                    if len(flags_model) != 0:
                        flags_model = flags_model[0]
                        links_pattern_model = re.compile(r'<a href=\"(.*?)\">')
                        links_model = re.findall(links_pattern_model, flags_model)
                        if len(links_model) != 0:
                            for i in range(len(links_model)):
                                final_text = final_text.replace(links_model[i], links[i])
                        else:
                            print("Fara links in flags model")
                    else:
                        print("Fara flags in model")
                else:
                    print("Fara linkuri in flags.")
            else:
                print("Fara flags in articol original.")

            # STARS - PHP
            stars_php_pattern = re.compile(r'\$item_id = (.*?);')
            stars_php = re.findall(stars_php_pattern, text_html)
            stars_php_model = re.findall(stars_php_pattern, final_text)
            if len(stars_php) != 0 and len(stars_php_model) != 0:
                final_text = final_text.replace(stars_php_model[0], stars_php[0])
            else:
                print("No stars fisier original sau model")

            # TITLE
            title_pattern = re.compile(r'<title>(.*?)</title>')
            text_title = re.findall(title_pattern, text_html)
            text_title_model = re.findall(title_pattern, final_text)
            if len(text_title) != 0 and len(text_title_model) != 0:
                final_text = final_text.replace(text_title_model[0], text_title[0])
            else:
                print("Fisier html fara tag title: {}".format(cale_fisier_html))

            # DESCRIPTION
            description_pattern = re.compile(r'<meta name="description" content="(.*?)">')
            text_description = re.findall(description_pattern, text_html)
            text_description_model = re.findall(description_pattern, final_text)
            if len(text_description) != 0 and len(text_description_model) != 0:
                final_text = final_text.replace(text_description_model[0], text_description[0])
            else:
                print("Fisier html fara tag description: {}".format(cale_fisier_html))

            # CANONICAL
            canonical_pattern = re.compile(r'<link rel="canonical" href="(.*?)" />')
            text_canonical = re.findall(canonical_pattern, text_html)
            text_canonical_model = re.findall(canonical_pattern, final_text)
            if len(text_canonical) != 0 and len(text_canonical_model) != 0:
                final_text = final_text.replace(text_canonical_model[0], text_canonical[0])
            else:
                print("Fisier html fara tag canonical: {}".format(cale_fisier_html))

            # ULTIMELE ARTICOLE
            ult_art_pattern = re.compile(r'<!-- Ultimele articole -->([\s\S]*?)<!-- Ultimele articole final -->')
            ult_art_model_pattern = re.compile(r'<!-- Recent Post -->([\s\S]*?)<!-- Categories -->')
            ult_art = re.findall(ult_art_pattern, text_html)
            ult_art_model = re.findall(ult_art_model_pattern, final_text)
            if len(ult_art) != 0 and len(ult_art_model) != 0:
                articole_pattern = re.compile(r'<li><a href=\"(.*?)\">(.*?)</a></li>')
                articole = re.findall(articole_pattern, ult_art[0])
                articole_model_pattern = re.compile(r'<a href=\"(.*?)\" class="color-grey">(.*?)</a>')
                articole_model = re.findall(articole_model_pattern, ult_art_model[0])
                for i in range(len(articole)):
                    final_text = final_text.replace(articole_model[i][0], articole[i][0])
                    final_text = final_text.replace(articole_model[i][1], articole[i][1])
            else:
                print("No lista articole fisier original sau model")
        else:
            print("Nu exista articol categorie în index2.html")
    else:
        # Cod pentru cazul în care 'articol_categorie' nu este găsit
        # Aici poți adăuga codul necesar similar cu cel de mai sus, adaptat pentru acest caz
        pass

    # Scriem rezultatul final în fișierul de ieșire
    file_path = os.path.join(cale_fisiere_gata, os.path.basename(cale_fisier_html))
    write_to_file(final_text, file_path)
    print("Scriere efectuată cu succes.")

def creare_fisiere_html(cale_folder_html, cale_fisiere_gata):
    """
    Functia itereaza printr-un folder care contine fisiere html si creeaza fisiere html modificate
    """
    count = 0

    fisiere_de_ignorat = [
        # Lista de fișiere de ignorat
    ]

    for f in os.listdir(cale_folder_html):
        if f.endswith('.html'):
            if f in fisiere_de_ignorat:
                print(f"Ignorăm fișierul: {f}")
                continue
            cale_fisier_html = os.path.join(cale_folder_html, f)
            print("FISIER CURENT: ", cale_fisier_html)
            copiaza_continut_html(cale_fisier_html, cale_fisiere_gata)
            count += 1
    print("Numarul de fisiere modificate: ", count)

def main():
    creare_fisiere_html("C:\\Folder1\\fisiere_html", "C:\\Folder1\\fisiere_gata")

if __name__ == '__main__':
    main()
