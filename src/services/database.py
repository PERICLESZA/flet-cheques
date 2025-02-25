import mysql.connector


def conectar_bd():
    """Conecta ao banco de dados e retorna a conexão"""
    try:
        conn = mysql.connector.connect(
            host="mysql.cedroinfo.com.br",
            port="3306",
            database="cedroibr7",
            user="cedroibr7",
            password="Acd3590t",
            autocommit=False  # Desativa autocommit para controle de transações
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao MySQL: {err}")
        return None


def verificar_conexao(conn):
    """Verifica se a conexão está ativa e reconecta se necessário"""
    try:
        if conn is None or not conn.is_connected():
            print("🔄 Conexão perdida. Tentando reconectar...")
            return conectar_bd()  # Reconecta automaticamente
    except mysql.connector.Error as err:
        print(f"Erro ao verificar conexão: {err}")
        return conectar_bd()  # Reconectar se houver erro
    return conn
