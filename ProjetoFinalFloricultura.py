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
        with conex.cursor() as c:
            sql = "SELECT * FROM cliente WHERE IdCliente = " + idCliente + ";"
            c.execute(sql)
            res = c.fetchone()
            ConsultaClientes.txtSobreNomeClienteConsulta.setText(res['SobreNomeCliente'])
            ConsultaClientes.txtNomeClienteConsulta.setText(res['NomeCliente'])
            ConsultaClientes.txt_EnderecoConsulta.setText(res['EnderecoCliente'])
            ConsultaClientes.txtRgClienteConsulta.setText(str(res['RgCliente']))

    except Exception:
        msgProblemaDb()
    finally:
        conex.close()


def consultaProduto():
    try:
        conectarBanco()
        idProduto = ConsultaProdutos.txtconsultaProdutoId.text()
        with conex.cursor() as c:
            sql = "SELECT * FROM produto WHERE IdProduto = " + idProduto + ";"
            print(sql)
            c.execute(sql)
            res = c.fetchone()
            ConsultaProdutos.txtNomeProdConsulta.setText(res['NomeProduto'])
            ConsultaProdutos.txtTipoProdConsulta.setText(res['TipoProduto'])
            ConsultaProdutos.txtPrecoProdConsulta.setText(str(res['PrecoProduto']))
            ConsultaProdutos.txtQtdProdConsulta.setText(str(res['QtdEstoque']))

    except Exception:
        msgProblemaDb()
    finally:
        conex.close()


def cadastroCliente():
    try:
        conectarBanco()
        NomeCliente = CadastroClientes.txtNomeClienteCadastro.text()
        SobreNomeCliente = CadastroClientes.txtSobreNomeClienteCadastro.text()
        rgCliente = CadastroClientes.txtRgCadastro.text()
        EnderecoCliente = CadastroClientes.txtEnderecoCadastro.text()
        IdBairro = CadastroClientes.txtBairroCadastro.text()
        with conex.cursor() as c:
            sql = "INSERT INTO CLIENTE (`RgCliente`, `NomeCliente`, `SobreNomeCliente`, `EnderecoCliente`, `IdBairro`) VALUES ('" + rgCliente + "','" + NomeCliente + "',' " + SobreNomeCliente + "','" + EnderecoCliente + "','" + IdBairro + "');"
            print(sql)
            c.execute(sql)
            conex.commit()
            c.close()
            msgSucesso()
            limpaCamposCadCliente()

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

def msgSucesso():
    msgSucess = QMessageBox()
    msgSucess.setWindowTitle('Sucesso')
    msgSucess.setText('Procedimento realizado com sucesso!')
    msgSucess.exec()

def limpaCamposCadCliente():
    CadastroClientes.txtNomeClienteCadastro.setText("")
    CadastroClientes.txtSobreNomeClienteCadastro.setText("")
    CadastroClientes.txtRgCadastro.setText("")
    CadastroClientes.txtEnderecoCadastro.setText("")
    CadastroClientes.txtBairroCadastro.setText("")

#Botão entrar no sistema
login.btnEntrar.clicked.connect(abreTelaPrincipal)

ConsultaClientes.btnConsultaIdCliente.clicked.connect(consultaCliente)
ConsultaProdutos.btnIdProdConsulta.clicked.connect(consultaProduto)
CadastroClientes.btnCadastrarCliente.clicked.connect(cadastroCliente)

login.show()
app.exec()
