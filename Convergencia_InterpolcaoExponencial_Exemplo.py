import numpy as np
import matplotlib.pyplot as plt

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

def f(x):
    '''
            Essa funcao calcula e retorna o
            valor de f no ponto x
    '''

    return np.cos(x)

def g(x,a,b):
    '''
            Essa funcao calcula e retorna o
            valor de g no ponto x
    '''

    return np.log((np.cos(x)-b)/a)

def main():
    '''
        Essa funcao plota os graficos
        de P(x), f(x), h(x) e |h(x)-p_5(x)|
    '''
    a = 1

    for k in range(1, 7):
        b = -2**k

        vetor_x = np.array([-5, -3, -1, 1, 3, 5])
        vetor_f = f(vetor_x)
        vetor_g = g(vetor_x, a, b)

        diagonal_p = coeficientes(vetor_x, vetor_f)
        diagonal_pg = coeficientes(vetor_x, vetor_g)

        pontosx_paraPlotar = []
        pontosf_paraPlotar = []
        pontosP_paraPlotar = []
        pontos_h_paraPlotar = []
        pontos_hp_paraPlotar = []

        m = 10000
        delta = 10/m

        for i in range(10001):
            xi = -5 + i*delta
            pontosx_paraPlotar.append(xi)

            # Polinomio p_5
            px = constroiPolinomio(
                xi, vetor_x, vetor_f, diagonal_p
            )
            pontosP_paraPlotar.append(px)

            # Funcao h
            px_g = constroiPolinomio(
                xi, vetor_x, vetor_g, diagonal_pg
            )

            hx = np.e**(px_g) + b
            pontos_h_paraPlotar.append(hx)

            # Erro |h(x)-p_5(x)|
            pontos_hp_paraPlotar.append(abs(hx - px))

            # Funcao f
            pontosf_paraPlotar.append(f(xi))

        # =====================================================
        # Valores em x = 0
        # =====================================================

        x0 = 0

        # p_5(0)
        p5_0 = constroiPolinomio(
            x0, vetor_x, vetor_f, diagonal_p
        )

        # h(0)
        pg_0 = constroiPolinomio(
            x0, vetor_x, vetor_g, diagonal_pg
        )

        h_0 = np.e**(pg_0) + b

        # Diferenca
        diferenca = abs(h_0 - p5_0)

        # =====================================================
        # Plot
        # =====================================================

        plt.figure(figsize=(10, 6))

        plt.plot(
            pontosx_paraPlotar,
            pontosf_paraPlotar,
            label="f(x)",
            color="red"
        )

        plt.plot(
            pontosx_paraPlotar,
            pontosP_paraPlotar,
            label="p_5(x)",
            color="blue"
        )

        plt.plot(
            pontosx_paraPlotar,
            pontos_h_paraPlotar,
            label="h(x)",
            color="green"
        )

        plt.plot(
            pontosx_paraPlotar,
            pontos_hp_paraPlotar,
            label=r"$|h(x)-p_5(x)|$",
            color="orange",
            linestyle="--"
        )

        # =====================================================
        # Destaque dos pontos x = 0
        # =====================================================

        plt.scatter(
            0, p5_0,
            color="blue",
            s=100,
            zorder=5
        )

        plt.scatter(
            0, h_0,
            color="green",
            s=100,
            zorder=5
        )

        # Linha vertical mostrando a diferença
        plt.vlines(
            x=0,
            ymin=min(p5_0, h_0),
            ymax=max(p5_0, h_0),
            color="black",
            linestyle="--",
            linewidth=2,
            label=rf"$|h(0)-p_5(0)|={diferenca:.4e}$"
        )

        # Linhas horizontais pequenas nos pontos
        plt.plot(
            [-0.08, 0.08],
            [p5_0, p5_0],
            color="blue",
            linewidth=2
        )

        plt.plot(
            [-0.08, 0.08],
            [h_0, h_0],
            color="green",
            linewidth=2
        )

        # Anotações
        plt.annotate(
            rf"$p_5(0)={p5_0:.4f}$",
            (0, p5_0),
            xytext=(10, -20),
            textcoords="offset points",
            color="blue",
            fontsize=10
        )

        plt.annotate(
            rf"$h(0)={h_0:.4f}$",
            (0, h_0),
            xytext=(10, 10),
            textcoords="offset points",
            color="green",
            fontsize=10
        )

        # Linha vertical em x=0
        plt.axvline(
            x=0,
            color="gray",
            linestyle=":",
            linewidth=1
        )

        plt.legend()
        plt.title(f"Interpolação por Exponencial com b={b:.1f}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)

        plt.show()


main()
