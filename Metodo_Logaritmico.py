import math
def f(x):
    return math.e**(x**2)



def Formula_metodoLogaritmico_1interavalo(xi,xii):
    '''
       Essa funcao calcula, para o intervalo [xi,xii], a formula do metodo logaritmico apresentada no relatorio
    '''

    numerador=math.log(f(xii),math.e)-math.log(f(xi),math.e)
    denominador=f(xii)-f(xi)

    return f(xi)*f(xii)*numerador/denominador

def metodo_logaritmico(a,b,n):
    '''
           Essa funcao calcula a formula do metodo logaritmico apresentada no relatorio
    '''

    delta=(b-a)/n
    x0=a
    integral=0
    for k in range(1,n+1):
        xi=x0+(k-1)*delta
        xii=x0+k*delta
        integral+=Formula_metodoLogaritmico_1interavalo(xi,xii)
    return delta*integral

def Estimativa_Erro_MetodoLogaritmico(a,b,n):
    '''
                       Essa funcao calcula a estimativa de erro do metodo logaritmico apresentada no relatorio
    '''
    Mf=218.3926001
    Mg=0.89252064
    Lambda_g=13.6495327

    delta=(b-a)/n
    return ((delta**2)*Mg*Lambda_g+delta)*(b-a)*Mf


def nTrapezios(a,b,n):
    '''
               Essa funcao calcula a formula do metodo dos n-Trapezios
    '''
    delta = (b - a) / n
    x0 = a
    integral = f(a)/2+f(b)/2
    for k in range(1, n):
        xi = x0 + k * delta
        integral += f(xi)
    return delta * integral

def Estimativa_Erro_nTrapezios(a,b,n):
    '''
                   Essa funcao calcula a estimativa de erro do metodo dos n-Trapezios
    '''

    M2=982.76670059
    delta=(b-a)/n

    return M2*(delta**2)*(b-a)/12

def main():
    '''
                   Essa funcao plota a tabela mostrada no relatorio
    '''

    valor_exato=14.98997601
    a,b=1,2
    integral_metodo_logaritmico=metodo_logaritmico(a,b,1)
    integral_metodo_trapezio=nTrapezios(a,b,1)

    erro_exato1=abs(integral_metodo_logaritmico-valor_exato)
    erro_exato2=abs(integral_metodo_trapezio-valor_exato)

    erro_aproximado1=Estimativa_Erro_MetodoLogaritmico(a,b,1)
    erro_aproximado2=Estimativa_Erro_nTrapezios(a,b,1)
    print('--------------------------')
    print('METODO LOGARITMICO')
    print()
    print('Valor aproximado da Integral (n=1): ', integral_metodo_logaritmico)
    print()
    print('Estimativa do Erro: ', erro_aproximado1)
    print('Erro exato: ', erro_exato1)
    print()
    print('METODO n-TRAPEZIOS')
    print()
    print('Valor aproximado da Integral (n=1): ', integral_metodo_trapezio)
    print()
    print('Estimativa do Erro: ', erro_aproximado2)
    print('Erro exato: ', erro_exato2)
    print()

    erros_exatos1=[erro_exato1]
    erros_exatos2=[erro_exato2]
    for k in range(1,11):
        n=2**k
        integral_metodo_logaritmico = metodo_logaritmico(a, b, n)
        integral_metodo_trapezio = nTrapezios(a, b, n)

        erro_exato1 = abs(integral_metodo_logaritmico - valor_exato)
        erro_exato2 = abs(integral_metodo_trapezio - valor_exato)

        erro_aproximado1 = Estimativa_Erro_MetodoLogaritmico(a, b, n)
        erro_aproximado2 = Estimativa_Erro_nTrapezios(a, b, n)

        erros_exatos1.append(erro_exato1)
        erros_exatos2.append(erro_exato2)
        print('--------------------------')
        print('METODO LOGARITMICO')
        print()
        print(f'Valor aproximado da Integral (n={n}): ', integral_metodo_logaritmico)
        print()
        print('Estimativa do Erro: ', erro_aproximado1)
        print('Erro exato: ', erro_exato1)
        print('Ordem de Convergencia: ', math.log(erros_exatos1[k-1]/erros_exatos1[k],2))
        print()
        print('METODO n-TRAPEZIOS')
        print()
        print(f'Valor aproximado da Integral (n={n}): ', integral_metodo_trapezio)
        print()
        print('Estimativa do Erro: ', erro_aproximado2)
        print('Erro exato: ', erro_exato2)
        print('Ordem de Convergencia: ', math.log(erros_exatos2[k - 1] / erros_exatos2[k], 2))
        print()


main()
