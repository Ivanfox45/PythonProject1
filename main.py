import argparse
import os
import time

from utils.run_folder import get_next_run_folder, create_readme
from parsers.base_sites import SITES
from utils.logger import log_error


def run_parser(name, ParserClass, results_dir, success_list, infection=None):
    """Execute a single parser and log its outcome."""
    readme_path = os.path.join(results_dir, "README.txt")
    try:
        try:
            parser = ParserClass(results_dir, infection)
        except TypeError:
            parser = ParserClass(infection=infection)
            if hasattr(parser, "set_results_dir"):
                parser.set_results_dir(results_dir)
        parser.parse()
        print(f"[✓] {name} — успешно")
        with open(readme_path, "a", encoding="utf-8") as fh:
            fh.write(f"[✓] {name} — успешно\n")
        success_list.append(name)
    except Exception as e:
        short_error = log_error(name, str(e), results_dir)
        with open(readme_path, "a", encoding="utf-8") as fh:
            fh.write(f"[X] {name} — ошибка: {short_error}\n")
        print(f"[X] {name} — ошибка: {short_error}")
        return short_error


def parse_unparsed_sites(results_dir, run_name, site_keys, infection=None):

    print("\n[🔁] Повторный парсинг: только не обработанные сайты")

    parsed_names = {
        f.split("_")[0]
        for f in os.listdir(results_dir)
        if f.endswith(".txt")
    }

    success = []
    failed = {}

    for name in site_keys:
        if name in parsed_names:
            continue
        parser_class = SITES[name]
        error = run_parser(name, parser_class, results_dir, success, infection)
        if error:
            failed[name] = error

    print("\n[📃] Повторная запись README.txt с учётом новых данных...")
    create_readme(
        results_dir,
        run_name,
        site_keys=site_keys,
        success=success,
        failed=failed,
        elapsed=None,
    )


def main():
    parser = argparse.ArgumentParser(description="Run site parsers")
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Продолжить последний запуск, парся только неудачные сайты",
    )
    parser.add_argument(
        "--sites",
        nargs="+",
        help="Имена сайтов для парсинга (по умолчанию все)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        dest="list_sites",
        help="Показать доступные сайты и выйти",
    )
    parser.add_argument(
        "--infection",
        help="Строка для поиска конкретной инфекции",
    )
    args = parser.parse_args()

    if args.list_sites:
        for key in sorted(SITES.keys()):
            print(key)
        return

    site_keys = args.sites if args.sites else list(SITES.keys())

    if args.resume:
        base = "results"
        all_runs = sorted(
            [d for d in os.listdir(base) if d.startswith("run_")]
        )
        if not all_runs:
            print("[❌] Нет предыдущих запусков для повторной попытки.")
            return
        run_name = all_runs[-1]
        results_dir = os.path.join(base, run_name)
        print(f"[♻️] Повторная попытка запуска: {run_name}")
        parse_unparsed_sites(results_dir, run_name, site_keys, args.infection)
        return

    results_dir, run_name = get_next_run_folder()
    print(f"[📦] Запуск: {run_name}")
    print(f"[📁] Сохранение всех результатов в: {results_dir}")

    start = time.time()
    success = []
    failed = {}

    for name in site_keys:
        parser_class = SITES[name]
        error = run_parser(
            name, parser_class, results_dir, success, args.infection
        )
        if error:
            failed[name] = error

    elapsed = time.time() - start

    create_readme(
        results_dir,
        run_name,
        site_keys=site_keys,
        success=success,
        failed=failed,
        elapsed=elapsed,
    )


if __name__ == "__main__":
    main()
