import flet as ft
from controllers.cityController import CityController
from models.city import City


def cityScreen(page: ft.Page):
    page.title = "Cadastro de Cidades"

    controller = CityController()

    # 🔍 Campo de busca dinâmica
    search_field = ft.TextField(
        label="Buscar cidade...",
        on_change=lambda e: filter_cities(e.control.value),
        border_radius=10,
        bgcolor=ft.Colors.GREY_100,
        prefix_icon=ft.icons.SEARCH
    )

    # 📋 Lista de cidades (Tabela dinâmica)
    city_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nome")),
            ft.DataColumn(ft.Text("Ações")),
        ],
        rows=[]
    )

    def save_city(city_id, text_field):
        new_name = text_field.value.strip()
        if not new_name:
            show_snackbar("❌ O nome da cidade não pode estar vazio!", False)
            return

        city = City(city_id, new_name)
        success = controller.update_city(city)

        if success:
            show_snackbar("✅ Cidade salva com sucesso!", True)
            update_city_list()
        else:
            show_snackbar("❌ Erro ao salvar a cidade!", False)

    def update_city_list():
        cities = controller.get_all_cities()
        city_table.rows = []
        for city in cities:
            text_field = ft.TextField(value=city.name_city, on_submit=lambda e,
                                      idcity=city.idcity, field=city.name_city: save_city(idcity, e.control))
            city_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(city.idcity))),
                        ft.DataCell(text_field),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.SAVE,
                                    on_click=lambda e, idcity=city.idcity, field=text_field: save_city(
                                        idcity, field)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    on_click=lambda e, idcity=city.idcity: delete_city(
                                        idcity)
                                ),
                            ])
                        ),
                    ]
                )
            )
        city_table.update()

    def filter_cities(query):
        update_city_list()
        city_table.rows = [
            row for row in city_table.rows
            if query.lower() in row.cells[1].content.value.lower()
        ]
        page.update()

    def show_snackbar(msg, success):
        page.snack_bar = ft.SnackBar(
            ft.Text(msg), bgcolor=ft.Colors.GREEN if success else ft.Colors.RED)
        page.snack_bar.open = True
        page.update()

    def delete_city(idcity):
        success = controller.delete_city(idcity)  # Remove do banco de dados
        if success:
            show_snackbar("✅ Cidade excluída com sucesso!", True)
            update_city_list()  # Atualiza a lista de cidades
        else:
            show_snackbar("❌ Erro ao excluir a cidade!", False)

    # 🏗️ Layout principal
    return ft.Column([
        search_field,
        ft.ElevatedButton(
            "Nova Cidade", on_click=lambda _: open_modal(), icon=ft.icons.ADD),
        city_table
    ], spacing=20)
