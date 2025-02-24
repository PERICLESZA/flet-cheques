import flet as ft
from controllers.cityController import CityController
from models.city import City


def cityScreen(page: ft.Page):
    page.title = "Cadastro de Cidades"

    status_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD)

    idcity_field = ft.TextField(
        label="ID da Cidade", border_radius=10, bgcolor=ft.Colors.GREY_100)
    name_city_field = ft.TextField(
        label="Nome da Cidade", border_radius=10, bgcolor=ft.Colors.GREY_100)

    controller = CityController()

    def save_city(e):
        city = City(idcity_field.value, name_city_field.value)
        if controller.create_city(city):
            status_text.value = "✅ Cidade cadastrada com sucesso!"
            status_text.color = ft.Colors.GREEN
        else:
            status_text.value = "❌ Erro ao cadastrar a cidade!"
            status_text.color = ft.Colors.RED
        status_text.update()

    save_button = ft.ElevatedButton(
        "Salvar",
        on_click=save_city,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700,
                             color=ft.Colors.WHITE),
    )

    container = ft.Container(
        content=ft.Column(
            [
                ft.Text("Cadastro de Cidade", size=24,
                        weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                idcity_field, name_city_field,
                ft.Container(save_button, alignment=ft.alignment.center),
                status_text,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=300,
        height=400,
        padding=20,
        border_radius=15,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(blur_radius=10, spread_radius=2,
                            color=ft.Colors.GREY_300),
    )

    return ft.Container(  # Retorna o container para ser usado em `content_container`
        content=container,
        alignment=ft.alignment.center,  # Centraliza corretamente
        expand=True,
        bgcolor=ft.Colors.BLUE_50,
    )


# ft.app(target=city_screen)
