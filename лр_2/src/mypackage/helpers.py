"""Запрос текущей погоды через OpenWeather API."""

import requests


def get_weather(city: str, api_key: str) -> dict:
    """Вернуть данные о текущей погоде в городе в формате JSON API."""
    if not city or not api_key:
        raise ValueError("Нужны название города и ключ OpenWeather API")

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": api_key, "units": "metric", "lang": "ru"},
        timeout=5,
    )
    response.raise_for_status()
    return response.json()
