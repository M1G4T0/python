# Miguel Lobato
# ist1118345@tecnico.ulisboa.pt
# FP2526P1 - Scrabble

LETRAS = 'A','B','C','Ç','D','E','F','G','H','I','J','L','M','N','O','P','Q','R','S','T','U','V','X','Z'

PONTOS = {
'A': 1, 'B': 3, 'C': 2, 'Ç': 3, 'D': 2, 'E': 1,
'F': 4, 'G': 4, 'H': 4, 'I': 1, 'J': 5, 'L': 2,
'M': 1, 'N': 3, 'O': 1, 'P': 2, 'Q': 6, 'R': 1,
'S': 1, 'T': 1, 'U': 1, 'V': 4, 'X': 8, 'Z': 8 }

def cria_conjunto (conj_letras, num_occ):
    """ 
    A função cria um dicionário com as chaves sendo os elementos do primeiro 
    tuplo e o valor sendo o elemento do segundo tuplo de mesmo índice.

    Argumentos:
        let (tup): Um tuplo com letras.
        occ (tup): Um tuplo com inteiros positivos

    Return:
        occ_cada_let (dict): Um dicionário com o número de ocorrências
    de cada letra.

    Raises:
        ValueError: se os argumentos não forem tuplos e tiverem tamanhos diferentes;
    se as ocorrências não forem inteiros positivos e se as letras não pertencerem ao
    abecedário português; se existirem letras repetidas no let. 
    """

    occ_cada_let = {}       # Se os tuplos forem vazios: occ_cada_let = {}

    if type(conj_letras) != tuple or type(num_occ) != tuple:
        raise ValueError('cria_conjunto: argumentos inválidos')
    if len(conj_letras) != len(num_occ):
        raise ValueError('cria_conjunto: argumentos inválidos')
    for i in num_occ:
        if type(i) != int or i < 1:
            raise ValueError('cria_conjunto: argumentos inválidos')
    for i in range(len(conj_letras)):
        if conj_letras[i] not in LETRAS:
            raise ValueError('cria_conjunto: argumentos inválidos')
        for j in conj_letras[i + 1:]:
            if conj_letras[i] == j:
                raise ValueError('cria_conjunto: argumentos inválidos')                                                
    
    for i in range(len(conj_letras)):
        occ_cada_let[conj_letras[i]] = num_occ[i]       # Atribuir o número de ocorrências a uma letra única 1 a 1
    return occ_cada_let


def gera_numero_aleatorio (estado):
    """
    A função recebe um inteiro positivo como estado inicial do gerador (seed) e
    devolve uma modificação pseudoaleatória do estado através de operações xorshift.
    """

    if type(estado) != int or estado < 0:                                   
        raise ValueError('gera_numero_aleatorio: argumento inválido')

    estado ^= ( estado << 13 ) & 0xFFFFFFFF         # Operações xorshift
    estado ^= ( estado >> 17 ) & 0xFFFFFFFF
    estado ^= ( estado << 5 ) & 0xFFFFFFFF
  
    return estado


def permuta_letras (let, estado):
    """
    A função recebe uma lista com letras únicas e um estado pseudoaleatório,
    modificando destrutivamente a lista de forma pseudoaleatória de acordo
    com o algoritmo de Fisher-Yates.
    """

    n = len(let)
    
    for i in range(n - 1, 0, -1):
        estado = gera_numero_aleatorio(estado)
        j = estado % (i + 1)
        let[i], let[j] = let[j], let[i]         # Permutar a letra do último índice com uma letra de índice aleatório

    return

def ordena_dict (conj_letras):      #Função auxiliar
    """
    A função recebe um dicionário com letras únicas como chaves e
    o número de ocorrências da mesma letra como valor e devolve uma
    lista com todas as ocorrências de cada letra ordenadas de acordo
    com o abecedário português.
    """

    conj_comp = []          # Conjunto completo: com todas as ocorrências de cada letra
    conj_ord = []           # Conjunto ordenado: letras ordenadas de acordo com o abecedário

    for i in conj_letras:               
        for j in range(conj_letras[i]):
            conj_comp.append(i)

    for i in LETRAS:
        for j in conj_comp:
            if i == j:
                conj_ord.append(i)

    return conj_ord


