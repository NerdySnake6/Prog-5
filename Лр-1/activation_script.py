"""Подключить импорт Python-модулей и пакетов по HTTP через requests."""

import sys
from importlib.abc import Loader, PathEntryFinder
from importlib.util import spec_from_loader

import requests

TIMEOUT = 5


class URLLoader(Loader):
    """Загрузить и выполнить исходный код модуля по URL."""

    def create_module(self, spec):
        """Поручить создание модуля самому Python."""
        return None

    def exec_module(self, module):
        """Скачать код и выполнить его в пространстве имён модуля."""
        url = module.__spec__.origin
        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()
        except requests.RequestException as error:
            raise ImportError(f"Не удалось загрузить модуль: {url}") from error
        module.__file__ = url
        code = compile(response.content, url, "exec")
        exec(code, module.__dict__)


class URLFinder(PathEntryFinder):
    """Найти обычный модуль или пакет в удалённом каталоге."""

    def __init__(self, url):
        """Запомнить адрес каталога."""
        self.url = url.rstrip("/")

    def find_spec(self, fullname, target=None):
        """Проверить наличие пакета, затем обычного файла модуля."""
        name = fullname.rsplit(".", 1)[-1]
        for suffix, is_package in (("/__init__.py", True), (".py", False)):
            origin = f"{self.url}/{name}{suffix}"
            try:
                response = requests.get(origin, timeout=TIMEOUT)
                if response.status_code == 404:
                    continue
                response.raise_for_status()
            except requests.RequestException as error:
                raise ImportError(
                    f"Не удалось обратиться к серверу: {origin}"
                ) from error
            spec = spec_from_loader(
                fullname, URLLoader(), origin=origin, is_package=is_package
            )
            if is_package:
                spec.submodule_search_locations = [f"{self.url}/{name}"]
            return spec
        return None


def url_hook(path):
    """Обработать HTTP-адрес из sys.path и вернуть поисковик модулей."""
    if not isinstance(path, str) or not path.startswith(("http://", "https://")):
        raise ImportError
    try:
        response = requests.get(path, timeout=TIMEOUT)
        # GitHub Raw не отдаёт список каталога, но отдаёт отдельные файлы.
        if response.status_code not in (400, 404):
            response.raise_for_status()
    except requests.RequestException as error:
        print(f"Сервер недоступен: {path}", file=sys.stderr)
        raise ImportError(f"Не удалось открыть {path}") from error
    return URLFinder(path)


if url_hook not in sys.path_hooks:
    sys.path_hooks.append(url_hook)
    sys.path_importer_cache.clear()
