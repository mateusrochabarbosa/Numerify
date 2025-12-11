import flet as ft
import math

def conteudo_secante(page, conteudo, usuario_logado, mostrar_conteudos_callback):
    # Configurar cores claras estáticas
    COR_PRIMARIA = ft.Colors.BLUE_700
    COR_FUNDO = ft.Colors.WHITE
    
    # Variáveis para os inputs
    funcao = ft.TextField(
        label="f(x) - Use sintaxe Python",
        value="x**2 - 4",
        width=400,
        border_radius=10,
        border_color=COR_PRIMARIA,
        bgcolor=ft.Colors.WHITE
    )
    
    x0_input = ft.TextField(
        label="x₀ (primeiro chute inicial)",
        value="1.5",
        width=180,
        border_radius=10,
        border_color=COR_PRIMARIA,
        bgcolor=ft.Colors.WHITE
    )
    
    x1_input = ft.TextField(
        label="x₁ (segundo chute inicial)",
        value="3.5",
        width=180,
        border_radius=10,
        border_color=COR_PRIMARIA,
        bgcolor=ft.Colors.WHITE
    )
    
    tol_input = ft.TextField(
        label="Tolerância",
        value="0.0001",
        width=180,
        border_radius=10,
        border_color=COR_PRIMARIA,
        bgcolor=ft.Colors.WHITE
    )
    
    max_iter_input = ft.TextField(
        label="Máximo de iterações",
        value="50",
        width=180,
        border_radius=10,
        border_color=COR_PRIMARIA,
        bgcolor=ft.Colors.WHITE
    )
    
    resultado = ft.Text("", size=14, weight=ft.FontWeight.BOLD)
    tabela = ft.DataTable(
        width=700,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        columns=[
            ft.DataColumn(ft.Text("Iteração", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("x₀", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("x₁", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("f(x₀)", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("f(x₁)", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("x₂", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Erro", weight=ft.FontWeight.BOLD))
        ]
    )
    
    def avaliar_funcao(f_str, x):
        try:
            f_str = f_str.replace('^', '**')
            return eval(f_str, {"math": math, "x": x})
        except:
            return None
    
    def executar_secante(e):
        try:
            if not funcao.value.strip():
                resultado.value = "Digite uma função!"
                resultado.color = ft.Colors.RED_700
                page.update()
                return
            
            f_str = funcao.value
            x0 = float(x0_input.value)
            x1 = float(x1_input.value)
            tol = float(tol_input.value)
            max_iter = int(max_iter_input.value)
            
            if x0 == x1:
                resultado.value = "Erro: x₀ e x₁ devem ser diferentes"
                resultado.color = ft.Colors.RED_700
                page.update()
                return
            
            f0 = avaliar_funcao(f_str, x0)
            f1 = avaliar_funcao(f_str, x1)
            
            if f0 is None or f1 is None:
                resultado.value = "Erro na função! Use sintaxe Python válida."
                resultado.color = ft.Colors.RED_700
                page.update()
                return
            
            iteracoes = []
            x_ant = x0
            x_atual = x1
            f_ant = f0
            f_atual = f1
            
            for i in range(max_iter):
                if f_atual - f_ant == 0:
                    resultado.value = "Erro: f(x₁) - f(x₀) = 0 (divisão por zero)"
                    resultado.color = ft.Colors.RED_700
                    page.update()
                    return
                
                x_prox = x_atual - f_atual * (x_atual - x_ant) / (f_atual - f_ant)
                erro = abs(x_prox - x_atual)
                
                iteracoes.append({
                    "iteracao": i + 1,
                    "x₀": x_ant,
                    "x₁": x_atual,
                    "f(x₀)": f_ant,
                    "f(x₁)": f_atual,
                    "x₂": x_prox,
                    "erro": erro
                })
                
                if erro < tol:
                    break
                
                x_ant = x_atual
                f_ant = f_atual
                x_atual = x_prox
                f_atual = avaliar_funcao(f_str, x_atual)
                
                if f_atual is None:
                    resultado.value = "Erro ao calcular f(x) na iteração"
                    resultado.color = ft.Colors.RED_700
                    page.update()
                    return
            
            tabela.rows = []
            for it in iteracoes:
                tabela.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(it["iteracao"]))),
                        ft.DataCell(ft.Text(f"{it['x₀']:.6f}")),
                        ft.DataCell(ft.Text(f"{it['x₁']:.6f}")),
                        ft.DataCell(ft.Text(f"{it['f(x₀)']:.6E}")),
                        ft.DataCell(ft.Text(f"{it['f(x₁)']:.6E}")),
                        ft.DataCell(ft.Text(f"{it['x₂']:.6f}")),
                        ft.DataCell(ft.Text(f"{it['erro']:.6E}"))
                    ])
                )
            
            raiz = iteracoes[-1]["x₂"]
            resultado.value = f"✓ Raiz aproximada: {raiz:.10f}\n"
            resultado.value += f"✓ Iterações: {len(iteracoes)}\n"
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
        x0_input.value = "1.5"
        x1_input.value = "3.5"
        tol_input.value = "0.0001"
        max_iter_input.value = "50"
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
                                title=ft.Text(conteudo["titulo"], size=18, weight=ft.FontWeight.BOLD),
                                subtitle=ft.Text(f"Dificuldade: {conteudo['dificuldade']}"),
                            ),
                        ]),
                        padding=15
                    )
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Fórmula: x₂ = x₁ - f(x₁) * (x₁ - x₀) / (f(x₁) - f(x₀))", 
                               size=14, 
                               weight=ft.FontWeight.BOLD,
                               color=ft.Colors.BLUE_700),
                        ft.Divider(height=10),
                        
                        ft.Text("Parâmetros de Entrada", size=16, weight=ft.FontWeight.BOLD),
                        
                        funcao,
                        
                        ft.Row([
                            x0_input,
                            ft.VerticalDivider(width=20),
                            x1_input
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
                                on_click=executar_secante
                            ),
                            ft.ElevatedButton(
                                text="Limpar",
                                icon=ft.Icons.CLEAR,
                                icon_color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.GREY_600,
                                color=ft.Colors.WHITE,
                                on_click=limpar_campos
                            )
                        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                        
                        ft.Divider(height=20),
                        
                        ft.Container(
                            content=resultado,
                            padding=15,
                            border_radius=10,
                            bgcolor=ft.Colors.BLUE_50,
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
                        ft.Text("Resultados das Iterações", size=16, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Column([tabela], scroll=ft.ScrollMode.AUTO),
                            height=300,
                            width=700
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