import flet as ft

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0

    def tela_inicial():
        page.appbar = ft.AppBar(
            title=ft.Text("NUMERIFY"),
            center_title=True,
            bgcolor=ft.Colors.BLUE
        )

        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(label="Início", icon=ft.Icons.HOME),
                ft.NavigationBarDestination(label="Métodos", icon=ft.Icons.CONSTRUCTION),
                ft.NavigationBarDestination(label="Perfil", icon=ft.Icons.PERSON)
            ]
        )

        page.add(
            ft.Text("HOME PAGE")
        )

        page.update()

    def acesso_login(e):
        if username.value == "admin" and password.value == "123":
            page.controls.clear()
            tela_inicial()

            sucesso = ft.SnackBar(
                content=ft.Text("Bem-Vindo ao Numerify"),
                bgcolor=ft.Colors.GREEN,
                show_close_icon=True,
            )
            page.overlay.append(sucesso)
            sucesso.open = True
            page.update()
        else:
            falho = ft.SnackBar(
                content=ft.Text("Nome de usuário ou senha inválidos", color=ft.Colors.WHITE, size=20),
                bgcolor=ft.Colors.RED,
                show_close_icon=True,
            )
            page.overlay.append(falho)
            falho.open = True
            page.update()


    username = ft.TextField(
        label='Usuário',
        prefix_icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.all(10),
        border_color=ft.Colors.BLUE,
        border_width=2,
        width=300,
    )

    password = ft.TextField(
        label="Senha",
        prefix_icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.all(10),
        border_color=ft.Colors.BLUE,
        border_width=2,
        password=True,
        can_reveal_password=True,
        width=300
    )

    button_login = ft.ElevatedButton(
        text="Entrar",
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE,
        width=300,
        on_click=acesso_login
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[username, password, button_login],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )
    page.update()

ft.app(main)