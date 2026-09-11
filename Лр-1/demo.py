"""Проверить удалённый импорт с указанного HTTP-сервера."""

import argparse
import importlib
import sys

from activation_script import url_hook


def main():
    """Показать импорт модуля, пакета или ошибку недоступного сервера."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Адрес каталога с myremotemodule.py")
    parser.add_argument("--unavailable", action="store_true")
    args = parser.parse_args()

    assert url_hook in sys.path_hooks
    print("1. До добавления URL:", flush=True)
    try:
        importlib.import_module("myremotemodule")
    except ModuleNotFoundError as error:
        print(f"{type(error).__name__}: {error}", flush=True)
    else:
        raise AssertionError("Модуль не должен находиться локально")

    sys.path.append(args.url)
    print(f"\n2. Добавлен URL: {args.url}", flush=True)
    if args.unavailable:
        try:
            importlib.import_module("myremotemodule")
        except ImportError as error:
            print(f"Ошибка обработана: {type(error).__name__}: {error}")
        else:
            raise AssertionError("Ожидалась ошибка недоступного сервера")
        return

    module = importlib.import_module("myremotemodule")
    module.myfoo()
    print("Источник:", module.__spec__.origin)
    assert module.__spec__.origin == f"{args.url.rstrip('/')}/myremotemodule.py"

    print("\n3. Импорт пакета с относительным импортом:")
    package = importlib.import_module("mypackage")
    print(package.hello())
    print("Путь пакета:", package.__path__)
    helper = importlib.import_module("mypackage.helpers")
    assert package.hello is helper.hello
    assert package.__path__ == [f"{args.url.rstrip('/')}/mypackage"]
    print("Проверки пройдены.")


if __name__ == "__main__":
    main()
