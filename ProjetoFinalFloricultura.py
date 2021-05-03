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
        nomeCliente = ConsultaClientes.txtconsultaClienteNome.text()
        with conex.cursor() as c:
            if idCliente == "":
                sql = "SELECT CLIENTE.*, BAIRRO.* FROM CLIENTE INNER JOIN BAIRRO ON CLIENTE.IdBairro = BAIRRO.IdBairro WHERE NomeCliente = '" + nomeCliente + "';"
                nomeCliente = ""
            else:
                sql = "SELECT CLIENTE.*, BAIRRO.* FROM CLIENTE INNER JOIN BAIRRO ON CLIENTE.IdBairro = BAIRRO.IdBairro WHERE IdCliente = " + idCliente + ";"
                idCliente = ""
            print(sql)
            c.execute(sql)
            res = c.fetchone()
            print(res)
            ConsultaClientes.txtSobreNomeClienteConsulta.setText(res['SobreNomeCliente'])
            ConsultaClientes.txtNomeClienteConsulta.setText(res['NomeCliente'])
            ConsultaClientes.txt_EnderecoConsulta.setText(res['EnderecoCliente'])
            ConsultaClientes.txtRgClienteConsulta.setText(str(res['RgCliente']))
            ConsultaClientes.txtBairroConsulta.setText(res['NomeBairro'] + ", " + res['Cidade'])
            print(res)

    except Exception:
        msgProblemaDb()
    finally:
        conex.close()


def consultaProduto():
    try:
        conectarBanco()
        idProduto = ConsultaProdutos.txtconsultaProdutoId.text()
        nomeProduto = ConsultaProdutos.txtconsultaProdutoNome.text()
        with conex.cursor() as c:
            if idProduto == "":
                sql = "SELECT * FROM produto WHERE NomeProduto = '" + nomeProduto + "';"
                nomeProduto = ""
            else:
                sql = "SELECT * FROM produto WHERE IdProduto = " + idProduto + ";"
                idProduto = ""
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


def cadastroProduto():
    try:
        conectarBanco()
        nomeProduto = CadastroProdutos.txtNomeProdCadastro.text()
        tipoProduto = CadastroProdutos.txtTipoProdCadastro.text()
        precoProduto = CadastroProdutos.txtPrecoProdCadastro.text()
        qtdProduto = CadastroProdutos.txtQtdProdCadastro.text()

        with conex.cursor() as c:
            sql = "INSERT INTO PRODUTO (`NomeProduto`, `TipoProduto`, `PrecoProduto`, `QtdEstoque`) VALUES ('" + nomeProduto + "','" + tipoProduto + "',' " + precoProduto + "','" + qtdProduto + "');"
            print(sql)
            c.execute(sql)
            conex.commit()
            c.close()
            msgSucesso()
            limpaCamposCadProduto()

    except Exception:
        msgProblemaDb()
    finally:
        conex.close()


def carregaVendas():
    try:
        conectarBanco()
        with conex.cursor() as c:
            sql = 'SELECT * FROM Compra;'
            c.execute(sql)
            resVendas = c.fetchall()
            print (resVendas)
    except Exception:
        msgProblemaDb()
    else:
        linhas = len(resVendas)
        colunas = len(resVendas[0])
        print(colunas)
        Vendas.tblVendas.setRowCount(linhas)
        Vendas.tblVendas.setColumnCount(colunas)

        # Ajustar cabeçalho e dimensões da tabela
        Vendas.tblVendas.setHorizontalHeaderLabels((list(resVendas[0].keys())))
        Vendas.tblVendas.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        for l in range(linhas):
            for c in range(colunas):
                item = (list(resVendas[l].values())[c])
                Vendas.tblVendas.setItem(l, c, QTableWidgetItem(str(item)))
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

def limpaCamposCadProduto():
    CadastroProdutos.txtNomeProdCadastro.setText("")
    CadastroProdutos.txtTipoProdCadastro.setText("")
    CadastroProdutos.txtPrecoProdCadastro.setText("")
    CadastroProdutos.txtQtdProdCadastro.setText("")


#Botão entrar no sistema
login.btnEntrar.clicked.connect(abreTelaPrincipal)

#Botão Consulta Clientes
ConsultaClientes.btnConsultaIdCliente.clicked.connect(consultaCliente)
Principal.btnConsultaClientePrincipal.clicked.connect(ConsultaClientes.show)

#Botão Consulta Produtos
ConsultaProdutos.btnIdProdConsulta.clicked.connect(consultaProduto)
Principal.btnConsultaProdPrincipal.clicked.connect(ConsultaProdutos.show)

#Botão Cadastro Clientes
CadastroClientes.btnCadastrarCliente.clicked.connect(cadastroCliente)
Principal.btnCadClientePrincipal.clicked.connect(CadastroClientes.show)

#Botão Cadastro Produtos
CadastroProdutos.btnCadastrarProduto.clicked.connect(cadastroProduto)
Principal.btnCadProdPrincipal.clicked.connect(CadastroProdutos.show)

#Botão Vendas
Principal.btnVendasPrincipal.clicked.connect(Vendas.show)

Vendas.btnVendas.clicked.connect(carregaVendas)
carregaVendas()


login.show()
app.exec()

Vendas.tabelaAutores = QTableWidget()
Vendas.tabelaAutores.move(1, 2)
Vendas.tabelaAutores.resize(250, 300)


