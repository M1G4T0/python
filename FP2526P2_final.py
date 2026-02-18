# Miguel Lobato
# ist1118345@tecnico.ulisboa.pt
# FP2526P2 - Scrabble

LETRAS = 'A','B','C','Ç','D','E','F','G','H','I','J','L','M','N','O','P','Q','R','S','T','U','V','X','Z'

TAMANHO_TAB = 15

PONTOS = {
'A': 1, 'B': 3, 'C': 2, 'Ç': 3, 'D': 2, 'E': 1,
'F': 4, 'G': 4, 'H': 4, 'I': 1, 'J': 5, 'L': 2,
'M': 1, 'N': 3, 'O': 1, 'P': 2, 'Q': 6, 'R': 1,
'S': 1, 'T': 1, 'U': 1, 'V': 4, 'X': 8, 'Z': 8 }

SACO = {
'A': 14, 'B': 3, 'C': 4, 'Ç': 2, 'D': 5, 'E': 11,
'F': 2, 'G': 2, 'H': 2, 'I': 10, 'J': 2, 'L': 5,
'M': 6, 'N': 4, 'O': 10, 'P': 4, 'Q': 1, 'R': 6,
'S': 8, 'T': 5, 'U': 7, 'V': 2, 'X': 1, 'Z': 1 }

# TAD casa

# Construtor:
def cria_casa(lin, col):
    """
    Recebe dois inteiros dentro dos limites do tabuleiro e devolve um TAD casa associado a esses
    valores para a linha e coluna, respetivamente.
    """
    if type(lin) != int or type(col) != int:
        raise ValueError('cria_casa: argumentos inválidos')
    if lin < 1 or lin > TAMANHO_TAB or col < 1 or col > TAMANHO_TAB:
        raise ValueError('cria_casa: argumentos inválidos')
    return (lin, col)

# Seletores:
def obtem_lin(c):
    """
    Recebe um TAD casa e devolve o valor correspondente da sua linha.
    """
    return c[0]

def obtem_col(c):
    """
    Recebe um TAD casa e devolve o valor correspondente da sua linha.
    """
    return c[1]

# Reconhecedor:
def eh_casa(arg):
    """
    Verifica se um argumento é um TAD casa e devolve True se for e False caso contrário.
    """
    if type(arg) != tuple or len(arg) != 2:
        return False
    if type(arg[0]) != int or type(arg[1]) != int:
        return False
    if arg[0] < 1 or arg[0] > TAMANHO_TAB or arg[1] < 1 or arg[1] > TAMANHO_TAB:
        return False
    
    return True

# Teste:
def casas_iguais(c1, c2):
    """
    Recebe dois argumentos e verifica se são dois TAD casa iguais devolvendo True se forem e False caso contrário.
    """
    if not eh_casa(c1) or not eh_casa(c2):
        return False
    if c1[0] != c2[0] or c1[1] != c2[1]:
        return False
    
    return True

# Transformadores:
def casa_para_str(c):
    """
    Recebe um TAD casa e devolve a sua representação externa em string.
    """
    return f'({c[0]},{c[1]})'

def str_para_casa(c):
    c = c[1 : len(c) - 1]       # Retira os parênteses
    c = c.split(',')

    return cria_casa(int(c[0]), int(c[1]))

# Função de alto nível:
def incrementa_casa(c, direcao, dist):
    """
    Incrementa uma distância (dist) a um TAD casa (c) na direção (direcao) e devolve o TAD casa correspondente.
    """
    if direcao == 'V':
        if obtem_lin(c) + dist > TAMANHO_TAB:
            return c
        return cria_casa(obtem_lin(c) + dist, obtem_col(c))
    elif direcao == 'H':
        if obtem_col(c) + dist > TAMANHO_TAB:
            return c
        return cria_casa(obtem_lin(c), obtem_col(c) + dist)
    return c


# TAD jogador

# Construtores:
def cria_humano(nome):
    """
    Cria um TAD jogador humano.
    """
    if type(nome) != str or len(nome) == 0:
        raise ValueError('cria_humano: argumento inválido')
    return {'id': nome, 'pontos': 0, 'conj_let': {}, 'tipo': 'humano'}

def cria_agente(nivel):
    """
    Cria um TAD jogador agente.
    """
    if type(nivel) != str:
        raise ValueError('cria_agente: argumento inválido')
    if nivel != 'FACIL' and nivel != 'MEDIO' and nivel != 'DIFICIL':
        raise ValueError('cria_agente: argumento inválido')
    return {'id': nivel, 'pontos': 0, 'conj_let': {}, 'tipo': 'agente'}

