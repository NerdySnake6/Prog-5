"""Подключить удалённый импорт модулей и пакетов через requests."""

import sys
from importlib.abc import Loader, PathEntryFinder
from importlib.util import spec_from_loader

import requests


class URLLoader(Loader):
    """Скачать и выполнить код модуля."""

    def __init__(self, url):
        """Скачать исходный код один раз."""
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        self.source = response.content

    def create_module(self, spec):
        """Поручить создание модуля Python."""
        return None

    def exec_module(self, module):
        """Выполнить код внутри модуля."""
        module.__file__ = module.__spec__.origin
        exec(compile(self.source, module.__file__, "exec"), module.__dict__)


class URLFinder(PathEntryFinder):
    """Найти модуль или пакет по URL."""

    def __init__(self, url):
        """Запомнить адрес каталога."""
        self.url = url.rstrip("/")

    def find_spec(self, fullname, target=None):
        """Попробовать загрузить пакет, затем обычный модуль."""
        name = fullname.rsplit(".", 1)[-1]
        for suffix, is_package in (("/__init__.py", True), (".py", False)):
            url = f"{self.url}/{name}{suffix}"
            try:
                loader = URLLoader(url)
            except requests.RequestException as error:
                if error.response is not None and error.response.status_code == 404:
                    continue
                raise ImportError(f"Не удалось загрузить {url}") from error
            spec = spec_from_loader(
                fullname, loader, origin=url, is_package=is_package
            )
            if is_package:
                spec.submodule_search_locations = [f"{self.url}/{name}"]
            return spec
        return None


def url_hook(path):
    """Обработать HTTP-адрес из sys.path."""
    if not isinstance(path, str) or not path.startswith(("http://", "https://")):
        raise ImportError
    try:
        response = requests.get(path, timeout=5)
        # На Pages у каталога пакета может не быть страницы index.html.
        if response.status_code != 404:
            response.raise_for_status()
    except requests.RequestException as error:
        print(f"Сервер недоступен: {path}", file=sys.stderr)
        raise ImportError(path) from error
    return URLFinder(path)


sys.path_hooks.append(url_hook)
sys.path_importer_cache.clear()
