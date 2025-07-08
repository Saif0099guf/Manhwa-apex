import requests, os, time
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://mgekox.com"
SAVE_DIR = "posts"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

os.makedirs(SAVE_DIR, exist_ok=True)

def get_manga_list():
    r = requests.get(f"{BASE_URL}/manga/", headers=HEADERS, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    return [a['href'] for a in soup.select("div.bsx > a")]

def get_chapters(manga_url):
    r = requests.get(manga_url, headers=HEADERS, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    return [a['href'] for a in soup.select("li.wp-manga-chapter > a")]

def get_images(chapter_url):
    r = requests.get(chapter_url, headers=HEADERS, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    return [img['src'] for img in soup.select(".reading-content img")]

def save_chapter(manga_name, chapter_slug, image_urls, prev_slug, next_slug):
    dirpath = os.path.join(SAVE_DIR, manga_name, chapter_slug)
    os.makedirs(dirpath, exist_ok=True)
    with open("index_template.html", encoding="utf-8") as t:
        html = t.read()
    title = f"{manga_name.replace('-', ' ').title()} — {chapter_slug}"
    body = ""
    if prev_slug:
        body += f'<a href="../{prev_slug}/">⟵ Previous</a> '
    if next_slug:
        body += f'<a style="float:right" href="../{next_slug}/">Next ⟶</a><br>'
    body += "\n".join(f'<img src="{u}" loading="lazy">' for u in image_urls)
    html = html.replace("{{TITLE}}", title).replace("{{CONTENT}}", body)
    with open(os.path.join(dirpath, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

def save_index(manga_data):
    with open("home_template.html", encoding="utf-8") as t:
        html = t.read()
    listing = "\n".join(
        f'<li><a href="posts/{m}/{c}/">{m.replace("-", " ").title()} - {c}</a></li>'
        for m, chapters in manga_data.items() for c in chapters
    )
    html = html.replace("{{LISTING}}", listing)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

def run():
    manga_links = get_manga_list()
    all_data = {}
    for link in manga_links[:10]:
        manga_name = link.strip("/").split("/")[-1]
        chapters = get_chapters(link)[:5]
        all_data[manga_name] = []
        slugs = [c.strip("/").split("/")[-1] for c in chapters]
        for i, ch_url in enumerate(chapters):
            ch_slug = slugs[i]
            prev_slug = slugs[i-1] if i > 0 else None
            next_slug = slugs[i+1] if i + 1 < len(slugs) else None
            imgs = get_images(ch_url)
            if imgs:
                save_chapter(manga_name, ch_slug, imgs, prev_slug, next_slug)
                all_data[manga_name].append(ch_slug)
            time.sleep(1)
    save_index(all_data)

if __name__ == "__main__":
    run()