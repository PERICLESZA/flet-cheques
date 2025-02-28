import flet as ft
from controllers.cashflowController import exchangeController


def exchangeScreen(page):
    controller = exchangeController()

    page.title = "Cadastro Rápido de Cheques"

    # Labels e Entradas
    customer_id_entry = ft.TextField(label="ID Cliente:")
    amount_entry = ft.TextField(label="Valor:")
    date_entry = ft.TextField(label="Data:")

    # Botões
    add_button = ft.ElevatedButton("Adicionar", on_click=lambda e: add_exchange(
        page, controller, customer_id_entry, amount_entry, date_entry))

    # Tabela (Lista)
    exchange_table = ft.DataTable(columns=[
        ft.DataColumn(label=ft.Text("ID")),
        ft.DataColumn(label=ft.Text("Cliente")),
        ft.DataColumn(label=ft.Text("Valor")),
        ft.DataColumn(label=ft.Text("Data")),
    ])

    def add_exchange(page, controller, customer_id_entry, amount_entry, date_entry):
        customer_id = customer_id_entry.value
        amount = amount_entry.value
        date = date_entry.value

        if controller.add_exchange(customer_id, amount, date):
            page.add(ft.Text("Cheque cadastrado com sucesso!"))
            load_exchanges(page, controller, exchange_table)
        else:
            page.add(ft.Text("Falha ao cadastrar cheque."))

    def load_exchanges(page, controller, exchange_table):
        exchanges = controller.get_all_exchanges()
        rows = [ft.DataRow(cells=[
            ft.DataCell(ft.Text(exchange[0])),
            ft.DataCell(ft.Text(exchange[1])),
            ft.DataCell(ft.Text(exchange[2])),
            ft.DataCell(ft.Text(exchange[3]))
        ]) for exchange in exchanges]
        exchange_table.rows = rows
        page.add(exchange_table)

    # Exibir todos os elementos
    page.add(customer_id_entry, amount_entry, date_entry, add_button)


# Inicialização do Flet
ft.app(target=exchangeScreen)
