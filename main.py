import json
import time
import re
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

with open('config.json', 'r') as f:
    data = json.load(f)

chrome_driver_path = os.getenv('CHROMEDRIVER_PATH', data.get('chrome_driver_path', ''))
urls = data['urls']
base_url = 'https://help.boomi.com'
output_folder = 'knowledge_base'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.binary_location = os.getenv('CHROME_BIN', None)
chrome_service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

def fetch_html(url):
    driver.get(url)
    time.sleep(2)
    return driver.page_source

def extract_article_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    content_div = soup.find('div', class_='theme-doc-markdown markdown')
    return str(content_div) if content_div else ""

def fix_relative_urls(html):
    soup = BeautifulSoup(html, 'html.parser')
    for a in soup.find_all('a', href=True):
        href = a['href']
        parsed_href = urlparse(href)
        if not parsed_href.scheme and not parsed_href.netloc:
            a['href'] = urljoin(base_url, href)
        else:
            a['href'] = href
    for img in soup.find_all('img', src=True):
        src = img['src']
        if src.startswith('/'):
            img['src'] = urljoin(base_url, src)
    return str(soup)

def remove_class_id_and_svg(html):
    soup = BeautifulSoup(html, 'html.parser')
    for tag in soup.find_all(True):
        if 'class' in tag.attrs:
            del tag.attrs['class']
        if 'id' in tag.attrs:
            del tag.attrs['id']
    for svg in soup.find_all('svg'):
        svg.decompose()
    return str(soup)

def build_breadcrumbs(path):
    return " > ".join(f"<a href='{url}'>{title}</a>" for title, url in path)

def sanitize_filename(title):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', title) + '.html'

def process_url(url_obj, path, indent_level=0):
    url = url_obj['url']
    html = fetch_html(url)
    article_content = extract_article_content(html)
    article_content = fix_relative_urls(article_content)
    article_content = remove_class_id_and_svg(article_content)

    soup = BeautifulSoup(article_content, 'html.parser')
    first_heading = soup.find('h1')
    title = first_heading.text if first_heading else url
    filename = sanitize_filename(title)
    
    path.append((title, url))
    breadcrumbs = build_breadcrumbs(path)
    html_output = f"<h{indent_level + 1}>{title}</h{indent_level + 1}>\n\n"
    html_output += f"<p><strong>Path:</strong> {breadcrumbs}</p>\n\n"

    if first_heading:
        first_heading.extract()
    content_html = str(soup)
    html_output += content_html + "\n\n"
    
    for child in url_obj.get('children', []):
        _, child_content = process_url(child, path[:], indent_level + 1)
        html_output += child_content
    
    path.pop()
    return filename, html_output

os.makedirs(output_folder, exist_ok=True)

for url_obj in urls:
    filename, content = process_url(url_obj, [])
    file_path = os.path.join(output_folder, filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

driver.quit()

print("HTML files generated successfully")