from services.database import conectar_bd

class Login:
    def __init__(self, active, email, idlogin, login, nome, perfil, senha, token):
        self.active = active
        self.email = email
        self.idlogin = idlogin
        self.login = login
        self.nome = nome
        self.perfil = perfil
        self.senha = senha
        self.token = token

    @staticmethod
    def autenticar(email, senha):
        conexao = conectar_bd()
        cursor = conexao.cursor(dictionary=True)

        # Busca o usuário no banco
        query = "SELECT * FROM login WHERE email = %s AND senha = %s"
        cursor.execute(query, (email, senha))
        usuario = cursor.fetchone()

        cursor.close()
        conexao.close()

        # Se encontrou um usuário, retorna um objeto Login
        if usuario:
            return Login(**usuario)
        return None
