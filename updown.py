'''
2.
Добавить обработку клавиш PgUp и PgDown,
по нажатию на которые соответственно увеличивать и уменьшать масштаб отображения карты.
Необходимо отслеживать предельные значения,
за которые значения переменных не должны заходить.
'''

from searching import search_btn_pressed


def updown(last_adres, pressed_button, delta):
    if pressed_button == 'up':
        return search_btn_pressed(last_adres, delta + 0.001)
    elif pressed_button == 'down':
        return search_btn_pressed(last_adres, delta - 0.001)
