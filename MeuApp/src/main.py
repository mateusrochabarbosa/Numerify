import flet as ft

def main(page: ft.Page):
    page.vertical_alignment = ft.VerticalAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    username = ft.TextField(
        label='Username',
        prefix_icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.BLACK,
        border_radius=ft.border_radius.all(10),
        border_color=ft.Colors.WHITE,
        border_width=2,
    )

    password = ft.TextField(
        label="Password",
        prefix_icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.BLACK,
        border_radius=ft.border_radius.all(10),
        border_color=ft.Colors.WHITE,
        border_width=2,
        password=True,
        can_reveal_password=True,
    )


ft.app(main)