# Seletores:
def jogador_identidade(jog):
    """
    Devolve a indentidade do TAD jogador.
    """
    return jog['id']

def jogador_pontos(jog):
    """
    Devolve o número de pontos do TAD jogador.
    """
    return jog['pontos']

def jogador_letras(jog):
    """
    Devolve o conjunto de letras do TAD jogador.
    """
    conj_let_ord = "".join(ordena_dict(jog['conj_let']))
    return conj_let_ord

# Modificadores:
def recebe_letra(jog, let):
    """
    Modifica destrutivamente o conjunto de letras do TAD jogador ao adicionar-lhe a letra (let).
    """
    if let in jog['conj_let']:
        jog['conj_let'][let] += 1
    else:
        jog['conj_let'][let] = 1
    return jog

def usa_letra(jog, let):
    """
    Modifica destrutivamente o conjunto de letras do TAD jogador ao remover-lhe a letra (let).
    """
    jog['conj_let'][let] += -1
    if jog['conj_let'][let] == 0:
        del jog['conj_let'][let]
    return jog

def soma_pontos(jog, pontos):
    """
    Modifica destrutivamente o número de pontos do TAD jogador ao adicionar-lhe uma quantidade de pontos (pontos).
    """
    jog['pontos'] += pontos
    return jog

# Reconhecedores:
def eh_jogador(arg):
    """
    Verifica se o argumento (arg) é um TAD jogador e devolve True se for e False caso contrário.
    """
    if type(arg) != dict or len(arg) != 4:
        return False
    if 'id' not in arg or 'pontos' not in arg or 'conj_let' not in arg or 'tipo' not in arg:
        return False
    if type(arg['id']) != str or len(arg['id']) == 0:
        return False
    if type(arg['pontos']) != int or arg['pontos'] < 0:
        return False
    if type(arg['conj_let']) != dict:
        return False
    if arg['tipo'] != 'humano' and arg['tipo'] != 'agente':
        return False
    if len(arg['conj_let']) != 0:
        cont = 0
        for i in arg['conj_let']:
            if i not in LETRAS or type(arg['conj_let'][i]) != int or arg['conj_let'][i] < 0:
                return False
            cont += arg['conj_let'][i]
        if cont > 7:
            return False
        
    return True

def eh_humano(arg):
    """
    Verifica se o argumento (arg) é um TAD jogador humano e devolve True se for e False caso contrário.
    """
    return eh_jogador(arg) and arg['tipo'] == 'humano'

def eh_agente(arg):
    """
    Verifica se o argumento (arg) é um TAD jogador agente e devolve True se for e False caso contrário.
    """
    if not eh_jogador(arg):
        return False
    if arg['id'] != 'FACIL' and arg['id'] != 'MEDIO' and arg['id'] != 'DIFICIL':
        return False
    return arg['tipo'] == 'agente'

# Teste:
def jogadores_iguais(arg1, arg2):
    """
    Recebe dois argumentos e verifica se são TAD jogador iguais devolvendo True se forem e False caso contrário.
    """
    if not eh_jogador(arg1) or not eh_jogador(arg2):
        return False
    if arg1['id'] != arg2['id'] or arg1['pontos'] != arg2['pontos']:
        return False
    if arg1['conj_let'] != arg2['conj_let'] or arg1['tipo'] != arg2['tipo']:
        return False
    
    return True


def ordena_dict (conj_let):      # Função auxiliar
    """
    A função recebe um dicionário com letras únicas como chaves e o número de ocorrências da mesma letra como valor
    e devolve uma lista com todas as ocorrências de cada letra ordenadas de acordo com o abecedário português.
    """

    conj_comp = []          # Conjunto completo: com todas as ocorrências de cada letra

    for i in conj_let:               
        conj_comp.extend(i * conj_let[i])

    conj_ord = sorted(conj_comp, key=lambda x: LETRAS.index(x))     # Ordenar de acordo com o índice das letras no abecedário português

    return conj_ord

# Transformador:
def jogador_para_str(jog):
    """
    Recebe um TAD jogador e devolve a sua representação externa em string.
    """
    list_let = []
    for let in jogador_letras(jog):
        list_let += let
    str_let_ord = ' '.join(list_let)        # String com espaços entre as letras

    if eh_agente(jog):
        str_jog = f"BOT({(jog['id'])}) ({jog['pontos']:3}): {str_let_ord}".rstrip()
    else:
        str_jog = f"{jog['id']} ({jog['pontos']:3}): {str_let_ord}".rstrip()
        
    return str_jog

