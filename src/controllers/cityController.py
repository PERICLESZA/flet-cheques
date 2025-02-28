from models.city import City
from services.database import conectar_bd, verificar_conexao


class CityController:
    def create_city(self, city: City):
        """Cria uma cidade garantindo que a conexão esteja ativa"""
        try:
            conn = verificar_conexao(conectar_bd())  # Nova conexão
            cursor = conn.cursor()

            sql = "INSERT INTO city (name_city) VALUES (%s)"
            cursor.execute(sql, (city.name_city,))

            conn.commit()
            return True
        except Exception as err:
            print(f"Erro: {err}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_city(self, idcity: str) -> City | None:
        """Busca uma cidade pelo ID"""
        conn = verificar_conexao(conectar_bd())
        cursor = conn.cursor()

        cursor.execute(
            "SELECT idcity, name_city FROM city WHERE idcity = %s", (idcity,))
        row = cursor.fetchone()

        cursor.close()
        conn.close()

        return City(idcity=row[0], name_city=row[1]) if row else None

    def update_city(self, city: City) -> bool:
        """Atualiza os dados de uma cidade"""
        try:
            conn = verificar_conexao(conectar_bd())
            cursor = conn.cursor()

            cursor.execute("UPDATE city SET name_city = %s WHERE idcity = %s",
                           (city.name_city, city.idcity))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Erro ao atualizar cidade:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def delete_city(self, idcity: str) -> bool:
        """Deleta uma cidade pelo ID"""
        try:
            conn = verificar_conexao(conectar_bd())
            cursor = conn.cursor()

            cursor.execute("DELETE FROM city WHERE idcity = %s", (idcity,))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("Erro ao deletar cidade:", e)
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_all_cities(self) -> list[City]:
        """Obtém todas as cidades"""
        conn = verificar_conexao(conectar_bd())
        cursor = conn.cursor()

        cursor.execute("SELECT idcity, name_city FROM city")
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return [City(idcity=row[0], name_city=row[1]) for row in rows]
