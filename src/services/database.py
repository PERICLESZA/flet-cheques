import mysql.connector


def conectar_bd():
    return mysql.connector.connect(
        host="mysql.cedroinfo.com.br",
        port="3306",
        database="cedroibr7",
        user="cedroibr7",
        password="Acd3590t"
    )
