import os
import re

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def write_to_file(text, file_path):
    with open(file_path, 'wb') as f:
        f.write(text.encode('utf8', 'ignore'))

def copiaza_continut_html(cale_fisier_html, cale_fisiere_gata):
    text_html = read_text_from_file(cale_fisier_html)
    final_text = ''

    articol_categorie_pattern = re.compile(r'<!-- ARTICOL CATEGORIE START -->([\s\S]*?)<!-- ARTICOL CATEGORIE FINAL -->')
    articol_categorie = re.findall(articol_categorie_pattern, text_html)

    if len(articol_categorie) != 0:
        text_html_model = read_text_from_file("e:\\Carte\\BB\\17 - Site Leadership\\alte\\Ionel Balauta\\Aryeht\\Task 1 - Traduce tot site-ul\\Doar Google Web\\Andreea\\Meditatii\\Sedinta 18\\ENGLEZA\\index2.html")
        articol_categorie = articol_categorie[0]

        width_pattern = re.compile(r'<td width="449"><span class="den_articol">')
        if re.search(width_pattern, articol_categorie):
            print("ATENȚIE: S-au găsit cazuri cu width='449'")
            articol_categorie = re.sub(width_pattern, '<td><span class="den_articol">', articol_categorie)
            print("Cazurile cu width='449' au fost corectate")

            span_pattern = re.compile(r'<td(?:\s+width="\d+")?\s*><span class="den_articol"><a href=\"(.*?)\" class="linkMare">(.*?)</a></span></td>')
            span_nou = '<td><span class="linkMare"><a href="{}" class="linkMare"><span class="den_articol">{}</span></a></span></td>'
            span = re.findall(span_pattern, articol_categorie)
            print(f"Număr de potriviri găsite: {len(span)}")

            lista_span_nou = [span_nou.format(s[0], s[1]) for s in span]
            span_pattern = re.compile(r'<td><span class="den_articol"><a href=\".*?\" class="linkMare">.*?</a></span></td>')
            span = re.findall(span_pattern, articol_categorie)
            for old, new in zip(span, lista_span_nou):
                articol_categorie = articol_categorie.replace(old, new)

            remaining_patterns = re.findall(r'<td(?:\s+width="\d+")?\s*><span class="den_articol">', articol_categorie)
            if remaining_patterns:
                print(f"ATENȚIE: Au rămas {len(remaining_patterns)} cazuri neprocesate")
                print("Exemple de cazuri rămase:")
                for i, pattern in enumerate(remaining_patterns[:5]):
                    print(f"  {i+1}. {pattern}")

            if remaining_patterns:
                articol_categorie = re.sub(r'<td(?:\s+width="\d+")?\s*><span class="den_articol">', '<td><span class="den_articol">', articol_categorie)
                print("Cazurile rămase au fost corectate")

            remaining_patterns_after = re.findall(r'<td(?:\s+width="\d+")?\s*><span class="den_articol">', articol_categorie)
            if remaining_patterns_after:
                print(f"ATENȚIE: Au rămas {len(remaining_patterns_after)} cazuri neprocesate după corecție")
            else:
                print("Toate cazurile au fost procesate cu succes")

            categ_link_title_pattern = re.compile(r'<td><span class="linkMare"><a href="(.*?)" class="linkMare"><span class="den_articol">(.*?)</span></a></span></td>')
            categ_link_title = re.findall(categ_link_title_pattern, articol_categorie)
            print(f"Total {len(categ_link_title)} ARTICOLE")

            categ_date_link_title_desc_pattern = re.compile(r'<td class="text_dreapta">(.*?)<a href=\"(.*?)\" title=\"(.*?)\" class="external" rel="category tag">(.*?)</a>, by Neculai Fantanaru</td>')
            categ_date_link_title_desc = re.findall(categ_date_link_title_desc_pattern, articol_categorie)
            paragraf_pattern = re.compile(r'<p class="text_obisnuit2"><em>(.*?)</em></p>')
            paragraf = re.findall(paragraf_pattern, articol_categorie)

            citeste_buton_pattern = re.compile(r'<div align="right" id="external2"><a href=\"(.*?)\">cite&#351;te mai departe </a>')
            citeste_buton = re.findall(citeste_buton_pattern, articol_categorie)
            read_more_buton_pattern = re.compile(r'<div align="right" id="external2"><a href=\"(.*?)\">read more </a>')
            read_more_buton = re.findall(read_more_buton_pattern, articol_categorie)

            articol_categorie_index2_pattern = re.compile(r'<!-- ARTICOL START -->([\s\S]*?)<!-- ARTICOL FINAL -->')
            articol_categorie_index2 = re.findall(articol_categorie_index2_pattern, text_html_model)
            if len(articol_categorie_index2) != 0:
                articol_categorie_index2 = articol_categorie_index2[0]
                template_categorie = read_text_from_file("C:\\Folder1\\template_categorie.txt")

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

                lista_pattern = re.compile(r'<ul id="sidebarNavigation">([\s\S]*?)</ul>')
                lista = re.findall(lista_pattern, text_html)
                if len(lista) != 0:
                    lista = lista[0]
                    elemente_lista_pattern = re.compile(r'<li><a href=\"(.*?)\" title=\"(.*?)\">(.*?) \((.*?)\)</a></li>')
                    elemente_lista = re.findall(elemente_lista_pattern, lista)
                    if len(elemente_lista) != 0:
                        categories_pattern = re.compile(r'<!-- Categories -->([\s\S]*?)<!-- BOOKS START -->')
                        categories = re.findall(categories_pattern, final_text)[0]
                        elemente_lista_model_pattern = re.compile(r'<div class="categories-name">([\s\S]*?)</div>')
                        elemente_lista_model = re.findall(elemente_lista_model_pattern, categories)
                        template_category = read_text_from_file('C:\\Folder1\\category-name.txt')

                        for i in range(len(elemente_lista_model)):
                            new_template_category = template_category
                            a_pattern = re.compile(r'<a href=\"(.*?)\" title=\"(.*?)\">')
                            a = re.findall(a_pattern, new_template_category)[0]
                            p_pattern = re.compile(r'<p class="font-16 color-grey text-capitalize"><i class="fa fa-angle-right font-14 color-blue mr-1"></i> (.*?) <span>(.*?)</span> </p>')
                            p = re.findall(p_pattern, new_template_category)[0]
                            new_template_category = new_template_category.replace(a[0], elemente_lista[i][0])
                            new_template_category = new_template_category.replace(a[1], elemente_lista[i][1])
                            new_template_category = new_template_category.replace(p[0], elemente_lista[i][2])
                            new_template_category = new_template_category.replace(p[1], elemente_lista[i][3])
                            final_text = final_text.replace(elemente_lista_model[i], new_template_category)

                flags_pattern = re.compile(r'<!-- FLAGS_1 -->([\s\S]*?)<!-- FLAGS -->')
                flags = re.findall(flags_pattern, text_html)
                if len(flags) != 0:
                    flags = flags[0]
                    links_pattern = re.compile(r'<a href=\"(.*?)\">')
                    links = re.findall(links_pattern, flags)
                    if len(links) != 0:
                        flags_model = re.findall(flags_pattern, final_text)[0]
                        links_pattern_model = re.compile(r'<li><a cunt_code=\"\+\d+\" href=\"(.*?)\">')
                        links_model = re.findall(links_pattern_model, flags_model)
                        if len(links_model) != 0:
                            for i in range(len(links)):
                                final_text = final_text.replace(links_model[i], links[i])

                stars_php_pattern = re.compile(r'\$item_id = (.*?);')
                stars_php = re.findall(stars_php_pattern, text_html)
                stars_php_model = re.findall(stars_php_pattern, final_text)
                if len(stars_php) != 0:
                    stars_php = stars_php[0]
                    if len(stars_php_model) != 0:
                        stars_php_model = stars_php_model[0]
                        final_text = final_text.replace(stars_php_model, stars_php)

                title_pattern = re.compile(r'<title>(.*?)</title>')
                text_title = re.findall(title_pattern, text_html)
                text_title_model = re.findall(title_pattern, final_text)
                if len(text_title) != 0 and len(text_title_model) != 0:
                    text_title = text_title[0]
                    text_title_model = text_title_model[0]
                    final_text = final_text.replace(text_title_model, text_title)

                description_pattern = re.compile(r'<meta name="description" content="(.*?)">')
                text_description = re.findall(description_pattern, text_html)
                text_description_model = re.findall(description_pattern, final_text)
                if len(text_description) != 0 and len(text_description_model) != 0:
                    text_description = text_description[0]
                    text_description_model = text_description_model[0]
                    final_text = final_text.replace(text_description_model, text_description)

                canonical_pattern = re.compile(r'<link rel="canonical" href="(.*?)" />')
                text_canonical = re.findall(canonical_pattern, text_html)
                text_canonical_model = re.findall(canonical_pattern, final_text)
                if len(text_canonical) != 0 and len(text_canonical_model) != 0:
                    text_canonical = text_canonical[0]
                    text_canonical_model = text_canonical_model[0]
                    final_text = final_text.replace(text_canonical_model, text_canonical)

                ult_art_pattern = re.compile(r'<!-- Ultimele articole -->([\s\S]*?)<!-- Ultimele articole final -->')
                ult_art_model_pattern = re.compile(r'<!-- Recent Post -->([\s\S]*?)<!-- Categories -->')
                ult_art = re.findall(ult_art_pattern, text_html)
                ult_art_model = re.findall(ult_art_model_pattern, final_text)
                if len(ult_art) != 0:
                    ult_art = ult_art[0]
                    if len(ult_art_model) != 0:
                        ult_art_model = ult_art_model[0]
                        articole_pattern = re.compile(r'<li><a href=\"(.*?)\">(.*?)</a></li>')
                        articole = re.findall(articole_pattern, ult_art)
                        if len(articole) != 0:
                            articole_model_pattern = re.compile(r'<a href=\"(.*?)\" class="color-grey">(.*?)</a>')
                            articole_model = re.findall(articole_model_pattern, ult_art_model)
                            if len(articole_model) != 0:
                                for i in range(len(articole)):
                                    final_text = final_text.replace(articole_model[i][0], articole[i][0])
                                    final_text = final_text.replace(articole_model[i][1], articole[i][1])

        else:
            text_html_model = read_text_from_file("e:\\Carte\\BB\\17 - Site Leadership\\alte\\Ionel Balauta\\Aryeht\\Task 1 - Traduce tot site-ul\\Doar Google Web\\Andreea\\Meditatii\\Sedinta 18\\ENGLEZA\\index.html")
            articol_pattern = re.compile(r'<!-- ARTICOL START -->([\s\S]*?)<!-- ARTICOL FINAL -->[\s\S]*?')
            text_articol = re.findall(articol_pattern, text_html)
            text_articol_model = re.findall(articol_pattern, text_html_model)
            if len(text_articol) != 0 and len(text_articol_model) != 0:
                text_articol = text_articol[0]
                text_articol_model = text_articol_model[0]
                text_html_model_1 = text_html_model.replace(text_articol_model, text_articol)
                final_text = text_html_model_1

                title_pattern = re.compile(r'<title>(.*?)</title>')
                text_title = re.findall(title_pattern, text_html)
                text_title_model = re.findall(title_pattern, text_html_model_1)
                if len(text_title) != 0 and len(text_title_model) != 0:
                    text_title = text_title[0]
                    text_title_model = text_title_model[0]
                    text_html_model_2 = text_html_model_1.replace(text_title_model, text_title)
                    final_text = text_html_model_2

                description_pattern = re.compile(r'<meta name="description" content="(.*?)">')
                text_description = re.findall(description_pattern, text_html)
                text_description_model = re.findall(description_pattern, text_html_model_2)
                if len(text_description) != 0 and len(text_description_model) != 0:
                    text_description = text_description[0]
                    text_description_model = text_description_model[0]
                    text_html_model_3 = text_html_model_2.replace(text_description_model, text_description)
                    final_text = text_html_model_3

                canonical_pattern = re.compile(r'<link rel="canonical" href="(.*?)" />')
                text_canonical = re.findall(canonical_pattern, text_html)
                text_canonical_model = re.findall(canonical_pattern, text_html_model_3)
                if len(text_canonical) != 0 and len(text_canonical_model) != 0:
                    text_canonical = text_canonical[0]
                    text_canonical_model = text_canonical_model[0]
                    text_html_model_4 = text_html_model_3.replace(text_canonical_model, text_canonical)
                    final_text = text_html_model_4

                text_articol_model = re.findall(articol_pattern, text_html_model_4)[0]
                text_articol_model_old = text_articol_model
                text_articol_model = text_articol_model.replace("<div align=\"justify\">", '').replace("</div>", '')

                table_pattern = re.compile(r'<table[\s\S]*?</table>')
                text_table = re.findall(table_pattern, text_articol_model)
                if len(text_table) != 0:
                    text_table = text_table[0]
                    text_articol_model = text_articol_model.replace(text_table, '')
                    text_html_model_5 = text_html_model_4.replace(text_articol_model_old, text_articol_model)
                    final_text = text_html_model_5

                article_title_pattern = re.compile(r'<h1 class="den_articol" itemprop="name">(.*?)</h1>')
                article_title = re.findall(article_title_pattern, text_articol_model_old)
                if len(article_title) != 0:
                    article_title = article_title[0]
                    h3_title_pattern = re.compile(r'<h3 class="font-weight-normal" itemprop="name"><a href="javascript:void\(0\)" class="color-black">(.*?)</a></h3>')
                    h3_title = re.findall(h3_title_pattern, text_html_model_5)
                    if len(h3_title) != 0:
                        h3_title = h3_title[0]
                        text_html_model_6 = text_html_model_5.replace(h3_title, article_title)
                        final_text = text_html_model_6

                date_pattern = re.compile(r'<td class="text_dreapta">(.*?), in <a')
                date = re.findall(date_pattern, text_articol_model_old)
                if len(date) != 0:
                    date = date[0]
                    date_section_pattern = re.compile(r'<!--STARTDATES-->([\s\S]*?)<!--FINNISHDATES-->')
                    date_section = re.findall(date_section_pattern, text_html_model_6)
                    if len(date_section) > 0:
                        date_section = date_section[0]
                        date_pattern_model = re.compile(r'<a href="javascript:void\(0\)" class="color-black">(.*?)</a>')
                        date_model = re.findall(date_pattern_model, date_section)
                        if len(date_model) != 0:
                            date_model = date_model[0]
                            text_html_model_7 = text_html_model_6.replace(date_model, date)
                            final_text = text_html_model_7

                section_pattern_model = re.compile(r'<a href=\"(.*?)\" title=\"(.*?)\" class="color-green font-weight-600 mx-1" id="hidden">(.*?)</a>')
                section_model = re.findall(section_pattern_model, text_html_model_7)[0]
                section_pattern = re.compile(r'<a href=\"(.*?)\" title=\"(.*?)\" class="external" rel="category tag">(.*?)</a>')
                section = re.findall(section_pattern, text_articol_model_old)[0]
                text_html_model_8 = text_html_model_7.replace(section_model[0], section[0])
                text_html_model_9 = text_html_model_8.replace(section_model[1], section[1])
                text_html_model_10 = text_html_model_9.replace(section_model[2], section[2])
                final_text = text_html_model_10

                lista_pattern = re.compile(r'<ul id="sidebarNavigation">([\s\S]*?)</ul>')
                lista = re.findall(lista_pattern, text_html)
                if len(lista) != 0:
                    lista = lista[0]
                    elemente_lista_pattern = re.compile(r'<li><a href=\"(.*?)\" title=\"(.*?)\">(.*?) \((.*?)\)</a></li>')
                    elemente_lista = re.findall(elemente_lista_pattern, lista)
                    if len(elemente_lista) != 0:
                        categories_pattern = re.compile(r'<!-- Categories -->([\s\S]*?)<!-- BOOKS START -->')
                        categories = re.findall(categories_pattern, text_html_model_10)[0]
                        elemente_lista_model_pattern = re.compile(r'<div class="categories-name">([\s\S]*?)</div>')
                        elemente_lista_model = re.findall(elemente_lista_model_pattern, categories)
                        template_category = read_text_from_file('C:\\Folder1\\category-name-en.txt')

                        for i in range(len(elemente_lista_model)):
                            new_template_category = template_category
                            a_pattern = re.compile(r'<a href=\"(.*?)\" title=\"(.*?)\">')
                            a = re.findall(a_pattern, new_template_category)[0]
                            p_pattern = re.compile(r'<p class="font-16 color-grey text-capitalize"><i class="fa fa-angle-right font-14 color-blue mr-1"></i> (.*?) <span>(.*?)</span> </p>')
                            p = re.findall(p_pattern, new_template_category)[0]
                            new_template_category = new_template_category.replace(a[0], elemente_lista[i][0])
                            new_template_category = new_template_category.replace(a[1], elemente_lista[i][1])
                            new_template_category = new_template_category.replace(p[0], elemente_lista[i][2])
                            new_template_category = new_template_category.replace(p[1], elemente_lista[i][3])
                            final_text = final_text.replace(elemente_lista_model[i], new_template_category)

                flags_pattern = re.compile(r'<!-- FLAGS_1 -->([\s\S]*?)<!-- FLAGS -->')
                flags = re.findall(flags_pattern, text_html)
                if len(flags) != 0:
                    flags = flags[0]
                    links_pattern = re.compile(r'<a href=\"(.*?)\">')
                    links = re.findall(links_pattern, flags)
                    if len(links) != 0:
                        flags_model = re.findall(flags_pattern, text_html_model_14)[0]
                        links_pattern_model = re.compile(r'<li><a cunt_code=\"\+\d+\" href=\"(.*?)\">')
                        links_model = re.findall(links_pattern_model, flags_model)
                        if len(links_model) != 0:
                            for i in range(len(links)):
                                final_text = final_text.replace(links_model[i], links[i])

                stars_php_pattern = re.compile(r'\$item_id = (.*?);')
                stars_php = re.findall(stars_php_pattern, text_html)
                stars_php_model = re.findall(stars_php_pattern, text_html_model_15)
                if len(stars_php) != 0:
                    stars_php = stars_php[0]
                    if len(stars_php_model) != 0:
                        stars_php_model = stars_php_model[0]
                        text_html_model_16 = text_html_model_15.replace(stars_php_model, stars_php)
                        final_text = text_html_model_16

                ult_art_pattern = re.compile(r'<!-- Ultimele articole -->([\s\S]*?)<!-- Ultimele articole final -->')
                ult_art_model_pattern = re.compile(r'<!-- Recent Post -->([\s\S]*?)<!-- Categories -->')
                ult_art = re.findall(ult_art_pattern, text_html)
                ult_art_model = re.findall(ult_art_model_pattern, text_html_model_16)
                if len(ult_art) != 0:
                    ult_art = ult_art[0]
                    if len(ult_art_model) != 0:
                        ult_art_model = ult_art_model[0]
                        articole_pattern = re.compile(r'<li><a href=\"(.*?)\">(.*?)</a></li>')
                        articole = re.findall(articole_pattern, ult_art)
                        if len(articole) != 0:
                            articole_model_pattern = re.compile(r'<a href=\"(.*?)\" class="color-grey">(.*?)</a>')
                            articole_model = re.findall(articole_model_pattern, ult_art_model)
                            if len(articole_model) != 0:
                                for i in range(len(articole)):
                                    final_text = final_text.replace(articole_model[i][0], articole[i][0])
                                    final_text = final_text.replace(articole_model[i][1], articole[i][1])

    file_path = os.path.join(cale_fisiere_gata, os.path.basename(cale_fisier_html))
    write_to_file(final_text, file_path)
    print("Scriere efectuata cu succes.")

