import flet as ft

def main(page: ft.Page):
    page.vertical_alignment = ft.VerticalAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    username = ft.TextField(
        label='Usuário',
        prefix_icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.BLACK,
        border_radius=ft.border_radius.all(10),
        border_color=ft.Colors.WHITE,
        border_width=2,
        width=300,
    )

    password = ft.TextField(
        label="Senha",
        prefix_icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.BLACK,
        border_radius=ft.border_radius.all(10),
        border_color=ft.Colors.WHITE,
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