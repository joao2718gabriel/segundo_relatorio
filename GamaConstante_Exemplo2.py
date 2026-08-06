import numpy as np

def f(x):
    return 2*np.sqrt(25-x**2)/25

def Q(x):
    return (x**2-25)/x

def Q_linha(x):
    return (x**2+25)/(x**2)


def ordem_convergencia(erro_n,erro_2n):
    '''
           Essa funcao calcula a ordem
           de convergencia
    '''


    return abs(np.log(erro_n/erro_2n)/np.log(2))

def GamaConstante(xi,xii):
    '''
       Essa funcao calcula a formula de quadratura do Metodo
       Gama Constante para o intervalo [xi,xii]
    '''

    numerador=(xii**2-25)*f(xii)/xii-(xi**2-25)*f(xi)/xi
    denominador=(xii**2-25)/xii-(xi**2-25)/xi+xii-xi #Note que h=xii-xi
    return numerador/denominador



def erro_GamaConstante_Delta1(xi,xii,epsilon,h):
    '''
           Essa funcao calcula a estimativa de erro
           cometida pelo Metodo Gama Constante
           em [xi,xii], com x1<xii em Delta_1
    '''
    s=f(epsilon)
    numerador=Q_linha(xii)-Q_linha(xi)
    denominador=abs(Q(xii)-Q(xi)+h)
    return s*(h**2)*numerador/denominador

def erro_GamaConstante_Delta2(xi,xii,epsilon,h):
    '''
           Essa funcao calcula a estimativa de erro
           cometida pelo Metodo Gama Constante
           em [xi,xii], com x1<xii em Delta_2
    '''
    s = f(epsilon)
    numerador = Q_linha(xi) - Q_linha(xii)
    denominador = abs(Q(xii) - Q(xi) + h)
    return s*(h**2)*numerador/denominador



def gerar_tabela_latex(
    ordem_convergencia_gama,
    aproximacoes_gama_delta1,
    estimativa_erro_gama_delta1,
    aproximacao_trapezio,
    estimativa_trapezio,
    aproximacoes_gama_delta2,
    estimativa_erro_gama_delta2,
    aproximacao_gauss,
    erro_exato_gauss,
    erro_exato_gama
):

    # -------------------------------------------------------
    # Tabela do Método Gama Constante
    # -------------------------------------------------------

    tabela = []

    tabela.append(r"\begin{table}[ht]")
    tabela.append(r"\centering")
    tabela.append(r"\begin{tabular}{ccccccc}")
    tabela.append(r"\hline")
    tabela.append(
        r"$n$ & Em $\Delta_1$ & Em $\Delta_2$ & Integral em $[-5,5]$ & Estimativa de erro & Erro exato & Ordem de Convergência \\"
    )
    tabela.append(r"\hline")

    n = 2

    for i in range(len(aproximacoes_gama_delta1)):

        aproximacao_total = (
            aproximacoes_gama_delta1[i]
            + aproximacoes_gama_delta2[i]
            + aproximacao_trapezio
        )

        estimativa_total = (
            estimativa_erro_gama_delta1[i]
            + estimativa_erro_gama_delta2[i]
            + estimativa_trapezio
        )

        ordem = (
            f"{ordem_convergencia_gama[i]:.6f}"
            if ordem_convergencia_gama[i] is not None
            else "-"
        )

        tabela.append(
            f"{n} & "
            f"{aproximacoes_gama_delta1[i]:.4e} & "
            f"{aproximacoes_gama_delta2[i]:.4e} & "
            f"{aproximacao_total:.4e} & "
            f"{estimativa_total:.4e} & "
            f"{erro_exato_gama[i]:.4e} & "
            f"{ordem} \\\\"
        )

        n *= 2

    tabela.append(r"\hline")
    tabela.append(r"\end{tabular}")
    tabela.append(r"\caption{Resultados obtidos pelo Método Gama Constante}")
    tabela.append(r"\label{tab:gama_constante-exemplo2}")
    tabela.append(r"\end{table}")

    print("\n".join(tabela))

    # -------------------------------------------------------
    # Tabela do Método de Gauss
    # -------------------------------------------------------

    tabela_gauss = []

    tabela_gauss.append(r"\begin{table}[ht]")
    tabela_gauss.append(r"\centering")
    tabela_gauss.append(r"\begin{tabular}{cc}")
    tabela_gauss.append(r"\hline")
    tabela_gauss.append(r"Aproximação & Erro exato \\")
    tabela_gauss.append(r"\hline")

    tabela_gauss.append(
        f"{aproximacao_gauss:.4e} & "
        f"{erro_exato_gauss:.4e} \\\\"
    )

    tabela_gauss.append(r"\hline")
    tabela_gauss.append(r"\end{tabular}")
    tabela_gauss.append(r"\caption{Resultado obtido pela Quadratura Gaussiana}")
    tabela_gauss.append(r"\label{tab:gauss-exemplo2-gama-constante}")
    tabela_gauss.append(r"\end{table}")

    print("\n".join(tabela_gauss))




