# ЛР-1. Удалённый импорт

Игорь Калинин.

Сделал импорт через `requests`, обработку недоступного сервера (*)
и загрузку пакета (***). Файлы размещены на
[GitHub Pages](https://nerdysnake6.github.io/Prog-5/Лр-1/rootserver/).

## 1. Импорт модуля

В папке `Лр-1` установить зависимость и запустить Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -i activation_script.py
```

Вводить команды по очереди:

```python
import myremotemodule  # Пока будет ModuleNotFoundError
sys.path.append("https://nerdysnake6.github.io/Prog-5/Лр-1/rootserver")
import myremotemodule
myremotemodule.myfoo()
```

Результат: `Игорь Калинин's module is imported`.
Локальный сервер для GitHub Pages не нужен.

![Импорт с GitHub Pages](screenshots/pages.png)

Для локальной проверки запустить в отдельном терминале из папки `Лр-1`:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory rootserver
```

Затем открыть новый `python3 -i activation_script.py` и повторить команды,
заменив адрес GitHub Pages на `http://localhost:8765`.

![Локальная проверка](screenshots/local.png)

## 2. Недоступный сервер (*)

Остановить локальный сервер через Ctrl+C. В новом
`python3 -i activation_script.py` выполнить:

```python
sys.path.append("http://localhost:8765")
try:
    import myremotemodule
except ImportError:
    print("Ошибка импорта обработана")
```

После последней строки нажать Enter ещё раз. Появится сообщение
`Сервер недоступен`, затем `Ошибка импорта обработана`.
У запросов задан `timeout=5`, сетевые ошибки перехватываются.
Новый процесс нужен, чтобы Python не взял модуль из памяти.

![Проверка ошибки](screenshots/unavailable.png)

## 3. Импорт пакета (***)

После добавления адреса GitHub Pages выполнить:

```python
import mypackage
print(mypackage.hello())
```

Результат: `Пакет и его подмодуль загружены по HTTP`.
Это видно на скриншотах успешного импорта.

Весь механизм находится в `activation_script.py`: `url_hook` распознаёт
HTTP-адрес, `URLFinder` ищет `имя/__init__.py` или `имя.py`, а `URLLoader`
скачивает и выполняет код. Ответ 404 означает, что такого файла нет.
Для пакета задаются `is_package=True` и URL в `submodule_search_locations`.
По нему Python находит подмодуль при `from .helpers import hello`.

Все три проверки пройдены. Скриншоты показывают вывод реальных интерактивных
запусков от 11.09.2026. Файл `.nojekyll` в корне репозитория позволяет
GitHub Pages публиковать `__init__.py`.
