import requests
from utils.logger import log_error

def check_response(response: requests.Response, name: str, url: str, results_dir: str):
    """Проверяет статус ответа и логирует ошибку при необходимости"""
    if response.status_code != 200:
        error = f"HTTP {response.status_code} — {response.reason} [{url}]"
        short_error = log_error(name, error, results_dir)
        raise Exception(short_error)
