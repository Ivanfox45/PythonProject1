import os
from datetime import datetime

def get_next_run_folder(base="results"):
    os.makedirs(base, exist_ok=True)
    existing = [d for d in os.listdir(base) if d.startswith("run_")]
    numbers = [int(d[4:]) for d in existing if d[4:].isdigit()]
    next_id = max(numbers) + 1 if numbers else 1
    run_folder = f"run_{next_id:03d}"
    path = os.path.join(base, run_folder)

    os.makedirs(path, exist_ok=True)
    os.makedirs(os.path.join(path, "google"), exist_ok=True)
    os.makedirs(os.path.join(path, "html"), exist_ok=True)
    os.makedirs(os.path.join(path, "errors"), exist_ok=True)

    return path, run_folder

def create_readme(results_dir, run_name, site_keys, success=None, failed=None, elapsed=None):
    print("[DEBUG] Внутри функции create_readme")  # 👈 добавим это

    readme_path = os.path.join(results_dir, "README.txt")
    print(f"[DEBUG] Попытка создать файл по пути: {readme_path}")  # 👈 ещё одно


    try:
        print(f"[📄] README.txt успешно создан в: {readme_path}")
        with open(readme_path, "r", encoding="utf-8") as f:
            print("[📄] Содержимое README.txt:\n" + f.read())

            f.write(f"📝 Запуск: {run_name}\n")
            f.write(f"📅 Дата и время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"🔢 Всего источников: {len(site_keys)}\n")
            if elapsed is not None:
                f.write(f"⏱ Время выполнения: {elapsed:.2f} сек\n\n")
            else:
                f.write("\n")

            if success:
                f.write("✅ Успешно выполнены:\n")
                for name in success:
                    f.write(f"  - {name}\n")

            if failed:
                f.write("\n❌ Ошибки:\n")
                for name, err in failed.items():
                    f.write(f"  - {name}: {err}\n")
        print(f"[📄] README.txt успешно создан в: {readme_path}")
    except Exception as e:
        print(f"[❌] Ошибка при создании README.txt: {e}")
