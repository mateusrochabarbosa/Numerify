import flet as ft
import re
import json
import os

USUARIOS_FILE = "usuarios.json"

def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, 'r') as f:
            return json.load(f)
    return {}

def salvar_usuario(usuarios):
    with open(USUARIOS_FILE, 'w') as f:
        json.dump(usuarios, f)

def validar_senha(senha):
    if len(senha) < 8:
        return False, "A senha deve ter, pelo menos, 8 caracteres"
    if not re.search(r'\d', senha):
        return False, "A senha deve ter, pelo menos, 1 número"
    if not re.search(r'[!?@#$%&^*,.:"{}()|<>]', senha):
        return False, "A senha deve ter, pelo menos, um caracter especial"
    return True, "senha válida"

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0

    usuarios = carregar_usuarios()

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
            ft.Text("PÁGINA INICIAL")
        )

        page.update()

    def acesso_login(e):
        if usuario.value == "admin" and senha.value == "123":
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


    usuario = ft.TextField(
        label='Usuário',
        prefix_icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.all(10),
        border_color=ft.Colors.BLUE,
        border_width=2,
        width=300,
    )

    senha = ft.TextField(
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

    botao_entrar = ft.ElevatedButton(
        text="Entrar",
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE,
        width=300,
        on_click=acesso_login
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[usuario, senha, botao_entrar],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )
    page.update()

ft.app(main)