def baralha_conjunto (conj_letras, estado):
    """
    A função ordena o conjunto de letras de acordo com o abecedário
    português, utilizando a função auxiliar ordena_dict e permuta
    pseudoaleatoriamente a ordem com recurso à permuta_letras, efetivamente
    baralhando o conjunto.

    Argumentos:
        conj_letras (dict): Um dicionário com letras únicas como chaves
    e o número de ocorrências de cada letra como valor.
        estado (int): Um inteiro positivo que representa o estado
    pseudoaleatório do gerador de xorshift.

    Return:
        conj_baralhado (list): Uma lista pseudoaleatoriamente baralhada
    com todas as ocorrências de cada letra única.
    """

    conj_baralhado = ordena_dict(conj_letras)
    permuta_letras(conj_baralhado, estado)

    return conj_baralhado


def testa_palavra (palavra, sequencia):         # Função auxiliar
    """
    A função recebe uma palavra e uma sequência do tabuleiro e testa se é possível
    inserir a palavra na sequência, retornando True se for possível e False se não.    
    """

    if len(palavra) != len(sequencia):                                         
        return False
    else:
        for i in range(len(palavra)):
            if sequencia[i] != '.' and sequencia[i] != palavra[i]:
                return False
    
    return True


def testa_palavra_padrao (palavra, sequencia, conj_letras):
    """
    A função recebe uma palavra, uma sequência do tabuleiro e um dicionário
    formado por letras únicas e o número de ocorrências de cada letra. Se 
    for possível formar a palavra com as letras do conjunto e colocar a palavra 
    na sequência a função devolve True, caso contrário, devolve False.
    """

    conj_letras_mod = conj_letras.copy()        # De forma a não modificar o conjunto de letras

    if not testa_palavra(palavra, sequencia):
        return False
    else:
        for i in range(len(palavra)):
            if sequencia[i] == '.':         # Não é necessário utilizar uma letra se essa letra já existir na sequência
                if palavra[i] not in conj_letras_mod:
                    return False                                       
                elif conj_letras_mod[palavra[i]] == 0:
                    return False
                else:
                    conj_letras_mod[palavra[i]] += -1
                                                                             
    return True


def cria_tabuleiro ():
    """
    A função recebe um argumento vazio e devolve um tabuleiro vazio de 
    dimensões 15 x 15, com as casas vazias a serem representadas por ".".
    """

    tab = []
    linha = ['.' , '.' , '.' , '.' , '.' , '.' , '.' , '.' , '.' , '.' , '.' , '.' , '.' , '.' , '.' ]

    for _ in range(15):
        tab.append(linha[:])

    return tab


def cria_casa (lin, col):
    """
    A função recebe dois inteiros positivos entre 1 e 15, 
    representando, respetivamente, a linha e a coluna da
    casa do tabuleiro e devolvendo essa casa como um tuplo.
    """

    if type(lin) != int or lin < 1 or lin > 15:
        raise ValueError('cria_casa: argumentos inválidos')
    if type(col) != int or col < 1 or col > 15:
        raise ValueError('cria_casa: argumentos inválidos')
    
    casa = (lin, col)

    return casa


def obtem_valor (tab, casa):

    """
    A função recebe o tabuleiro e uma casa e devolve o valor
    atual nessa casa do tabuleiro, tendo em atenção a diferença
    de índices.
    """

    valor = tab[casa[0] - 1][casa[1] - 1]       # Os índices do tabuleiro vão de 0 a 14 e as casas de 1 a 15
    
    return valor


def insere_letra (tab, casa, letra):
    """
    A função recebe o tabuleiro, uma casa e uma letra e
    retorna o tabuleiro com a letra na casa indicada.
    """
    
    if letra not in LETRAS:
        raise ValueError('insere_letra: argumentos inválidos')
    
    tab[casa[0] - 1][casa[1] - 1] = letra

    return tab


