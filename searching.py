'''
5.
Добавить текстовое поле, в которое можно ввести запрос для поиска объекта.
По завершению ввода (например, при нажатии на кнопку «Искать») требуется найти указанный объект,
спозиционировать карту на его центральную точку, добавить метку на карту в центральную точку объекта.
'''

from io import BytesIO
import requests
from PIL import Image


def search_btn_pressed(adres, delta=0.005):
    if not adres:
        return False
    toponym_to_find = adres
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        return False

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    delta = str(delta) # размер карты

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }

    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)

    return BytesIO(response.content)


if __name__ == '__main__':
    adres = input()
    Image.open(search_btn_pressed(adres)).show()
