import flet as ft
from controllers.cityController import CityController
from models.city import City


def cityScreen(page: ft.Page):
    page.title = "Cadastro de Cidades"

    controller = CityController()

    search_field = ft.TextField(
        label="Buscar cidade...",
        on_change=lambda e: filter_cities(e.control.value),
        border_radius=10,
        bgcolor=ft.Colors.GREY_100,
        prefix_icon=ft.icons.SEARCH,
        text_align=ft.TextAlign.LEFT,
    )

    city_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID"), numeric=True),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    city_table_container = ft.Container(
        content=ft.ListView(
            [city_table],
            expand=True,
            spacing=10,
        ),
        expand=True,
        padding=10,
    )

    idcity_field = ft.TextField(
        label="ID da Cidade", disabled=True, text_align=ft.TextAlign.LEFT)
    name_city_field = ft.TextField(
        label="Nome da Cidade", text_align=ft.TextAlign.LEFT)

    def save_city(e):
        city = City(idcity_field.value, name_city_field.value)
        if idcity_field.value:
            success = controller.update_city(city)
        else:
            success = controller.create_city(city)

        if success:
            show_snackbar("✅ Cidade salva com sucesso!", True)
            update_city_list()
            close_modal()
        else:
            show_snackbar("❌ Erro ao salvar a cidade!", False)

    save_button = ft.ElevatedButton(
        "Salvar", on_click=save_city, style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE)
    )

    def open_modal(city=None):
        if city:
            idcity_field.value = str(city.idcity)
            name_city_field.value = city.name_city
        else:
            idcity_field.value = ""
            name_city_field.value = ""

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
                ft.Text("Cadastro de Cidade", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=3, bgcolor=ft.Colors.BLUE_700,
                            border_radius=2)  # Linha azul no cabeçalho
            ], spacing=5),
            padding=10
        ),
        content=ft.Container(
            content=ft.Column(
                [idcity_field, name_city_field, save_button],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            width=400,  # Define a largura do modal
            height=300,  # Define a altura do conteúdo
            padding=20
        ),
        actions=[ft.TextButton("Fechar", on_click=lambda _: close_modal())],
    )

    def delete_city(city_id):
        if controller.delete_city(city_id):
            show_snackbar("✅ Cidade removida!", True)
            update_city_list()
        else:
            show_snackbar("❌ Erro ao remover!", False)

    def update_city_list():
        cities = controller.get_all_cities()
        city_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(city.idcity))),
                    ft.DataCell(ft.Text(city.name_city)),
                    ft.DataCell(ft.Row([
                        ft.IconButton(
                            ft.icons.EDIT, on_click=lambda e, c=city: open_modal(c)),
                        ft.IconButton(
                            ft.icons.DELETE, on_click=lambda e, c=city.idcity: delete_city(c))
                    ]))
                ]
            ) for city in cities
        ]
        page.update()

    def filter_cities(query):
        update_city_list()
        city_table.rows = [row for row in city_table.rows if query.lower(
        ) in row.cells[1].content.value.lower()]
        page.update()

    def show_snackbar(msg, success):
        page.snack_bar = ft.SnackBar(
            ft.Text(msg), bgcolor=ft.Colors.GREEN if success else ft.Colors.RED
        )
        page.snack_bar.open = True
        page.update()

    return ft.Column([
        search_field,
        ft.ElevatedButton(
            "Nova Cidade", on_click=lambda _: open_modal(), icon=ft.icons.ADD
        ),
        city_table_container,
        modal
    ], expand=True, spacing=20)