def testa_limite_tab (casa, direcao, tamanho):          # Função auxiliar
    """
    A função recebe a casa da primeira letra da palavra a
    tentar inserir, a direção da palavra no tabuleiro,
    sendo 'H' para horizontal e 'V' para vertical, e o 
    tamanho da palavra, devolvendo True se a palavra cabe 
    dentro dos limites do tabuleiro e False caso contrário.
    """

    if direcao == 'H':
        if casa[1] + tamanho - 1 > 15:
            return False
        else:
            return True
        
    if direcao == 'V':
        if casa[0] + tamanho - 1 > 15:
            return False
        else:
            return True
        

def obtem_sequencia (tab, casa, direcao, tamanho):
    """
    A função recebe o tabuleiro, a casa da primeira letra
    da palavra a tentar inserir, a direção da palavra no
    tabuleiro, sendo 'H' para horizontal e 'V' para vertical,
    e o tamanho da palavra, e devolve a sequência do tabuleiro
    onde será introduzida a palavra, se possível.
    """

    sequencia = ''

    if direcao != 'H' and direcao != 'V':
        raise ValueError('obtem_sequencia: argumentos inválidos')
    
    if not testa_limite_tab(casa, direcao, tamanho):
        raise ValueError('obtem_sequencia: argumentos inválidos')

    if direcao == 'H':
        for i in range(tamanho):
            prox_casa = (casa[0], casa[1] + i)
            sequencia += obtem_valor(tab, prox_casa)
    if direcao == 'V':
        for i in range(tamanho):
            prox_casa = (casa[0] + i, casa[1])
            sequencia += obtem_valor(tab, prox_casa)

    return sequencia


def insere_palavra (tab, casa, direcao, palavra):
    """
    A função recebe o tabuleiro, a casa da primeira letra
    da palavra a tentar inserir, a direção da palavra no
    tabuleiro, sendo 'H' para horizontal e 'V' para vertical,
    e a palavra, e devolve o tabuleiro com a palavra inserida,
    se for possível, e o tabuleiro sem alterações no caso contrário.
    """         

    if not testa_limite_tab(casa, direcao, len(palavra)):
        return tab    

    for i in range(len(palavra)):
        if direcao == 'H':
            prox_casa = (casa[0], casa[1] + i)          # Andar para a casa à direita
            tab = insere_letra(tab, prox_casa, palavra[i])
        elif direcao == 'V':
            prox_casa = (casa[0] + i, casa[1])          # Andar para a casa de baixo
            tab = insere_letra(tab, prox_casa, palavra[i])
        else:
            return tab
    return tab


def tabuleiro_para_str (tab):
    """
    A função recebe um tabuleiro e devolve como string a
    representação externa desse tabuleiro.
    """

    tab_str = ""

    tab_str += '                       1 1 1 1 1 1\n'           # Cabeçalho
    tab_str += '     1 2 3 4 5 6 7 8 9 0 1 2 3 4 5\n'
    tab_str += '   +-------------------------------+\n'            
    
    for i in range(len(tab)):           # Tabuleiro
        for j in range(len(tab[i])):
            if j == 0:
                tab_str += f"{i + 1:2} | "      # Colocar os números das linhas
            tab_str += tab[i][j]        # Adicionar os elementos de cada linha e coluna
            tab_str += " "
            if j == len(tab) - 1:
                tab_str += "|\n"
    
    tab_str += '   +-------------------------------+'

    return tab_str


