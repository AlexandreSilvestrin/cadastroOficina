from PyQt5 import QtWidgets
from PyQt5 import uic
from classes import Forms

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    tela = uic.loadUi("formulario.ui")
    tela2 = uic.loadUi("pesquisar.ui")
    t = Forms(app, tela, tela2)

