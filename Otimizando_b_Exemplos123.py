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
    '''
               Essa funcao plota os graficos
               de P(x) e f(x)
    '''
    # Intervalo c,d
    c,d=-5,5 #Para o exemplo 1
    #c,d=-5,10 #Para o exemplo 2
    #c,d=-10,10 #Para o exemplo 3
    a=1
    vetor_x=[] #[x0,x1,...,xn]
    h=(d-c)/n
    for i in range(n+1):
        xi=c+i*h
        vetor_x.append(xi)
    vetor_x=np.array(vetor_x)
    vetor_f=f(vetor_x)

    #Infimo de f
    inf_f=1/26 #Para o exemplo 1
    #inf_f=1/np.e #Para o exemplo 2
    #inf_f=0 #Para o exemplo 3
    b_otimo=Otimizando_b(vetor_x,vetor_f,inf_f,a)
    vetor_g = g(vetor_x, a, b_otimo)  # [g(x0),g(x1),...,g(xn)]
    diagonal_pg = coeficientes(vetor_x, vetor_g)



    diagonal_p = coeficientes(vetor_x, vetor_f)  # Vetor dos coeficientes [a0,a1,...,an] do polinomio interpolador p
    pontosx_paraPlotar = []  # Esse e o vetor de pontos x para plotar os graficos
    pontosf_paraPlotar = []  # Esse e o vetor de pontos f(x) para plotar os graficos
    pontosP_paraPlotar = []  # Esse e o vetor de pontos p_5(x) para plotar os graficos
    pontos_h_paraPlotar = []  # Esse e o vetor de pontos h(x) para plotar os graficos
    m = 10000  # numero de pontos para plotar os graficos
    delta = (d-c) / m  # (5-(-5))/m
    for i in range(10001):
        xi = c + i * delta
        pontosx_paraPlotar.append(xi)

        # Construindo polinomio p
        px = constroiPolinomio(xi, vetor_x, vetor_f, diagonal_p)
        pontosP_paraPlotar.append(px)

        # Construindo a funcao h
        px_g = constroiPolinomio(xi, vetor_x, vetor_g, diagonal_pg)
        pontos_h_paraPlotar.append(a*np.e ** (px_g) + b_otimo)

        # Construindo a funcao f
        pontosf_paraPlotar.append(f(xi))

    # Plotando os graficos
    plt.plot(pontosx_paraPlotar, pontosf_paraPlotar, label="f(x)", color="red")
    plt.plot(pontosx_paraPlotar, pontosP_paraPlotar, label="p(x)", color="blue")
    plt.plot(pontosx_paraPlotar, pontos_h_paraPlotar, label="h(x)", color="green")
    plt.legend()
    plt.title(f"Interpolação por Exponencial com b*={b_otimo:.5f} e n={n}")
    plt.grid(True)
    plt.show()


lista_n=[2,5,10,15]
for n in lista_n:
    main(n)
