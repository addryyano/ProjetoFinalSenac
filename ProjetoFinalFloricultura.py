import datetime

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
#Nova Venda
NovaVenda=uic.loadUi("NovaVenda.ui")

#MenuBar
Principal.actionConsultar_Clientes.triggered.connect(ConsultaClientes.show)
Principal.actionConsultar_Produtos.triggered.connect(ConsultaProdutos.show)
Principal.actionCadastrar_Clientes.triggered.connect(CadastroClientes.show)
Principal.actionCadastrar_Produtos.triggered.connect(CadastroProdutos.show)
Principal.actionHistorico_de_vendas.triggered.connect(Vendas.show)
Principal.actionRegistrar_Nova_Venda.triggered.connect(NovaVenda.show)
Principal.actionSair.triggered.connect(Principal.close)
Principal.actionSair.triggered.connect(ConsultaClientes.close)
Principal.actionSair.triggered.connect(ConsultaProdutos.close)
Principal.actionSair.triggered.connect(CadastroClientes.close)
Principal.actionSair.triggered.connect(CadastroProdutos.close)
Principal.actionSair.triggered.connect(Vendas.close)
Principal.actionSair.triggered.connect(NovaVenda.close)

def abreTelaPrincipal():
    if (login.txtUsuario.text() == "root" and login.txtSenha.text() == "root"):
        login.lblResultado.setText("")
        login.close()
        Principal.show()
    else:
        login.lblResultado.setText("    Usuário ou senha invalido!")

def consultaCliente():
    try:
        idCliente = ConsultaClientes.txtconsultaClienteId.text()
        nomeCliente = ConsultaClientes.txtconsultaClienteNome.text()
        if ConsultaClientes.btnConsultaIdCliente.text == "Excluir":
            if idCliente == "":
                excluirProdutoOuCliente("nomeCliente", nomeCliente)
                # nomeCliente = ""
            else:
                excluirProdutoOuCliente("idCliente", idCliente)
                # idCliente = ""
            ConsultaClientes.btnConsultaIdCliente.setText("CONSULTAR")
        elif ConsultaClientes.btnConsultaIdCliente.text() == "CONSULTAR":
            conectarBanco()
            with conex.cursor() as c:
                if ConsultaClientes.btnConsultaIdCliente.text() =="CONSULTAR":
                    if idCliente == "":
                        sql = "SELECT CLIENTE.*, BAIRRO.* FROM CLIENTE INNER JOIN BAIRRO ON CLIENTE.IdBairro = BAIRRO.IdBairro WHERE NomeCliente = '" + nomeCliente + "';"
                        nomeCliente = ""
                    else:
                        sql = "SELECT CLIENTE.*, BAIRRO.* FROM CLIENTE INNER JOIN BAIRRO ON CLIENTE.IdBairro = BAIRRO.IdBairro WHERE IdCliente = " + idCliente + ";"
                        idCliente = ""
                    ConsultaClientes.btnConsultaIdCliente.setText("Excluir")
                c.execute(sql)
                res = c.fetchone()
                print(res)
                ConsultaClientes.txtSobreNomeClienteConsulta.setText(res['SobreNomeCliente'])
                ConsultaClientes.txtNomeClienteConsulta.setText(res['NomeCliente'])
                ConsultaClientes.txt_EnderecoConsulta.setText(res['EnderecoCliente'])
                ConsultaClientes.txtRgClienteConsulta.setText(str(res['RgCliente']))
                ConsultaClientes.txtBairroConsulta.setText(res['NomeBairro'] + ", " + res['Cidade'])
                ConsultaClientes.txtClienteIdConsulta.setText(str(res['IdCliente']))
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
        dataCompraDe = Vendas.dataVendasDe.text()
        dataCompraAte = Vendas.dataVendasAte.text()
        with conex.cursor() as c:
            sql = "SELECT PRODUTO.NomeProduto as Produto, PRODUTO.PrecoProduto, CONCAT(CLIENTE.NomeCliente, ' ', CLIENTE.SobreNomeCliente) as Cliente, COMPRA.*, (PrecoProduto * QtdComprado) as ' Total R$' FROM COMPRA INNER JOIN CLIENTE ON CLIENTE.IdCliente = COMPRA.IdCliente INNER JOIN PRODUTO ON PRODUTO.IdProduto = COMPRA.IdProduto WHERE DataCompra BETWEEN '" + dataCompraDe + "' AND '" + dataCompraAte + "'; "

            c.execute(sql)
            resVendas = c.fetchall()

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