# Função de alto nível:
def distribui_letras(jog, saco, n):
    """
    Modifica destrutivamente o conjunto de letras do TAD jogador (jog) 
    """
    for _ in range(n):
        if len(saco) == 0:
            break
        recebe_letra(jog, saco.pop())
    return jog


# TAD vocabulário

# Construtor:
def cria_vocabulario(conj_palav):
    """
    Recebe um tuplo com palavras e devolve um TAD vocabulário com todas as palavras únicas, com, entre
    duas e quinze letras, organizadas por tamanho e primeira letra e ordenadas por pontuação e ordem alfabética
    para a mesma pontuação. 
    """
    if type(conj_palav) != tuple or len(conj_palav) == 0:
        raise ValueError('cria_vocabulario: argumento inválido')
    vocab = {}
    conj_palav_ord = []
    palav_dup_test = set()          # Utilizar um set para verificar palavras duplicadas
    abecedario = set(LETRAS)
    
    for palav in conj_palav:
        pontos = 0
        if type(palav) != str or len(palav) < 2 or len(palav) > 15 or palav in palav_dup_test:
            raise ValueError('cria_vocabulario: argumento inválido')
        for let in palav:
            if let not in abecedario:               # Verifica automaticamente se são maiúsculas (mais eficiente em set)
                raise ValueError('cria_vocabulario: argumento inválido')
            pontos += PONTOS[let]
        conj_palav_ord.append((palav, pontos))
        palav_dup_test.add(palav)
    conj_palav_ord.sort(key = lambda x: tuple(LETRAS.index(let) for let in x[0]))      # Utilizar o sort para ordenar as palavras de acordo com o índice das letras do alfabeto
    conj_palav_ord.sort(key = lambda x: -x[1])

    for par in conj_palav_ord:
        palav = par[0]
        if len(palav) not in vocab:
            vocab[len(palav)] = {palav[0] : [(par)]}
        else:
            if palav[0] not in vocab[len(palav)]:
                vocab[len(palav)][palav[0]] = [(par)]
            else:
                vocab[len(palav)][palav[0]] += [(par)]

    vocab['todas_palav'] = palav_dup_test           # Manter o set com todas as palavras dentro do vocabulario para poder verificar noutras funções se uma palavra pertence ao vocabulário
    return vocab

# Seletores:
def obtem_pontos(vocab, palav):
    """
    Devolve o número de pontos da palavra se esta estiver no TAD vocabulário (vocab) ou 0 caso contrário.
    """
    for par in vocab[len(palav)][palav[0]]:
        if par[0] == palav:
            return par[1]
    return 0

def obtem_palavras(vocab, tamanho, prim_let):
    """
    Devolve todas as palavras contidas no TAD vocabulário (vocab) com tamanho (tamanho) e primeira letra (prim_let).
    """
    if tamanho not in vocab:
        return tuple()
    if prim_let not in vocab[tamanho]:
        return tuple()      
    return tuple(vocab[tamanho][prim_let])           # Palavras já ordenadas no vocab

# Teste:
def testa_palavra_padrao(vocab, palav, padrao, conj_let):
    """
    Verifica se é possível colocar a palavra (palav) no padrão do tabuleiro (padrao) com as letras (conj_let)
    e se a palavra pertence ao TAD vocabulário (vocab), devolvendo True se estas condições se verificarem e
    False caso contrário.
    """
    if len(palav) != len(padrao):
        return False
    if all(carater != '.' for carater in padrao):
        return False
    if len(palav) not in vocab or palav[0] not in vocab[len(palav)]:
        return False
    if palav not in vocab['todas_palav']:           # Verificar se a palavra pertence ao vocab
        return False

    conj_let_test = list(conj_let)          # Cria uma cópia

    for carater in range(len(padrao)):
        if padrao[carater] != '.':
            if padrao[carater] != palav[carater]:
                return False
        else:
            if palav[carater] in conj_let_test:
                let_index = conj_let_test.index(palav[carater])
                del(conj_let_test[let_index])       # Remover a letra do conjunto de teste sem modificar o conjunto original
            else:
                return False
            
    return True

# Transformadores:
def ficheiro_para_vocabulario(nome_fich):
    """
    Recebe um ficheiro com palavras e devolve um TAD vocabulário com todas as palavras únicas, com, entre
    duas e quinze letras, e em letra maiúscula, organizadas por tamanho e primeira letra e ordenadas por
    pontuação e ordem alfabética para a mesma pontuação.
    """
    conj_palav = set()       # Não aceita palavras duplicadas
    with open(nome_fich, 'r', encoding= 'utf-8') as fich:
        for lin in fich:
            palav = lin.strip().upper()
            if type(palav) != str or len(palav) < 2 or len(palav) > 15:
                continue
            if any(let not in LETRAS for let in palav):
                continue
            conj_palav.add(palav)
    return cria_vocabulario(tuple(conj_palav))         

