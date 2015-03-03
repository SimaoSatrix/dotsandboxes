"""MODULO MODO
   Descricao: Implementa e controla todos os modos de jogo disponiveis
   Autores: Daniel Ramos(29423), Eduardo Martins(29035)
"""
#temporario para swampy, visualstudio bulllshit
import sys
sys.path.append("c:\\python27\\lib\\swampy")

#VARIAVEIS CONSTANTES
LETRA_JOGADOR = ['A','B','C','D','E']
COR_JOGADOR = ['red','blue','black','green','yellow']
LIMITE_MIN_TABULEIRO = (1,1)

MODO_JOGO_NENHUM                       = 0
MODO_JOGO_HUMANO_VS_HUMANO_TEXTO       = 1
MODO_JOGO_HUMANO_VS_COMPUTADOR_TEXTO   = 2
MODO_JOGO_HUMANO_VS_HUMANO_GRAFICO     = 3
MODO_JOGO_HUMANO_VS_COMPUTADOR_GRAFICO = 4

MODO_JOGADOR_HUMANO     = 0
MODO_JOGADOR_PC         = 1

ESTADO_TABULEIRO_EM_PROGRESSO = 0
ESTADO_TABULEIRO_GAMEOVER     = 1

FLAG_NENHUM   = 0
FLAG_EMPATE   = 1
FLAG_VENCEDOR = 2

class Rectangulo:
    """Implementacao da class rectangulo"""
    def __init__(self):
        self.int_x = 0
        self.int_y = 0
        self.int_width = 0
        self.int_height = 0
        self.str_color = "red"
        self.str_jogador = "unk"

    def colide(self, x, y):
        x1 = self.int_x
        x2 = self.x + self.int_width
        y1 = self.int_y
        y2 = self.int_y + self.int_height
        if (x >= x1 and event.x <= x2 and y >= y1 and event.y <= y2):
            return True
        return False

class Jogador:
    """Implementacao da class jogador"""        

    def __init__(self, id, tipo):
        self.int_tipo = tipo                      # tipo de jogador
        self.str_jogador = LETRA_JOGADOR[id]      # letra do jogador
        self.str_cor_jogador = COR_JOGADOR[id]    # cor do jogador 

