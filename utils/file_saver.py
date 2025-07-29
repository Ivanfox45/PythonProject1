# utils/file_saver.py

import os
def save_text_file(source, date, text, filename, results_dir):
    path = os.path.join(results_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"Источник: {source}\nДата: {date}\n\n{text}")


