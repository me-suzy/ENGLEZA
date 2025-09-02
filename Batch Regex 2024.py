import os
import re
import regex

def process_html_content(content):
    # Pasul 1: Transformă <p class="text_obisnuit"><span class="text_obisnuit2">Leadership: în <p class="text_obisnuit2">Leadership:
    pattern1 = r'<p class="text_obisnuit"><span class="text_obisnuit2">(Leadership:.*?)</span>(.*?)</p>'
    content = re.sub(pattern1, r'<p class="text_obisnuit2">\1\2</p>', content, flags=re.DOTALL)



    return content


def process_html_content(content):
    # Definim BSR, ESR și FR
    BSR = r'<p class="text_obisnuit2">'
    ESR = r'</p>'
    FR = r'</?span>'

    # Folosim formula Generic Regex pentru a elimina span-urile
    pattern = fr'(?s)(?:{BSR}|(?!\A)\G)(?:(?!{ESR}).)*?\K(?:{FR})'
    content = regex.sub(pattern, '', content)



    return content

def clean_html_content(content):

    # Elimină toate tagurile <span class="text_obisnuit"> și </span> doar din interiorul tagurilor <p class="text_obisnuit">...</p>
    content = regex.sub(r'(<p class="text_obisnuit">)\s*<span class="text_obisnuit">(.*?)</span>\s*(</p>)', r'\1\2\3', content)


    # Păstrează <span class="text_obisnuit2">, dar elimină alte taguri <span> și </span>
    pattern = r'(<p class="text_obisnuit2">.*?)(</?span(?!\s+class="text_obisnuit2")[^>]*>)(.*?</p>)'
    replacement = r'\1\3'
    content = regex.sub(pattern, replacement, content, flags=regex.DOTALL | regex.IGNORECASE)

    return content

    # Scoate orice <strong> si </strong>
    pattern = r'(<p class="text_obisnuit(?:2)?">.*?)(</?strong>)(.*?</p>)'

    # Funcția de înlocuire
    def remove_strong(match):
        return match.group(1) + match.group(3)

    # Aplicarea înlocuirii
    content = regex.sub(pattern, remove_strong, content, flags=regex.DOTALL)


    # Elimină toate tagurile <em></em> goale din conținut
    content = regex.sub(r'<em></em>', '', content)

    # Înlocuiește <span class="text_obisnuit">...</span> cu <p class="text_obisnuit">...</p>
    content = regex.sub(r'(?-s)</p>\s+.\K(<span class="text_obisnuit">)(.*?)(</span>)', r'<p class="text_obisnuit">\2</p>', content)

    # Înlocuiește <span class="text_obisnuit">...</span> cu <p class="text_obisnuit">...</p>
    content = regex.sub(r'(<p><span class="text_obisnuit">)(.*)(</span></p>)', r'<p class="text_obisnuit">\2</p>', content)

    # Înlocuiește <span class="text_obisnuit">...</span> cu <p class="text_obisnuit">...</p>
    content = regex.sub(r'(\w+)(<em>)(\w+)(</em>)', r'\1\x20\3', content)

    # Înlocuiește <span class="text_obisnuit">...</span> cu <p class="text_obisnuit">...</p>
    content = regex.sub(r'(.*<p>&nbsp;</p>).*\R.*(<p class="text_obisnuit">)', r'           <br><br>\n \2', content)

    # Înlocuiește <span class="text_obisnuit">...</span> cu <p class="text_obisnuit">...</p>
    content = regex.sub(r'(\h*)<p class="text_obisnuit"></p>(?=\h*\R\h*<p class="text_obisnuit">)', r'           <br><br>', content)

    # Înlocuiește <span class="text_obisnuit">...</span> cu <p class="text_obisnuit">...</p>
    content = regex.sub(r'(\h*)<p>&nbsp;</p>(?=\h*\R\h*<p class="text_obisnuit">)', r'           <br><br>', content)

    # Elimină spațiile albe și newline-urile dintre tagurile <p class="text_obisnuit"> și </p>
    content = regex.sub(r'(?-si:<p class="text_obisnuit">|(?!\A)\G)(?s-i:(?!</p>).)*?\K\s+', r' ', content)

    # Elimină spațiile albe și newline-urile dintre tagurile <p class="text_obisnuit"> și </p>
    content = regex.sub(r'(<p class="text_obisnuit">)(\* Not&#259;:)', r'\1<span class="text_obisnuit2">\2</span>', content)
    content = regex.sub(r'(<p class="text_obisnuit">)(\* Notă:)', r'\1<span class="text_obisnuit2">\2</span>', content)
    content = regex.sub(r'(<p class="text_obisnuit">)(\* Note:)', r'\1<span class="text_obisnuit2">\2</span>', content)

    content = regex.sub(r'<p><span class="text_obisnuit2">(.*?)</span></p>', r'<p class="text_obisnuit2">\1</p>', content)





    return content

def process_files_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.html'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Procesăm conținutul fișierului
            cleaned_content = process_html_content(content)

            # Verificăm dacă au fost făcute modificări și salvăm fișierul dacă este cazul
            if content != cleaned_content:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_content)
                print(f"Modificări făcute în fișierul: {filename}")

# Specifică directorul cu fișierele HTML
directory = r'd:\55'
process_files_in_directory(directory)
