from PyQt5 import QtWidgets
from PyQt5 import uic
from classes import Forms1, Forms2

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    tela = uic.loadUi("formulario.ui")
    tela2 = uic.loadUi("pesquisar.ui")
    Forms1(tela, tela2, app)
