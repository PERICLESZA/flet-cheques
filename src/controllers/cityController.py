from models.city import City
from services.database import conectar_bd, verificar_conexao


class CityController:
    def __init__(self):
        self.conn = conectar_bd()
        self.cursor = self.conn.cursor()

    def create_city(self, city: City):
        """Cria uma cidade garantindo que a conexão esteja ativa"""
        try:
            # Verifica/Reestabelece conexão
            self.conn = verificar_conexao(self.conn)
            self.cursor = self.conn.cursor()  # Recria o cursor
            
            sql = "INSERT INTO city (name_city) VALUES (%s)"
            self.cursor.execute(sql, (city.name_city,))
            
            self.conn.commit()
            return True
        except Exception as err:
            print(f"Erro: {err}")
            self.conn.rollback()
            return False

    def get_city(self, idcity: str) -> City | None:
        """Busca uma cidade pelo ID"""
        self.conn = verificar_conexao(self.conn)
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            "SELECT idcity, name_city FROM city WHERE idcity = %s", (idcity,))
        row = self.cursor.fetchone()
        return City(idcity=row[0], name_city=row[1]) if row else None

    def update_city(self, city: City) -> bool:
        """Atualiza os dados de uma cidade"""
        try:
            self.conn = verificar_conexao(self.conn)
            self.cursor = self.conn.cursor()
            self.cursor.execute("UPDATE city SET name_city = %s WHERE idcity = %s",
                                (city.name_city, city.idcity))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print("Erro ao atualizar cidade:", e)
            self.conn.rollback()
            return False

    def delete_city(self, idcity: str) -> bool:
        """Deleta uma cidade pelo ID"""
        try:
            self.conn = verificar_conexao(self.conn)
            self.cursor = self.conn.cursor()
            self.cursor.execute(
                "DELETE FROM city WHERE idcity = %s", (idcity,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print("Erro ao deletar cidade:", e)
            self.conn.rollback()
            return False

    def get_all_cities(self) -> list[City]:
        """Obtém todas as cidades"""
        self.conn = verificar_conexao(self.conn)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT idcity, name_city FROM city")
        rows = self.cursor.fetchall()
        return [City(idcity=row[0], name_city=row[1]) for row in rows]

    # def close_connection(self):
    #     """Fecha a conexão com o banco de dados"""
    #     self.cursor.close()
    #     self.conn.close()