class Modo_Texto:
    """Implementacao do modo texto do jogo"""

    def __init__(self,x,y):
        #guarda os dados de cada ponto do tabuleiro
        self.dict_tabuleiro = dict()

        #compensar aqui para que este desenha linhas/colunas adicionais para
        #formar o numero de linhas e colunas exacto na grelha
        self.int_linhas = x+1
        self.int_colunas = y+1
        #inicia a lista list_quadrados com arrays bidimensionais
        #nao e necessario compensar
        #guarda os dados de cada quadrado
        self.list_quadrados = [ [0 for i in range(x)] for i in range(y)]
    
    def update(self):
        return True

    def desenhar_tabuleiro(self):
        #desenha a tabela na forma invertida, comecando do fim
        #outra solucao seria desenhar na forma nao invertida e converter as 
        #coordenadas para a base actual (x1, y1 - nlinhas)(x1, y2 - nlinhas)
        #desenha a primeira linha para manter consistencia e evitar que se use
        #codigo adicional para
        #que este nao desenhe uma linha de colunas adicional no fim.

        #desenha a primeira linha
        for i in range(self.int_linhas-1, self.int_linhas-2, -1):
            #desenha n partes da linha por n colunas
            for j in range(self.int_colunas):
                #verifica se existe uma jogada: ex (0,0)(1,0)
                if(self.dict_tabuleiro.has_key(((j,i),(j+1,i)))):
                    print 'o - - - - ',
                #fecha a linha quando esta chega a ultima coluna que equivale
                #a colunas - 1
                elif(j == (self.int_colunas-1)):
                    print 'o'
                else:
                    print 'o         ',

        #desenha as restantes linhas, comecando por desenhar a linha 
        #"vertical" que forma as colunas da primeira linha anteriormente 
        #desenhada
        # |    |     |    |
        #desenha ate a ultima linha que equivale ao zero
        # o(0,3)-----(1,3)o <- primeira linha
        # |               |
        # |     (0,2)     |
        # o(0,2)-----(1,2)o  <--- comeca aqui
        for i in range(self.int_linhas-2, -1, -1):
            #verticais
            ##consistencia, desenha 4 vezes a coluna verticalmente
            for k in range(4): 
                for j in range(self.int_colunas):
                    #verifica se existe uma jogada feita: ex: (0,0)(0,1)
                    if(self.dict_tabuleiro.has_key(((j,i),(j,i+1)))):
                        #fecha a linha "vertical" quando esta chega a ultima
                        #coluna
                        #verifica se existe um quadrado preenchido e escreve o
                        #numero do jogador
                        #a coordenada do quadrado equivale ao i e j actual
                        if(j != (self.int_colunas-1) and 
                           self.list_quadrados[j][i] and k == 2):
                            print '|   ',self.list_quadrados[j][i],'   ',
                        else:
                            print '|         ',
                    else:
                        print '          ',
                print ''
            #horizontais
            #desenha a linha seguinte
            for j in range(self.int_colunas):
                #verifica se existe uma jogada feita: ex: (0,0)(1,0)
                if(self.dict_tabuleiro.has_key(((j,i),(j+1,i)))):
                    print 'o - - - - ',
                #fecha a linha quando esta chega a ultima coluna que equivale
                #a colunas - 1
                elif(j == (self.int_colunas-1)):
                    print 'o'
                else:
                    print 'o         ',

    def set_coordenadas(self, x1, y1, x2, y2):
        #converte as coordenadas para a base original
        #y1 = self.int_linhas - y1
        #y2 = self.int_linhas - y2
        #verificacao da validade de coordenadas
        #caso 1: coordenadas de origem e destino sao iguais
        if( (x1,y1) == (x2,y2)):
            return (False, "Coordenadas sao iguais")
        #caso 2: as coordenadas forma uma diagonal
        if( abs(x1 - x2) == 1 and abs(y1 - y2) == 1):
            return (False, "Coordenadas invalidas, jogada diagonal nao" +
                    " permitida")
        #caso 3: as coordenadas de destino sao maiores que o ponto adjacente
        if( abs(x1 - x2) > 1 or abs(y1 - y2) > 1):
            return (False, "Coordenadas invalidas, ponto adjacente muito" +
                    " longe")
        #caso 4: out of bounds
        if(x1 >= self.int_colunas or x2 >= self.int_colunas or 
           y1 >= self.int_linhas or y2 >= self.int_linhas):
            return (False, "Coordenadas fora de alcance")
        #caso 4: jogada ja feita
        if( (x1,y1) > (x2,y2)):
            if( self.dict_tabuleiro.has_key( ((x2,y2),(x1,y1)) )):
                return (False, "Jogada nao permitida, a jogada ja foi feita" +
                        " anteriormente")
        else:
            if( self.dict_tabuleiro.has_key( ((x1,y1),(x2,y2)) )):
                return (False, "Jogada nao permitida, a jogada ja foi feita" +
                        " anteriormente")

        #verificacao de coordenadas. As coordenadas devem ser re-ordenadas
        #caso seja necessario
        if( (x1,y1) > (x2,y2)):
            #inverte as coordenadas
            self.dict_tabuleiro[(x2,y2),(x1,y1)] = 1
        else:
            self.dict_tabuleiro[(x1,y1),(x2,y2)] = 1
        return (True, None)

    def actualizar_tabuleiro(self, jogador):
        #verificar se o jogador completou quadrados
        #3x3 -> 0 1 2 x 0 1 2
        bool_completou_quadrados = 0
        for i in range(self.int_linhas-1):
            for j in range(self.int_colunas-1):
                if (self.dict_tabuleiro.has_key(((j,i),(j+1,i))) and
                    self.dict_tabuleiro.has_key(((j,i),(j,i+1))) and
                    self.dict_tabuleiro.has_key(((j,i+1),(j+1,i+1))) and
                    self.dict_tabuleiro.has_key(((j+1,i),(j+1,i+1)))):
                    if( not self.list_quadrados[j][i]):
                        self.list_quadrados[j][i] = jogador
                        bool_completou_quadrados += 1
        return bool_completou_quadrados

    def verificar_quadrado_out_of_bounds(self, x, y):

        if(x >= self.int_colunas-1 or y >= self.int_linhas-1):
            return True
        return False

    def contar_lados_quadrado(self, j, i):
        lados = 0
        if(not self.list_quadrados[j][i]):

            if(self.dict_tabuleiro.has_key(((j,i),(j+1,i)))):
                lados += 1

            if(self.dict_tabuleiro.has_key(((j,i),(j,i+1)))):
                lados += 1

            if(self.dict_tabuleiro.has_key(((j,i+1),(j+1,i+1)))):
                    lados +=1
                       
            if(self.dict_tabuleiro.has_key(((j+1,i),(j+1,i+1)))):
                    lados +=1
            return lados
        else:
            return 4

    def ai_calcular_jogada(self):
        #AI, calculo de jogadas.
        #caso 1: completar quadrados duplos
        #caso 2: completar quadrados com 3 lados
        #caso 2: verificar quadrados com 0 ou 1 lado, evitando quadrados com 2 lados
        #caso 3: jogar para 1 ou 2 lados de um quadrado
        #caso 4: jogar para os restantes lados de qualquer quadrado

        a = 0
        b = 0
        c = 0
        d = 0
        lados =0
        #verificar double boxes
        for i in range(self.int_linhas-1):
            for j in range(self.int_colunas-1):
                #verificar se este quadrado nao esta completo
                
                if(not self.list_quadrados[j][i]):
                    lados = 0
                    if(self.dict_tabuleiro.has_key(((j,i),(j+1,i)))):
                        lados += 1
                        a = 0
                    else:
                        a = ((j,i),(j+1,i))

                    if(self.dict_tabuleiro.has_key(((j,i),(j,i+1)))):
                        lados += 1
                        b = 0
                    else:
                        b = ((j,i),(j,i+1))

                    if(self.dict_tabuleiro.has_key(((j,i+1),(j+1,i+1)))):
                        lados +=1
                        c = 0
                    else:
                        c = ((j,i+1),(j+1,i+1))
                       
                    if(self.dict_tabuleiro.has_key(((j+1,i),(j+1,i+1)))):
                        lados +=1
                        d = 0
                    else:
                        d = ((j+1,i),(j+1,i+1))
                    if(lados == 3):
                        if( a ):
                            #verificar quadrado a sul
                            if( not self.verificar_quadrado_out_of_bounds(j ,i-1)):
                                #contar os lados do quadrado adjacente sul
                                count = self.contar_lados_quadrado(j,i-1)
                                ##jogada dupla detectada
                                if(count == 3):
                                    bool_validade, str_erro = self.set_coordenadas(j,i, j+1, i)
                                    assert(str_erro == None)
                                    return True
                        if(b):
                            #verificar o quadrado oeste
                            if( not self.verificar_quadrado_out_of_bounds(j-1 ,i)):
                                #contar os lados do quadrado adjacente oeste
                                count = self.contar_lados_quadrado(j-1,i)
                                #ignorar se o quadrado tem 2 lados preenchidos
                                if(count == 3):
                                    bool_validade, str_erro = self.set_coordenadas(j,i, j, i+1) # ((j,i),(j,i+1))
                                    assert(str_erro == None)
                                    return True
                        if(c):
                            #verificar o quadrado norte
                            if( not self.verificar_quadrado_out_of_bounds(j ,i+1)):
                                #contar os lados do quadrado adjacente norte
                                count = self.contar_lados_quadrado(j,i+1)
                                #ignorar se o quadrado tem 2 lados preenchidos
                                if(count == 3):
                                    bool_validade, str_erro = self.set_coordenadas(j,i+1, j+1, i+1)
                                    assert(str_erro == None)
                                    return True
                        if(d):
                            #verificar quadrados a este
                            if( not self.verificar_quadrado_out_of_bounds(j+1 ,i)):
                                #contar os lados do quadrado adjacente norte
                                count = self.contar_lados_quadrado(j+1,i)
                                #ignorar se o quadrado tem 2 lados preenchidos
                                if(count == 3):
                                    bool_validade, str_erro = self.set_coordenadas(j+1,i, j+1, i+1) #((j+1,i),(j+1,i+1))
                                    assert(str_erro == None)
                                    return True
        #verificar 3 single side boxes
        for i in range(self.int_linhas-1):
            for j in range(self.int_colunas-1):
                #verificar se este quadrado nao esta completo
                
                if(not self.list_quadrados[j][i]):
                    lados = 0
                    if(self.dict_tabuleiro.has_key(((j,i),(j+1,i)))):
                        lados += 1
                        a = 0
                    else:
                        a = ((j,i),(j+1,i))

                    if(self.dict_tabuleiro.has_key(((j,i),(j,i+1)))):
                        lados += 1
                        b = 0
                    else:
                        b = ((j,i),(j,i+1))

                    if(self.dict_tabuleiro.has_key(((j,i+1),(j+1,i+1)))):
                        lados +=1
                        c = 0
                    else:
                        c = ((j,i+1),(j+1,i+1))
                       
                    if(self.dict_tabuleiro.has_key(((j+1,i),(j+1,i+1)))):
                        lados +=1
                        d = 0
                    else:
                        d = ((j+1,i),(j+1,i+1))
                    if(lados == 3):
                        if(a):
                            bool_validade, str_erro = self.set_coordenadas(j,i, j+1, i)
                            assert(str_erro == None)
                            return True
                        if(b):
                            bool_validade, str_erro = self.set_coordenadas(j,i, j, i+1) # ((j,i),(j,i+1))
                            assert(str_erro == None)
                            return True
                        if(c):
                            bool_validade, str_erro = self.set_coordenadas(j,i+1, j+1, i+1)
                            assert(str_erro == None)
                            return True
                        if(d):
                            bool_validade, str_erro = self.set_coordenadas(j+1,i, j+1, i+1) #((j+1,i),(j+1,i+1))
                            assert(str_erro == None)
                            return True



                     

        #verificar quadrados com 0 e 1
        for i in range(self.int_linhas-1):
            for j in range(self.int_colunas-1):
                #verificar se este quadrado nao esta completo
                
                if(not self.list_quadrados[j][i]):
                    lados = 0
                    if(self.dict_tabuleiro.has_key(((j,i),(j+1,i)))):
                        lados += 1
                        a = 0
                    else:
                        a = ((j,i),(j+1,i))

                    if(self.dict_tabuleiro.has_key(((j,i),(j,i+1)))):
                        lados += 1
                        b = 0
                    else:
                        b = ((j,i),(j,i+1))

                    if(self.dict_tabuleiro.has_key(((j,i+1),(j+1,i+1)))):
                        lados +=1
                        c = 0
                    else:
                        c = ((j,i+1),(j+1,i+1))
                       
                    if(self.dict_tabuleiro.has_key(((j+1,i),(j+1,i+1)))):
                        lados +=1
                        d = 0
                    else:
                        d = ((j+1,i),(j+1,i+1))

                    #preencher quadrados que tenham 0 ou 1 lados
                    #evitando os quadrados adjacentes com 2 lados
                    #evita que se form um quadrado com 3 lados disponivel na
                    #seguinte jogada
                    if(lados == 0 or lados == 1): #requer adjacencia pelos vistos
                        if(a):
                            #verificar quadrados a sul
                            if( not self.verificar_quadrado_out_of_bounds(j ,i-1)):
                                #contar os lados do quadrado adjacente sul
                                count = self.contar_lados_quadrado(j,i-1)
                                #ignorar se o quadrado tem 2 lados preenchidos
                                if(count == 2):
                                     pass
                                else:
                                     bool_validade, str_erro = self.set_coordenadas(j,i, j+1, i)
                                     assert(str_erro == None)
                                     return True
                            else:
                                #nao existe quadrados a sul
                                bool_validade, str_erro = self.set_coordenadas(j,i, j+1, i)
                                assert(str_erro == None)
                                return True

                        if(b):
                            #verificar quadrados a oeste
                            if( not self.verificar_quadrado_out_of_bounds(j-1 ,i)):
                                #contar os lados do quadrado adjacente oeste
                                count = self.contar_lados_quadrado(j-1,i)
                                #ignorar se o quadrado tem 2 lados preenchidos
                                if(count == 2):
                                     pass
                                else:
                                     bool_validade, str_erro = self.set_coordenadas(j,i, j, i+1) # ((j,i),(j,i+1))
                                     assert(str_erro == None)
                                     return True
                            else:

                                bool_validade, str_erro = self.set_coordenadas(j,i, j, i+1) # ((j,i),(j,i+1))
                                assert(str_erro == None)
                                return True

                        if(c):
                            #verificar quadrados a norte
                            if( not self.verificar_quadrado_out_of_bounds(j ,i+1)):
                                #contar os lados do quadrado adjacente norte
                                count = self.contar_lados_quadrado(j,i+1)
                                #ignorar se o quadrado tem 2 lados preenchidos
                                if(count == 2):
                                     pass
                                else:
                                     bool_validade, str_erro = self.set_coordenadas(j,i+1, j+1, i+1)
                                     assert(str_erro == None)
                                     return True
                            else:
                                bool_validade, str_erro = self.set_coordenadas(j,i+1, j+1, i+1)
                                assert(str_erro == None)
                                return True
                        if(d):
                            #verificar quadrados a este
                            if( not self.verificar_quadrado_out_of_bounds(j+1 ,i)):
                                #contar os lados do quadrado adjacente norte
                                count = self.contar_lados_quadrado(j+1,i)
                                #ignorar se o quadrado tem 2 lados preenchidos
                                if(count == 2):
                                     pass
                                else:
                                     bool_validade, str_erro = self.set_coordenadas(j+1,i, j+1, i+1) #((j+1,i),(j+1,i+1))
                                     assert(str_erro == None)
                                     return True
                            else:
                                bool_validade, str_erro = self.set_coordenadas(j+1,i, j+1, i+1)
                                assert(str_erro == None)
                                return True
        #verificar os restantes casos
        for i in range(self.int_linhas-1):
            for j in range(self.int_colunas-1):
                #verificar se este quadrado nao esta completo
                
                if(not self.list_quadrados[j][i]):
                    lados = 0
                    if(self.dict_tabuleiro.has_key(((j,i),(j+1,i)))):
                        lados += 1
                        a = 0
                    else:
                        a = ((j,i),(j+1,i))

                    if(self.dict_tabuleiro.has_key(((j,i),(j,i+1)))):
                        lados += 1
                        b = 0
                    else:
                        b = ((j,i),(j,i+1))

                    if(self.dict_tabuleiro.has_key(((j,i+1),(j+1,i+1)))):
                        lados +=1
                        c = 0
                    else:
                        c = ((j,i+1),(j+1,i+1))
                       
                    if(self.dict_tabuleiro.has_key(((j+1,i),(j+1,i+1)))):
                        lados +=1
                        d = 0
                    else:
                        d = ((j+1,i),(j+1,i+1))

                    if(a):
                        bool_validade, str_erro = self.set_coordenadas(j,i, j+1, i)
                        assert(str_erro == None)
                        return True
                    if(b):
                        bool_validade, str_erro = self.set_coordenadas(j,i, j, i+1)
                        assert(str_erro == None)
                        return True
                    if(c):
                        bool_validade, str_erro = self.set_coordenadas(j,i+1, j+1, i+1)
                        assert(str_erro == None)
                        return True
                    if(d):
                        bool_validade, str_erro = self.set_coordenadas(j+1,i, j+1, i+1)
                        assert(str_erro == None)
                        return True


        ###CRITICO### BOOM HEADSHOT
        return False
                 
    def obter_estado_tabuleiro(self):
        #verifica se o jogo terminou
        int_counter = 0
        dict_pontos = dict()
        #contagem de pontos por jogador
        for i in range( self.int_linhas-1):
            for j in range(self.int_colunas-1):
                if self.list_quadrados[j][i]:
                    int_counter += 1
                    dict_pontos[self.list_quadrados[j][i]] =\
                    dict_pontos.get(self.list_quadrados[j][i], 0) + 1

        #verificar se ouve empate ou vencedor, reordenar pelo jogador que
        #obteve mais pontos
        #se o counter for igual ao numero de quadrados no tabuleiro
        #entao o jogo terminou
        if (int_counter == ((self.int_linhas-1) * (self.int_colunas-1))):
            
            #reordena por pontos (pontos,jogador)
            list_dados = []
            for i in dict_pontos:
                list_dados.append((dict_pontos[i], i))

            list_dados.sort(reverse = True)
            
            #se existir quadrados com mais de 1 jogador atribuido
            #verificar se ouve empate(so funciona com dois jogadores ofc)
            if(len(list_dados) > 1 and list_dados[0][0] == list_dados[1][0]):
                return (ESTADO_TABULEIRO_GAMEOVER, FLAG_EMPATE, None)
            else:
                #retorna os dados do vencedor que esta no index 0 da lista
                #que por sua vez e uma tupple
                pontos, jogador = list_dados[0]
                return (ESTADO_TABULEIRO_GAMEOVER, FLAG_VENCEDOR, jogador)
        return (ESTADO_TABULEIRO_EM_PROGRESSO, None, None)
 