def cria_jogador (ordem, pontos, conj_letras):
    """
    A função cria um jogador com os atributos ordem,
    pontos, e conjunto de letras.

    Argumentos:
        ordem (int): Ordem de jogada do jogador.
        pontos (int): Total de pontos do jogador
        conj_letras (dict): Um dicionário com as letras únicas
    como chaves e o número de ocorrências de cada letra como valor.

    Return:
        jog (dict): Um dicionário com a ordem, pontos e conjunto
    de letras do jogador.

    Raise:
        ValueError: se a ordem não for um inteiro entre 1 e 4;
    se os pontos não forem um inteiro positivo; se o conjunto de
    letras não for um dicionário; se as letras não pertencerem
    ao abecedário português; se o número de ocorrência das letras
    não for um inteiro positivo; se o conjunto de letras tiver
    letras repetidas nas chaves; se o número de letras do conjunto
    for maior de 7.
    """

    num_letras = 0

    if type(ordem) != int or ordem < 1 or ordem > 4:
        raise ValueError('cria_jogador: argumentos inválidos')
    if type(pontos) != int or pontos < 0:
        raise ValueError('cria_jogador: argumentos inválidos')
    if type(conj_letras) != dict:
        raise ValueError('cria_jogador: argumentos inválidos')
    
    for i in conj_letras:
        if i not in LETRAS:
            raise ValueError('cria_jogador: argumentos inválidos')
        if type(conj_letras[i]) != int or conj_letras[i] < 1:
            raise ValueError('cria_jogador: argumentos inválidos')
        num_letras += conj_letras[i]
    if num_letras > 7:
        raise ValueError('cria_jogador: argumentos inválidos')

    jog = {'id' : ordem, 'pontos' : pontos, 'letras' : conj_letras}
    
    return jog


def jogador_para_str (jog):
    """
    A função recebe um jogador na forma de dicionário e devolve
    a representação externa desse jogador em string.
    """

    conj_letras = " ".join(ordena_dict(jog['letras']))      # Ordenar o conjunto de letras e tranformar em str

    jog_str = f"#{jog['id']} ({jog['pontos']:3}): {conj_letras}"

    return jog_str


def distribui_letra (pilha, jog):       # pode nao ser o saco n tenho a ctz
    """
    A função retira a última letra da pilha e coloca
    no conjunto de letras do jogador, se possível.

    Argumentos:
        pilha(list): Lista ordenada de letras
        jog(dict): Um jogador com os atributos ordem,
    pontos e conjunto de letras.

    Return:
        True se distribuir uma letra ao jogador.
        False se a pilha estiver vazia.
    """
    
    if pilha == []:
        return False
    else:
        if pilha[len(pilha) - 1] not in jog['letras']:
            jog['letras'][pilha[len(pilha) - 1]] = 1
            pilha.pop()
        else:
            jog['letras'][pilha[len(pilha) - 1]] += 1
            pilha.pop()

    return True


def ordena_tuple (letras_jogadas):          # Função auxiliar
    """
    A função recebe um tuplo com letras e devolve
    um tuplo com as letras ordenadas de acordo
    com o abecedário português.
    """

    letras_jogadas_ord = {}
    letras_jogadas_ord_tuple = tuple()

    for i in range(len(letras_jogadas)):        # Tranformar o tuplo das letras em dicionário para utilizar a ordena_dict
        if letras_jogadas[i] not in letras_jogadas_ord:
            letras_jogadas_ord[letras_jogadas[i]] = 1
        else:
            letras_jogadas_ord[letras_jogadas[i]] += 1
    letras_jogadas_ord = ordena_dict(letras_jogadas_ord)
    for i in range(len(letras_jogadas_ord)):        # Tranformar a lista ordenada de volta para tuplo
        letras_jogadas_ord_tuple += tuple(letras_jogadas_ord[i])
    
    return letras_jogadas_ord_tuple


