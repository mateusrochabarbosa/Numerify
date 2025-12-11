import flet as ft
import re
import json
import os
import cadastro

# Importações dos métodos
try:
    import bisseccao
    import newton_raphson
    import secante
    import gauss
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")

USUARIOS_FILE = "usuarios.json"

CONTEUDOS = {
    "bisseccao": {
        "titulo": "Método da Bissecção",
        "descricao": "Encontra raízes de funções contínuas",
        "dificuldade": "Iniciante",
        "icone": ft.Icons.FUNCTIONS,
        "cor": ft.Colors.GREEN_700
    },
    "newton_raphson": {
        "titulo": "Método de Newton-Raphson",
        "descricao": "Método iterativo para encontrar raízes",
        "dificuldade": "Intermediário",
        "icone": ft.Icons.TRENDING_UP,
        "cor": ft.Colors.YELLOW_700
    },
    "secante": {
        "titulo": "Método da Secante",
        "descricao": "Aproximação numérica sem derivada",
        "dificuldade": "Intermediário",
        "icone": ft.Icons.SHOW_CHART,
        "cor": ft.Colors.ORANGE_700
    },
    "gauss": {
        "titulo": "Eliminação de Gauss",
        "descricao": "Resolução de sistemas lineares",
        "dificuldade": "Avançado",
        "icone": ft.Icons.GRID_ON,
        "cor": ft.Colors.RED_700
    }
}

def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        try:
            with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, KeyError):
            return {}
    return {}

