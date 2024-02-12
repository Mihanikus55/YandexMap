import sys
from io import BytesIO

import requests
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from maps import Ui_MainWindow

from PIL import Image


class YandexMap(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.adres = "Кузнецова 14"
        self.map_mod = 'map'
        self.delta = 0.005
        self.find_toponim()
        self.map_image()

    def initUI(self):
        self.setupUi(self)
        self.search_btn.clicked.connect(self.search_place)
        self.clear_btn.clicked.connect(self.clear_the_search)
        self.scheme_btn.clicked.connect(self.do_scheme_map)
        self.satellite_btn.clicked.connect(self.do_sattelite_map)
        self.hybrid_btn.clicked.connect(self.do_hybrid_map)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.toponym_lattitude = str(float(self.toponym_lattitude) + self.delta)
            self.map_image()
        if event.key() == Qt.Key_Down:
            self.toponym_lattitude = str(float(self.toponym_lattitude) - self.delta)
            self.map_image()

        if event.key() == Qt.Key_Right:
            self.toponym_longitude = str(float(self.toponym_longitude) + self.delta)
            self.map_image()
        if event.key() == Qt.Key_Left:
            self.toponym_longitude = str(float(self.toponym_longitude) + self.delta)
            self.map_image()
        if event.key() == Qt.Key_PageUp:
            self.delta /= 2
            self.map_image()
        if event.key() == Qt.Key_PageDown:
            self.delta *= 2
            self.map_image()

    def search_place(self):
        self.adres = self.seaarch_line.text()
        self.find_toponim()
        self.map_image()

    def clear_the_search(self):
        self.seaarch_line.setText("")

    def do_scheme_map(self):
        self.map_mod = "map"
        self.map_image()

    def do_sattelite_map(self):
        self.map_mod = "sat"
        self.map_image()

    def do_hybrid_map(self):
        self.map_mod = "sat,skl"
        self.map_image()

    def find_toponim(self):
        if not self.adres:
            return False
        toponym_to_find = self.adres
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
        self.toponym_longitude, self.toponym_lattitude = toponym_coodrinates.split(" ")

    def map_image(self):
        delta = str(self.delta)  # размер карты

        map_params = {
            "ll": ",".join([self.toponym_longitude, self.toponym_lattitude]),
            "spn": ",".join([delta, delta]),
            "l": self.map_mod
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        Image.open(BytesIO(response.content)).save('map.png')

        self.map.setPixmap(QPixmap('map.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YandexMap()
    ex.show()
    sys.exit(app.exec_())
