import flet as ft
import base64
from views.cityScreen import cityScreen
from views.customerScreen import customerScreen

# Função para converter uma imagem para Base64


def carregar_imagem_base64(caminho):
    with open(caminho, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")


def main_screen(page: ft.Page):
    page.title = "Sistema de Troca de Cheques"
    page.window_maximized = True

    # Converter imagem para Base64
    imagem_b64 = carregar_imagem_base64("assets/LunaLogo.png")

    # Recuperar o nome do usuário logado da sessão
    usuario_nome = page.session.get("usuario")

    # Função para fazer logout
    def handle_logout(e):
        page.session.clear()  # Limpa a sessão
        page.go("/")  # Volta para a tela de login

    def menu_option_selected(e):
        selected_option = e.control.data

        # Limpar o conteúdo anterior
        content_container.content = None
        page.update()

        if selected_option == "Logout":
            handle_logout(e)
        elif selected_option == "City":
            content_container.content = cityScreen(page)  # Exibe a tela de cidades
        elif selected_option == "Exchange": content_container.content = customerScreen(page)  # Exibe a tela de cidades
        else:
            content_container.content = ft.Text(
                f"Você selecionou: {selected_option}", size=20)

        page.update()

    # Navbar
    navbar = ft.Container(
        content=ft.Row(
            [
                ft.Image(
                    src=f"data:image/png;base64,{imagem_b64}", width=100, height=50),
                ft.Container(expand=True),
                ft.Text(usuario_nome, size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),  # Exibe o nome do usuário
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Exchange", data="Exchange", on_click=menu_option_selected),
                        ft.PopupMenuItem(text="City", data="City", on_click=menu_option_selected),
                        ft.PopupMenuItem(text="Bank", data="Bank",  on_click=menu_option_selected),
                        ft.PopupMenuItem(text="Customer", data="Customer", on_click=menu_option_selected),
                        ft.PopupMenuItem(text="Logout", data="Logout", on_click=menu_option_selected),
                    ],
                    icon=ft.Icons.MENU,
                    style=ft.ButtonStyle(bgcolor=ft.Colors.WHITE,  # Cor de fundo branca
                                         color=ft.Colors.BLACK,    # Cor do ícone preta
                    ),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            expand=True,  # Faz o Row se expandir ao longo da largura disponível
        ),
        bgcolor="#336699",
        padding=ft.padding.symmetric(horizontal=20),
        height=60,  # Altura fixa para o navbar
    )

    # Content container (ajustando para ocupar o máximo de espaço)
    content_container = ft.Container(
        alignment=ft.alignment.center,  # Centraliza o conteúdo na tela
        expand=True,  # Expande o container para ocupar todo o espaço
        bgcolor=ft.Colors.BLUE_50,  # Apenas para visualização
    )

#    content_container = ft.Container(
        # content=ft.Column(
        #     [
        #         ft.Text("Bem-vindo ao sistema!", size=20),
        #     ],
        #     alignment=ft.MainAxisAlignment.CENTER,  # Alinha tudo no centro
        #     expand=True,  # Faz o conteúdo ocupar o espaço disponível
        # ),
        # alignment=ft.alignment.center,
        # expand=True,  # Garante que o container ocupe o espaço restante entre o navbar e o rodapé
 #   )

    # Layout principal ajustado para ocupar toda a área disponível
    page.add(
        ft.Column(
            [
                navbar,  # Navbar no topo
                content_container  # Conteúdo que será alterado conforme a seleção do menu
            ],
            expand=True,  # O layout do Column se expande para preencher o espaço disponível
        )
    )

    # Atualiza a página
    page.update()
