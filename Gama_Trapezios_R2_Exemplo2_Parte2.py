import numpy as np

def Delta(x1):

    num1=8*(x1**4)
    num2=8*(x1**3)
    dif=num1-num2
    return (dif**2)/2

def theta(x1):
    return 4*(x1**2)-4*(x1**(3/2))

def Psi1(x1):

    return 32*(x1**3)-24*(x1**2)

def delta(x1):
    return x1-np.sqrt(x1)


def gerar_tabela(erros, valores_aproximados):
    n = len(erros)

    tabela = r"""\begin{table}[H]
\centering
\begin{tabular}{cccc}
\hline
$n$ & Aproximação & Erro Exato  \\
\hline
"""

    for i in range(n):


        tabela += (
            f"{2**(i)} & "
            f"{valores_aproximados[i]:.10e} & "
            f"{erros[i]:.10e} & \\\\\n"
        )

    tabela += r"""\hline
\end{tabular}
\end{table}"""

    return tabela


def main():
    h12,h11=np.e**(-1/2),np.e**(3/2)
    valor_exato=141.7840616778
    valores_integral=[]#Lista que guarda os valores aproximados gerados pelo metodo
    erros=[]#Lista que guarda os erros exatos
    for k in range(15):
        n=2**k
        beta = (h11 - h12)/n
        integral=0
        for i in range(n):
            lambdai=h12+beta*i
            lambdaii=h12+beta*(i+1)

            I1=Delta(lambdaii)-Delta(lambdai)
            I2=beta*(Psi1(lambdaii)*theta(lambdaii)+Psi1(lambdai)*theta(lambdai))/2
            I3=beta*(delta(lambdaii)+delta(lambdai))/2

            integral+=I3*I1/I2


        valores_integral.append(integral)
        erro=abs(integral-valor_exato)
        erros.append(erro)


    #Gerando a tabela
    print(gerar_tabela(erros,valores_integral))
main()


