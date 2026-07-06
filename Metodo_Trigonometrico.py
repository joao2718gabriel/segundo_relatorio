import math
def f(x):
    return math.cos(x**2)



def Formula_metodoTrigonometrico_1interavalo(xi,xii):
    '''
       Essa funcao calcula, para o intervalo [xi,xii], a formula do metodo trigonometrico apresentada no relatorio
    '''

    numerador=math.sin(xii**2)-math.sin(xi**2)
    denominador=xi+xii

    return numerador/denominador

def metodo_trigonometrico(a,b,n):
    '''
           Essa funcao calcula a formula do metodo trigonometrico apresentada no relatorio
    '''

    delta=(b-a)/n
    x0=a
    integral=0
    for k in range(1,n+1):
        xi=x0+(k-1)*delta
        xii=x0+k*delta
        integral+=Formula_metodoTrigonometrico_1interavalo(xi,xii)
    return integral

def Estimativa_Erro_MetodoTrigonometrico(a,b,n):
    '''
                       Essa funcao calcula a estimativa de erro do metodo trigonometrico apresentada no relatorio
    '''
    Mf=3.0272099
    Mg=2
    Lambda_g=1
    delta=(b-a)/n
    return ((delta**2)*Mg*Lambda_g+delta)*(b-a)*Mf


def nTrapezios(a,b,n):
    '''
               Essa funcao calcula a formula do metodo dos n-Trapezios
    '''
    delta = (b - a) / n
    x0 = a
    integral = f(a)/2+f(b)/2
    for k in range(1, n):
        xi = x0 + k * delta
        integral += f(xi)
    return delta * integral

def Estimativa_Erro_nTrapezios(a,b,n):
    '''
                   Essa funcao calcula a estimativa de erro do metodo dos n-Trapezios
    '''

    M2=13.82693087
    delta=(b-a)/n

    return M2*(delta**2)*(b-a)/12


def gerar_tabela_latex(dados, titulo, legenda, label):
    """
    Gera tabela em LaTeX no para o relatório.
    """

    latex = []

    latex.append(r"\begin{table}[H]")
    latex.append(r"\centering")
    latex.append(r"\begin{tabular}{|c|c|c|c|c|}")
    latex.append(r"\hline")
    latex.append(
        r"$n$ & Integral Aproximada & Erro Aproximado & Erro Exato & Ordem de Convergência \\"
    )
    latex.append(r"\hline")

    for linha in dados:
        n, integral, erro_aprox, erro_exato, ordem = linha

        integral_str = f"{integral:.7f}"
        erro_aprox_str = f"{erro_aprox:.7f}"
        erro_exato_str = f"{erro_exato:.7f}"

        if ordem is None:
            ordem_str = ""
        else:
            ordem_str = f"{ordem:.7f}"

        latex.append(
            f"{n} & {integral_str} & {erro_aprox_str} & "
            f"{erro_exato_str} & {ordem_str} \\\\"
        )

    latex.append(r"\hline")
    latex.append(r"\end{tabular}")
    latex.append(f"\\caption{{{legenda}}}")
    latex.append(f"\\label{{{label}}}")
    latex.append(r"\end{table}")

    print("\n")
    print("="*80)
    print(titulo.upper())
    print("="*80)
    print("\n".join(latex))
    print("\n")


def main():
    """
    Gera tabelas em LaTeX dos métodos de integração.
    """

    valor_exato = -0.4430627749
    a, b = 1,2

    dados_trigonometrico = []
    dados_trapezio = []

    erros_exatos1 = []
    erros_exatos2 = []

    for k in range(11):

        n = 2**k

        integral_metodo_trigonometrico = metodo_trigonometrico(a, b, n)
        integral_metodo_trapezio = nTrapezios(a, b, n)

        erro_exato1 = abs(integral_metodo_trigonometrico - valor_exato)
        erro_exato2 = abs(integral_metodo_trapezio - valor_exato)

        erro_aproximado1 = Estimativa_Erro_MetodoTrigonometrico(a, b, n)
        erro_aproximado2 = Estimativa_Erro_nTrapezios(a, b, n)

        erros_exatos1.append(erro_exato1)
        erros_exatos2.append(erro_exato2)

        # Ordem de convergência
        if k == 0:
            ordem1 = None
            ordem2 = None
        else:
            ordem1 = math.log(
                erros_exatos1[k - 1] / erros_exatos1[k], 2
            )

            ordem2 = math.log(
                erros_exatos2[k - 1] / erros_exatos2[k], 2
            )

        dados_trigonometrico.append([
            n,
            integral_metodo_trigonometrico,
            erro_aproximado1,
            erro_exato1,
            ordem1
        ])

        dados_trapezio.append([
            n,
            integral_metodo_trapezio,
            erro_aproximado2,
            erro_exato2,
            ordem2
        ])

    # Gerar tabela LaTeX do Método Trigonométrico
    gerar_tabela_latex(
        dados_trigonometrico,
        titulo="Método Trigonométrico",
        legenda=r"Analisando o Método Trigonométrico para $\int_{1}^{2} \cos(x^2)dx$",
        label="tab:metodo_trigonometrico"
    )

    # Gerar tabela LaTeX do método dos n-trapézios
    gerar_tabela_latex(
        dados_trapezio,
        titulo="Método dos n-Trapézios",
        legenda=r"Analisando o Método dos $n$-Trapézios para $\int_{1}^{2} \cos(x^2)dx$",
        label="tab:metodo_trapezios-trigometrico"
    )


main()
