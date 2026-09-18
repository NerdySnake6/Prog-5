# ЛР-2. Пакет для OpenWeather

Автор: Игорь Калинин.

Это простой PyPI-пакет на основе `mypackage` из
[ЛР-1](https://github.com/NerdySnake6/Prog-5/tree/main/%D0%9B%D1%80-1/rootserver/mypackage):
сохранил пакет из `__init__.py` и `helpers.py`, а учебную функцию `hello()`
заменил запросом погоды. Пакет получает текущую погоду по названию города через
[OpenWeather Current Weather API](https://openweathermap.org/current).

Исходный код: [GitHub](https://github.com/NerdySnake6/Prog-5/tree/main/%D0%BB%D1%80_2).

## Установка

После публикации в TestPyPI:

```bash
python3 -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ nerdysnake6-openweather
```

`--extra-index-url` нужен для зависимости `requests`, которая может отсутствовать
в TestPyPI. Для локальной установки из этой папки: `python3 -m pip install .`.

## Использование

Нужен собственный ключ [OpenWeather](https://home.openweathermap.org/api_keys).
В примере ключ берётся из переменной окружения, чтобы не сохранять его в коде:

```bash
export OPENWEATHER_API_KEY="ваш_ключ"
```

```python
import os
from mypackage import get_weather

weather = get_weather("Moscow", os.environ["OPENWEATHER_API_KEY"])
print(weather["name"], weather["main"]["temp"], weather["weather"][0]["description"])
```

`get_weather()` возвращает исходный JSON-ответ как словарь. Температура в °C,
описание на русском. Пустой город или ключ вызывают `ValueError`; ошибки сети
и HTTP передаются из `requests`.

## Что сделано по заданию

- Посмотрел устройство [requests](https://pypi.org/project/requests/),
  [yandex-weather-api](https://pypi.org/project/yandex-weather-api/) и
  [python-open-weather](https://github.com/pmk456/python-open-weather):
  у пакета есть импортируемый код, зависимости, версия и описание применения.
- Код ЛР-1 перенесён в отдельную папку с `src`-структурой. Добавлены
  `pyproject.toml`, метаданные, ссылка на GitHub и инструкция по установке.
- Предусмотрены сборка `sdist` и `wheel`, тесты функции и проверка установки.

Публикация: [TestPyPI](https://test.pypi.org/project/nerdysnake6-openweather/) (ссылка заработает после загрузки).

## Сборка и публикация

```bash
python3 -m pip install build twine
python3 -m build
python3 -m twine check dist/*
python3 -m twine upload --repository testpypi dist/*
```

Для последней команды нужен токен TestPyPI. В поле имени пользователя —
`__token__`, в поле пароля — токен с префиксом `pypi-`.
