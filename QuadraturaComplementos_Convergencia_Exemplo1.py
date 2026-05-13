import math

def Formula_Quadratura(xi,xii):
    '''
       Essa funcao realiza o calculo de cada parcela da formula da quadratura
       apresentada no relatorio
    '''
    q=math.cos(xi)-math.cos(xii)
    return q/(xi+xii)

def integral(n):
    '''
           Essa funcao realiza o calculo da formula da quadratura
           apresentada no relatorio
    '''
    x0=1
    delta=(math.pi-1)/n
    integral=0
    for i in range(1,n+1):
        xi=x0+(i-1)*delta
        xii=x0+i*delta
        integral+=Formula_Quadratura(xi,xii)
    return 2*integral

def erro(n):
    '''
               Essa funcao realiza o calculo da estimativa do erro apresentada
               no relatorio
    '''

    delta=(math.pi-1)/n
    Mf=2.081575981#Maximo da Derivada do Modulo de f
    Mg=1#Maximo da Derivada do Modulo de g
    Lambda_g=1/1#1/inf|g|

    return (Mg**Lambda_g*delta**2+delta)*(math.pi-1)*Mf

def main():
    '''
                   Essa funcao plota a tabela mostrada no relatorio
    '''
    area1=integral(1)
    erro_exato1=abs(area1-0.9058539816152)
    erro_aproximado1=erro(1)
    print('--------------------------')
    print('Valor aproximado da Integral (n=1): ', area1)
    print()
    print('Estimativa do Erro: ', erro_aproximado1)
    print('Erro exato: ', erro_exato1)
    print()

    erros_exatos=[erro_exato1]
    for k in range(1,11):
        area=integral(2**k)
        erro_aproximado=erro(2**k)
        erro_exato=abs(area-0.9058539816152)
        erros_exatos.append(erro_exato)
        print('--------------------------')
        print()
        print(f'Valor aproximado da Integral (n={2**k}): ', area)
        print('Estimativa do Erro: ', erro_aproximado)
        print('Erro exato: ', erro_exato)
        print('Ordem de convergencia: ', math.log(erros_exatos[k-1]/erros_exatos[k],2))
        print()


main()
