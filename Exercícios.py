def resumo_FP (notas_dict):                 # dict 4
    res = tuple()
    reprovados = 0
    aprovados = 0
    media_aprovados = 0
    for i in notas_dict:
        if i < 10:
            reprovados += len(notas_dict[i])
        else:
            aprovados += len(notas_dict[i])
            media_aprovados += i * len(notas_dict[i])
    res = (media_aprovados / aprovados, reprovados)
    return res


def metabolismo (dict):                     # dict 5
    res = {}
    for i in dict:
        genero = dict[i][0]
        idade = dict[i][1]
        altura = dict[i][2]
        peso = dict[i][3]
        if genero == 'M':
            ind_metab_nasal = 66 + 6.3 * peso + 12.9 * altura + 6.8 * idade
        else:
            ind_metab_nasal = 655 + 4.3 * peso + 4.7 * altura + 4.7 * idade
        res[i] = ind_metab_nasal
    return res


def conta_palavras (string):                # dict 6
    res = {}
    lista = string.split()
    print(string)
    for palavra in lista:
        cont = lista.count(palavra)
        res[palavra] = cont
    return res


def depois_rel(r1, r2):                     # TADs 3a
    if horas(r2) > horas(r1):
        return True
    elif horas(r2) == horas(r1) and minutos(r2) > minutos(r1):
        return True
    elif horas(r2) == horas(r1) and minutos(r2) == minutos(r1) and segundos(r2) > segundos(r1):
        return True
    else:
        return False
    

def dif_segs(r1, r2):                       # TADs 3b
    if not depois_rel(r1, r2):
        raise ValueError('primeiro arg posterior ao segundo')
    total_segs1 = horas(r1) * 60 * 60 + minutos(r1) * 60 + segundos(r1)
    total_segs2 = horas(r2) * 60 * 60 + minutos(r2) * 60 + segundos(r2)
    return total_segs2 - total_segs1


def cria_rel(h, m, s):                            # TADs 3c
    return [h, m, s]

def horas(l):
    return l[0]

def minutos(l):
    return l[1]

def segundos(l):
    return l[2]

def eh_relogio(l):
    if type(l) != list or len(l) != 3:
        return False
    if type(l[0]) != int or type(l[1]) != int or type(l[2]) != int:
        return False
    if l[0] < 0 or l[0] > 23 or l[1] < 0 or l[1] > 59 or l[2] < 0 or l[2] > 59:
        return False
    return True

def eh_meia_noite(l):
    return l[0] == 0 and l[1] == 0 and l[2] == 0

def eh_meio_dia(l):
    return l[0] == 12 and l[1] == 0 and l[2] == 0

def mesmas_horas(l1, l2):
    return l1[0] == l2[0] and l1[1] == l2[1] and l1[2] == l2[2]


def escreve_relogio(rel):                   # TADs 3e
    if horas(rel) < 10:
        hh = f'0{horas(rel)}'
    else:
        hh = str(horas(rel))
    if minutos(rel) < 10:
        mm = f'0{minutos(rel)}'
    else:
        mm = str(minutos(rel))
    if segundos(rel) < 10:
        ss = f'0{segundos(rel)}'
    else:
        ss = str(segundos(rel))
    return f'{hh}:{mm}:{ss}'


def soma_fn(n, fn):                         # Funcionais 3a
    soma = 0
    for i in range(1, n + 1):
        soma += fn(i)
    return soma


def filtra(lst, tst):                       # Funcionais 4a
    if lst == []:
        return []
    else:
        if tst(lst[0]):
            return [lst[0]] + filtra(lst[1:], tst)
        else:
            return filtra (lst[1:], tst)


def transforma(lst, tst):                   # Funcionais 4b
    if lst == []:
        return []
    else:
        return [tst(lst[0])] + transforma(lst[1:], tst)


def acumula(lst, fn):                       # Funcionais 4c
    if lst == []:
        return 0
    else:
        return fn(0, lst[0]) + acumula(lst[1:], fn)


def soma_quadrados_impares(l):              # Funcionais 5
    return sum(map(lambda x : x*x, filter(lambda x: x % 2 == 1, l)))