def vocabulario_para_str(vocab):
    """
    Recebe um TAD vocabulário (vocab) e devolve a sua representação externa em string.
    """
    lista_palav = []
    if len(vocab) == 0:
        return ''
    for tamanho in range(2, TAMANHO_TAB + 1):
        if tamanho not in vocab:
            continue
        for let in LETRAS:
            if let in vocab[tamanho]:
                for par in vocab[tamanho][let]:
                    lista_palav.append(par[0])
    
    vocab_str = '\n'.join(lista_palav)
    return vocab_str.strip()                # Remove o \n no final

# Função de alto nível:
def procura_palavra_padrao(vocab, padrao, conj_let, min_pontos):
    """
    Devolve um tuplo com a melhor palavra pertencente ao TAD vocabulário (vocab) que é possível
    ser inserida no padrão do tabuleiro (padrao) com as letras (conj_let) e com pontuação maior
    a (min_pontos), e a sua pontuação. Se não encontrar uma palavra que cumpra estas condições
    devolve ('', 0).
    """
    if padrao[0] != '.':
        palav_possiveis = obtem_palavras(vocab, len(padrao), padrao[0])
        for par in palav_possiveis:
            if par[1] >= min_pontos and testa_palavra_padrao(vocab, par[0], padrao, conj_let):
                return par          # Como o tuplo do obtem_palavras está ordenado, a melhor palavra é a primeira que cumpre os requisitos
        return ('', 0)        
    
    else:
        melhores_palav = []
        for let in list(set(conj_let)):         # Transformar em set para remover duplicados e de volta para lista (não repete padrões)
            palav_possiveis = obtem_palavras(vocab, len(padrao), let)
            for par in palav_possiveis:
                if par[1] >= min_pontos and testa_palavra_padrao(vocab, par[0], padrao, conj_let):
                    melhores_palav.append(par)          # Encontra a melhor palavra que cumpre os requisitos para cada letra do conjunto
                    break
        if len(melhores_palav) == 0:
            return ('', 0) 
        
        melhores_palav.sort(key = lambda x: tuple(LETRAS.index(let) for let in x[0]))
        melhores_palav.sort(key = lambda x: -x[1])
        return melhores_palav[0]            # Devolve a melhor palavra do conjunto das melhores
    

# TAD tabuleiro

# Construtor:
def cria_tabuleiro():
    """
    A função recebe um argumento vazio e devolve um TAD tabuleiro vazio de dimensões 
    15 x 15 (ajustável), com as casas vazias a serem representadas por ".".
    """

    tab = []
    espaco = ['.']

    for _ in range(TAMANHO_TAB):
        linha = []
        for _ in range(TAMANHO_TAB):
            linha.extend(espaco[:])
        tab.append(linha[:])

    return tab

# Seletor:
def obtem_letra(tab, casa):
    """
    Devolve o valor da casa (casa) no TAD tabuleiro (tab).
    """
    return tab[obtem_lin(casa) - 1][obtem_col(casa) - 1]

# Modificador:
def insere_letra(tab, casa, let):
    """
    Modifica destrutivamente o TAD tabuleiro (tab) colocando a letra (let) na casa (casa) e devolve o tabuleiro modificado.
    """
    tab[obtem_lin(casa) - 1][obtem_col(casa) - 1] = let
    return tab

# Reconhecedores:
def eh_tabuleiro(arg):
    """
    Verifica se o argumento (arg) é um TAD tabuleiro, devolvendo True se for e False caso contrário.
    """
    if type(arg) != list or len(arg) != TAMANHO_TAB:
        return False
    for lin in arg:
        if len(lin) != TAMANHO_TAB:
            return False
        for casa in lin:
            if casa != '.' and casa not in LETRAS:
                return False
    return True

def eh_tabuleiro_vazio(arg):
    """
    Verifica se o argumento (arg) é um TAD tabuleiro vazio (sem letras), devolvendo True se for e False caso contrário.
    """
    if type(arg) != list or len(arg) != TAMANHO_TAB:
        return False
    for lin in arg:
        if len(lin) != TAMANHO_TAB:
            return False
        if any(casa != '.' for casa in lin):
                return False
    return True

# Teste:
def tabuleiros_iguais(arg1, arg2):
    """
    Recebe dois argumentos e verifica se são TAD tabuleiro iguais devolvendo True se forem e False caso contrário.
    """
    if not eh_tabuleiro(arg1) or not eh_tabuleiro(arg2):
        return False
    for lin in range(TAMANHO_TAB):
        for casa in range(TAMANHO_TAB):
            if arg1[lin][casa] != arg2[lin][casa]:
                return False
    return True

