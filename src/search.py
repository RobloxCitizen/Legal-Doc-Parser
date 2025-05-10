from sentence_transformers import SentenceTransformer
import faiss
import pickle
import numpy as np
import json
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_path="config.json"):
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Ошибка загрузки конфигурации: {e}")
        return {}

def search_relevant_chunks(query, k=3, model_name="all-MiniLM-L6-v2"):
    try:
        model = SentenceTransformer(model_name)
        query_embedding = model.encode([query])[0]
        index = faiss.read_index("data/output/legal_index.faiss")
        with open("data/output/texts.pkl", "rb") as f:
            texts = pickle.load(f)
        distances, indices = index.search(np.array([query_embedding]), k)
        return [texts[idx] for idx in indices[0]]
    except Exception as e:
        logging.error(f"Ошибка при поиске: {e}")
        return []

def generate_answer(query, relevant_texts):
    try:
        config = load_config()
        api_key = os.getenv("OPENAI_API_KEY", config.get("openai_api_key", ""))
        if not api_key:
            logging.error("OpenAI API ключ не найден.")
            return "Ошибка: OpenAI API ключ не настроен. Пример: 'В документах нет информации о возврате.'"
        return "API ключ есть, но OpenAI не подключён в этой версии."
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return f"Ошибка: {str(e)}. Пример: 'В документах нет информации о возврате.'"