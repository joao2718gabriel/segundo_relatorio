import numpy as np

def f(x):
    return np.log(x**2+2)

def f_linha(x):
    return (2*x)/(x**2+2)

def Simpson(vetor_x,h):
    n=len(vetor_x)
    integral=f(vetor_x[0])+f(vetor_x[n-1])
    for i in range(1,n-1):
        if i%2==0:
            integral+=2*f(vetor_x[i])
        else:
            integral+=4*f(vetor_x[i])
    return (h/3)*integral
def p(x):
    L0=(x-3)*(x-4)*(x-5)/(-6)
    L1=(x-2)*(x-4)*(x-5)/(2)
    L2=(x-2)*(x-3)*(x-5)/(-2)
    L3=(x-2)*(x-3)*(x-4)/(6)

    return L0*f(2)+L1*f(3)+L2*f(4)+L3*f(5)

def p_linha(x):
    l0=(3*(x**2)-24*x+47)/(-6)
    l1 = (3 * (x ** 2) - 22 * x + 38) / (2)
    l2 = (3 * (x ** 2) - 20 * x + 31) / (-2)
    l3 = (3 * (x ** 2) - 18 * x + 26) / (6)

    return l0 * f(2) + l1 * f(3) + l2 * f(4) + l3 * f(5)



def P(x):
    l0=((x**4)/4-12*(x**3)/3+47*(x**2)/2-60*x)/(-6)
    l1 = ((x ** 4) / 4 - 11 * (x ** 3) / 3 + 38 * (x ** 2) / 2 - 40 * x) / (2)
    l2 = ((x ** 4) / 4 - 10 * (x ** 3) / 3 + 31 * (x ** 2) / 2 - 30 * x) / (-2)
    l3 = ((x ** 4) / 4 - 9 * (x ** 3) / 3 + 26 * (x ** 2) / 2 - 24 * x) / (6)

    return l0 * f(2) + l1 * f(3) + l2 * f(4) + l3 * f(5)

def gama(x):
    return (p_linha(x)/(p(x)**2))*P(x)

def formula_quadratura(xi,xii,h):
    '''
       Calcula a formula de qudratura dada no relatorio
    '''
    numerador=gama(xii)*(f(xii)**2)/f_linha(xii)-gama(xi)*(f(xi)**2)/f_linha(xi)
    integral_gama=xii-P(xii)/p(xii)-(xi-P(xi)/p(xi))
    denominador=gama(xii)*(f(xii))/f_linha(xii)-gama(xi)*(f(xi))/f_linha(xi)+integral_gama

    return h*(numerador/denominador)

def ordem_convergencia(erro_n,erro_2n):
    '''
           Essa funcao calcula a ordem
           de convergencia
    '''


    return abs(np.log(erro_n/erro_2n)/np.log(2))


def gerar_tabelas(lista_integrais_gama, lista_erros_gama, lista_ordem_gama,
                  lista_integrais_simpson, lista_erros_simpson,
                  lista_ordem_simpson):

    # Valores de n
    lista_n = [2**k for k in range(1, 11)]

    # ==========================================================
    # TABELA - MÉTODO GAMA
    # ==========================================================

    print(r"\begin{table}[ht]")
    print(r"\centering")
    print(r"\begin{tabular}{cccc}")
    print(r"\hline")
    print(r"$n$ & Integral Aproximada & Erro Exato & Ordem de Convergência \\")
    print(r"\hline")

    for i in range(len(lista_n)):

        n = lista_n[i]

        aproximacao = lista_integrais_gama[i]
        erro = lista_erros_gama[i]

        # Para n=2 ainda não existe ordem de convergência
        if i == 0:
            ordem = "--"
        else:
            ordem = f"{lista_ordem_gama[i-1]:.10f}"

        print(
            f"{n} & "
            f"{aproximacao:.10f} & "
            f"{erro:.10f} & "
            f"{ordem} \\\\"
        )

    print(r"\hline")
    print(r"\end{tabular}")
    print(r"\caption{Resultados obtidos pelo método Gama.}")
    print(r"\label{tab:gama-exemploNumerico-aplicacaoTeorema}")
    print(r"\end{table}")


    print("\n")


    # ==========================================================
    # TABELA - MÉTODO DE SIMPSON
    # ==========================================================

    print(r"\begin{table}[ht]")
    print(r"\centering")
    print(r"\begin{tabular}{cccc}")
    print(r"\hline")
    print(r"$n$ & Integral Aproximada & Erro Exato & Ordem de Convergência \\")
    print(r"\hline")

    for i in range(len(lista_n)):

        n = lista_n[i]

        aproximacao = lista_integrais_simpson[i]
        erro = lista_erros_simpson[i]

        # Para n=2 ainda não existe ordem de convergência
        if i == 0:
            ordem = "--"
        else:
            ordem = f"{lista_ordem_simpson[i-1]:.10f}"

        print(
            f"{n} & "
            f"{aproximacao:.10f} & "
            f"{erro:.10f} & "
            f"{ordem} \\\\"
        )

    print(r"\hline")
    print(r"\end{tabular}")
    print(r"\caption{Resultados obtidos pelo método de Simpson.}")
    print(r"\label{tab:simpson-exemploNumerico-aplicacaoTeorema}")
    print(r"\end{table}")


#tab:simpson-exemploNumerico-aplicacaoTeorema
def main():
    lista_erros_gama = []  # lista que guarda os erros exatos
    lista_erros_simpson = []
    lista_ordem_gama = []  # lista que guarda as ordens de convergencia
    lista_ordem_simpson = []
    lista_integrais_gama = []
    lista_integrais_simpson = []
    for k in range(1,11):
        n=2**k
        h=3/n
        vetor_x=[2] #lista com os pontos [x0,x1,...,xn]
        integral_metodo_gama=0
        for i in range(n):
            xi=2+i*h
            xii=2+(i+1)*h
            vetor_x.append(xii)
            integral_metodo_gama+=formula_quadratura(xi,xii,h)
        integral_simpson=Simpson(vetor_x,h)

        valor_exato=7.8568693242
        erro_gama=abs(integral_metodo_gama-valor_exato)
        erro_simpson=abs(integral_simpson-valor_exato)
        lista_erros_gama.append(erro_gama)
        lista_erros_simpson.append(erro_simpson)
        lista_integrais_gama.append(integral_metodo_gama)
        lista_integrais_simpson.append(integral_simpson)

        if k>1:
            lista_ordem_gama.append(ordem_convergencia(lista_erros_gama[k-2],lista_erros_gama[k-1]))
            lista_ordem_simpson.append(ordem_convergencia(lista_erros_simpson[k - 2], lista_erros_simpson[k - 1]))

    gerar_tabelas(lista_integrais_gama,lista_erros_gama,lista_ordem_gama,lista_integrais_simpson
                 ,lista_erros_simpson,lista_ordem_simpson)



main()