# Transformador:
def tabuleiro_para_str(tab):
    """
    Recebe um TAD tabuleiro (tab) e devolve a sua representação externa em string.
    """

    tab_str = ''

    tab_str += '                       1 1 1 1 1 1\n'           # Cabeçalho
    tab_str += '     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5\n'           # Teria de mudar isto para alterar o tamanho do tabuleiro
    tab_str += '   +-------------------------------+\n'            
    
    for lin in range(1, TAMANHO_TAB + 1):           # Tabuleiro
        for col in range(1, TAMANHO_TAB + 1):
            if col == 1:
                tab_str += f"{lin :2} | "      # Colocar os números das linhas
            tab_str += tab[lin - 1][col - 1]        # Adicionar os elementos de cada linha e coluna
            tab_str += " "
            if col == TAMANHO_TAB:
                tab_str += "|\n"
    
    tab_str += '   +-------------------------------+'

    return tab_str

# Funções de alto nível:
def obtem_padrao(tab, casa_i, casa_f):
    """
    Devolve a sequência de valores do TAD tabuleiro (tab) da casa (casa_i) até à casa (casa_f).
    """
    padrao = ''
    
    if obtem_lin(casa_i) == obtem_lin(casa_f):          # Direção horizontal
        for col in range(obtem_col(casa_i), obtem_col(casa_f) + 1):
            casa = cria_casa(obtem_lin(casa_i), col)
            padrao += obtem_letra(tab, casa)
    
    else:           # Direção vertical
        for lin in range(obtem_lin(casa_i), obtem_lin(casa_f) + 1):
            casa = cria_casa(lin, obtem_col(casa_i))
            padrao += obtem_letra(tab, casa)

    return padrao

def insere_palavra(tab, casa, direcao, palav):
    """
    Modifica destrutivamente o TAD tabuleiro (tab), colocando a palavra (palav) na casa inicial (casa) na direção (direcao).
    """
    let = 0
    
    if direcao == 'H':
        for col in range(obtem_col(casa), obtem_col(casa) + len(palav)):
            c = cria_casa(obtem_lin(casa), col)
            insere_letra(tab, c, palav[let])
            let += 1
    
    else:
        for lin in range(obtem_lin(casa), obtem_lin(casa) + len(palav)):
            c = cria_casa(lin, obtem_col(casa))
            insere_letra(tab, c, palav[let])
            let += 1
    
    return tab

def obtem_subpadroes(tab, casa_i, casa_f, num_p):
    """
    Devolve um tuplo com todos os subpadrões viáveis do TAD tabuleiro (tab) entre a casa (casa_i) e
    a casa (casa_f) com, no máximo, (num_p) espaços livres, e a casa inicial desses subpadrões.
    Para um subpadrão ser viável tem de ter pelo menos um espaço livre, pelo menos uma letra e não pode
    ter uma letra na casa anterior ou na casa a seguir.
    """
    lista_subpadroes = []
    lista_casas_i = []
    
    if obtem_lin(casa_i) == obtem_lin(casa_f):
        direcao = 'H'
        max_padrao = obtem_col(casa_f) - obtem_col(casa_i) + 1
    else:
        direcao = 'V'
        max_padrao = obtem_lin(casa_f) - obtem_lin(casa_i) + 1
    
    for i in range(max_padrao):
            casa_i_padrao = incrementa_casa(casa_i, direcao, i)
            for j in range(max_padrao, i, -1):
                casa_f_padrao = incrementa_casa(casa_i, direcao, j - 1)
                padrao = obtem_padrao(tab, casa_i_padrao, casa_f_padrao)
                
                cont = 0
                if all(carac == '.' for carac in padrao) or all(carac != '.' for carac in padrao):
                    continue
                for carac in padrao:
                    if carac == '.':
                        cont += 1
                if cont > num_p:
                    continue

                if i != 0:
                    casa_antes = incrementa_casa(casa_i, direcao, i - 1)
                    if obtem_letra(tab, casa_antes) != '.':
                        continue
                if j != max_padrao:
                    casa_depois = incrementa_casa(casa_f_padrao, direcao, 1)
                    if obtem_letra(tab, casa_depois) != '.':
                        continue
                lista_subpadroes.append(padrao)
                lista_casas_i.append(casa_i_padrao)
    return tuple(lista_subpadroes), tuple(lista_casas_i)
    

