from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_vector_db(text_files, model_name="all-MiniLM-L6-v2", index_dir="data/output"):
    """Создает векторную базу из текстовых файлов."""
    try:
        model = SentenceTransformer(model_name)
        texts = []
        for file in text_files:
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
                # Разбиваем на куски по ~500 символов
                chunks = [text[i:i+500] for i in range(0, len(text), 500)]
                texts.extend(chunks)

        # Создаем эмбеддинги
        embeddings = model.encode(texts, show_progress_bar=True)

        # Сохраняем FAISS индекс
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings)
        faiss.write_index(index, os.path.join(index_dir, "legal_index.faiss"))

        # Сохраняем тексты
        with open(os.path.join(index_dir, "texts.pkl"), "wb") as f:
            pickle.dump(texts, f)

        # Устанавливаем флаг блокировки
        with open(os.path.join(index_dir, "indexing_done.flag"), "w") as f:
            f.write("1")
        logging.info("Векторная база создана, внешние запросы заблокированы.")
    except Exception as e:
        logging.error(f"Ошибка при создании векторной базы: {e}")

def index_documents(output_dir="data/output"):
    """Индексирует все текстовые файлы в папке."""
    text_files = [os.path.join(output_dir, f) for f in os.listdir(output_dir) if f.endswith(".txt")]
    if text_files:
        create_vector_db(text_files)
    else:
        logging.warning("Текстовые файлы для индексации не найдены.")