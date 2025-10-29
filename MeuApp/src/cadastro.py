import flet as ft
import re
import json
import os

USUARIOS_FILE = "usuarios.json"

def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        try:
            with open(USUARIOS_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def salvar_usuario(usuarios):
    with open(USUARIOS_FILE, 'w') as f:
        json.dump(usuarios, f)


def tela_cadastro(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0

    def adicionar_usuario(e):
        user = carregar_usuarios()

        if usuario.value in user:
            mensagem("Usuário já existe")
        else:
            validar = validar_senha(senha.value)
            if validar == True:
                user[usuario.value] = senha.value
                salvar_usuario(user)
                mensagem("Usuário cadastrado com sucesso")
            else:
                mensagem(validar)

    def validar_senha(senha):
        if len(senha) < 8:
            return "A senha deve ter, pelo menos, 8 caracteres"
        if not re.search(r'\d', senha):
            return "A senha deve ter, pelo menos, 1 número"
        if not re.search(r'[!?@#$%&^*,.:"{}()|<>]', senha):
            return "A senha deve ter, pelo menos, um caracter especial"
        return True

    def mensagem(msg):
        verificar = ft.SnackBar(
            content=ft.Text(msg)
        )
        page.overlay.append(verificar)
        verificar.open = True
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
        prefix_icon=ft.Icons.KEY,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.all(10),
        border_color=ft.Colors.BLUE,
        border_width=2,
        password=True,
        can_reveal_password=True,
        width=300
    )

    botao_cadastro = ft.ElevatedButton(
        text="Cadastrar",
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE,
        width=300,
        on_click=adicionar_usuario
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[usuario, senha, botao_cadastro],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        )
    )