def creare_fisiere_html(cale_folder_html, cale_fisiere_gata):
    count = 0

    fisiere_de_ignorat = [
        "webinar-a-black-square-into-the-dazzling-white.html",
        "webinar-a-king-for-my-kingdom.html",
        "webinar-convince-me-that-you-are-alive.html",
        "webinar-in-emptiness-is-hidden-the-fullness.html",
        "webinars.html",
        "webinar-the-circle-that-closes-all-senses.html",
        "webinar-the-dirigible-progress-of-leadership.html",
        "webinar-the-distinctive-color-of-leadership.html",
        "webinar-the-impetus-towards-excellence.html",
        "webinar-the-man-who-made-the-june-26.html",
        "webinar-the-mystery-of-leadership.html",
        "webinar-the-narrow-corridor-towards-the-heights-of-perfection.html",
        "webinar-the-road-of-truth.html",
        "webinar-the-sweet-source-of-perfection.html",
        "webinar-the-too-narrow-ladder-of-leadership.html",
        "webinar-the-unitary-whole-of-leadership.html",
        "webinar-the-weak-construction-of-leadership.html",
        "directory.html",
        "Python - EXEMPLU EXAMPLE.html",
        "y_key_e479323ce281e459.html"
    ]

    for f in os.listdir(cale_folder_html):
        if f.endswith('.html') and f not in fisiere_de_ignorat:
            cale_fisier_html = os.path.join(cale_folder_html, f)
            print("FISIER CURENT: ", cale_fisier_html)
            copiaza_continut_html(cale_fisier_html, cale_fisiere_gata)
            count += 1
    print("Numarul de fisiere modificate: ", count)

def main():
    creare_fisiere_html("C:\\Folder1\\fisiere_html", "C:\\Folder1\\fisiere_gata")

if __name__ == '__main__':
    main()