def gera_todos_padroes(tab, num_p):
    """
    Devolve um tuplo com todos os subpadrões viáveis no tabuleiro atual (tab) com, no máximo,
    (num_p) espaços livres, a casa inicial de cada subpadrão e a sua direção no tabuleiro. 
    """
    lista_tds_padroes = []
    lista_casas_i = []
    lista_direcao_padroes = []

    for lin in range(1, TAMANHO_TAB + 1):
        casa_i = cria_casa(lin, 1)
        casa_f = incrementa_casa(casa_i, 'H', TAMANHO_TAB - 1)
        subpadroes, sub_casas_i = obtem_subpadroes(tab, casa_i, casa_f, num_p)
        lista_tds_padroes.extend(subpadroes)
        lista_casas_i.extend(sub_casas_i)
        lista_direcao_padroes.extend(('H') * len(subpadroes))

    for col in range(1, TAMANHO_TAB + 1):
        casa_i = cria_casa(1, col)
        casa_f = incrementa_casa(casa_i, 'V', TAMANHO_TAB - 1)
        subpadroes, sub_casas_i = obtem_subpadroes(tab, casa_i, casa_f, num_p)
        lista_tds_padroes.extend(subpadroes)
        lista_casas_i.extend(sub_casas_i)
        lista_direcao_padroes.extend(('V') * len(subpadroes))

    return tuple(lista_tds_padroes), tuple(lista_casas_i), tuple(lista_direcao_padroes)


def gera_numero_aleatorio (seed):     # Função auxiliar
    """
    Eecebe um inteiro positivo como estado inicial do gerador (seed) e devolve 
    uma modificação pseudoaleatória do estado através de operações xorshift.
    """

    if type(seed) != int or seed < 0:                                   
        raise ValueError('gera_numero_aleatorio: argumento inválido')

    seed ^= ( seed << 13 ) & 0xFFFFFFFF         # Operações xorshift
    seed ^= ( seed >> 17 ) & 0xFFFFFFFF
    seed ^= ( seed << 5 ) & 0xFFFFFFFF
  
    return seed


def baralha_saco(seed):
    """
    Devolve uma lista de letras baralhada pseudoaleatoriamente de acordo com o estado inicial (seed).
    """

    saco_baralhado = ordena_dict(SACO)
    
    for i in range(len(saco_baralhado) - 1, 0, -1):
        seed = gera_numero_aleatorio(seed)
        j = seed % (i + 1)
        saco_baralhado[i], saco_baralhado[j] = saco_baralhado[j], saco_baralhado[i]         # Permutar a letra do último índice com uma letra de índice aleatório

    return saco_baralhado

def let_usadas(palav, padrao):       # Função auxiliar
    """
    Devolve todas as letras utilizadas para inserir a palavra (palav) no padrão do tabuleiro (padrao).
    """
    let_usadas = ''
    for carater in range(len(padrao)):          # A função assume que é possível colocar a palavra no padrão com as letras do conjunto
        if padrao[carater] == '.':
            let_usadas += palav[carater]
    return let_usadas