def main():
    epsilon=0.001

    valor_exato=np.pi
    #Aproximação do Metodo dos Trapezios para o intervalo [-epsilon,epsilon]
    integral_trapezios=2*epsilon*f(epsilon)
    #Estimaitiva do erro do Metodo dos Trapezios para o intervalo [-epsilon,epsilon]
    estimativa_erro_trapezios=4*(epsilon**3)*f(epsilon)/3

    #Calculando a Quadratura Gaussiana
    k1,k2,k3=0.7745966,0,-0.7745966
    w1,w2,w3=0.5,8/9,0.5
    integral_gauss=w1*(2*np.sqrt(1-k1**2))+w2*(2*np.sqrt(1-k2**2))+w3*(2*np.sqrt(1-k3**2))
    erro_exato_gauss=abs(integral_gauss-valor_exato)

    #Calculando o Metodo Gama para os intervalos [-5,-epsilon] e [epsilon,5]
    lista_erro_exato = []
    lista_integral_delta1 = []
    lista_integral_delta2 = []
    lista_estimativa_erro_gama_delta1 = []
    lista_estimativa_erro_gama_delta2 = []
    lista_ordem_convergencia = []
    for k in range(1,11):
        n=2**k
        h=(5-epsilon)/n
        integral_delta1 = 0
        integral_delta2 = 0
        estimativa_erro_gama_delta1 = 0
        estimativa_erro_gama_delta2 = 0
        for i in range(n):
            #Para o intervalo [-5,-epsilon]
            xi=-5+i*h
            xii=-5+(i+1)*h
            integral_delta1+=GamaConstante(xi,xii)
            estimativa_erro_gama_delta1+=erro_GamaConstante_Delta1(xi,xii,epsilon,h)

            # Para o intervalo [epsilon,5]
            yi = epsilon + i * h
            yii = epsilon + (i + 1) * h
            integral_delta2 += GamaConstante(yi, yii)
            estimativa_erro_gama_delta2 += erro_GamaConstante_Delta2(yi, yii, epsilon, h)

        lista_integral_delta1.append(h*integral_delta1)
        lista_estimativa_erro_gama_delta1.append(estimativa_erro_gama_delta1)
        lista_integral_delta2.append(h*integral_delta2)
        lista_estimativa_erro_gama_delta2.append(estimativa_erro_gama_delta2)

        integral=h*integral_delta1+h*integral_delta2+integral_trapezios
        erro_exato=abs(integral-valor_exato)
        lista_erro_exato.append(erro_exato)

        if k>1:
            lista_ordem_convergencia.append(ordem_convergencia(lista_erro_exato[k-2],lista_erro_exato[k-1]))
        else:
            lista_ordem_convergencia.append(None)
    gerar_tabela_latex(lista_ordem_convergencia,lista_integral_delta1,lista_estimativa_erro_gama_delta1
,integral_trapezios,estimativa_erro_trapezios,lista_integral_delta2,lista_estimativa_erro_gama_delta1,
integral_gauss,erro_exato_gauss,lista_erro_exato)


main()
