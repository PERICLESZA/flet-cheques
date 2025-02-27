import flet as ft
from controllers.cityController import CityController
from models.city import City

def cityScreen(page: ft.Page):
    page.title = "Cadastro de Cidades"

    controller = CityController()
    selected_city = None

    city_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text("Nome", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Ações", color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)),
        ],
        rows=[]
    )

    def filter_cities(query):
        update_city_list()
        city_table.rows = [row for row in city_table.rows if query.lower(
        ) in row.cells[1].content.value.lower()]
        page.update()

    search_field = ft.TextField(
        label="Buscar cidade...", on_change=lambda e: filter_cities(e.control.value),
        border_radius=10, bgcolor=ft.Colors.GREY_100, prefix_icon=ft.icons.SEARCH, text_align=ft.TextAlign.LEFT,
    )

    idcity_field = ft.TextField(label="ID da Cidade", disabled=True)
    name_city_field = ft.TextField(
        label="Nome da Cidade", on_change=lambda e: check_changes()
    )

    original_name = ""
    save_button = ft.ElevatedButton("Salvar", on_click=lambda e: save_city(),
                                    style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700,
                                    color=ft.Colors.WHITE),
                                    disabled=True
    )

    def check_changes():
        """Ativa o botão se o nome da cidade foi alterado."""
        save_button.disabled = name_city_field.value.strip() == original_name.strip()
        page.update()

    def save_city():
        city = City(idcity_field.value, name_city_field.value)
        success = controller.update_city(
            city) if idcity_field.value else controller.create_city(city)

        if success:
            show_snackbar("✅ Cidade salva com sucesso!", True)
            update_city_list()
            close_modal()
        else:
            show_snackbar("❌ Erro ao salvar a cidade!", False)

        page.update()

    def open_modal(city=None):
        nonlocal original_name  # Para modificar a variável dentro da função
        if city:
            idcity_field.value = str(city.idcity)
            name_city_field.value = city.name_city
        else:
            idcity_field.value = ""
            name_city_field.value = ""

        original_name = name_city_field.value
        save_button.disabled = True

        modal.open = True
        page.update()

    def close_modal():
        modal.open = False
        page.update()

    modal = ft.AlertDialog(
        modal=True,
        adaptive=True,
        title=ft.Container(
            content=ft.Column([ 
                ft.Text("Cadastro de Cidade", size=18,
                        weight=ft.FontWeight.BOLD),
                ft.Container(height=3, bgcolor=ft.Colors.BLUE_700,
                             border_radius=5)
            ], spacing=5),
            padding=10
        ),
        content=ft.Container(
            content=ft.Column([idcity_field, name_city_field, save_button],
                              horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=400,
            height=200,
            padding=20
        ),
        actions=[ft.TextButton("Fechar", on_click=lambda _: close_modal())],
        shape=ft.RoundedRectangleBorder(radius=5)
    )

    def confirm_delete(city):
        nonlocal selected_city
        selected_city = city
        confirm_delete_dialog.content = ft.Text(
            f"Deseja realmente apagar a cidade '{city.name_city}'?")
        confirm_delete_dialog.open = True
        page.update()

    def delete_confirmed(e):
        nonlocal selected_city
        if selected_city:
            success = delete_city(selected_city.idcity)
            confirm_delete_dialog.open = False
            selected_city = None
            if success:
                update_city_list()
            page.update()

    def close_confirm_dialog(e):
        confirm_delete_dialog.open = False
        page.update()

    confirm_delete_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Container(content=ft.Text(
            "Confirmação", size=18, weight=ft.FontWeight.BOLD), padding=10, border_radius=5, ),
        content=ft.Container(content=ft.Text(
            "Deseja realmente apagar a cidade?"), padding=10, border_radius=5, ),
        actions=[
            ft.TextButton("Cancelar", on_click=close_confirm_dialog),
            ft.TextButton("Apagar", on_click=delete_confirmed, style=ft.ButtonStyle(
                bgcolor=ft.Colors.RED, color=ft.Colors.WHITE))
        ],
        shape=ft.RoundedRectangleBorder(radius=5)
    )

    def delete_city(idcity):
        return controller.delete_city(idcity)

    def update_city_list():
        cities = controller.get_all_cities()

        city_table.rows.clear()  # Limpa as linhas anteriores

        # Adiciona as novas linhas corretamente
        for city in cities:
            row = ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(city.idcity), color=ft.Colors.BLACK)),
                    ft.DataCell(ft.Text(city.name_city, color=ft.Colors.BLACK)),
                    ft.DataCell(ft.Row([
                        ft.IconButton(ft.icons.EDIT, on_click=lambda e, c=city: open_modal(c)),
                        ft.IconButton(ft.icons.DELETE, on_click=lambda e, c=city: confirm_delete(c))
                    ]))
                ]
            )
            city_table.rows.append(row)

        page.update()

    def show_snackbar(msg, success):
        page.snack_bar = ft.SnackBar(
            ft.Text(msg), bgcolor=ft.Colors.GREEN if success else ft.Colors.RED
        )
        page.snack_bar.open = True
        page.update()

    update_city_list()

    # Contêiner para permitir scroll na tabela
    # Substituindo o uso de scroll no Container para usar ft.Scroll
    city_table_container = ft.Column(
        controls=[city_table],
        height=400,  # Define a altura máxima da tabela
        width=600,   # Ajuste a largura conforme necessário
        scroll=ft.ScrollMode.AUTO  # Habilita o scroll automático
)

    return ft.Column([
        search_field,
        ft.ElevatedButton("Nova Cidade", on_click=lambda _: open_modal(), icon=ft.icons.ADD),
        city_table_container,  # Substitua city_table por city_table_container
        confirm_delete_dialog,
        modal
    ], expand=True, spacing=20)
