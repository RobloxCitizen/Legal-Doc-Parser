from trafilatura import extract
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clean_text(html_content):
    """Очищает HTML-контент, удаляя теги, лишние пробелы и нормализуя текст."""
    try:
        # Извлекаем основной текст с помощью trafilatura
        cleaned_text = extract(html_content, include_formatting=False, deduplicate=True)
        if not cleaned_text:
            logging.warning("Не удалось извлечь текст из HTML.")
            return ""
        # Нормализация пробелов
        cleaned_text = ' '.join(cleaned_text.split())
        logging.info("Текст успешно очищен.")
        return cleaned_text
    except Exception as e:
        logging.error(f"Ошибка при очистке текста: {e}")
        return ""