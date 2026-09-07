import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize,shgo

def coeficientes(vetor_x, vetor_f):
    '''
    Essa funcao calcula os coeficientes do polinomio
    interpolador a partir das diferencas de Newton.
    Recebe o vetor_ com os pontos [x0,...,xn] e
    o vetor_f com os pontos [f(x_0),f(x_1),...,f(x_n)].
    Retorna um vetor com os coeficientes a0,...,an
    '''


    n=len(vetor_x)

    ar=np.zeros((n,n),float)


    i=0
    for f in vetor_f:
        ar[i][0]=f
        i+=1


    for col in range(1,n):
        for lin in range(col,n):
            ar[lin][col]=(ar[lin][col-1]-ar[lin-1][col-
            1])/(vetor_x[lin]-vetor_x[lin-col])

    diagonal=[]
    for q in range(n):
        diagonal.append(ar[q][q])
    return diagonal

def constroiPolinomio(x,vetor_x, vetor_f, coeficientes):
    '''
        Essa funcao constroi o polinomio interpolador P,
        ja calculado no ponto x.

        Recebe: O ponto x para se calcular P(x), o vetor_x=[x0,...,xn] ,
        o vetor_f=[f(x_0),f(x_1),...,f(x_n)] e o vetor
        coeficientes=[a0,a1,...,an].

        Retorna: O valor de P(x)
    '''

    P_x=vetor_f[0]
    for i in range(1,len(vetor_x)):
        polinomio=1
        for k in range(i):
            polinomio*=x-vetor_x[k]
        P_x+=polinomio*coeficientes[i]

    return P_x


def Calculadora_PolinomiosLagrange(vetor_x,x_barra,n):
    #Constroi os polinomios de Lagrange
    vetor_L=[]
    for k in range(n):
        L = 1
        for i in range(n):
            if i != k:
                L=((x_barra-vetor_x[i])/(vetor_x[k]-vetor_x[i]))*L
        vetor_L.append(L)
    return vetor_L

def Otimizando_b(vetor_x,vetor_f,inf_f,a):
    n=len(vetor_x) #n+1
    pontos_otimo=[] #Lista que guarda os pontos otimos
    for i in range(n-1):
        xi=vetor_x[i]
        xii=vetor_x[i+1]
        x_barra=(xi+xii)/2
        vetor_L = Calculadora_PolinomiosLagrange(vetor_x, x_barra, n)

        #Construindo o polinomio pg
        #Note que a=1
        def funcao_objetivo(b):
            soma = 0
            for i in range(n):
                soma += np.log((vetor_f[i] - b)/a) * (vetor_L[i])
            return abs(a*np.e**soma + b - f(x_barra))
        if inf_f>0:
            b0 = np.array([inf_f/2]) #Valor inicial
        elif inf_f>0:
            b0=np.array([inf_f+inf_f/2])
        else:
            b0=np.array([inf_f-0.5])
        limites = [(-100000, inf_f-1e-12)]
        resultado = minimize(funcao_objetivo, b0, bounds=limites, method='L-BFGS-B')
        pontos_otimo.append(resultado.x[0])
    pontos_otimo=np.array(pontos_otimo)

    print(f"Para n={n-1}, temos os valores de b otimo:{pontos_otimo}")
    return np.median(pontos_otimo)


def f(x):
    '''
            Essa funcao calcula e retorna o
            valor de f no ponto x
    '''
    return 1/(x**2+1) #Para o exemplo 1
    # return np.e**(np.sin(x)) #Para o exemplo 2
    #return np.log(x**2+1) #Para o exemplo 3

def g(x,a,b):
    '''
            Essa funcao calcula e retorna o
            valor de g no ponto x
    '''

    return np.log((f(x)-b)/a)


