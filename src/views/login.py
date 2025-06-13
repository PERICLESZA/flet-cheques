import flet as ft

from controllers.loginController import Login

def main(page: ft.Page):
    page.title = "Login - Flet + MySQL"
    page.window_width = 400
    page.window_height = 500
    page.window_resizable = False

    status_text = ft.Text("", size=14, weight=ft.FontWeight.BOLD)

    email_field = ft.TextField(
        label="E-mail", border_radius=10, bgcolor=ft.Colors.GREY_100)
    password_field = ft.TextField(
        label="Senha", password=True, can_reveal_password=True, border_radius=10, bgcolor=ft.Colors.GREY_100)

    def login_click(e):
        usuario = Login.autenticar(email_field.value, password_field.value)
        if usuario:
            status_text.value = f"✅ Bem-vindo, {usuario.nome}!"
            status_text.color = ft.Colors.GREEN
        else:
            status_text.value = "❌ E-mail ou senha inválidos!"
            status_text.color = ft.Colors.RED
        status_text.update()

    login_button = ft.ElevatedButton(
        "Entrar",
        on_click=login_click,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_700,
                             color=ft.Colors.WHITE),
    )

    page.add(
        ft.Container(
            content=ft.Column(
                [
                    ft.Text("Bem-vindo!", size=24,
                            weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700),
                    ft.Text("Faça login para continuar",
                            size=14, color=ft.Colors.GREY_600),
                    email_field,
                    password_field,
                    ft.Container(login_button, alignment=ft.alignment.center),
                    status_text,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=300,
            padding=20,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                blur_radius=10, spread_radius=2, color=ft.Colors.GREY_300),
        )
    )


ft.app(target=main)
