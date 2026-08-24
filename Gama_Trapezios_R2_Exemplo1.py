import numpy as np

def f(x1,x2):

    return (np.e**(np.sin(x1)))*x2

def Delta(x1):

    num1=(np.e**(2*np.sin(x1)))*(np.cos(x1)**4)
    num2=(np.e**(2*np.sin(x1)))*(np.cos(x1)**2)

    dif=num1/2-num2/2

    return (dif**2)/2

def theta(x1):
    return (np.e**(np.sin(x1)))*(np.cos(x1)**2-np.cos(x1))

def Psi1(x1):
    num1=np.e**(2*np.sin(x1))

    num2=(2*(np.cos(x1))**5-2*np.cos(x1)**3+2*np.sin(x1)*np.cos(x1)-4*(np.cos(x1)**3)*np.sin(x1))

    return num1*num2/2

def delta(x1):
    return np.cos(x1)**2-np.cos(x1)


def ordem_convergencia(erro_n,erro_2n):
    '''
           Essa funcao calcula a ordem
           de convergencia
    '''


    return abs(np.log(erro_n/erro_2n)/np.log(2))


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
    h12,h11=-5,5
    valor_exato=-0.75540596655
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
