import argparse
import streamlit as st
import os
import sys
import shutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.parser import parse_legal_docs
from src.indexer import index_documents
from src.search import search_relevant_chunks, generate_answer

def reset_indexing():
    """Сбрасывает индексацию, удаляя файлы в data/output."""
    output_dir = "data/output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
        os.makedirs(output_dir)
        print("Индексация сброшена.")
        return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Legal Document Parser")
    parser.add_argument('--url', help="URL сайта для парсинга")
    parser.add_argument('--question', help="Вопрос для поиска ответа")
    parser.add_argument('--reset', action='store_true', help="Сбросить индексацию")
    args = parser.parse_args()

    if args.reset:
        reset_indexing()

    if args.url:
        print(f"Парсинг сайта: {args.url}")
        try:
            parse_legal_docs(args.url)
            print("Индексация документов...")
            index_documents()
        except Exception as e:
            print(f"Ошибка: {e}")
        if args.question:
            print(f"Вопрос: {args.question}")
            relevant_texts = search_relevant_chunks(args.question)
            if relevant_texts:
                answer = generate_answer(args.question, relevant_texts)
                print(f"Ответ: {answer}")
            else:
                print("Релевантные документы не найдены.")
    else:
        st.title("Юридический помощник")
        if st.button("Сбросить индексацию"):
            if reset_indexing():
                st.success("Индексация сброшена!")
            else:
                st.info("Индексация уже сброшена.")
        url = st.text_input("Введите URL сайта:")
        if st.button("Собрать документы"):
            try:
                parse_legal_docs(url)
                index_documents()
                st.success("Документы собраны и проиндексированы!")
            except Exception as e:
                st.error(f"Ошибка: {e}")
        question = st.text_input("Задайте вопрос:")
        if st.button("Получить ответ"):
            if os.path.exists("data/output/legal_index.faiss"):
                relevant_texts = search_relevant_chunks(question)
                if relevant_texts:
                    answer = generate_answer(question, relevant_texts)
                    st.write("Ответ:", answer)
                else:
                    st.error("Релевантные документы не найдены.")
            else:
                st.error("Сначала соберите документы.")

if __name__ == "__main__":
    main()