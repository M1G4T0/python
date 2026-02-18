def conta_palavras(string):
    res = {}
    lista = string.split()
    for palavra in lista:
        cont = lista.count(palavra)
        res[palavra] = cont
    return res