def main(page: ft.Page):
    # Configuração da página em modo claro estático
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.BLUE,
        use_material3=True
    )
    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.bgcolor = ft.Colors.WHITE
    page.title = "NUMERIFY - Login"

    usuario_logado = [""]

    def voltar_login_tela():
        """Retorna para a tela de login"""
        page.clean()
        usuario_logado[0] = ""
        mostrar_tela_login()
    
    def mostrar_tela_login():
        """Mostra a tela de login inicial"""
        titulo = ft.Text(
            "NUMERIFY", 
            size=36, 
            weight=ft.FontWeight.BOLD, 
            color=ft.Colors.BLUE_700
        )

        subtitulo = ft.Text(
            "Sistema de Cálculo Numérico", 
            size=18, 
            color=ft.Colors.GREY_700
        )

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
            prefix_icon=ft.Icons.LOCK,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border_color=ft.Colors.BLUE_700,
            border_width=2,
            password=True,
            can_reveal_password=True,
            width=300,
            text_size=14
        )

        botao_entrar = ft.ElevatedButton(
            text="Entrar no Sistema",
            icon=ft.Icons.LOGIN,
            icon_color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
            width=300,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            on_click=lambda e: acesso_login(usuario, senha)
        )

        botao_cadastro = ft.OutlinedButton(
            text="Criar Nova Conta",
            icon=ft.Icons.PERSON_ADD,
            width=300,
            height=45,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10)
            ),
            on_click=ir_para_cadastro
        )

        rodape = ft.Text(
            "Desenvolvido para estudos de Cálculo Numérico",
            size=12,
            color=ft.Colors.GREY_600,
            text_align=ft.TextAlign.CENTER
        )

        page.add(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Icon(ft.Icons.CALCULATE, size=60, color=ft.Colors.BLUE_700),
                        titulo,
                        subtitulo,
                        ft.Divider(height=30, color=ft.Colors.GREY_300),
                        usuario,
                        senha,
                        botao_entrar,
                        botao_cadastro,
                        ft.Divider(height=20, color=ft.Colors.GREY_300),
                        rodape
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

    def ir_para_cadastro(e):
        page.clean()
        cadastro.tela_cadastro(page)

    def tela_inicial():
        page.clean()
        
        page.appbar = ft.AppBar(
            title=ft.Text("NUMERIFY - Cálculo Numérico", color=ft.Colors.WHITE),
            center_title=True,
            bgcolor=ft.Colors.BLUE_700,
            toolbar_height=60,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Sair",
                    on_click=lambda e: confirmar_sair()
                )
            ]
        )

        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    label="Início", 
                    icon=ft.Icons.HOME,
                    selected_icon=ft.Icons.HOME
                ),
                ft.NavigationBarDestination(
                    label="Conteúdos", 
                    icon=ft.Icons.MENU_BOOK,
                    selected_icon=ft.Icons.MENU_BOOK
                ),
                ft.NavigationBarDestination(
                    label="Perfil", 
                    icon=ft.Icons.PERSON,
                    selected_icon=ft.Icons.PERSON
                )
            ],
            on_change=mudar_pagina,
            selected_index=0,
            bgcolor=ft.Colors.WHITE,
            elevation=5
        )

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CALCULATE, size=80, color=ft.Colors.BLUE_700),
                    ft.Text("Bem-vindo ao NUMERIFY!", 
                           size=24, 
                           weight=ft.FontWeight.BOLD,
                           color=ft.Colors.BLUE_900,
                           text_align=ft.TextAlign.CENTER),
                    ft.Text("Sistema de Cálculo Numérico", 
                           size=16, 
                           color=ft.Colors.GREY_700,
                           text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=30, color=ft.Colors.GREY_300),
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"Usuário: {usuario_logado[0]}", 
                                   size=14, 
                                   weight=ft.FontWeight.BOLD,
                                   color=ft.Colors.BLUE_800),
                            ft.Text("Sessão ativa", 
                                   size=12, 
                                   color=ft.Colors.GREEN_700),
                        ]),
                        padding=10,
                        border_radius=10,
                        bgcolor=ft.Colors.BLUE_50,
                        width=300
                    ),
                    ft.Text("Explore os métodos numéricos disponíveis", 
                           size=14,
                           color=ft.Colors.GREY_700,
                           text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=20, color=ft.Colors.GREY_300),
                    ft.ElevatedButton(
                        text="Ver Conteúdos Disponíveis",
                        icon=ft.Icons.MENU_BOOK,
                        icon_color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                        width=300,
                        height=50,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                        on_click=lambda e: mostrar_conteudos()
                    ),
                    ft.Divider(height=20, color=ft.Colors.GREY_300),
                    ft.OutlinedButton(
                        text="Sair do Sistema",
                        icon=ft.Icons.LOGOUT,
                        icon_color=ft.Colors.RED_700,
                        width=300,
                        height=45,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                        on_click=lambda e: confirmar_sair()
                    )
                ], 
                alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15),
                padding=40,
                margin=20,
                bgcolor=ft.Colors.WHITE
            )
        )
        page.update()

    def confirmar_sair():
        """Mostra diálogo de confirmação para sair"""
        def sair(e):
            page.close(dlg)
            voltar_login_tela()
        
        def cancelar(e):
            page.close(dlg)
        
        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar Saída", color=ft.Colors.BLUE_900),
            content=ft.Text(f"Deseja realmente sair do sistema, {usuario_logado[0]}?", 
                           color=ft.Colors.GREY_700),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    style=ft.ButtonStyle(color=ft.Colors.GREY_700),
                    on_click=cancelar
                ),
                ft.TextButton(
                    "Sair",
                    style=ft.ButtonStyle(color=ft.Colors.RED_700),
                    on_click=sair
                )
            ]
        )
        page.open(dlg)

    def mostrar_conteudos():
        page.clean()
        
        page.appbar = ft.AppBar(
            title=ft.Text("Conteúdos Disponíveis", color=ft.Colors.WHITE),
            center_title=True,
            bgcolor=ft.Colors.BLUE_700,
            toolbar_height=60,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Sair",
                    on_click=lambda e: confirmar_sair()
                )
            ]
        )

        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    label="Início", 
                    icon=ft.Icons.HOME,
                    selected_icon=ft.Icons.HOME
                ),
                ft.NavigationBarDestination(
                    label="Conteúdos", 
                    icon=ft.Icons.MENU_BOOK,
                    selected_icon=ft.Icons.MENU_BOOK
                ),
                ft.NavigationBarDestination(
                    label="Perfil", 
                    icon=ft.Icons.PERSON,
                    selected_icon=ft.Icons.PERSON
                )
            ],
            on_change=mudar_pagina,
            selected_index=1,
            bgcolor=ft.Colors.WHITE,
            elevation=5
        )

        cards_conteudos = []
        
        for chave, conteudo in CONTEUDOS.items():
            card = ft.Card(
                elevation=3,
                color=ft.Colors.WHITE,
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(conteudo["icone"], color=conteudo["cor"], size=30),
                            title=ft.Text(conteudo["titulo"], 
                                         weight=ft.FontWeight.BOLD,
                                         color=ft.Colors.BLUE_900),
                            subtitle=ft.Text(conteudo["descricao"], 
                                            color=ft.Colors.GREY_700),
                        ),
                        ft.Row([
                            ft.Container(
                                content=ft.Text(
                                    conteudo["dificuldade"],
                                    size=12,
                                    color=ft.Colors.WHITE,
                                    weight=ft.FontWeight.BOLD,
                                    width=100,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                border_radius=8,
                                bgcolor=conteudo["cor"]
                            ),
                            ft.ElevatedButton(
                                text="Estudar",
                                icon=ft.Icons.SCHOOL,
                                icon_color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.BLUE_700,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8)
                                ),
                                on_click=lambda e, chave=chave: abrir_conteudo(chave)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]),
                    padding=15,
                    width=350
                ),
                margin=ft.margin.symmetric(vertical=8)
            )
            cards_conteudos.append(card)

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Métodos Numéricos",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_900,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Selecione um método para estudar:",
                        size=14,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Divider(height=20, color=ft.Colors.GREY_300),
                    *cards_conteudos,
                    ft.Divider(height=20, color=ft.Colors.GREY_300),
                    ft.OutlinedButton(
                        text="Voltar ao Início",
                        icon=ft.Icons.HOME,
                        width=300,
                        height=45,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                        on_click=lambda e: tela_inicial()
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO),
                padding=20,
                expand=True,
                margin=10,
                bgcolor=ft.Colors.WHITE
            )
        )
        page.update()

    def abrir_conteudo(metodo):
        conteudo = CONTEUDOS[metodo]
        
        page.clean()
        
        page.appbar = ft.AppBar(
            title=ft.Text(conteudo["titulo"], color=ft.Colors.WHITE),
            center_title=True,
            bgcolor=conteudo["cor"],
            toolbar_height=60,
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                icon_color=ft.Colors.WHITE,
                on_click=lambda e: mostrar_conteudos()
            ),
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Sair",
                    on_click=lambda e: confirmar_sair()
                )
            ]
        )

        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    label="Início", 
                    icon=ft.Icons.HOME,
                    selected_icon=ft.Icons.HOME
                ),
                ft.NavigationBarDestination(
                    label="Conteúdos", 
                    icon=ft.Icons.MENU_BOOK,
                    selected_icon=ft.Icons.MENU_BOOK
                ),
                ft.NavigationBarDestination(
                    label="Perfil", 
                    icon=ft.Icons.PERSON,
                    selected_icon=ft.Icons.PERSON
                )
            ],
            on_change=mudar_pagina,
            selected_index=1,
            bgcolor=ft.Colors.WHITE,
            elevation=5
        )

        if metodo == "bisseccao":
            bisseccao.conteudo_bisseccao(page, conteudo, usuario_logado, mostrar_conteudos)
        elif metodo == "newton_raphson":
            newton_raphson.conteudo_newton_raphson(page, conteudo, usuario_logado, mostrar_conteudos)
        elif metodo == "secante":
            secante.conteudo_secante(page, conteudo, usuario_logado, mostrar_conteudos)
        elif metodo == "gauss":
            gauss.conteudo_gauss(page, conteudo, usuario_logado, mostrar_conteudos)
        else:
            conteudo_padrao(page, conteudo)

    def conteudo_padrao(page, conteudo):
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Card(
                        color=ft.Colors.WHITE,
                        elevation=3,
                        content=ft.Container(
                            content=ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(conteudo["icone"], color=conteudo["cor"]),
                                    title=ft.Text(conteudo["titulo"], 
                                                 size=18, 
                                                 weight=ft.FontWeight.BOLD,
                                                 color=ft.Colors.BLUE_900),
                                    subtitle=ft.Text(f"Dificuldade: {conteudo['dificuldade']}",
                                                    color=ft.Colors.GREY_700),
                                ),
                            ]),
                            padding=15
                        )
                    ),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Conteúdo em Desenvolvimento", 
                                   size=18, 
                                   weight=ft.FontWeight.BOLD,
                                   color=ft.Colors.BLUE_900),
                            ft.Text(
                                f"O conteúdo detalhado do {conteudo['titulo']} "
                                "está sendo preparado com cuidado para oferecer "
                                "a melhor experiência de aprendizado.",
                                size=14,
                                color=ft.Colors.GREY_700,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Divider(height=20, color=ft.Colors.GREY_300),
                            ft.Text(conteudo["descricao"], 
                                   size=14, 
                                   color=ft.Colors.GREY_700,
                                   text_align=ft.TextAlign.CENTER),
                        ]),
                        padding=30,
                        bgcolor=ft.Colors.YELLOW_50,
                        border_radius=15,
                        border=ft.border.all(1, ft.Colors.GREY_200)
                    ),
                    
                    ft.Row([
                        ft.ElevatedButton(
                            text="Voltar para Lista de Conteúdos",
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_700,
                            color=ft.Colors.WHITE,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10)
                            ),
                            on_click=lambda e: mostrar_conteudos()
                        ),
                        ft.OutlinedButton(
                            text="Sair do Sistema",
                            icon=ft.Icons.LOGOUT,
                            icon_color=ft.Colors.RED_700,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10)
                            ),
                            on_click=lambda e: confirmar_sair()
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20),
                padding=20,
                bgcolor=ft.Colors.WHITE
            )
        )

    def mudar_pagina(e):
        indice = e.control.selected_index
        
        if indice == 0: 
            tela_inicial()
        elif indice == 1: 
            mostrar_conteudos()
        elif indice == 2:
            mostrar_perfil()

    def mostrar_perfil():
        page.clean()
        
        page.appbar = ft.AppBar(
            title=ft.Text("Meu Perfil", color=ft.Colors.WHITE),
            center_title=True,
            bgcolor=ft.Colors.BLUE_700,
            toolbar_height=60,
            actions=[
                ft.IconButton(
                    icon=ft.Icons.LOGOUT,
                    icon_color=ft.Colors.WHITE,
                    tooltip="Sair",
                    on_click=lambda e: confirmar_sair()
                )
            ]
        )

        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(
                    label="Início", 
                    icon=ft.Icons.HOME,
                    selected_icon=ft.Icons.HOME
                ),
                ft.NavigationBarDestination(
                    label="Conteúdos", 
                    icon=ft.Icons.MENU_BOOK,
                    selected_icon=ft.Icons.MENU_BOOK
                ),
                ft.NavigationBarDestination(
                    label="Perfil", 
                    icon=ft.Icons.PERSON,
                    selected_icon=ft.Icons.PERSON
                )
            ],
            on_change=mudar_pagina,
            selected_index=2,
            bgcolor=ft.Colors.WHITE,
            elevation=5
        )

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PERSON, size=80, color=ft.Colors.BLUE_700),
                    ft.Text(usuario_logado[0], 
                           size=24, 
                           weight=ft.FontWeight.BOLD,
                           color=ft.Colors.BLUE_900),
                    ft.Text("Usuário NUMERIFY", 
                           size=16, 
                           color=ft.Colors.GREY_700),
                    ft.Divider(height=30, color=ft.Colors.GREY_300),
                    
                    ft.Card(
                        color=ft.Colors.WHITE,
                        elevation=3,
                        content=ft.Container(
                            content=ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.SCHOOL, color=ft.Colors.BLUE_700),
                                    title=ft.Text("Conteúdos Estudados", 
                                                 color=ft.Colors.BLUE_900),
                                    subtitle=ft.Text(f"{len(CONTEUDOS)} métodos disponíveis",
                                                    color=ft.Colors.GREY_700),
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER_700),
                                    title=ft.Text("Nível de Progresso", 
                                                 color=ft.Colors.BLUE_900),
                                    subtitle=ft.Text("Intermediário",
                                                    color=ft.Colors.GREY_700),
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.GREEN_700),
                                    title=ft.Text("Membro desde", 
                                                 color=ft.Colors.BLUE_900),
                                    subtitle=ft.Text("Hoje",
                                                    color=ft.Colors.GREY_700),
                                ),
                            ]),
                            padding=10
                        )
                    ),
                    
                    ft.Divider(height=30, color=ft.Colors.GREY_300),
                    
                    ft.Row([
                        ft.ElevatedButton(
                            text="Voltar ao Início",
                            icon=ft.Icons.HOME,
                            icon_color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_700,
                            color=ft.Colors.WHITE,
                            width=200,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10)
                            ),
                            on_click=lambda e: tela_inicial()
                        ),
                        ft.OutlinedButton(
                            text="Sair do Sistema",
                            icon=ft.Icons.LOGOUT,
                            icon_color=ft.Colors.RED_700,
                            width=200,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10)
                            ),
                            on_click=lambda e: confirmar_sair()
                        )
                    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20),
                padding=40,
                bgcolor=ft.Colors.WHITE
            )
        )
        page.update()

    def acesso_login(usuario_field, senha_field):
        usuario_value = usuario_field.value
        senha_value = senha_field.value
        
        if not usuario_value.strip():
            mostrar_mensagem("Digite um nome de usuário", ft.Colors.ORANGE)
            return
            
        if not senha_value:
            mostrar_mensagem("Digite uma senha", ft.Colors.ORANGE)
            return

        usuarios = carregar_usuarios()

        if usuario_value in usuarios and senha_value == usuarios[usuario_value]:
            usuario_logado[0] = usuario_value
            page.clean()
            mostrar_mensagem(f"Bem-vindo, {usuario_value}!", ft.Colors.GREEN)
            tela_inicial()
        else:
            mostrar_mensagem("Usuário ou senha inválidos", ft.Colors.RED)

    def mostrar_mensagem(mensagem, cor=ft.Colors.BLUE_700):
        snack = ft.SnackBar(
            content=ft.Text(mensagem, color=ft.Colors.WHITE, size=14),
            bgcolor=cor,
            duration=3000,
            show_close_icon=True,
            close_icon_color=ft.Colors.WHITE
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    # Inicia com a tela de login
    mostrar_tela_login()

if __name__ == "__main__":
    ft.app(main, view=ft.AppView.FLET_APP)