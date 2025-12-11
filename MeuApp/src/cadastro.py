import flet as ft
import re
import json
import os

USUARIOS_FILE = "usuarios.json"

def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        try:
            with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def salvar_usuario(usuarios):
    with open(USUARIOS_FILE, 'w', encoding='utf-8') as f:
        json.dump(usuarios, f, indent=2)

def tela_cadastro(page: ft.Page):
    # Configurar página em modo claro
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    page.title = "NUMERIFY - Cadastro"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0

    def adicionar_usuario(e):
        if not usuario.value.strip():
            mensagem("Digite um nome de usuário", ft.Colors.RED_700)
            return
            
        if not senha.value:
            mensagem("Digite uma senha", ft.Colors.RED_700)
            return
            
        if not confirmar_senha.value:
            mensagem("Confirme a senha", ft.Colors.RED_700)
            return
        
        if senha.value != confirmar_senha.value:
            mensagem("As senhas não coincidem", ft.Colors.RED_700)
            return
        
        user = carregar_usuarios()

        if usuario.value in user:
            mensagem("Usuário já existe", ft.Colors.ORANGE_700)
            return
        
        validar = validar_senha(senha.value)
        if validar == True:
            user[usuario.value] = senha.value
            salvar_usuario(user)
            mensagem("Usuário cadastrado com sucesso!", ft.Colors.GREEN_700)
            usuario.value = ""
            senha.value = ""
            confirmar_senha.value = ""
            page.update()
        else:
            mensagem(validar, ft.Colors.RED_700)

    def validar_senha(senha):
        if len(senha) < 8:
            return "A senha deve ter, pelo menos, 8 caracteres"
        if not re.search(r'\d', senha):
            return "A senha deve ter, pelo menos, 1 número"
        if not re.search(r'[!?@#$%&^*,.:"{}()|<>]', senha):
            return "A senha deve ter, pelo menos, um caracter especial"
        if not re.search(r'[A-Z]', senha):
            return "A senha deve ter, pelo menos, uma letra maiúscula"
        if not re.search(r'[a-z]', senha):
            return "A senha deve ter, pelo menos, uma letra minúscula"
        return True

    def mensagem(msg, cor=ft.Colors.BLUE_700):
        snack = ft.SnackBar(
            content=ft.Text(msg, color=ft.Colors.WHITE),
            bgcolor=cor,
            duration=3000
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()
    
    def voltar_login(e):
        page.clean()
        from main import main as tela_login
        tela_login(page)

    def mostrar_requisitos_senha(e):
        requisitos = """
        REQUISITOS DA SENHA:
        
        • Mínimo 8 caracteres
        • Pelo menos 1 número
        • Pelo menos 1 caractere especial (!?@#$%&^*, etc.)
        • Pelo menos 1 letra maiúscula
        • Pelo menos 1 letra minúscula
        
        Exemplos válidos:
        • Senha123!
        • MeuNum123@
        • Calculo#2024
        """
        
        dlg = ft.AlertDialog(
            title=ft.Text("Requisitos da Senha", color=ft.Colors.BLUE_900),
            content=ft.Text(requisitos, color=ft.Colors.GREY_700),
            actions=[
                ft.TextButton(
                    "Fechar", 
                    style=ft.ButtonStyle(color=ft.Colors.BLUE_700),
                    on_click=lambda e: page.close(dlg)
                )
            ]
        )
        page.open(dlg)

    usuario = ft.TextField(
        label='Usuário',
        hint_text="Digite seu nome de usuário",
        prefix_icon=ft.Icons.PERSON,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        border_color=ft.Colors.BLUE_700,
        border_width=2,
        width=300,
        text_size=14
    )

    senha = ft.TextField(
        label="Senha",
        hint_text="Digite sua senha",
        prefix_icon=ft.Icons.KEY,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        border_color=ft.Colors.BLUE_700,
        border_width=2,
        password=True,
        can_reveal_password=True,
        width=300,
        text_size=14,
        suffix=ft.IconButton(
            icon=ft.Icons.HELP,
            icon_size=18,
            on_click=mostrar_requisitos_senha,
            tooltip="Ver requisitos da senha"
        )
    )

    confirmar_senha = ft.TextField(
        label="Confirmar Senha",
        hint_text="Digite a senha novamente",
        prefix_icon=ft.Icons.KEY,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        border_color=ft.Colors.BLUE_700,
        border_width=2,
        password=True,
        can_reveal_password=True,
        width=300,
        text_size=14
    )

    botao_cadastro = ft.ElevatedButton(
        text="Cadastrar",
        icon=ft.Icons.PERSON_ADD,
        icon_color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREEN_700,
        color=ft.Colors.WHITE,
        width=300,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        on_click=adicionar_usuario
    )
    
    botao_voltar = ft.OutlinedButton(
        text="Voltar para Login",
        icon=ft.Icons.ARROW_BACK,
        width=300,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        on_click=voltar_login
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(ft.Icons.PERSON_ADD, size=60, color=ft.Colors.BLUE_700),
                    ft.Text("Criar Nova Conta", 
                           size=24, 
                           weight=ft.FontWeight.BOLD,
                           color=ft.Colors.BLUE_700),
                    ft.Divider(height=30, color=ft.Colors.GREY_300),
                    usuario,
                    senha,
                    confirmar_senha,
                    botao_cadastro,
                    botao_voltar
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            padding=40,
            margin=20,
            border_radius=15,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_200),
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12)
        )
    )
    page.update()