def joga_palavra (tab, palavra, casa, direcao, conj_letras, prim_jogada):
    """
    A função verifica se é possível inserir a palavra no tabuleiro atual
    com as letras do jogador, tendo em conta se é a primeira jogada e,
    se possível, modifica o tabuleiro devolve as letras utilizadas para
    o jogador formar a palavra de acordo com a ordme do abecedário português,
    caso contrário não modifica o tabuleiro e devolve um tuplo vazio.

    Argumentos:
        tab(list): O tabuleiro atual.
        palavra(str): A palavra a tentar ser inserida no tabuleiro.
        casa(tuple): A casa da primeira letra a ser inserida.
        direcao(str): A direção da palavra a tentar ser inserida:
                     'H' se for horizontal
                     'V' se for vertical
        conj_letras(dict): O conjunto de letras do jogador.
        prim_jogada(bool): 'True' se a casa central não estiver ocupada
                           'False' se a casa central estiver ocupada
    
    Return:
        letras_jogadas_ord(tuple): Um tuplo com as letras utilizadas para o
    jogador formar a palavra acordo com a ordem do abecedário português.

    Para ser possível inserir a palavra no tabuleiro é necessário verificar:
        Se a palavra pode ser inserida dentor dos limites do tabuleiro; se
        é possível inserir a palavra na sequência do tabuleiro indicada; se
        se a palavra não conter 2 letras; se na primeira jogada a palavra não
        ocupa a casa central; se as jogadas seguintes não utilizarem uma letra
        já no tabuleiro.

    """
    letras_jogadas = tuple()
    
    if not testa_limite_tab(casa, direcao, len(palavra)):
        return letras_jogadas

    sequencia = obtem_sequencia(tab, casa, direcao, len(palavra))
    tab_mod = []
    for i in tab:
        tab_mod.append(i[:])        # Criar uma deep copy do tabuleiro para verificar se a casa central está ocupada depois de inserir a palavra

    if not testa_limite_tab:
        raise letras_jogadas
    
    if prim_jogada:
        if not testa_palavra_padrao(palavra, sequencia, conj_letras):
            return letras_jogadas
        else:
            if len(palavra) < 2:
                return letras_jogadas
            else:
                tab_mod = insere_palavra(tab_mod, casa, direcao, palavra)
                if obtem_valor(tab_mod, cria_casa(8, 8)) == '.':
                    return letras_jogadas
                else:
                    for i in range(len(palavra)):
                        letras_jogadas += tuple(palavra[i])
        letras_jogadas_ord = ordena_tuple(letras_jogadas)
        tab = insere_palavra(tab, casa, direcao, palavra)       # Inserir a palavra no tabuleiro apenas quando todas as condições foram verificadas
        return letras_jogadas_ord

    else:
        if len(palavra) < 2:
            return letras_jogadas
        else:
            if any(i != '.' for i in sequencia):            # Como já não é a primeira jogada, tem de existir pelo menos uma letra na sequência onde vamos colocar a palavra
                if not testa_palavra_padrao(palavra, sequencia, conj_letras):
                    return letras_jogadas
                else:
                    for i in range(len(palavra)):
                        if sequencia[i] == '.':
                            letras_jogadas += tuple(palavra[i])
            else:
                return letras_jogadas
        letras_jogadas_ord = ordena_tuple(letras_jogadas)
        tab = insere_palavra(tab, casa, direcao, palavra)       # Inserir a palavra no tabuleiro apenas quando todas as condições foram verificadas
        return letras_jogadas_ord


