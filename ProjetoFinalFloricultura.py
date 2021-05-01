from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import *
import pymysql
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *

app=QtWidgets.QApplication([])

#TelaLogin
login=uic.loadUi("login.ui")
#TelaPrincipal
Principal=uic.loadUi("Principal.ui")
#CadastroClientes
CadastroClientes=uic.loadUi("CadastroClientes.ui")
#CadastroProdutos
CadastroProdutos=uic.loadUi("CadastroProdutos.ui")
#ConsultaClientes
ConsultaClientes=uic.loadUi("ConsultaClientes.ui")
#ConsultaProdutos
ConsultaProdutos=uic.loadUi("ConsultaProdutos.ui")
#Vendas
Vendas=uic.loadUi("Vendas.ui")


#MenuBar
Principal.actionConsultar_Clientes.triggered.connect(ConsultaClientes.show)
Principal.actionConsultar_Produtos.triggered.connect(ConsultaProdutos.show)
Principal.actionCadastrar_Clientes.triggered.connect(CadastroClientes.show)
Principal.actionCadastrar_Produtos.triggered.connect(CadastroProdutos.show)
Principal.actionHistorico_de_vendas.triggered.connect(Vendas.show)
Principal.actionSair.triggered.connect(Principal.close)
Principal.actionSair.triggered.connect(ConsultaClientes.close)
Principal.actionSair.triggered.connect(ConsultaProdutos.close)
Principal.actionSair.triggered.connect(CadastroClientes.close)
Principal.actionSair.triggered.connect(CadastroProdutos.close)
Principal.actionSair.triggered.connect(Vendas.close)

#def botoes():
#    ConsultaClientes.btnConsultaIdCliente.clicked.connect(msgProblemaDb)


def abreTelaPrincipal():
    if (login.txtUsuario.text() == "root" and login.txtSenha.text() == "root"):
        login.lblResultado.setText("")
        login.close()
        Principal.show()
    else:
        login.lblResultado.setText("    Usuário ou senha invalido!")


def consultaCliente():
    try:
        conectarBanco()
        idCliente = ConsultaClientes.txtconsultaClienteId.text()
        print(idCliente)
        with conex.cursor() as c:
            #sql = "SELECT NomeCliente FROM cliente WHERE IdCliente = " + idCliente + ";"
            sql = "SELECT * FROM cliente WHERE IdCliente = " + idCliente + ";"
            c.execute(sql)
            res = c.fetchone()
            ConsultaClientes.txtNomeClienteConsulta.setText(res['NomeCliente'])
        print("teste")
    except Exception:
        msgProblemaDb()
    finally:
        conex.close()





def conectarBanco():
    global conex
    conex = pymysql.connect(host='localhost', user='root', password='root', database='db_floricultura',
                            cursorclass=pymysql.cursors.DictCursor)
    print("banco conectado")

def msgProblemaDb():
    msgProblema = QMessageBox()
    msgProblema.setWindowTitle('Problema')
    msgProblema.setText('Falha ao obter dados, contate o administrador')
    msgProblema.exec()



#Botão entrar no sistema
login.btnEntrar.clicked.connect(abreTelaPrincipal)

ConsultaClientes.btnConsultaIdCliente.clicked.connect(consultaCliente)

login.show()
app.exec()
