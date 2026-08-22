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

    return np.sin(x)+np.cos(x)

def g(x,a,b):
    '''
            Essa funcao calcula e retorna o
            valor de g no ponto x
    '''

    return np.log((np.cos(x)-b)/a)

def main():
    '''
               Essa funcao plota os graficos
               de P(x) e f(x)
    '''
    #Note que, nesse caso, n=1
    a=1
    lista_b=[-np.sqrt(2)-1e-10,-100]
    vetor_x=[-2*np.pi,np.pi] # Guarda o vetor [x0,x1]
    x_barra = -np.pi/2
    f_barra = f(x_barra)
    for b in lista_b:
        vetor_g = g(vetor_x, a, b)  # Guarda o vetor [g(x0),g(x1)]
        diagonal_pg=coeficientes(vetor_x,vetor_g)

        pontosx_paraPlotar = []  # Vetor de pontos x para plotar os gráficos
        pontosf_paraPlotar = []  # Vetor de pontos f(x) para plotar os gráficos
        pontos_h_paraPlotar = []  # Vetor de pontos h(x) para plotar os gráficos

        m = 10000  # Número de pontos para plotar os gráficos
        delta = (3 * np.pi) / m

        for i in range(10001):
            xi = -2 * np.pi + i * delta
            pontosx_paraPlotar.append(xi)

            # Construindo a função h
            px_g = constroiPolinomio(xi, vetor_x, vetor_g, diagonal_pg)
            pontos_h_paraPlotar.append(np.e ** (px_g) + b)

            # Construindo a função f
            pontosf_paraPlotar.append(f(xi))


        # Calculando h(x_barra)
        px_g_barra = constroiPolinomio(
            x_barra,
            vetor_x,
            vetor_g,
            diagonal_pg
        )

        h_barra = np.e ** (px_g_barra) + b

        # Erro em x_barra
        erro = abs(f_barra - h_barra)

        print(f"f(x̄) = {f_barra:.5f}")
        print(f"h(x̄) = {h_barra:.5f}")
        print(f"|f(x̄) - h(x̄)| = {erro:.5e}")


        # Plotando os gráficos

        plt.figure(figsize=(10, 6))

        # Gráfico de f(x)
        plt.plot(
            pontosx_paraPlotar,
            pontosf_paraPlotar,
            label="f(x)",
            color="blue"
        )

        # Gráfico de h(x)
        plt.plot(
            pontosx_paraPlotar,
            pontos_h_paraPlotar,
            label="h(x)",
            color="green"
        )


        # Destacando os pontos em x̄

        plt.scatter(
            [x_barra],
            [f_barra],
            color="blue",
            s=60,
            zorder=5,
            label=r"$f(\bar{x})$"
        )

        plt.scatter(
            [x_barra],
            [h_barra],
            color="green",
            s=60,
            zorder=5,
            label=r"$h(\bar{x})$"
        )

        # Linha vertical representando o erro

        plt.plot(
            [x_barra, x_barra],
            [f_barra, h_barra],
            color="red",
            linestyle="--",
            linewidth=2,
            label=rf"$|f(\bar{{x}})-h(\bar{{x}})|={erro:.4e}$"
        )

        # Configurações do gráfico

        plt.legend()
        plt.title(f"Interpolação por Exponencial com b={b:.5f}")
        plt.xlabel(r"$x$")
        plt.ylabel(r"$f(x),\,h(x)$")
        plt.grid(True)

        plt.show()

main()
