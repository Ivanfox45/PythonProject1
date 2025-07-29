from utils.run_folder import get_next_run_folder, create_readme
from parsers.base_sites import SITES
from utils.logger import log_error
from datetime import datetime
import time
import os
import sys

def run_parser(name, ParserClass, results_dir, success_list):
    readme_path = os.path.join(results_dir, "README.txt")
    try:
        # Создаем экземпляр парсера без передачи results_dir
        parser = ParserClass()
        # Если нужно установить results_dir, делаем это после создания
        if hasattr(parser, 'set_results_dir'):
            parser.set_results_dir(results_dir)
        parser.parse()
        print(f"[✓] {name} — успешно")
        with open(readme_path, "a", encoding="utf-8") as f:
            f.write(f"[✓] {name} — успешно\n")
        success_list.append(name)

    except Exception as e:
        short_error = log_error(name, str(e), results_dir)
        with open(readme_path, "a", encoding="utf-8") as f:
            f.write(f"[X] {name} — ошибка: {short_error}\n")
        print(f"[X] {name} — ошибка: {short_error}")
        return short_error

def parse_unparsed_sites(results_dir, run_name):
    print("\n[🔁] Повторный парсинг: только не обработанные сайты")

    parsed_names = {
        f.split("_")[0]
        for f in os.listdir(results_dir)
        if f.endswith(".txt")
    }

    success = []
    failed = {}

    for name, parser_class in SITES.items():
        if name in parsed_names:
            continue  # уже обработан

        error = run_parser(name, parser_class, results_dir, success)
        if error:
            failed[name] = error

    print("\n[📃] Повторная запись README.txt с учётом новых данных...")
    create_readme(
        results_dir,
        run_name,
        site_keys=SITES.keys(),
        success=success,
        failed=failed,
        elapsed=None
    )

def main():
    resume_mode = "--resume" in sys.argv

    if resume_mode:
        base = "results"
        all_runs = sorted([d for d in os.listdir(base) if d.startswith("run_")])
        if not all_runs:
            print("[❌] Нет предыдущих запусков для повторной попытки.")
            return
        run_name = all_runs[-1]
        results_dir = os.path.join(base, run_name)
        print(f"[♻️] Повторная попытка запуска: {run_name}")
        parse_unparsed_sites(results_dir, run_name)
        return

    # Обычный режим
    results_dir, run_name = get_next_run_folder()
    print(f"[📦] Запуск: {run_name}")
    print(f"[📁] Сохранение всех результатов в: {results_dir}")

    start = time.time()
    success = []
    failed = {}

    for name, parser_class in SITES.items():
        error = run_parser(name, parser_class, results_dir, success)
        if error:
            failed[name] = error

    elapsed = time.time() - start

    create_readme(
        results_dir,
        run_name,
        site_keys=SITES.keys(),
        success=success,
        failed=failed,
        elapsed=elapsed
    )

if __name__ == "__main__":
    main()