def jogada_humano(tab, jog, vocab, saco):
    """
    Processa a jogada de um jogador humano de acordo com o input do jogador, pedindo um input novo se não for válido.
    O jogador pode passar, trocar ou jogar:
    Passar - não altera nenhum argumento e devolve False
    Trocar - remove as letras no input do conjunto de letras do jogador e distribui o mesmo número de letras, se possível,
    devolvendo True
    Jogar - modifica o tabuleiro inserindo a palavra no input na casa inicial e na direção também no input, retirando as letras
    utilizadas do conjunto de letras do jogador e distribuindo o mesmo número de letras, se possível, adicionando o número
    de pontos da palavra aos pontos do jogador e devolvendo True
    """
    
    jogada = input(f'Jogada {jogador_identidade(jog)}: ')
    
    if type(jogada) != str:
        return jogada_humano(tab, jog, vocab, saco)
    jogada = jogada.strip().split()
    if len(jogada) == 0:
        return jogada_humano(tab, jog, vocab, saco)
    
    if jogada[0] == 'P':
        if len(jogada) != 1:
            return jogada_humano(tab, jog, vocab, saco)
        return False
    
    elif jogada[0] == 'T':
        if len(jogada) == 1 or len(jogada) > 8 or len(saco) < 7:
            return jogada_humano(tab, jog, vocab, saco)

        let_troca = jogada[1:]
        letr_usadas = ''
        if any(let not in LETRAS for let in let_troca):
            return jogada_humano(tab, jog, vocab, saco)
        for let in let_troca:
            if let in jogador_letras(jog):
                usa_letra(jog, let)
                letr_usadas += let
            else:
                for letra in letr_usadas:
                    recebe_letra(jog, letra)          # Se o jogador não tiver uma das letras recebe todas as anteriores de volta
                return jogada_humano(tab, jog, vocab, saco)
        distribui_letras(jog, saco, len(let_troca))
        return True
    
    elif jogada[0] == 'J':
        if len(jogada) != 5 or not jogada[1].isdigit() or not jogada[2].isdigit():
            return jogada_humano(tab, jog, vocab, saco)
        if jogada[3] != 'H' and jogada[3] != 'V':
            return jogada_humano(tab, jog, vocab, saco)
        if int(jogada[1]) < 1 or int(jogada[1]) > 15 or int(jogada[2]) < 1 or int(jogada[2]) > 15:
            return jogada_humano(tab, jog, vocab, saco)
        
        lin = int(jogada[1])
        col = int(jogada[2])
        direcao = jogada[3]
        palav = jogada[4]
        casa_i = cria_casa(lin, col)
        casa_f = incrementa_casa(casa_i, direcao, len(palav) - 1)
        padrao = obtem_padrao(tab, casa_i, incrementa_casa(casa_i, direcao, len(palav) - 1))

        if eh_tabuleiro_vazio(tab):        # Indicador primeira jogada
            tab_test = cria_tabuleiro()
            insere_palavra(tab_test, casa_i, direcao, palav)
            if obtem_letra(tab_test, cria_casa(8, 8)) == '.':        # Verificar se a jogada ocupa a casa do meio num tabuleiro de teste
                return jogada_humano(tab, jog, vocab, saco)
            if not testa_palavra_padrao(vocab, palav, padrao, jogador_letras(jog)):
                return jogada_humano(tab, jog, vocab, saco)         # Verificar se a palavra pertence ao vocab e se o jogador tem as letras necessárias para formar a palavra
            insere_palavra(tab, casa_i, direcao, palav)
            for let in palav:
                usa_letra(jog, let)
            distribui_letras(jog, saco, len(palav))
            soma_pontos(jog, obtem_pontos(vocab, palav))
            return True
        
        else:
            if testa_palavra_padrao(vocab, palav, padrao, jogador_letras(jog)):
                if direcao == 'H':
                    if col != 1:
                        if obtem_letra(tab, incrementa_casa(casa_i, direcao, -1)) != '.':       # Verifica se não existe uma letra na casa anterior
                            return jogada_humano(tab, jog, vocab, saco)
                    if obtem_col(casa_f) != 15:
                        if obtem_letra(tab, incrementa_casa(casa_i, direcao, len(palav))) != '.':       # Verifica se não existe uma letra na casa a seguir
                            return jogada_humano(tab, jog, vocab, saco)
                else:
                    if lin != 1:
                        if obtem_letra(tab, incrementa_casa(casa_i, direcao, -1)) != '.':
                            return jogada_humano(tab, jog, vocab, saco)
                    if obtem_lin(casa_f) != 15:
                        if obtem_letra(tab, incrementa_casa(casa_i, direcao, len(palav))) != '.':
                            return jogada_humano(tab, jog, vocab, saco)
            else:
                return jogada_humano(tab, jog, vocab, saco)
            str_let_usadas = let_usadas(palav, padrao)
            insere_palavra(tab, casa_i, direcao, palav)
            for let in str_let_usadas:
                usa_letra(jog, let)
            distribui_letras(jog, saco, len(str_let_usadas))
            soma_pontos(jog, obtem_pontos(vocab, palav))
            return True
    else:
        return jogada_humano(tab, jog, vocab, saco)
    
