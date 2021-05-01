from PyQt5 import uic,QtWidgets
from PyQt5.QtWidgets import *
import pymysql
import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *

app=QtWidgets.QApplication([])
Principal=uic.loadUi("Principal.ui")
login=uic.loadUi("login.ui")


def AbreTelaPrincipal():
    if (login.txtUsuario.text() == "root" and login.txtSenha.text() == "root"):
        login.lblResultado.setText("")
        login.close()
        Principal.show()
    else:
        login.lblResultado.setText("    Usuário ou senha invalido!")



def conectarBanco():
    global conex
    conex = pymysql.connect(host='localhost', user='root', password='root', database='db_meuslivros',
                            cursorclass=pymysql.cursors.DictCursor)

def msgProblemaDb():
    msgProblema = QMessageBox()
    msgProblema.setWindowTitle('Problema')
    msgProblema.setText('Falha ao obter dados, contate o administrador')
    msgProblema.exec()

        

#Botão entrar no sistema
login.btnEntrar.clicked.connect(AbreTelaPrincipal)

login.show()
app.exec()