def eh_primo(n):                            # Funcionais 6
    for i in range(2, n):
        if n % i == 0:
            return False
    return n != 1

def nao_primos(n):
    return list(filter(lambda x: not eh_primo(x), range(1, n + 1)))


def misterio(num, p):                       # Funcionais 7b
    if num == 0:
        return 0
    elif p(num % 10):
        return (num % 10) + 10 * misterio(num // 10, p)
    else:
        return misterio(num // 10, p)
def filtra_pares(n):
    return misterio(n, lambda x: x % 2 == 0)


def lista_digitos(n):                       # Funcionais 8
    return list(map(int, str(n)))


def produto_digitos(n, pred):               # Funcionais 9
    from functools import reduce
    return reduce(lambda x, y: x * y, filter(pred, lista_digitos(n)), 1)


def apenas_digitos_impares(n):              # Funcionais 10
    return int(''.join(map(str, filter(lambda x: x % 2 == 1, lista_digitos(n)))))


def apenas_digitos_impares(n):              # Recursão 1
    if n == 0:
        return 0
    else:
        if n % 2 == 1:
            return n % 10 + 10 * apenas_digitos_impares(n // 10)
        else:
            return apenas_digitos_impares(n // 10)
        
def junta_ordenadas(l1, l2):                # Recursão 2
    if len(l1) == 0 or len(l2) == 0:
        return l1 + l2
    else:
        if l1[0] > l2[0]:
            return [l2[0]] + junta_ordenadas(l1, l2[1:])
        else:
            return [l1[0]] + junta_ordenadas(l1[1:], l2)

def sublistas(l):                           # Recursão 3
    if len(l) == 0:
        return 0
    else:
        if type(l[0]) == list:
            return 1 + sublistas(l[0] + l[1:])
        else:
            return sublistas(l[1:])

def soma_n_vezes(a, b, n):                  # Recursão 4
    if n == 0:
        return b
    else:
        return a + soma_n_vezes(a, b, n - 1)
    
def inverte(l):                             # Recursão 6
    if len(l) == 0:
        return []
    else:
        return inverte(l[1:]) + [l[0]]
    
def pertence(l, n):                         # Recursão 7
    if len(l) == 0:
        return False
    else:
        if l[0] == n:
            return True
        else:
            return pertence(l[1:], n)

def subtrai(l1, l2):                        # Recursão 8
    if len(l1) == 0:
        return []
    else:
        if l1[0] in l2:
            return subtrai(l1[1:], l2)
        else:
            return [l1[0]] + subtrai(l1[1:], l2)
        
def parte(l, n):                            # Recursão 9
    def aux(l, menores, maiores):
        if len(l) == 0:
            return [menores, maiores]
        else:
            if l[0] < n:
                return aux(l[1:], menores + [l[0]], maiores)
            else:
                return aux(l[1:], menores, maiores + [l[0]])
    return aux(l, [], [])

def maior(l):                               # Recursão 10
    def aux(l, maior):
        if len(l) == 0:
            return maior
        else:
            if l[0] > maior:
                return aux(l[1:], l[0])
            else:
                return aux(l[1:], maior)
    return aux(l, 0)

def lposicoes(l, n):                        # Recursão 11
    def aux(l, n, posicoes, cont):
        if len(l) == 0:
            return posicoes
        else:
            if l[0] == n:
                return aux(l[1:], n, posicoes + [cont], cont + 1)
            else:
                return aux(l[1:], n, posicoes, cont + 1)
    return aux(l, n, [], 0)

def numero_digitos(n):                      # Outra recursão 3a
    if type(n) != int or n < 0:
        raise ValueError('erro')
    if n == 0:
        return 0
    else:
        return 1 + numero_digitos(n // 10)
    
def numero_digitos(n):                      # Outra recursão 3b
    def aux(n, cont):
        if n == 0:
            return cont
        else:
            return aux(n // 10, cont + 1)

    return aux(n, 0)

def numero_digitos(n):                      # Outra recursão 3c
    cont = 0
    while n != 0:
        n = n // 10
        cont += 1
    return cont
