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
               de P(x) e f(x)
    '''
    a=1
    for k in range(1,7):
        b=-2**k
        vetor_x = np.array([-5,-3,-1,1,3,5]) # Insira aqui o vetor [x0,x1,...,xn]
        vetor_f=f(vetor_x)#Insira aqui o vetor [f(x0),f(x1),...,f(xn)]
        vetor_g =g(vetor_x,a,b)  # Guarda o vetor [g(x0),g(x1),...,g(xn)]
        diagonal_p=coeficientes(vetor_x,vetor_f) #Vetor dos coeficientes [a0,a1,...,an] do polinomio p_5
        diagonal_pg=coeficientes(vetor_x,vetor_g)

        pontosx_paraPlotar = []  # Esse e o vetor de pontos x para plotar os graficos
        pontosf_paraPlotar=[]  # Esse e o vetor de pontos f(x) para plotar os graficos
        pontosP_paraPlotar=[]  # Esse e o vetor de pontos p_5(x) para plotar os graficos
        pontos_h_paraPlotar=[] # Esse e o vetor de pontos h(x) para plotar os graficos
        m=10000 #numero de pontos para plotar os graficos
        delta=10/m #(5-(-5))/m
        for i in range(10001):
            xi=-5+i*delta
            pontosx_paraPlotar.append(xi)

            #Construindo polinomio p_10
            px=constroiPolinomio(xi,vetor_x,vetor_f,diagonal_p)
            pontosP_paraPlotar.append(px)

            #Construindo a funcao h
            px_g = constroiPolinomio(xi, vetor_x, vetor_g, diagonal_pg)
            pontos_h_paraPlotar.append(np.e**(px_g)+b)

            #Construindo a funcao f
            pontosf_paraPlotar.append(f(xi))


        #Plotando os graficos
        plt.plot(pontosx_paraPlotar, pontosf_paraPlotar, label="f(x)", color="red")
        plt.plot(pontosx_paraPlotar, pontosP_paraPlotar, label="p_5(x)", color="blue")
        plt.plot(pontosx_paraPlotar, pontos_h_paraPlotar, label="h(x)", color="green")
        plt.legend()
        plt.title(f"Interpolação por Exponencial com b={b:.1f}")
        plt.grid(True)
        plt.show()

main()
