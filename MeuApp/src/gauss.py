import flet as ft
import numpy as np

def conteudo_gauss(page, conteudo, usuario_logado, mostrar_conteudos_callback):
    # Configurar cores claras estáticas
    COR_PRIMARIA = ft.Colors.BLUE_700
    COR_FUNDO = ft.Colors.WHITE
    
    # Variáveis para os inputs
    n_input = ft.Dropdown(
        label="Tamanho do sistema (n)",
        options=[ft.dropdown.Option(str(i)) for i in range(2, 6)],
        value="3",
        width=150,
        border_radius=10,
        border_color=COR_PRIMARIA,
        bgcolor=ft.Colors.WHITE
    )
    
    sistema_input = ft.TextField(
        label="Coeficientes (matriz aumentada)",
        multiline=True,
        min_lines=4,
        max_lines=8,
        value="2, 1, -1, 8\n-3, -1, 2, -11\n-2, 1, 2, -3",
        width=500,
        border_radius=10,
        border_color=COR_PRIMARIA,
        bgcolor=ft.Colors.WHITE
    )
    
    resultado = ft.Text("", size=14, weight=ft.FontWeight.BOLD)
    solucao_text = ft.Text("", size=14)
    tabela_operacoes = ft.DataTable(
        width=700,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        columns=[
            ft.DataColumn(ft.Text("Operação", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Descrição", weight=ft.FontWeight.BOLD))
        ]
    )
    
    def parse_matriz():
        try:
            n = int(n_input.value)
            lines = sistema_input.value.strip().split('\n')
            
            if len(lines) < n:
                return None, None, f"Insira pelo menos {n} linhas"
            
            A = np.zeros((n, n))
            b = np.zeros(n)
            
            for i in range(n):
                line = lines[i].strip()
                if not line:
                    return None, None, f"Linha {i+1} vazia"
                
                parts = [p.strip() for p in line.split(',')]
                
                if len(parts) != n + 1:
                    return None, None, f"Linha {i+1}: esperados {n+1} valores, encontrados {len(parts)}"
                
                try:
                    for j in range(n):
                        A[i, j] = float(parts[j])
                    b[i] = float(parts[n])
                except ValueError:
                    return None, None, f"Linha {i+1}: valores numéricos inválidos"
            
            return A, b, None
            
        except Exception as e:
            return None, None, f"Erro: {str(e)}"
    
    def executar_gauss(e):
        try:
            A, b, error = parse_matriz()
            if error:
                resultado.value = error
                resultado.color = ft.Colors.RED_700
                page.update()
                return
            
            n = len(A)
            
            operacoes = []
            Ab = np.column_stack((A.copy(), b.copy()))
            
            operacoes.append({
                "tipo": "Inicial",
                "descricao": f"Matriz aumentada {n}x{n+1}"
            })
            
            for k in range(n-1):
                max_row = np.argmax(np.abs(Ab[k:, k])) + k
                if max_row != k:
                    Ab[[k, max_row]] = Ab[[max_row, k]]
                    operacoes.append({
                        "tipo": "Pivotagem",
                        "descricao": f"Troca linha {k+1} com linha {max_row+1}"
                    })
                
                for i in range(k+1, n):
                    if Ab[k, k] == 0:
                        resultado.value = "Erro: elemento diagonal zero após pivotagem"
                        resultado.color = ft.Colors.RED_700
                        page.update()
                        return
                    
                    factor = Ab[i, k] / Ab[k, k]
                    Ab[i, k:] = Ab[i, k:] - factor * Ab[k, k:]
                    
                    operacoes.append({
                        "tipo": "Eliminação",
                        "descricao": f"L{i+1} = L{i+1} - ({factor:.4f}) × L{k+1}"
                    })
            
            for i in range(n):
                if abs(Ab[i, i]) < 1e-10:
                    if abs(Ab[i, n]) < 1e-10:
                        resultado.value = "Sistema possui infinitas soluções"
                        resultado.color = ft.Colors.ORANGE_700
                    else:
                        resultado.value = "Sistema sem solução (inconsistente)"
                        resultado.color = ft.Colors.RED_700
                    page.update()
                    return
            
            x = np.zeros(n)
            for i in range(n-1, -1, -1):
                x[i] = (Ab[i, n] - np.dot(Ab[i, i+1:n], x[i+1:n])) / Ab[i, i]
            
            tabela_operacoes.rows = []
            for op in operacoes:
                tabela_operacoes.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(ft.Text(op["tipo"])),
                        ft.DataCell(ft.Text(op["descricao"]))
                    ])
                )
            
            sol_str = "Solução do sistema:\n"
            for i in range(n):
                sol_str += f"x{i+1} = {x[i]:.6f}\n"
            solucao_text.value = sol_str
            
            resultado.value = f"✓ Sistema {n}x{n} resolvido com sucesso!"
            resultado.color = ft.Colors.GREEN_700
            
        except Exception as ex:
            resultado.value = f"Erro: {str(ex)}"
            resultado.color = ft.Colors.RED_700
        
        page.update()
    
    def mostrar_matriz(e):
        A, b, error = parse_matriz()
        if error:
            resultado.value = error
            resultado.color = ft.Colors.RED_700
        else:
            n = len(A)
            mat_str = f"Matriz A ({n}x{n}) e vetor b:\n\n"
            for i in range(n):
                row = ""
                for j in range(n):
                    row += f"{A[i, j]:6.2f} "
                mat_str += f"[{row}] = [{b[i]:6.2f}]\n"
            
            resultado.value = mat_str
            resultado.color = ft.Colors.BLUE_700
        
        page.update()
    
    def limpar_campos(e):
        n_input.value = "3"
        sistema_input.value = "2, 1, -1, 8\n-3, -1, 2, -11\n-2, 1, 2, -3"
        resultado.value = ""
        solucao_text.value = ""
        tabela_operacoes.rows = []
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
                        ft.Text("Parâmetros de Entrada", size=16, weight=ft.FontWeight.BOLD),
                        ft.Divider(height=10),
                        
                        ft.Row([n_input], alignment=ft.MainAxisAlignment.CENTER),
                        
                        sistema_input,
                        
                        ft.Row([
                            ft.ElevatedButton(
                                text="Executar Eliminação de Gauss",
                                icon=ft.Icons.PLAY_ARROW,
                                icon_color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.GREEN_700,
                                color=ft.Colors.WHITE,
                                on_click=executar_gauss
                            ),
                            ft.ElevatedButton(
                                text="Mostrar Matriz",
                                icon=ft.Icons.TABLE_CHART,
                                icon_color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.BLUE_700,
                                color=ft.Colors.WHITE,
                                on_click=mostrar_matriz
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
                        ),
                        
                        ft.Container(
                            content=solucao_text,
                            padding=15,
                            border_radius=10,
                            bgcolor=ft.Colors.GREEN_50,
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
                        ft.Text("Operações Realizadas", size=16, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Column([tabela_operacoes], scroll=ft.ScrollMode.AUTO),
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