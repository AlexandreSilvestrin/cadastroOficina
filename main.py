from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
import sqlite3
import time
import pandas as pd


def listar_dados():
    conn = sqlite3.connect('banco_cadastro.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM dados")
    dados_lidos = cursor.fetchall()
    tela.tabela.setRowCount(len(dados_lidos))
    tela.tabela.setColumnCount(5)
    for i in range(0, len(dados_lidos)):
        for j in range(0, 5):
            tela.tabela.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    conn.close()
    

def salvar_dados():
    nome = tela.nometxt.text()
    placa = tela.placatxt.text()
    tell = tela.telltxt.text()
    carro = tela.carrotxt.text()
    info = tela.infotxt.toPlainText()
    ano, mes, dia, hora, minuto, f, g, h, i = time.localtime()
    data = f'{dia:02}/{mes:02}/{ano} {hora}:{minuto:02}'

    try:
        banco = sqlite3.connect('banco_cadastro.db') 
        cursor = banco.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS dados(
                        nome text,
                        tell text,
                        placa primary key,
                        carro text,
                        data text,
                        info text)
                        ''')
        if nome.strip() == '' or tell.strip() == '' or placa.strip() == '' or carro.strip() == '' or data.strip() == '':
            QMessageBox.about(tela, 'Alerta', '''Usuario nao cadastrado, complete todos os campos.''')
        else:
            cursor.execute(f'''INSERT INTO dados VALUES ('{nome}','{tell}','{placa}','{carro}','{data}', '{info}')''')
            banco.commit()
            banco.close()
            tela.nometxt.setText("")
            tela.telltxt.setText("")
            tela.placatxt.setText("")
            tela.carrotxt.setText("")
            print("Dados inseridos com sucesso!")
            listar_dados()

    except sqlite3.Error as erro:
        print("Erro ao inserir os dados: ", erro)
        if str(erro) == 'UNIQUE constraint failed: dados.placa':
            QMessageBox.about(tela,'Alerta','Placa ja existente')


def pesquisar_dados():
    tela2.show()
    placa = tela.placatxt.text()
    banco = sqlite3.connect('banco_cadastro.db')
    cursor = banco.cursor()
    cursor.execute(f'''SELECT * from dados WHERE placa = '{placa}' ''')
    teste = cursor.fetchall()
    nome, tell, placa, carro, data, info = teste[0]
    tela2.ptxtnome.setText(nome)
    tela2.ptxttell.setText(tell)
    tela2.ptxtplaca.setText(placa)
    tela2.ptxtcarro.setText(carro)
    tela2.ptxtdata.setText(data)


def limpar_dados():
    tela.nometxt.setText("")
    tela.telltxt.setText("")
    tela.placatxt.setText("")
    tela.carrotxt.setText("")
    tela.infotxt.clear()


app = QtWidgets.QApplication([])
tela = uic.loadUi("formulario.ui")
tela2 = uic.loadUi("pesquisar.ui")
tela.btnsalvar.clicked.connect(salvar_dados)
tela.btnlimpar.clicked.connect(limpar_dados)
tela.btnatt.clicked.connect(listar_dados)
tela.btnpesquisar.clicked.connect(pesquisar_dados)
tela.show()
app.exec()
