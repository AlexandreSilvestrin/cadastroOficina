from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sqlite3
import time
from PyQt5 import uic


def data():
    ano, mes, dia, hora, minuto, f, g, h, i = time.localtime()
    dataa = f'{dia:02}/{mes:02}/{ano} {hora}:{minuto:02}'
    return dataa


class Forms1:
    def __init__(self, tela, tela2, app):
        self.tela = tela
        self.banco = sqlite3.connect("banco_cadastro.db")
        self.cursor = self.banco.cursor()
        self.tela.btnatt.clicked.connect(self.listar_dados)
        self.tela.btnsalvar.clicked.connect(self.salvar_dados)
        self.tela.btnlimpar.clicked.connect(self.limpar_dados)
        self.tela.btnpesquisar.clicked.connect(self.pesquisar_dados)
        self.tela.setFixedSize(1356, 674)
        self.tela.show()
        self.forms2 = Forms2(self, tela2, self.banco)
        self.app = app
        app.exec()

    def listar_dados(self):
        self.cursor.execute("SELECT * FROM dados")
        dados_lidos = self.cursor.fetchall()
        dados_lidos = dados_lidos[::-1]
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
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS dados(nome text,tell text,placa primary key,carro text,
            data text, info text)''')
            if nome.strip() == '' or tell.strip() == '' or placa.strip() == '' or carro.strip() == '':
                QMessageBox.about(self.tela, 'Alerta', '''Usuario nao cadastrado, complete todos os campos.''')
            else:
                self.cursor.execute(f'''INSERT INTO dados VALUES ('{nome}','{tell}','{placa}','{carro}','{data()}', '{info}')''')
                self.banco.commit()
                QMessageBox.about(self.tela, 'Alerta', "Dados inseridos com sucesso!")
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
        result = self.cursor.execute(f'''SELECT * from dados WHERE placa = '{self.tela.placatxt.text()}' ''').fetchall()
        if len(result) == 0:
            QMessageBox.about(self.tela, 'Alerta', f'Placa: {self.tela.placatxt.text()} nao encontrada\nInsira uma placa existente')
        else:
            self.forms2.tela2.show()
            self.forms2.bloq_desbloq(False)
            self.forms2.listar_dados(self.tela.placatxt.text())
        self.limpar_dados()


class Forms2:
    def __init__(self, form1, tela2, banco):
        self.banco = banco
        self.cursor = self.banco.cursor()
        self.tela1 = form1
        self.tela2 = tela2
        self.tela2.btneditarP.clicked.connect(self.editarClicado)
        self.tela2.btncancelarP.clicked.connect(self.cancelarClicado)
        self.tela2.btnsalvarP.clicked.connect(self.salvarClicado)
        self.tela2.btnexcluirP.clicked.connect(self.excluirClicado)
        self.tela2.setFixedSize(930, 464)

    def listar_dados(self, placa):
        nome, tell, placa, carro, data, info = self.cursor.execute(f'''SELECT * from dados WHERE placa = '{placa}' ''').fetchall()[0]
        self.tela2.ptxtnome.setText(nome)
        self.tela2.ptxttell.setText(tell)
        self.tela2.ptxtplaca.setText(placa)
        self.tela2.ptxtcarro.setText(carro)
        self.tela2.ptxtdata.setText(data)
        self.tela2.ptxtinfo.setText(info)

    def editarClicado(self):
        self.bloq_desbloq(True)

    def bloq_desbloq(self, cond):
        if cond:
            self.tela2.txtedit.setText("Edicao de dados")
        else:
            self.tela2.txtedit.setText("Visualizar dados")
        self.tela2.btncancelarP.setVisible(cond)
        self.tela2.btnsalvarP.setVisible(cond)
        self.tela2.btnexcluirP.setVisible(cond)
        self.tela2.ptxtnome.setEnabled(cond)
        self.tela2.ptxttell.setEnabled(cond)
        self.tela2.ptxtcarro.setEnabled(cond)
        self.tela2.ptxtinfo.setReadOnly(not cond)

    def cancelarClicado(self):
        self.listar_dados(self.tela2.ptxtplaca.text())
        self.bloq_desbloq(False)

    def salvarClicado(self):
        nome = self.tela2.ptxtnome.text()
        tell = self.tela2.ptxttell.text()
        placa = self.tela2.ptxtplaca.text()
        carro = self.tela2.ptxtcarro.text()
        info = self.tela2.ptxtinfo.toPlainText()
        try:
            if nome.strip() == '' or tell.strip() == '' or placa.strip() == '' or carro.strip() == '' or info.strip() == '':
                QMessageBox.about(self.tela2, 'Alerta', '''Usuario nao alterado, complete todos os campos.''')
            else:
                reply = QMessageBox.question(self.tela2, 'Confirmação', "Deseja realmente alterar os dados?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if reply == QMessageBox.Yes:
                    self.cursor.execute(f'''UPDATE dados SET nome = '{nome}', tell = '{tell}', carro = '{carro}', data = '{data()}', info = '{info}' WHERE placa = '{placa}' ''')
                    self.banco.commit()
                    QMessageBox.about(self.tela2, 'Alerta', "Dados alterados com sucesso!")
                else:
                    QMessageBox.about(self.tela2, 'Alerta', 'Operação cancelada')
            self.cancelarClicado()
        except sqlite3.Error as erro:
            print("Erro ao alterar os dados: ", erro)
            QMessageBox.about(self.tela2, 'Alerta', 'Erro ao alterar os dados')

    def excluirClicado(self):
        placa = self.tela2.ptxtplaca.text()
        try:
            reply = QMessageBox.question(self.tela2, 'Confirmação', "Deseja realmente excluir o registro?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.cursor.execute(f'''DELETE FROM dados WHERE placa = '{placa}' ''')
                self.banco.commit()
                QMessageBox.about(self.tela2, 'Alerta', 'Dado excluido')
                self.bloq_desbloq(False)
                self.tela1.listar_dados()
                self.tela2.hide()
            else:
                QMessageBox.about(self.tela2, 'Alerta', 'Operação cancelada')
        except sqlite3.Error as erro:
            print("Erro ao excluir o registro: ", erro)
            QMessageBox.about(self.tela2, 'Alerta', 'Erro ao excluir o registro')