def processa_jogada (tab, jog, pilha, PONTOS, prim_jogada):
    """
    A função recebe o input do jogador e se este for válido, processa
    a jogada dependendo da ação pretendida, podendo passar e não modificar
    os argumentos, trocar letras específicas do conjunto de letras do jogador
    e inserir uma palavra, atualizando o tabuleiro, os pontos e o conjunto de
    letras do jogador. Se o input do jogador não for válido, utilizando a
    recursão, pede ao jogador outro input até receber um válido.
    
    Argumentos:
        tab(list): O tabuleiro atual.
        jog(dict): Um dicionário com os parâmetros do jogador.
        pilha(list): Uma lista baralhada com as letras do jogo.
        PONTOS(dict): Um dicionário com o número de pontos.
    equivalentes a cada letra do abecedário português.
        prim_jogada(bool): 'True' se a casa central não estiver ocupada
                           'False' se a casa central estiver ocupada
    Return:
        Devolve True se o jogador trocar letras ou jogar uma palavra.
        Devolve False se o jogador passar a jogada.

    Para o input ser validado é necessário verificar:
        Se o input começa por 'P', 'T' ou 'J'; 
        Se começar por 'P', se o input tem exatamente 1 argumento;
        Se começar por 'T', se as letras pertencer ao conjunto de
        letras do jogador; se a pilha tem pelo menos 7 letras;
        Se começar por 'J', se os segundo e terceiro argumentos são
        inteiros entre 1 e 15; se o terceiro argumento é 'H' ou 'V';
        se a jogada tem exatamente 5 argumentos, se for utilizada
        pelo menos uma letra do jogador.
    """

    jogada = input(f"Jogada J{jog['id']}: ")                                # o jogador dá imput da jogada

    if jogada == '':
        return processa_jogada(tab, jog, pilha, PONTOS, prim_jogada)

    jogada = jogada.split(' ')
    
    if jogada[0] != 'P' and jogada[0] != 'T' and jogada[0] != 'J':
        return processa_jogada(tab, jog, pilha, PONTOS, prim_jogada)

    if jogada[0] == 'P':                                                    # se o jogador passar return False
        if len(jogada) != 1:
            return processa_jogada(tab, jog, pilha, PONTOS, prim_jogada)
        return False

    if jogada[0] == 'T':
        conj_letras_test = jog['letras'].copy()
        if len(pilha) < 8:                                                  # só é possível trocar se a pilha tiver pelo menos 7 letras
            return processa_jogada(tab, jog, pilha, PONTOS, prim_jogada)
        for i in range(1, len(jogada)):                                     # verificar se é possível trocar as letras sem alterar o conjunto do jogador
            if jogada[i] in conj_letras_test:
                conj_letras_test[jogada[i]] += -1
                if conj_letras_test[jogada[i]] == 0:
                    del(conj_letras_test[jogada[i]])
            else:
                return processa_jogada(tab, jog, pilha, PONTOS, prim_jogada)
        for i in range(1, len(jogada)):
            jog['letras'][jogada[i]] += -1
            if jog['letras'][jogada[i]] == 0:
                del(jog['letras'][jogada[i]])
            distribui_letra(pilha, jog)                                     # verifica se a pilha tem letras e remove a última letra da pilha e adiciona-a às letras do jogador                    
                
        return True
    
    if jogada[0] == 'J':
        if not jogada[1].isdigit():
            return processa_jogada(tab, jog, pilha, PONTOS, prim_jogada)
        else:
            if int(jogada[1]) < 1 or int(jogada[1]) > 15:
                return processa_jogada(tab, jog, pilha, PONTOS, prim_jogada)
            else:
                linha = int(jogada[1])
        if not jogada[2].isdigit():
            return processa_jogada(tab, jog, pilha, PONTOS, prim_jogada)
        else:
           if int(jogada[2]) < 1 or int(jogada[2]) > 15:
               return processa_jogada(tab, jog, pilha, PONTOS, prim_jogada)
           else:
               coluna = int(jogada[2])
        casa = cria_casa (linha, coluna)
        if jogada[3] != 'H' and jogada[3] != 'V':
            return processa_jogada(tab, jog, pilha, PONTOS, prim_jogada)
        else:
            direcao = jogada[3]
        if len(jogada) != 5:
            return processa_jogada(tab, jog, pilha, PONTOS, prim_jogada)
        palavra = jogada[4]
        letras_jog = joga_palavra(tab, palavra, casa, direcao, jog['letras'], prim_jogada)
        if len(letras_jog) == 0:
            return processa_jogada(tab, jog, pilha, PONTOS, prim_jogada)
        else:
            for i in palavra:
                jog['pontos'] += PONTOS[i]
            for i in letras_jog:
                jog['letras'][i] += -1
                if jog['letras'][i] == 0:
                    del(jog['letras'][i])
                distribui_letra(pilha, jog)
        return True


