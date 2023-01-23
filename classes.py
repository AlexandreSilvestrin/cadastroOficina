from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sqlite3
import time


class Forms:
    def __init__(self, app, tela, tela2):
        self.app = app
        self.tela = tela
        self.tela2 = tela2
        f = funcoes(self.tela, self.tela2)
        self.tela.btnatt.clicked.connect(f.listar_dados)
        self.tela.btnsalvar.clicked.connect(f.salvar_dados)
        self.tela.btnlimpar.clicked.connect(f.limpar_dados)
        self.tela.btnpesquisar.clicked.connect(f.pesquisar_dados)
        self.tela2.btnatualizarP.clicked.connect(f.pesquisar_dados)
        self.tela.show()
        self.app.exec()
        f.banco.close()


class funcoes:
    def __init__(self, tela, tela2):
        self.tela = tela
        self.tela2 = tela2
        self.banco = sqlite3.connect('banco_cadastro.db')
        self.cursor = self.banco.cursor()

    def listar_dados(self):
        self.cursor.execute("SELECT * FROM dados")
        dados_lidos = self.cursor.fetchall()
        self.tela.tabela.setRowCount(len(dados_lidos))
        self.tela.tabela.setColumnCount(5)
        for i in range(0, len(dados_lidos)):
            for j in range(0, 5):
                self.tela.tabela.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

    def salvar_dados(self):
        nome = self.tela.nometxt.text()
        placa = self.tela.placatxt.text()
        tell = self.tela.telltxt.text()
        carro = self.tela.carrotxt.text()
        info = self.tela.infotxt.toPlainText()
        ano, mes, dia, hora, minuto, f, g, h, i = time.localtime()
        data = f'{dia:02}/{mes:02}/{ano} {hora}:{minuto:02}'
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS dados(nome text,tell text,placa primary key,carro text,
            data text, info text)''')
            if nome.strip() == '' or tell.strip() == '' or placa.strip() == '' or carro.strip() == '' or data.strip() == '':
                QMessageBox.about(self.tela, 'Alerta', '''Usuario nao cadastrado, complete todos os campos.''')
            else:
                self.cursor.execute(f'''INSERT INTO dados VALUES ('{nome}','{tell}','{placa}','{carro}','{data}', '{info}')''')
                self.banco.commit()
                print("Dados inseridos com sucesso!")
                self.limpar_dados()
                self.listar_dados()
        except sqlite3.Error as erro:
            print("Erro ao inserir os dados: ", erro)
            if str(erro) == 'UNIQUE constraint failed: dados.placa':
                QMessageBox.about(self.tela, 'Alerta', 'Placa ja existente')

    def limpar_dados(self):
        self.tela.nometxt.setText("")
        self.tela.telltxt.setText("")
        self.tela.placatxt.setText("")
        self.tela.carrotxt.setText("")
        self.tela.infotxt.clear()

    def pesquisar_dados(self):
        self.tela2.show()
        placa = self.tela.placatxt.text()
        self.cursor.execute(f'''SELECT * from dados WHERE placa = '{placa}' ''')
        teste = self.cursor.fetchall()
        nome, tell, placa, carro, data, info = teste[0]
        self.tela2.ptxtnome.setText(nome)
        self.tela2.ptxttell.setText(tell)
        self.tela2.ptxtplaca.setText(placa)
        self.tela2.ptxtcarro.setText(carro)
        self.tela2.ptxtdata.setText(data)
        self.tela2.ptxtinfo.setText(info)