def registroVenda():
    try:
        conectarBanco()
        idCliente = NovaVenda.txtIdClienteVenda.text()
        idProduto = NovaVenda.txtIdProdutoVenda.text()
        dataCompra = NovaVenda.dataVendaNova.text()
        numeroNfse = NovaVenda.nNfse.text()
        codigoTransacao = NovaVenda.codOperacaoVenda.text()
        qtdComprado = NovaVenda.qtdVenda.text()
        with conex.cursor() as c:
            sql = "INSERT INTO COMPRA (`IdCliente`, `IdProduto`, `DataCompra`, `NumeroNfe`, `CodigoTransacao`, `QtdComprado`) VALUES ('" + idCliente + "','" + idProduto + "',' " + dataCompra + "','" + numeroNfse + "','" + codigoTransacao + "','" + qtdComprado + "');"
            print(sql)
            c.execute(sql)
            conex.commit()
            c.close()
            msgSucesso()
            limpaCamposNovaVenda()

    except Exception:
        msgProblemaDb()
    finally:
        conex.close()

def excluirProdutoOuCliente(prodOuCli, idOuNome):
    try:
        conectarBanco()
        with conex.cursor() as cur:
            if prodOuCli == "idCliente":
                sql = "DELETE FROM CLIENTE WHERE IdCliente = " + idOuNome + ";"
            elif prodOuCli == "nomeCliente":
                sql = "DELETE FROM CLIENTE WHERE NomeCliente = '" + idOuNome + "';"
            cur.execute(sql)
            conex.commit()
            cur.close()
    except Exception:
        msgProblemaDb()
    else:
        msgSucesso()
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

def limpaCamposConsultaCliente():
    ConsultaClientes.txtNomeClienteConsulta.setText("")
    ConsultaClientes.txtSobreNomeClienteConsulta.setText("")
    ConsultaClientes.txtRgClienteConsulta.setText("")
    ConsultaClientes.txt_EnderecoConsulta.setText("")
    ConsultaClientes.txtBairroConsulta.setText("")
    ConsultaClientes.txtClienteIdConsulta.setText("")
    ConsultaClientes.txtconsultaClienteId.setText("")
    ConsultaClientes.txtconsultaClienteNome.setText("")
    ConsultaClientes.btnConsultaIdCliente.setText("CONSULTAR")

def limpaCamposNovaVenda():
    NovaVenda.txtIdClienteVenda.setText("")
    NovaVenda.txtIdProdutoVenda.setText("")
    NovaVenda.nNfse.setText("")
    NovaVenda.codOperacaoVenda.setText("")
    NovaVenda.qtdVenda.setText("")

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
ConsultaClientes.btnLimparCliente.clicked.connect(limpaCamposConsultaCliente)
#ConsultaClientes.btnLimparCliente.clicked.connect()

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
NovaVenda.btnRegistraVenda.clicked.connect(registroVenda)
Vendas.btnNovaVendaPainel.clicked.connect(NovaVenda.show)
NovaVenda.btnAbreConsultaCliente.clicked.connect(ConsultaClientes.show)
NovaVenda.btnAbreConsultaProduto.clicked.connect(ConsultaProdutos.show)
Vendas.btnDataVendas.clicked.connect(carregaVendas)


login.show()
app.exec()
