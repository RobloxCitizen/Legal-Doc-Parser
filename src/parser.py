import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin
import logging
from src.cleaner import clean_text

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_path="config.json"):
    """Загружает конфигурацию из JSON-файла."""
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Ошибка загрузки конфигурации: {e}")
        return {"legal_pages": []}

def fetch_page(url):
    """Скачивает содержимое страницы по URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        logging.error(f"Ошибка при загрузке {url}: {e}")
        return None

def find_legal_links(base_url):
    """Ищет ссылки на юридические страницы."""
    config = load_config()
    legal_pages = config.get("legal_pages", [])
    legal_urls = []

    html_content = fetch_page(base_url)
    if not html_content:
        return legal_urls

    soup = BeautifulSoup(html_content, 'html.parser')
    for link in soup.find_all('a', href=True):
        href = link['href']
        for page in legal_pages:
            if page in href:
                full_url = urljoin(base_url, href)
                legal_urls.append(full_url)
                logging.info(f"Найдена юридическая страница: {full_url}")

    return list(set(legal_urls))

def save_text(url, text, output_dir="data/output"):
    """Сохраняет текст в файл."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = url.replace('https://', '').replace('http://', '').replace('/', '_') + '.txt'
    filepath = os.path.join(output_dir, filename)
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        logging.info(f"Текст сохранен: {filepath}")
    except Exception as e:
        logging.error(f"Ошибка сохранения файла {filepath}: {e}")

def parse_legal_docs(base_url):
    """Основная функция для парсинга юридических документов."""
    legal_urls = find_legal_links(base_url)
    if not legal_urls:
        logging.warning(f"Юридические страницы на {base_url} не найдены.")
        return

    for url in legal_urls:
        html_content = fetch_page(url)
        if html_content:
            cleaned_text = clean_text(html_content)
            if cleaned_text:
                save_text(url, cleaned_text)
            else:
                logging.warning(f"Не удалось очистить текст для {url}")