def scrabble (n_jogadores, saco, PONTOS, seed):
    """
    A função cria os jogadores e distribui do saco baralhado as letras 
    de cada um e inicia o jogo, pedindo inputs aos jogadores por ordem,
    modificando o tabuleiro e alterando dos pontos e as letras dos
    conjuntos de letras dos jogadores a cada jogada. O jogo termina
    quando todos os jogadores passam a jogada consecutivamente ou
    se um jogador ficar sem letras e não tiver mais letras na pilha.
    Quando o jogo temrina, devolve a pontuação final de cada jogador.

    Argumentos:
        n_jogadores(int): O número de jogadores que vão participar.
        saco(dict): Um dicionário com letras únicas do abecedário como
    chaves e o número de ocorrências de cada letra como valor, sendo estas
    todas as letras utilizadas durante o jogo.
        PONTOS(dict): Um dicionário com o número de pontos.
    equivalentes a cada letra do abecedário português.
        seed(int): Um inteiro positivo aleatório que serve como estado
    inicial do gerador de xorshift.

    Return:
        resultado(tuple): Um tuplo com as pontuações de cada jogador.

    Raises:
        ValueError: se os jogadores não forem um inteiro positivo entre 2 e 4;
    se o conjunto de letras não for um dicionário; se as letras do conjunto de 
    letras não pertencerem ao abecedário português; se o número de ocorrências
    não for um inteiro positivo; se o conjunto de pontos equivalentes a cada letra
    não for um dicionário; se as letras do conjunto de pontos não pertencerem ao
    abecedário português; se o número de pontos não for um inteiro positivo;
    se a seed não for um inteiro positivo; se o número de letras no saco for menor
    que o número de letras no conjunto de pontos; se o número total de ocorrências
    de letras no saco não for suficiente para distribuir 7 letras a todos os jogadores.
    """
    if type(n_jogadores) != int or n_jogadores < 2 or n_jogadores > 4:
        raise ValueError('scrabble: argumentos inválidos')
    if type(saco) != dict or type(PONTOS) != dict:
        raise ValueError('scrabble: argumentos inválidos')                  
    for i in saco:
        if i not in LETRAS or i not in PONTOS or type(saco[i]) != int or saco[i] < 1:
            raise ValueError('scrabble: argumentos inválidos')
    for i in PONTOS:
        if i not in LETRAS or type(PONTOS[i]) != int or PONTOS[i] < 1:
            raise ValueError('scrabble: argumentos inválidos')
    if type(seed) != int or seed < 1:                                      
        raise ValueError('scrabble: argumentos inválidos')
    if len(saco) > len(PONTOS):
        raise ValueError('scrabble: argumentos inválidos')
    numero_letras = 0
    for i in saco.values():
        numero_letras += i
    if numero_letras < 7 * n_jogadores:
        raise ValueError('scrabble: argumentos inválidos')
    
    pilha = baralha_conjunto(saco, seed)
    fim = False
    prim_jogada = True
    cont = 0
    conj_jogs = []
    for i in range(n_jogadores):
        conj_jogs += (cria_jogador(i + 1, 0, cria_conjunto((),())),)
    for jog in conj_jogs:
        for _ in range(7):
            distribui_letra(pilha, jog)
    tab = cria_tabuleiro()
    print('Bem-vindo ao SCRABBLE.')
    
    while not fim:
        for jog in conj_jogs:
            print(tabuleiro_para_str(tab))
            for j in conj_jogs:         # não posso utilizar a variável jog pois o loop já está dentro de um loop com essa variável
                print(jogador_para_str(j))
            if not processa_jogada(tab, jog, pilha, PONTOS, prim_jogada):
                cont += 1
            else:
                cont = 0
            if prim_jogada and obtem_valor(tab, cria_casa(8, 8)) != '.':
                prim_jogada = False         # Se a casa do meio não for ocupada ainda estamos na primeira jogada
            if cont == n_jogadores:
                fim = True
                break
            if len(pilha) == 0 and len(jog['letras']) == 0:
                fim = True
                break

    
    resultado = ()
    for jog in conj_jogs:
        resultado += (jog['pontos'],)
    return resultado