def main(n):
    """
    Essa funcao plota os graficos de P(x), f(x) e h(x) destacando os
    erros em alguns pontos
    """
    # Intervalo c,d
    #c, d = -5, 5  # Exemplo 1 (descomente conforme o exemplo)
    #c,d=-5,10 # Exemplo 2
    c,d=-10,10 # Exemplo 3

    a = 1
    vetor_x = np.linspace(c, d, n + 1)
    vetor_f = f(vetor_x)

    # Ínfimo de f
    #inf_f = 1 / 26  # Exemplo 1
    #inf_f = 1/np.e # Exemplo 2
    inf_f = 0 # Exemplo 3

    b_otimo = Otimizando_b(vetor_x, vetor_f, inf_f, a)
    vetor_g = g(vetor_x, a, b_otimo)

    diagonal_pg = coeficientes(vetor_x, vetor_g)
    diagonal_p = coeficientes(vetor_x, vetor_f)

    # Malha contínua para plotagem
    m = 10000
    pontosx_paraPlotar = np.linspace(c, d, m + 1)
    pontosf_paraPlotar = f(pontosx_paraPlotar)

    pontosP_paraPlotar = np.array(
        [
            constroiPolinomio(xi, vetor_x, vetor_f, diagonal_p)
            for xi in pontosx_paraPlotar
        ]
    )
    px_g_all = np.array(
        [
            constroiPolinomio(xi, vetor_x, vetor_g, diagonal_pg)
            for xi in pontosx_paraPlotar
        ]
    )
    pontos_h_paraPlotar = a * np.exp(px_g_all) + b_otimo

    # ---------------------------------------------------------
    # Cálculo das diferenças nos 3 pontos de interesse
    # ---------------------------------------------------------
    x_primeiros = (vetor_x[0] + vetor_x[1]) / 2.0
    x_centro = (c + d) / 2.0
    x_ultimos = (vetor_x[-2] + vetor_x[-1]) / 2.0

    pontos_interesse = {
        "Início": x_primeiros,
        "Centro": x_centro,
        "Fim": x_ultimos,
    }

    fig, ax = plt.subplots(figsize=(12, 7.5))

    ax.plot(
        pontosx_paraPlotar,
        pontosf_paraPlotar,
        label="f(x)",
        color="red",
        linewidth=1.5,
    )
    ax.plot(
        pontosx_paraPlotar,
        pontosP_paraPlotar,
        label="p(x)",
        color="blue",
        linewidth=1.5,
    )
    ax.plot(
        pontosx_paraPlotar,
        pontos_h_paraPlotar,
        label="h(x)",
        color="green",
        linewidth=1.5,
    )

    estilos = {
        "Início": "purple",
        "Centro": "darkorange",
        "Fim": "brown",
    }

    # Calcula amplitude vertical total para criar margem segura no topo
    y_min = min(
        min(pontosf_paraPlotar),
        min(pontosP_paraPlotar),
        min(pontos_h_paraPlotar),
    )
    y_max = max(
        max(pontosf_paraPlotar),
        max(pontosP_paraPlotar),
        max(pontos_h_paraPlotar),
    )
    amplitude_y = y_max - y_min

    # Define o limite do eixo Y com folga extra para os balões de texto
    ax.set_ylim(y_min - 0.1 * amplitude_y, y_max + 0.8 * amplitude_y)

    for rotulo, x_eval in pontos_interesse.items():
        y_f = f(x_eval)
        y_p = constroiPolinomio(x_eval, vetor_x, vetor_f, diagonal_p)
        y_g = constroiPolinomio(x_eval, vetor_x, vetor_g, diagonal_pg)
        y_h = a * np.exp(y_g) + b_otimo

        diff_hf = abs(y_h - y_f)
        diff_hp = abs(y_h - y_p)
        diff_pf = abs(y_p - y_f)

        cor = estilos[rotulo]

        # Linha vertical indicadora do ponto de amostragem
        ax.axvline(
            x=x_eval,
            color=cor,
            linestyle="--",
            alpha=0.6,
            label=f"Ponto {rotulo} (x={x_eval:.2f})",
        )

        # Marcadores nos pontos
        ax.scatter([x_eval] * 3, [y_f, y_p, y_h], color=cor, s=35, zorder=5)

        texto_diff = (
            f"[{rotulo}]\n"
            f"|h-f| = {diff_hf:.2e}\n"
            f"|h-p| = {diff_hp:.2e}\n"
            f"|p-f| = {diff_pf:.2e}"
        )

        # Ajuste de altura alternada para as caixas de texto
        y_topo_ponto = max(y_f, y_p, y_h)

        if rotulo == "Centro":
            # Caixa do centro posicionada com deslocamento controlado
            y_texto = y_topo_ponto + 0.12 * amplitude_y
        else:
            # Caixas das pontas levemente mais altas
            y_texto = y_topo_ponto + 0.18 * amplitude_y

        ax.annotate(
            texto_diff,
            xy=(x_eval, y_topo_ponto),
            xytext=(x_eval, y_texto),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=cor, alpha=0.9),
            arrowprops=dict(
                arrowstyle="->", color=cor, lw=1, connectionstyle="arc3"
            ),
            ha="center",
            fontsize=8,
        )

    ax.legend(loc="upper left")
    ax.set_title(
        f"Interpolação por Exponencial (b*={b_otimo:.5f}, n={n})\nComparações em x_inicio, x_centro e x_fim",
        pad=15,
    )
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    plt.tight_layout()
    plt.show()


lista_n=[2,5,10,15]
for n in lista_n:
    main(n)
