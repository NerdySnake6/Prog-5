"""Проверки публичной функции пакета без сетевых запросов."""

from unittest.mock import Mock, patch

import pytest
import requests

from mypackage import get_weather


def test_get_weather_returns_api_data():
    """Запросить погоду с нужными параметрами и вернуть JSON."""
    data = {"name": "Moscow", "main": {"temp": 15}}
    response = Mock()
    response.json.return_value = data

    with patch("mypackage.helpers.requests.get", return_value=response) as get:
        assert get_weather("Moscow", "secret") == data

    get.assert_called_once_with(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": "Moscow", "appid": "secret", "units": "metric", "lang": "ru"},
        timeout=5,
    )
    response.raise_for_status.assert_called_once_with()


@pytest.mark.parametrize("city, api_key", [("", "secret"), ("Moscow", "")])
def test_get_weather_requires_city_and_key(city, api_key):
    """Отклонить пустые входные данные до отправки запроса."""
    with patch("mypackage.helpers.requests.get") as get:
        with pytest.raises(ValueError):
            get_weather(city, api_key)
    get.assert_not_called()


def test_get_weather_raises_http_error():
    """Передать вызывающему коду ошибку API."""
    response = Mock()
    response.raise_for_status.side_effect = requests.HTTPError("401")

    with patch("mypackage.helpers.requests.get", return_value=response):
        with pytest.raises(requests.HTTPError):
            get_weather("Moscow", "invalid")