class modo_grafico:
    """Implementacao do modo grafico do jogo, usando swampy"""

    def __init(self, x, y):
        #guarda os dados de cada ponto do tabuleiro
        self.dict_tabuleiro = dict()
         #compensar aqui para que este desenha linhas/colunas adicionais para
        #formar o numero de linhas e colunas exacto na grelha
        self.int_linhas = x+1
        self.int_colunas = y+1
        #inicia a lista list_quadrados com arrays bidimensionais
        #nao e necessario compensar
        #guarda os dados de cada quadrado
        self.list_quadrados = [ [0 for i in range(x)] for i in range(y)]

        self.cls_world = World()
        self.cls_canvas = self.cls_world.ca(width=300, height=300, background='white')
        
    def update(self):
        return True

    def mouse_event_clicked(self, event):
        "loop principal aqui"
        wait_for_user()

    def preparar_tabuleiro(self):
        "preparar o tabuleiro grafico aqui pela primeira vez"
        #evento do rato para calculo de colisao
        self.canvas.bind('<Button-1>',self.mouse_event_clicked)


    def set_coordenadas(self, x1, y1, x2, y2):
        #verificacao de coordenadas. As coordenadas devem ser re-ordenadas
        #caso seja necessario
        if( (x1,y1) > (x2,y2)):
            #inverte as coordenadas
            self.dict_tabuleiro[(x2,y2),(x1,y1)] = 1
        else:
            self.dict_tabuleiro[(x1,y1),(x2,y2)] = 1
        return (True, None)

    def actualizar_tabuleiro(self, jogador):
        #verificar se o jogador completou quadrados
        #3x3 -> 0 1 2 x 0 1 2
        bool_completou_quadrados = 0
        for i in range(self.int_linhas-1):
            for j in range(self.int_colunas-1):
                if (self.dict_tabuleiro.has_key(((j,i),(j+1,i))) and
                    self.dict_tabuleiro.has_key(((j,i),(j,i+1))) and
                    self.dict_tabuleiro.has_key(((j,i+1),(j+1,i+1))) and
                    self.dict_tabuleiro.has_key(((j+1,i),(j+1,i+1)))):
                    if( not self.list_quadrados[j][i]):
                        self.list_quadrados[j][i] = jogador
                        bool_completou_quadrados += 1
        return bool_completou_quadrados

    def obter_estado_tabuleiro(self):
        #verifica se o jogo terminou
        int_counter = 0
        dict_pontos = dict()
        #contagem de pontos por jogador
        for i in range( self.int_linhas-1):
            for j in range(self.int_colunas-1):
                if self.list_quadrados[j][i]:
                    int_counter += 1
                    dict_pontos[self.list_quadrados[j][i]] =\
                    dict_pontos.get(self.list_quadrados[j][i], 0) + 1

        #verificar se ouve empate ou vencedor, reordenar pelo jogador que
        #obteve mais pontos
        #se o counter for igual ao numero de quadrados no tabuleiro
        #entao o jogo terminou
        if (int_counter == ((self.int_linhas-1) * (self.int_colunas-1))):
            
            #reordena por pontos (pontos,jogador)
            list_dados = []
            for i in dict_pontos:
                list_dados.append((dict_pontos[i], i))

            list_dados.sort(reverse = True)
            
            #se existir quadrados com mais de 1 jogador atribuido
            #verificar se ouve empate(so funciona com dois jogadores ofc)
            if(len(list_dados) > 1 and list_dados[0][0] == list_dados[1][0]):
                return (ESTADO_TABULEIRO_GAMEOVER, FLAG_EMPATE, None)
            else:
                #retorna os dados do vencedor que esta no index 0 da lista
                #que por sua vez e uma tupple
                pontos, jogador = list_dados[0]
                return (ESTADO_TABULEIRO_GAMEOVER, FLAG_VENCEDOR, jogador)
        return (ESTADO_TABULEIRO_EM_PROGRESSO, None, None)



