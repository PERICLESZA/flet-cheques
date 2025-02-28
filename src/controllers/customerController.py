
from models.customer import Customer
from services.database import conectar_bd, verificar_conexao


class customerController:
    def __init__(self):
        self.conn = conectar_bd()
        if not verificar_conexao(self.conn):
            print("Erro ao conectar ao banco de dados.")

    def add_exchange(self, customer_id, amount, date):
        try:
            query = "INSERT INTO Cashflow (customer_id, amount, date) VALUES (%s, %s, %s)"
            cursor = self.conn.cursor()
            cursor.execute(query, (customer_id, amount, date))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Erro ao inserir cheque:", e)
            return False

    def get_all_exchanges(self):
        try:
            query = "SELECT * FROM Cashflow"
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(query)
            exchanges = cursor.fetchall()
            cursor.close()
            return exchanges
        except Exception as e:
            print("Erro ao buscar registros:", e)
            return []

    def get_exchange_by_id(self, exchange_id):
        try:
            query = "SELECT * FROM Cashflow WHERE id = %s"
            cursor = self.conn.cursor(dictionary=True)
            cursor.execute(query, (exchange_id,))
            exchange = cursor.fetchone()
            cursor.close()
            return exchange
        except Exception as e:
            print("Erro ao buscar registro:", e)
            return None

    def update_exchange(self, exchange_id, customer_id, amount, date):
        try:
            query = "UPDATE Cashflow SET customer_id = %s, amount = %s, date = %s WHERE id = %s"
            cursor = self.conn.cursor()
            cursor.execute(query, (customer_id, amount, date, exchange_id))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Erro ao atualizar registro:", e)
            return False

    def delete_exchange(self, exchange_id):
        try:
            query = "DELETE FROM Cashflow WHERE id = %s"
            cursor = self.conn.cursor()
            cursor.execute(query, (exchange_id,))
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print("Erro ao excluir registro:", e)
            return False

    def close_connection(self):
        if self.conn.is_connected():
            self.conn.close()


if __name__ == "__main__":
    controller = customerController()
    controller.add_exchange(1, 100.50, "2024-02-27")
