import os
import requests
from bs4 import BeautifulSoup, Comment
import time

def get_image_from_article_page(url):
    """Extrage imaginea din pagina individuală"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Caută imaginea în feature-img-wrap
        feature_img = soup.find('div', class_='feature-img-wrap')
        if feature_img:
            img = feature_img.find('img')
            if img and img.get('src'):
                return img.get('src'), img.get('alt', '')

            # Caută video YouTube
            iframe = feature_img.find('iframe')
            if iframe and 'youtube.com/embed/' in str(iframe.get('src', '')):
                iframe_src = iframe.get('src')
                video_id = iframe_src.split('/embed/')[-1].split('?')[0]
                thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                return thumbnail_url, iframe.get('title', 'Video YouTube')

        # Fallback
        for img in soup.find_all('img'):
            src = img.get('src', '')
            if 'images/' in src and not src.endswith('.gif'):
                return src, img.get('alt', '')

        return None, None

    except Exception as e:
        print(f"Eroare imagine din {url}: {e}")
        return None, None

def process_html_file(file_path, base_url="https://neculaifantanaru.com"):
    """Procesează fișierul HTML"""

    print(f"Procesez: {file_path}")

    try:
        # Citește fișierul
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # Adaugă CSS dacă nu există
        css_code = '''    <style type="text/css">
        .article-card-new { padding: 15px; margin-bottom: 20px; border-bottom: 1px solid #eee; }
        .desktop-layout .article-header { display: flex; gap: 20px; align-items: flex-start; }
        .desktop-layout .article-image-container { flex-shrink: 0; width: 180px; }
        .desktop-layout .article-card-img { width: 100%; height: 135px; object-fit: cover; border-radius: 8px; box-shadow: 0 3px 15px rgba(0,0,0,0.12); }
        .desktop-layout .article-header-content { flex: 1; padding-top: 10px; }
        .desktop-layout .article-spacing { height: 10px; }
        .desktop-layout .article-body { margin-top: 10px; }
        .mobile-layout { text-align: left; }
        .mobile-image-container { width: 100%; margin-bottom: 15px; }
        .mobile-article-img { width: 100%; height: 200px; object-fit: cover; border-radius: 8px; }
        .mobile-title { margin-bottom: 15px; }
        .mobile-lead { margin-bottom: 15px; }
        .mobile-date { margin-bottom: 20px; }
    </style>'''

        if 'article-card-new' not in content:
            head_pos = content.find('</head>')
            if head_pos != -1:
                content = content[:head_pos] + css_code + '\n' + content[head_pos:]

        # Parsează HTML pentru a găsi articolele
        soup = BeautifulSoup(content, 'html.parser')

        # Găsește comentariile - CORECTAT
        start_comment = None
        end_comment = None

        for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
            if 'ARTICOL START' in str(comment):
                start_comment = comment
            elif 'ARTICOL FINAL' in str(comment):
                end_comment = comment
                break

        if not start_comment or not end_comment:
            print(f"Nu găsesc comentariile în {file_path}")
            return

        # Găsește toate articolele între comentarii
        current = start_comment.next_sibling
        articles = []

        while current and current != end_comment:
            if hasattr(current, 'name') and current.name == 'article':
                if current.get('class') and 'blog-box' in current.get('class'):
                    articles.append(current)
            current = current.next_sibling

        print(f"Găsite {len(articles)} articole")

        if not articles:
            print(f"Nu am găsit articole în {file_path}")
            return

        # Procesează fiecare articol
        new_articles = []

        for i, article in enumerate(articles):
            print(f"  Procesez articolul {i+1}/{len(articles)}")

            try:
                # Extrage datele din articol
                title_link = article.find('h2', class_='custom-h1')
                if not title_link:
                    continue

                link_tag = title_link.find('a')
                if not link_tag:
                    continue

                title = link_tag.get_text(strip=True)
                url = link_tag.get('href')

                # Data
                time_elem = article.find('time')
                date = time_elem.get_text(strip=True).replace('On ', '') if time_elem else ""

                # Categoria
                category_link = article.find('a', class_='color-green')
                category = category_link.get_text(strip=True) if category_link else ""
                category_url = category_link.get('href') if category_link else ""

                # Autorul
                author_elem = article.find('span', id='hidden2')
                author = author_elem.get_text(strip=True).replace('by ', '') if author_elem else "Neculai Fantanaru"

                # Descrierea
                desc_p = article.find('p', class_='mb-35px')
                description = desc_p.get_text(strip=True) if desc_p else ""

                # URL complet
                if url.startswith('/'):
                    full_url = base_url + url
                elif not url.startswith('http'):
                    full_url = base_url + '/' + url
                else:
                    full_url = url

                # Extrage imaginea
                img_src, img_alt = get_image_from_article_page(full_url)

                if not img_src:
                    print(f"    Nu am găsit imagine pentru {title}")
                    img_src = "https://neculaifantanaru.com/images/default-article.jpg"
                    img_alt = title
                else:
                    print(f"    Găsită imagine: {img_src}")

                # URL complet pentru imagine
                if img_src and img_src.startswith('/'):
                    img_src = base_url + img_src
                elif img_src and not img_src.startswith('http'):
                    img_src = base_url + '/' + img_src

                # Creează noul HTML
                new_article_html = f'''                    <article class="blog-box heading-space-half">
    <div class="blog-listing-inner news_item">
        <div class="article-card-new">
            <!-- Layout DESKTOP -->
            <div class="desktop-layout d-none d-md-block">
                <div class="article-header d-flex">
                    <div class="article-image-container">
                        <a href="{url}">
                            <img src="{img_src}" alt="{img_alt}" class="article-card-img">
                        </a>
                    </div>
                    <div class="article-header-content">
                        <h2 class="custom-h1" itemprop="name">
                            <a href="{url}" class="color-black">{title}</a>
                        </h2>
                        <div class="article-spacing"></div>
                        <div class="article-spacing"></div>
                        <div class="blog-post d-flex align-items-center flex-wrap">
                            <i class="fa fa-calendar mx-1"></i>
                            <time datetime="{date.split()[-1]}" class="color-black">{date}, in</time>
                            <a href="{category_url}" class="color-green font-weight-600 mx-1">{category}</a>
                        </div>
                        <div class="author-info color-black">by {author}</div>
                    </div>
                </div>
                <div class="article-body">
                    <div class="article-spacing"></div>
                    <div class="article-spacing"></div>
                    <p class="color-grey line-height-25px">{description}</p>
                    <a href="{url}" class="btn-setting color-black btn-hvr-up btn-blue btn-hvr-pink">
                        read more<span class="sr-only"> despre {title}</span>
                    </a>
                </div>
            </div>
            <!-- Layout MOBIL -->
            <div class="mobile-layout d-block d-md-none">
                <div class="mobile-image-container">
                    <a href="{url}">
                        <img src="{img_src}" alt="{img_alt}" class="mobile-article-img">
                    </a>
                </div>
                <h2 class="custom-h1 mobile-title">
                    <a href="{url}" class="color-black">{title}</a>
                </h2>
                <p class="color-grey line-height-25px mobile-lead">{description}</p>
                <div class="blog-post mobile-date">
                    <i class="fa fa-calendar mx-1"></i>
                    <time datetime="{date.split()[-1]}" class="color-black">{date}, in</time>
                    <a href="{category_url}" class="color-green font-weight-600 mx-1">{category}</a>
                </div>
                <a href="{url}" class="btn-setting color-black btn-hvr-up btn-blue btn-hvr-pink mobile-read-more">
                    Read More<span class="sr-only"> despre {title}</span>
                </a>
            </div>
        </div>
    </div>
</article>'''

                new_articles.append(new_article_html)
                time.sleep(0.5)  # Pauză pentru server

            except Exception as e:
                print(f"    Eroare la procesarea articolului: {e}")
                continue

        # Înlocuiește în conținutul original
        if new_articles:
            # Găsește pozițiile comentariilor în string
            start_pos = content.find('<!-- ARTICOL START -->')
            end_pos = content.find('<!-- ARTICOL FINAL -->')

            if start_pos != -1 and end_pos != -1:
                start_replace = start_pos + len('<!-- ARTICOL START -->')

                # Construiește noul conținut
                new_articles_content = '\n' + '\n'.join(new_articles) + '\n\t\t\t\t\t'

                final_content = (
                    content[:start_replace] +
                    new_articles_content +
                    content[end_pos:]
                )

                # Salvează doar dacă e diferit
                if final_content != original_content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(final_content)
                    print(f"✓ SALVAT: {file_path}")
                else:
                    print(f"- Neschimbat: {file_path}")
            else:
                print(f"✗ Nu găsesc pozițiile comentariilor în {file_path}")

    except Exception as e:
        print(f"✗ Eroare la procesarea {file_path}: {e}")

def main():
    files = [
        "index.html", "lideri-si-atitudine.html", "leadership-magic.html", "leadership-de-succes.html",
        "hr-resurse-umane.html", "legile-conducerii.html", "leadership-total.html",
        "leadership-de-durata.html", "principiile-conducerii.html", "leadership-plus.html",
        "calitatile-unui-lider.html", "leadership-de-varf.html", "leadership-impact.html",
        "dezvoltare-personala.html", "aptitudini-si-abilitati-de-leadership.html",
        "leadership-real.html", "leadership-de-baza.html", "leadership-360.html",
        "leadership-pro.html", "leadership-expert.html", "leadership-know-how.html",
        "jurnal-de-leadership.html", "alpha-leadership.html", "leadership-on-off.html",
        "leadership-deluxe.html", "leadership-xxl.html", "leadership-50-extra.html",
        "leadership-fusion.html", "leadership-v8.html", "leadership-x3-silver.html",
        "leadership-q2-sensitive.html", "leadership-t7-hybrid.html", "leadership-n6-celsius.html",
        "leadership-s4-quartz.html", "leadership-gt-accent.html", "leadership-fx-intensive.html",
        "leadership-iq-light.html", "leadership-7th-edition.html", "leadership-xs-analytics.html",
        "leadership-z3-extended.html", "leadership-ex-elite.html", "leadership-w3-integra.html",
        "leadership-sx-experience.html", "leadership-y5-superzoom.html", "performance-ex-flash.html",
        "leadership-mindware.html", "leadership-r2-premiere.html", "leadership-y4-titanium.html",
        "leadership-quantum-xx.html"
    ]

    base_path = r"e:\Carte\BB\17 - Site Leadership\Principal 2022\ro"

    print("Începe procesarea...")

    for file_name in files:
        file_path = os.path.join(base_path, file_name)
        if os.path.exists(file_path):
            process_html_file(file_path)
        else:
            print(f"✗ Nu există: {file_path}")
        print("-" * 30)

    print("Finalizat!")

if __name__ == "__main__":
    main()