import flet as ft
import re
import json
import os
import cadastro

USUARIOS_FILE = "usuarios.json"

CONTEUDOS = {
    "bisseccao": {
        "titulo": "Método da Bissecção",
        "descricao": "Encontra raízes de funções contínuas",
        "dificuldade": "Iniciante",
        "icone": ft.Icons.FUNCTIONS,
        "cor": ft.Colors.GREEN
    },
    "newton_raphson": {
        "titulo": "Método de Newton-Raphson",
        "descricao": "Método iterativo para encontrar raízes",
        "dificuldade": "Intermediário",
        "icone": ft.Icons.TRENDING_UP,
        "cor": ft.Colors.YELLOW
    },
    "secante": {
        "titulo": "Método da Secante",
        "descricao": "Aproximação numérica sem derivada",
        "dificuldade": "Intermediário",
        "icone": ft.Icons.SHOW_CHART,
        "cor": ft.Colors.YELLOW
    },
    "gauss": {
        "titulo": "Eliminação de Gauss",
        "descricao": "Resolução de sistemas lineares",
        "dificuldade": "Avançado",
        "icone": ft.Icons.GRID_ON,
        "cor": ft.Colors.RED
    }
}

def carregar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        try:
            with open(USUARIOS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, KeyError):
            return {}
    return {}

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.bgcolor = ft.Colors.WHITE
    page.title = "NUMERIFY - Login"

    usuario_logado = ""

    def ir_para_cadastro(e):
        page.clean()
        cadastro.tela_cadastro(page)

    def tela_inicial():
        page.clean()
        
        page.appbar = ft.AppBar(
            title=ft.Text("NUMERIFY - Cálculo Numérico"),
            center_title=True,
            bgcolor=ft.Colors.BLUE_700
        )

        page.navigation_bar = ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(label="Início", icon=ft.Icons.HOME),
                ft.NavigationBarDestination(label="Conteúdos", icon=ft.Icons.MENU_BOOK),
                ft.NavigationBarDestination(label="Perfil", icon=ft.Icons.PERSON)
            ],
            on_change=mudar_pagina
        )

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.CALCULATE, size=80, color=ft.Colors.BLUE_700),
                    ft.Text("Bem-vindo ao NUMERIFY!", 
                           size=24, 
                           weight=ft.FontWeight.BOLD,
                           text_align=ft.TextAlign.CENTER),
                    ft.Text("Sistema de Cálculo Numérico", 
                           size=16, 
                           color=ft.Colors.BLACK,
                           text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=30),
                    ft.Text(f"Usuário: {usuario_logado}", 
                           size=14, 
                           weight=ft.FontWeight.BOLD),
                    ft.Text("Explore os métodos numéricos disponíveis", 
                           size=14,
                           text_align=ft.TextAlign.CENTER),
                    ft.Divider(height=20),
                    ft.ElevatedButton(
                        text="Ver Conteúdos Disponíveis",
                        icon=ft.Icons.MENU_BOOK,
                        on_click=lambda e: mostrar_conteudos()
                    )
                ], 
                alignment=ft.MainAxisAlignment.CENTER, 
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10),
                padding=40,
                margin=20
            )
        )
        page.update()

    def mostrar_conteudos():
        page.clean()
        
        page.appbar = ft.AppBar(
            title=ft.Text("Conteúdos Disponíveis"),
            center_title=True,
            bgcolor=ft.Colors.BLUE_700
        )

        cards_conteudos = []
        
        for chave, conteudo in CONTEUDOS.items():
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            leading=ft.Icon(conteudo["icone"], color=conteudo["cor"]),
                            title=ft.Text(conteudo["titulo"], weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(conteudo["descricao"]),
                        ),
                        ft.Row([
                            ft.Container(
                                content=ft.Text(
                                    conteudo["dificuldade"],
                                    size=14,
                                    color=ft.Colors.BLACK,
                                    weight=ft.FontWeight.BOLD,
                                    width=90,
                                    text_align=ft.TextAlign.CENTER
                                ),
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                border_radius=10,
                                bgcolor=conteudo["cor"]
                            ),
                            ft.ElevatedButton(
                                text="Estudar",
                                icon=ft.Icons.SCHOOL,
                                on_click=lambda e, chave=chave: abrir_conteudo(chave)
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ]),
                    padding=10,
                    width=350
                ),
                elevation=5,
                margin=ft.margin.symmetric(vertical=5)
            )
            cards_conteudos.append(card)

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Métodos Numéricos",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Selecione um método para estudar:",
                        size=14,
                        color=ft.Colors.BLACK,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Divider(height=20),
                    *cards_conteudos
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ft.ScrollMode.AUTO),
                padding=20,
                expand=True,
                margin=10
            )
        )
        page.update()

    def abrir_conteudo(metodo):
        conteudo = CONTEUDOS[metodo]
        
        page.clean()
        
        page.appbar = ft.AppBar(
            title=ft.Text(conteudo["titulo"]),
            center_title=True,
            bgcolor=conteudo["cor"],
            leading=ft.IconButton(
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda e: mostrar_conteudos()
            )
        )

        if metodo == "bisseccao":
            conteudo_bisseccao(page, conteudo)
        else:
            conteudo_padrao(page, conteudo)

    def conteudo_bisseccao(page, conteudo):
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(conteudo["icone"], size=50, color=conteudo["cor"]),
                                    title=ft.Text(conteudo["titulo"], size=20, weight=ft.FontWeight.BOLD),
                                    subtitle=ft.Text(f"Dificuldade: {conteudo['dificuldade']}"),
                                ),
                            ]),
                            padding=15
                        )
                    ),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Introdução", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "O Método da Bissecção é um algoritmo numérico simples para encontrar "
                                "raízes de funções contínuas. É baseado no Teorema do Valor Intermediário.",
                                size=16,
                                text_align=ft.TextAlign.JUSTIFY
                            ),
                        ]),
                        padding=15,
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=10
                    ),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Como Funciona", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                "1. Escolha um intervalo [a, b] onde f(a) * f(b) < 0\n"
                                "2. Calcule o ponto médio c = (a + b) / 2\n"
                                "3. Verifique em qual subintervalo está a raiz\n"
                                "4. Repita até atingir a precisão desejada",
                                size=16
                            ),
                        ]),
                        padding=15,
                        bgcolor=ft.Colors.GREEN_50,
                        border_radius=10,
                        width=400
                    ),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Exemplo Prático", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text("Encontrar raiz de f(x) = x² - 4 no intervalo [1, 3]", size=16),
                            ft.Text("Iteração 1: c = (1 + 3)/2 = 2, f(2) = 0 → Raiz encontrada!", size=16),
                        ]),
                        padding=15,
                        bgcolor=ft.Colors.ORANGE_50,
                        border_radius=10,
                        width=400
                    ),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Vantagens e Desvantagens", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text("Sempre converge\nFácil implementação\nRobusto", size=16),
                            ft.Text("Convergência lenta\nPrecisa de intervalo inicial", size=16),
                        ]),
                        padding=15,
                        bgcolor=ft.Colors.PURPLE_50,
                        border_radius=10,
                        width=400
                    ),
                    
                    ft.Row([
                        ft.ElevatedButton(
                            text="Exercícios Práticos",
                            icon=ft.Icons.EDIT,
                            bgcolor=ft.Colors.BLUE,
                            color=ft.Colors.WHITE
                        ),
                        ft.ElevatedButton(
                            text="Voltar para Lista",
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda e: mostrar_conteudos()
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_EVENLY)
                ],
                spacing=15,
                scroll=ft.ScrollMode.ADAPTIVE),
                expand=True,
                padding=20
            )
        )

    def conteudo_padrao(page, conteudo):
        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(conteudo["icone"], color=conteudo["cor"]),
                                    title=ft.Text(conteudo["titulo"], size=18, weight=ft.FontWeight.BOLD),
                                    subtitle=ft.Text(f"Dificuldade: {conteudo['dificuldade']}"),
                                ),
                            ]),
                            padding=15
                        )
                    ),
                    
                    ft.Container(
                        content=ft.Column([
                            ft.Text("Conteúdo em Desenvolvimento", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                f"O conteúdo detalhado do {conteudo['titulo']} "
                                "está sendo preparado com cuidado para oferecer "
                                "a melhor experiência de aprendizado.",
                                size=14,
                                text_align=ft.TextAlign.CENTER
                            ),
                            ft.Divider(height=20),
                            ft.Text(conteudo["descricao"], size=14, text_align=ft.TextAlign.CENTER),
                        ]),
                        padding=30,
                        bgcolor=ft.Colors.YELLOW_50,
                        border_radius=15,
                        alignment=ft.alignment.center
                    ),
                    
                    ft.ElevatedButton(
                        text="Voltar para Lista de Conteúdos",
                        icon=ft.Icons.ARROW_BACK,
                        on_click=lambda e: mostrar_conteudos()
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20),
                padding=20
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
            title=ft.Text("Meu Perfil"),
            center_title=True,
            bgcolor=ft.Colors.BLUE
        )

        page.add(
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PERSON, size=80, color=ft.Colors.BLUE),
                    ft.Text(usuario_logado, size=24, weight=ft.FontWeight.BOLD),
                    ft.Text("Usuário NUMERIFY", size=16, color=ft.Colors.BLACK),
                    ft.Divider(height=30),
                    
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.SCHOOL, color=ft.Colors.BLUE),
                                    title=ft.Text("Conteúdos Estudados"),
                                    subtitle=ft.Text("1 método disponível"),
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.STAR, color=ft.Colors.AMBER),
                                    title=ft.Text("Nível de Progresso"),
                                    subtitle=ft.Text("Iniciante"),
                                ),
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.CALENDAR_MONTH, color=ft.Colors.GREEN),
                                    title=ft.Text("Membro desde"),
                                    subtitle=ft.Text("Hoje"),
                                ),
                            ]),
                            padding=10
                        )
                    ),
                    
                    ft.ElevatedButton(
                        text="Voltar ao Início",
                        icon=ft.Icons.HOME,
                        on_click=lambda e: tela_inicial()
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20),
                padding=40
            )
        )

    def acesso_login(e):
        if not usuario.value.strip():
            mostrar_mensagem("Digite um nome de usuário", ft.Colors.ORANGE)
            return
            
        if not senha.value:
            mostrar_mensagem("Digite uma senha", ft.Colors.ORANGE)
            return

        usuarios = carregar_usuarios()

        if usuario.value in usuarios and senha.value == usuarios[usuario.value]:
            usuario_logado = usuario.value
            page.controls.clear()
            mostrar_mensagem(f"Bem-vindo, {usuario.value}!", ft.Colors.GREEN)
            tela_inicial()
        else:
            mostrar_mensagem("Usuário ou senha inválidos", ft.Colors.RED)

    def mostrar_mensagem(mensagem, cor=ft.Colors.BLUE):
        snack = ft.SnackBar(
            content=ft.Text(mensagem, color=ft.Colors.WHITE, size=16),
            bgcolor=cor,
            show_close_icon=True,
            duration=3000
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

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
        border_radius=ft.border_radius.all(10),
        border_color=ft.Colors.BLUE,
        border_width=2,
        width=300,
    )

    senha = ft.TextField(
        label="Senha",
        hint_text="Digite sua senha",
        prefix_icon=ft.Icons.LOCK,
        bgcolor=ft.Colors.WHITE,
        border_radius=ft.border_radius.all(10),
        border_color=ft.Colors.BLUE,
        border_width=2,
        password=True,
        can_reveal_password=True,
        width=300
    )

    botao_entrar = ft.ElevatedButton(
        text="Entrar no Sistema",
        icon=ft.Icons.LOGIN,
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        width=300,
        height=50,
        on_click=acesso_login
    )

    botao_cadastro = ft.OutlinedButton(
        text="Criar Nova Conta",
        icon=ft.Icons.PERSON_ADD,
        width=300,
        height=45,
        on_click=ir_para_cadastro
    )

    rodape = ft.Text(
        "Desenvolvido para estudos de Cálculo Numérico",
        size=12,
        color=ft.Colors.BLACK,
        text_align=ft.TextAlign.CENTER
    )

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Icon(ft.Icons.CALCULATE, size=60, color=ft.Colors.BLUE_700),
                    titulo,
                    subtitulo,
                    ft.Divider(height=30, color=ft.Colors.BLACK),
                    usuario,
                    senha,
                    botao_entrar,
                    botao_cadastro,
                    ft.Divider(height=20, color=ft.Colors.BLACK),
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
            shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.BLACK12)
        )
    )
    page.update()

if __name__ == "__main__":
    ft.app(main)