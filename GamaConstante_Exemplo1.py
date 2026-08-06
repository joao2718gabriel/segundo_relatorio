import numpy as np

def f(x):
    return np.log(x)


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

    numerador=xii*(f(xii)**2)-xi*(f(xi)**2)
    denominador=xii*f(xii)-xi*f(xi)+xii-xi #Note que h=xii-xi
    return numerador/denominador

def erro_GamaConstante(h):
    '''
           Essa funcao calcula a estimativa de erro
           cometida pelo Metodo Gama Constante
    '''

    return ((h**2)*((1/np.e)+1)*(1/3)+h)*(np.e-1)

def Simpson(vetor_x,h):
    '''
           Essa funcao recebe o vetor [x0,...,xn], h e
           calcula a formula de n-Simpsons
           para o interavlo (dividido em
           n subintervalos)
    '''

    n=len(vetor_x)
    integral=f(vetor_x[0])+f(vetor_x[n-1])
    for k in range(1,n-1):
        if k%2==0:
            integral+=2*f(vetor_x[k])
        else:
            integral += 4*f(vetor_x[k])
    return (h/3)*integral

def erro_n_Simpsons(h):
    '''
           Essa funcao calcula a estimativa de erro
           cometida pelo Metodo dos n-Simpsons
    '''

    return 6*(np.e-1)*(h**4)/(180*(np.e**3))



def main():
    '''
    Essa funcao calcula as duas
    integrais e devolve duas tabelas
    em LaTeX, uma para cada método.
    '''

    a, b = np.e, np.e**2
    vetor_erros_n_gama = []
    vetor_erros_n_simpson = []

    dados_gama = []
    dados_simpson = []

    for i in range(1, 11):
        n = 2**i

        # Calculando h
        h = (b - a) / n

        estimativa_erro_gama = erro_GamaConstante(h)
        estimativa_erro_simpson = erro_n_Simpsons(h)

        # Método Gama Constante
        vetor_x = []
        integral_gama = 0
        for j in range(n):
            xi = a + j*h
            xii = a + (j + 1)*h
            integral_gama += GamaConstante(xi, xii)
            vetor_x.append(xi)

        integral_gama = h*integral_gama
        vetor_x.append(b)


        # Método de Simpson
        integral_simpsons = Simpson(vetor_x, h)

        # Valor exato
        valor_exato = np.e**2

        erro_exato_gama = abs(valor_exato - integral_gama)
        erro_exato_simpson = abs(valor_exato - integral_simpsons)

        vetor_erros_n_gama.append(erro_exato_gama)
        vetor_erros_n_simpson.append(erro_exato_simpson)

        if i == 1:
            convergencia_gama = "-"
            convergencia_simpson = "-"
        else:
            convergencia_gama = ordem_convergencia(
                vetor_erros_n_gama[i-2], vetor_erros_n_gama[i-1]
            )
            convergencia_simpson = ordem_convergencia(
                vetor_erros_n_simpson[i-2], vetor_erros_n_simpson[i-1]
            )

        dados_gama.append(
            (n, integral_gama, erro_exato_gama,
             estimativa_erro_gama, convergencia_gama)
        )

        dados_simpson.append(
            (n, integral_simpsons, erro_exato_simpson,
             estimativa_erro_simpson, convergencia_simpson)
        )

    # ---------------- Tabela Gama Constante ----------------
    print(r"\begin{table}[ht]")
    print(r"\centering")
    print(r"\begin{tabular}{ccccc}")
    print(r"\hline")
    print(r"$n$ & Aproximação da Integral & Erro Exato & Estimativa de Erro & Ordem de Convergência \\")
    print(r"\hline")
    for n, I, erro, est, ordem in dados_gama:
        print(f"{n} & {I:.10e} & {erro:.10e} & {est:.10e} & {ordem} \\\\")
    print(r"\hline")
    print(r"\end{tabular}")
    print(r"\caption{Resultados obtidos pelo Método Gama Constante}")
    print(r"\label{tab:gama_constante}")
    print(r"\end{table}")

    print("\n")

    # ---------------- Tabela Simpson ----------------
    print(r"\begin{table}[ht]")
    print(r"\centering")
    print(r"\begin{tabular}{ccccc}")
    print(r"\hline")
    print(r"$n$ & Aproximação da Integral & Erro Exato & Estimativa de Erro & Ordem de Convergência \\")
    print(r"\hline")
    for n, I, erro, est, ordem in dados_simpson:
        print(f"{n} & {I:.10e} & {erro:.10e} & {est:.10e} & {ordem} \\\\")
    print(r"\hline")
    print(r"\end{tabular}")
    print(r"\caption{Resultados obtidos pelo método de $n$-Simpsons}")
    print(r"\label{tab:simpson}")
    print(r"\end{table}")

main()
