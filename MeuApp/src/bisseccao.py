import flet as ft
import math

def conteudo_bisseccao(page, conteudo, usuario_logado, mostrar_conteudos_callback):
    COR_PRIMARIA = ft.Colors.BLUE_700
    COR_TEXTO = ft.Colors.BLUE_900
    COR_TEXTO_SECUNDARIO = ft.Colors.GREY_700
    
    funcao = ft.TextField(
        label="f(x) - Use sintaxe Python (ex: x**2 - 4)",
        value="x**2 - 4",
        width=400,
        border_radius=10,
        border_color=COR_PRIMARIA,
        bgcolor=ft.Colors.WHITE,
        text_size=14
    )
    
    a_input = ft.TextField(
        label="a (início do intervalo)",
        value="1",
        width=180,
        border_radius=10,
        border_color=COR_PRIMARIA,
        bgcolor=ft.Colors.WHITE,
        text_size=14
    )
    
    b_input = ft.TextField(
        label="b (fim do intervalo)",
        value="3",
        width=180,
        border_radius=10,
        border_color=COR_PRIMARIA,
        bgcolor=ft.Colors.WHITE,
        text_size=14
    )
    
    tol_input = ft.TextField(
        label="Tolerância",
        value="0.001",
        width=180,
        border_radius=10,
        border_color=COR_PRIMARIA,
        bgcolor=ft.Colors.WHITE,
        text_size=14
    )
    
    max_iter_input = ft.TextField(
        label="Máximo de iterações",
        value="100",
        width=180,
        border_radius=10,
        border_color=COR_PRIMARIA,
        bgcolor=ft.Colors.WHITE,
        text_size=14
    )
    
    resultado = ft.Text("", size=14, weight=ft.FontWeight.BOLD)
    tabela = ft.DataTable(
        width=700,
        column_spacing=20,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        columns=[
            ft.DataColumn(ft.Text("Iteração", weight=ft.FontWeight.BOLD, color=COR_TEXTO)),
            ft.DataColumn(ft.Text("a", weight=ft.FontWeight.BOLD, color=COR_TEXTO)),
            ft.DataColumn(ft.Text("b", weight=ft.FontWeight.BOLD, color=COR_TEXTO)),
            ft.DataColumn(ft.Text("c", weight=ft.FontWeight.BOLD, color=COR_TEXTO)),
            ft.DataColumn(ft.Text("f(c)", weight=ft.FontWeight.BOLD, color=COR_TEXTO)),
            ft.DataColumn(ft.Text("Erro", weight=ft.FontWeight.BOLD, color=COR_TEXTO))
        ]
    )
    
    def avaliar_funcao(f_str, x):
        try:
            f_str = f_str.replace('^', '**')
            f_str = f_str.replace('sen', 'math.sin')
            f_str = f_str.replace('cos', 'math.cos')
            f_str = f_str.replace('tan', 'math.tan')
            f_str = f_str.replace('exp', 'math.exp')
            f_str = f_str.replace('ln', 'math.log')
            f_str = f_str.replace('log', 'math.log10')
            f_str = f_str.replace('sqrt', 'math.sqrt')
            return eval(f_str, {"math": math, "x": x})
        except Exception as e:
            print(f"Erro ao avaliar função: {e}")
            return None
    
    def executar_bisseccao(e):
        try:
            if not funcao.value.strip():
                resultado.value = "Digite uma função!"
                resultado.color = ft.Colors.RED_700
                page.update()
                return
                
            f_str = funcao.value
            a = float(a_input.value)
            b = float(b_input.value)
            tol = float(tol_input.value)
            max_iter = int(max_iter_input.value)
            
            if a >= b:
                resultado.value = "Erro: a deve ser menor que b"
                resultado.color = ft.Colors.RED_700
                page.update()
                return
            
            fa = avaliar_funcao(f_str, a)
            fb = avaliar_funcao(f_str, b)
            
            if fa is None or fb is None:
                resultado.value = "Erro na função! Use sintaxe Python válida."
                resultado.color = ft.Colors.RED_700
                page.update()
                return
            
            if fa * fb >= 0:
                resultado.value = "Erro: f(a) e f(b) devem ter sinais opostos (f(a)*f(b) < 0)"
                resultado.color = ft.Colors.RED_700
                page.update()
                return
            
            iteracoes = []
            for i in range(max_iter):
                c = (a + b) / 2
                fc = avaliar_funcao(f_str, c)
                
                if fc is None:
                    resultado.value = "Erro ao calcular f(c)"
                    resultado.color = ft.Colors.RED_700
                    page.update()
                    return
                
                iteracoes.append({
                    "iteracao": i + 1,
                    "a": a,
                    "b": b,
                    "c": c,
                    "f(c)": fc,
                    "erro": abs(b - a) / 2
                })
                
                if fc == 0 or (b - a) / 2 < tol:
                    break
                
                if fa * fc < 0:
                    b = c
                    fb = fc
                else:
                    a = c
                    fa = fc
            
            tabela.rows = []
            for it in iteracoes[-10:]:
                tabela.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(it["iteracao"]), color=COR_TEXTO_SECUNDARIO)),
                            ft.DataCell(ft.Text(f"{it['a']:.6f}", color=COR_TEXTO_SECUNDARIO)),
                            ft.DataCell(ft.Text(f"{it['b']:.6f}", color=COR_TEXTO_SECUNDARIO)),
                            ft.DataCell(ft.Text(f"{it['c']:.6f}", color=COR_TEXTO_SECUNDARIO)),
                            ft.DataCell(ft.Text(f"{it['f(c)']:.6E}", color=COR_TEXTO_SECUNDARIO)),
                            ft.DataCell(ft.Text(f"{it['erro']:.6E}", color=COR_TEXTO_SECUNDARIO))
                        ]
                    )
                )
            
            raiz = iteracoes[-1]["c"]
            num_iter = len(iteracoes)
            resultado.value = f"✓ Raiz aproximada: {raiz:.8f}\n"
            resultado.value += f"✓ Iterações: {num_iter}\n"
            resultado.value += f"✓ Erro final: {iteracoes[-1]['erro']:.2E}"
            resultado.color = ft.Colors.GREEN_700
            
        except ValueError:
            resultado.value = "Erro: valores numéricos inválidos"
            resultado.color = ft.Colors.RED_700
        except Exception as ex:
            resultado.value = f"Erro: {str(ex)}"
            resultado.color = ft.Colors.RED_700
        
        page.update()
    
    def limpar_campos(e):
        funcao.value = "x**2 - 4"
        a_input.value = "1"
        b_input.value = "3"
        tol_input.value = "0.001"
        max_iter_input.value = "100"
        resultado.value = ""
        tabela.rows = []
        page.update()
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Card(
                    color=ft.Colors.WHITE,
                    elevation=3,
                    content=ft.Container(
                        content=ft.Column([
                            ft.ListTile(
                                leading=ft.Icon(conteudo["icone"], size=40, color=conteudo["cor"]),
                                title=ft.Text(conteudo["titulo"], 
                                             size=18, 
                                             weight=ft.FontWeight.BOLD,
                                             color=COR_TEXTO),
                                subtitle=ft.Text(f"Dificuldade: {conteudo['dificuldade']}",
                                                color=COR_TEXTO_SECUNDARIO),
                            ),
                        ]),
                        padding=15
                    )
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Parâmetros de Entrada", 
                               size=16, 
                               weight=ft.FontWeight.BOLD,
                               color=COR_TEXTO),
                        ft.Divider(height=10, color=ft.Colors.GREY_300),
                        
                        funcao,
                        
                        ft.Row([
                            a_input,
                            ft.VerticalDivider(width=20),
                            b_input
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        
                        ft.Row([
                            tol_input,
                            ft.VerticalDivider(width=20),
                            max_iter_input
                        ], alignment=ft.MainAxisAlignment.CENTER),
                        
                        ft.Row([
                            ft.ElevatedButton(
                                text="Executar Método",
                                icon=ft.Icons.PLAY_ARROW,
                                icon_color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.GREEN_700,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8)
                                ),
                                on_click=executar_bisseccao
                            ),
                            ft.ElevatedButton(
                                text="Limpar",
                                icon=ft.Icons.CLEAR,
                                icon_color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.GREY_600,
                                color=ft.Colors.WHITE,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=8)
                                ),
                                on_click=limpar_campos
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        
                        ft.Divider(height=20, color=ft.Colors.GREY_300),
                        
                        ft.Container(
                            content=resultado,
                            padding=15,
                            border_radius=10,
                            bgcolor=ft.Colors.BLUE_50,
                            border=ft.border.all(1, ft.Colors.BLUE_100),
                            width=700
                        )
                    ]),
                    padding=15,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    width=700
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Resultados das Iterações", 
                               size=16, 
                               weight=ft.FontWeight.BOLD,
                               color=COR_TEXTO),
                        ft.Container(
                            content=ft.Column([tabela], scroll=ft.ScrollMode.AUTO),
                            height=300,
                            width=700,
                            padding=10
                        )
                    ]),
                    padding=15,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    border=ft.border.all(1, ft.Colors.GREY_200)
                ),
                
                ft.Row([
                    ft.ElevatedButton(
                        text="Voltar para Conteúdos",
                        icon=ft.Icons.ARROW_BACK,
                        icon_color=ft.Colors.WHITE,
                        bgcolor=COR_PRIMARIA,
                        color=ft.Colors.WHITE,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10)
                        ),
                        on_click=lambda e: mostrar_conteudos_callback()
                    )
                ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            expand=True,
            padding=20,
            bgcolor=ft.Colors.WHITE
        )
    )