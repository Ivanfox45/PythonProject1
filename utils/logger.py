import os
from datetime import datetime

def log_error(source, message, results_dir=None):
    os.makedirs("logs", exist_ok=True)
    with open("logs/errors.log", "a", encoding="utf-8") as f:
        f.write(f"[{source}] {message}\n")
    if results_dir:
        with open(os.path.join(results_dir, "errors.txt"), "a", encoding="utf-8") as f:
            f.write(f"[{source}] {message}\n")
    return message[:200]  # короткая версия для вывода


def log_success(source, message):
    os.makedirs("logs", exist_ok=True)
    with open("logs/success.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] [{source}] ✅ {message}\n")
