import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from maps import Ui_MainWindow


class YandexMap(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.search_btn.clicked.connect(self.search_place)
        self.clear_btn.clicked.connect(self.clear_the_search)
        self.scheme_btn.clicked.connect(self.do_scheme_map)
        self.satellite_btn.clicked.connect(self.do_sattelite_map)
        self.hybrid_btn.clicked.connect(self.do_hybrid_map)

    def search_place(self):
        print('Ищем ваш запрос')

    def clear_the_search(self):
        print('Очищаем запрос')

    def do_scheme_map(self):
        print('Схематическая карта')

    def do_sattelite_map(self):
        print('Спутниковая карта')

    def do_hybrid_map(self):
        print('Гибридная карта')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YandexMap()
    ex.show()
    sys.exit(app.exec_())