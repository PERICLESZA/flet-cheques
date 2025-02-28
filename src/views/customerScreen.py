import flet as ft
from controllers.customerController import customerController
from controllers.cashflowController import cashflowController
from models.customer import Customer
from models.cashflow import Cashflow


def customerScreen(page: ft.Page):
    page.title = "Cadastro de Clientes"

    controller = CustomerController()
    cashflow_controller = CashflowController()
    selected_customer = None

    # Tabela de Clientes
    customer_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.BLACK,
                          weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text("Nome", color=ft.Colors.BLACK,
                          weight=ft.FontWeight.BOLD)),
            ft.DataColumn(
                ft.Text("Telefone", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Cidade", color=ft.Colors.BLACK,
                          weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Email", color=ft.Colors.BLACK,
                          weight=ft.FontWeight.BOLD)),
            ft.DataColumn(
                ft.Text("Data Nasc.", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Ações", color=ft.Colors.BLACK,
                          weight=ft.FontWeight.BOLD)),
        ],
        rows=[]
    )

    # Função para atualizar a lista de clientes
    def update_customer_list():
        customers = controller.get_all_customers()
        customer_table.rows.clear()

        for customer in customers:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(customer.id),
                                color=ft.Colors.BLACK)),
                    ft.DataCell(ft.Text(customer.name, color=ft.Colors.BLACK)),
                    ft.DataCell(
                        ft.Text(customer.phone, color=ft.Colors.BLACK)),
                    ft.DataCell(ft.Text(customer.city.name,
                                color=ft.Colors.BLACK)),
                    ft.DataCell(
                        ft.Text(customer.email, color=ft.Colors.BLACK)),
                    ft.DataCell(ft.Text(str(customer.dtbirth),
                                color=ft.Colors.BLACK)),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.icons.EDIT, on_click=lambda e,
                                      c=customer: open_customer_modal(c)),
                        ft.IconButton(ft.icons.DELETE, on_click=lambda e,
                                      c=customer: confirm_delete_customer(c)),
                        ft.IconButton(ft.icons.ADD, on_click=lambda e,
                                      c=customer: open_cashflow_modal(c))
                    ]))
                ]
            )
            customer_table.rows.append(row)
        page.update()

    # Modal para adicionar um novo cashflow
    def open_cashflow_modal(customer):
        selected_customer = customer
        cashflow_modal.open = True
        page.update()

    def close_cashflow_modal():
        cashflow_modal.open = False
        page.update()

    cashflow_modal = ft.AlertDialog(
        modal=True,
        adaptive=True,
        title=ft.Text("Lançamento de Cheque", size=18,
                      weight=ft.FontWeight.BOLD),
        content=ft.Column([
            ft.TextField(label="Data do Cheque (dtcashflow)"),
            ft.TextField(label="Tipo de Cheque (tchaflow)"),
            ft.TextField(label="ID Banco (fk_idbankmaster)"),
            ft.TextField(label="Valor (valueflow)"),
            ft.TextField(label="Centavos (centsflow)"),
            ft.TextField(label="Percentual (percentflow)"),
            ft.TextField(label="Valor Percentual (valuepercentflow)"),
            ft.TextField(label="Subtotal (subtotalflow)"),
            ft.TextField(label="Centavos 2 (cents2flow)"),
            ft.TextField(label="Wire (wire)"),
            ft.TextField(label="Total (totalflow)"),
            ft.TextField(label="Total a Pagar (totaltopay)"),
            ft.Checkbox(label="Cheque Validado (cashflowok)"),
            ft.ElevatedButton("Salvar", on_click=lambda e: save_cashflow()),
        ], spacing=10),
        actions=[ft.TextButton(
            "Fechar", on_click=lambda _: close_cashflow_modal())],
    )

    # Função para salvar o cashflow
    def save_cashflow():
        # Exemplo de como pegar os valores do modal (você precisará ajustar)
        cashflow = Cashflow(
            dtcashflow="data", tchaflow="tipo", fk_idbankmaster="banco",
            valueflow=100, centsflow=0, percentflow=10, valuepercentflow=10,
            subtotalflow=100, cents2flow=0, wire="wire", totalflow=110,
            totaltopay=110, cashflowok=True, customer_id=selected_customer.id
        )
        success = cashflow_controller.create_cashflow(cashflow)
        if success:
            show_snackbar(
                "✅ Lançamento de cheque realizado com sucesso!", True)
            close_cashflow_modal()
        else:
            show_snackbar("❌ Erro ao realizar lançamento do cheque!", False)

        page.update()

    # Função para mostrar snackbar de confirmação
    def show_snackbar(msg, success):
        page.snack_bar = ft.SnackBar(
            ft.Text(msg), bgcolor=ft.Colors.GREEN if success else ft.Colors.RED)
        page.snack_bar.open = True
        page.update()

    # Função para abrir o modal de edição de cliente
    def open_customer_modal(customer):
        # Lógica para abrir modal de edição do cliente
        pass

    def confirm_delete_customer(customer):
        # Lógica para confirmação de exclusão do cliente
        pass

    # Botão para adicionar um novo cliente
    add_customer_button = ft.ElevatedButton(
        "Novo Cliente", on_click=lambda _: open_customer_modal(None), icon=ft.icons.ADD
    )

    # Layout da página
    return ft.Column([
        add_customer_button,
        customer_table,
        cashflow_modal
    ], spacing=20)