def jogada_agente(tab, jog, vocab, saco):
    """
    Processa a jogada de um jogador agente, podendo jogar, trocar ou passar:
    Jogar: modifica o tabuleiro inserindo a melhor palavra dos N subpadrões válidos, sendo o N diference para
    cada dificuldade do agente, retirando as letras utilizadas do conjunto de letras do jogador e distribuindo 
    o mesmo número de letras, se possível, adicionando o número de pontos da palavra aos pontos do jogador e 
    devolvendo True
    Trocar - se não for possível jogar nenhuma palavra remove todas as letras do conjunto de letras do jogador e 
    distribui o mesmo número de letras, se possível, devolvendo True
    Passar - se for a primeira jogada (tabuleiro vazio) ou se não for possível nem jogar nem trocar não altera 
    nenhum argumento e devolve False
    """
    
    if eh_tabuleiro_vazio(tab) or len(jogador_letras(jog)) == 0:
        print(f'Jogada {jogador_identidade(jog)}: P')
        return False
    
    tds_subpadroes, casas, direcoes = gera_todos_padroes(tab, len(jogador_letras(jog)))
    if jogador_identidade(jog) == 'FACIL':
        N = 100
    elif jogador_identidade(jog) == 'MEDIO':
        N = 50
    else:
        N = 10

    padroes = tds_subpadroes[::N]
    casas = casas[::N]
    direcoes = direcoes[::N]

    maior_pont = -1
    melhor_par = (('', 0), 'nada')
    for i in range(len(padroes)):
        par = (procura_palavra_padrao(vocab, padroes[i], jogador_letras(jog), maior_pont + 1), padroes[i], casas[i], direcoes[i])
        if par[0] != ('', 0):           # Só existe palavra se a sua pontuação for maior que a pontuação da melhor palavra atual
            maior_pont = par[0][1]
            melhor_par = par
    
    if melhor_par[0] != ('', 0):        # Joga
        casa_i = melhor_par[2]
        direcao = melhor_par[3]
        str_let_usadas = let_usadas(melhor_par[0][0], melhor_par[1])
        insere_palavra(tab, casa_i, direcao, melhor_par[0][0])
        for let in str_let_usadas:
            usa_letra(jog, let)
        distribui_letras(jog, saco, len(str_let_usadas))
        soma_pontos(jog, melhor_par[0][1])
        if direcao == 'H':
            print(f'Jogada {jogador_identidade(jog)}: J {obtem_lin(casa_i)} {obtem_col(casa_i)} H {melhor_par[0][0]}')
        else:
            print(f'Jogada {jogador_identidade(jog)}: J {obtem_lin(casa_i)} {obtem_col(casa_i)} V {melhor_par[0][0]}')
        return True

    if len(saco) >= 7:          # Troca
        let_antes = ''
        for let in jogador_letras(jog):
            let_antes += f'{let} '
            usa_letra(jog, let)
        distribui_letras(jog, saco, 7)
        print(f'Jogada {jogador_identidade(jog)}: T {let_antes.rstrip()}')
        return True
    
    else:
        print(f'Jogada {jogador_identidade(jog)}: P')
        return False


def scrabble2(jogs, nome_fich, seed):
    """
    Realiza um jogo inteiro de scrabble para 2 a 4 jogadores humanos e/ou agentes, utilizando as palavras
    do ficheiro (nome_fich) como vocabulário e a (seed) como estado inicial do gerador pseudoaleatório.
    Cria os jogadores humanos e/ou agentes do tuplo (jogs), verificando a validade dos argumentos, cria um
    vocabulário com as palavras do ficheiro (nome_fich), baralha o saco com a (seed) e distribui 7 letras a
    cada jogador. A jogada de cada jogador é processada de acordo com a ordem dentro do tuplo de jogadores inicial
    (jogs) e varia se o jogador for humano ou agente, tendo as mesmas regras internas para os dois.
    O jogo acaba quando todos os jogadores passam a jogada sucessivamente ou quando um jogador fica sem letras e não há
    mais letras no saco, devolvendo um tuplo com a pontuação final de cada jogador.
    """
    if type(jogs) != tuple or len(jogs) < 2 or len(jogs) > 4:
        raise ValueError('scrabble2: argumentos inválidos')
    if type(nome_fich) != str or type(seed) != int or seed < 1:
        raise ValueError('scrabble2: argumentos inválidos')
    saco = baralha_saco(seed)
    lista_jogs = []
    for jog in jogs:
        if type(jog) != str or len(jog) == 0:
            raise ValueError('scrabble2: argumentos inválidos')
        if jog[0] != '@':
            jog = cria_humano(jog)
        else:
            if jog != '@FACIL' and jog != '@MEDIO' and jog != '@DIFICIL':
                raise ValueError('scrabble2: argumentos inválidos')
            else:
                jog = cria_agente(jog[1:])
        lista_jogs += (jog,)
        distribui_letras(jog, saco, 7)
    
    print('Bem-vindo ao SCRABBLE2.')
    tab = cria_tabuleiro()
    vocab = ficheiro_para_vocabulario(nome_fich)
    final = False
    cont = 0

    while not final:
        for jog in lista_jogs:
            print(tabuleiro_para_str(tab))
            for j in lista_jogs:
                print(jogador_para_str(j))
            if eh_agente(jog):
                if jogada_agente(tab, jog, vocab, saco):
                    cont = 0
                else:
                    cont += 1
            else:
                if jogada_humano(tab, jog, vocab, saco):
                    cont = 0
                else:
                    cont += 1

            if cont == len(lista_jogs):
                final = True
                break
            if len(jogador_letras(jog)) == 0 and len(saco) == 0:
                final = True
                break

    res = tuple()
    for jog in lista_jogs:
        res += (jogador_pontos(jog),)
    return res