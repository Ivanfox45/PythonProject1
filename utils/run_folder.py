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


def create_readme(
    results_dir,
    run_name,
    site_keys,
    success=None,
    failed=None,
    elapsed=None,
):
    """Create README.txt with run summary."""

    readme_path = os.path.join(results_dir, "README.txt")
    try:
        with open(readme_path, "w", encoding="utf-8") as f:
            f.write(f"📝 Запуск: {run_name}\n")
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"📅 Дата и время: {timestamp}\n")
            f.write(f"🔢 Всего источников: {len(site_keys)}\n")
            if elapsed is not None:
                f.write(f"⏱ Время выполнения: {elapsed:.2f} сек\n\n")
            else:
                f.write("\n")

            if success:
                for name in success:
                    f.write(f"[✓] {name} — успешно\n")

            if failed:
                for name, err in failed.items():
                    f.write(f"[X] {name} — ошибка: {err}\n")
    except Exception as e:
        print(f"[❌] Ошибка при создании README.txt: {e}")
