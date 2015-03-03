"""MODULO MODO
   Descricao: Implementa e controla todos os modos de jogo disponiveis
   Autores: Daniel Ramos(29423), Eduardo Martins(29035)
"""

import Modo

JOGADA_EM_ESPERA = 0
JOGADA_JOGADOR_SEGUINTE = 1

class Jogo:
    """implementacao da classe jogo que gere o jogo actual em progresso"""

    def __init__(self, modo, x, y, j_humano):
        self.int_id_gen         = 0     #gerador de ids do jogador
        self.list_jogadores     = []    #lista de jogadores
        self.int_jogador_actual = 0     #id do jogador actual
        self.cls_modo           = 0     #instancia da classe modo_xxx escolhida
        self.int_estado_jogada  = 0     #estado da jogada actual

        if(modo == Modo.MODO_JOGO_HUMANO_VS_HUMANO_TEXTO):
             #prepara o modo escolhido
             self.cls_modo = Modo.Modo_Texto(x,y)
             #prepara os jogadores
             self.list_jogadores.append(Modo.Jogador(self.gerar_id_jogador(), \
                                                     Modo.MODO_JOGADOR_HUMANO))
             self.list_jogadores.append(Modo.Jogador(self.gerar_id_jogador(), \
                                                     Modo.MODO_JOGADOR_HUMANO))
        
        if(modo == Modo.MODO_JOGO_HUMANO_VS_HUMANO_GRAFICO):
             #prepara o modo escolhido
             self.cls_modo = Modo.Modo_Grafico(x,y)
             #prepara os jogadores
             self.list_jogadores.append(Modo.Jogador(self.gerar_id_jogador(), \
                                                     Modo.MODO_JOGADOR_HUMANO))
             self.list_jogadores.append(Modo.Jogador(self.gerar_id_jogador(), \
                                                     Modo.MODO_JOGADOR_HUMANO))

        if(modo == Modo.MODO_JOGO_HUMANO_VS_COMPUTADOR_TEXTO):
            self.cls_modo = Modo.Modo_Texto(x,y)
            if(j_humano == 0):
                self.list_jogadores.append(Modo.Jogador(self.gerar_id_jogador(), Modo.MODO_JOGADOR_HUMANO))
                self.list_jogadores.append(Modo.Jogador(self.gerar_id_jogador(), Modo.MODO_JOGADOR_PC))
            else:
                self.list_jogadores.append(Modo.Jogador(self.gerar_id_jogador(), Modo.MODO_JOGADOR_PC))
                self.list_jogadores.append(Modo.Jogador(self.gerar_id_jogador(), Modo.MODO_JOGADOR_HUMANO))

    def gerar_id_jogador(self):
        int_id =  self.int_id_gen
        self.int_id_gen += 1
        return int_id

    def obter_jogador_seguinte(self):
        if(self.int_jogador_actual >= (len(self.list_jogadores)-1)):
            self.int_jogador_actual = 0
            return self.int_jogador_actual
        else:
            self.int_jogador_actual += 1
            return (self.int_jogador_actual)

    def ler_coordenadas(self,input, jogador):
        if len(input)<= 2*len(str(self.cls_modo.int_linhas))+2* \
            len(str(self.cls_modo.int_colunas))+6 and len(input)>=10:
             # verifica o input segundo comprimento, parenteses + virgulas, 
             # 6 indexes
             # minimo len possivel 10 (6 indexes + 4 unidades (coordenadas)
             # maximo len possivel (6 indexes + total de caracteres presentes 
             # no total de coordenadas)
             if (input[0]=='(') and (input[-1]==')') and (')(' in input):
                 #divisao do input em pontos de saida e partida
                 ponto1,ponto2=input[1:-1].split(')(')
                 # divisao do ponto de saida em coordenadas x e y
                 x1,y1=ponto1.split(',')
                 # divisao do ponto de chegada em coordenadas x e y
                 x2,y2=ponto2.split(',')
                 try:
                     x1=int(x1)
                     x2=int(x2)
                     y1=int(y1)
                     y2=int(y2)
                     return (x1,y1,x2,y2)
                 except:
                     print "Coordenadas nao sao validas"
                     i=raw_input(str.format("Jogador %s: segmento entre que pontos?(x1,y1)(x2,y2)" % jogador))
                     return self.ler_coordenadas(i,jogador)
             else:
                 print "Coordenadas nao sao validas"
                 i=raw_input(str.format("Jogador %s: segmento entre que pontos?(x1,y1)(x2,y2)" % jogador))
                 return self.ler_coordenadas(i,jogador)
        else:
            print "Coordenadas nao sao validas"
            i=raw_input(str.format("Jogador %s: segmento entre que pontos?(x1,y1)(x2,y2)" % jogador))
            return self.ler_coordenadas(i,jogador)

    def ai_concluir_jogada(self):
        self.cls_modo.ai_calcular_jogada()

    def actualizar(self):
        if(self.int_estado_jogada == JOGADA_EM_ESPERA):
            self.cls_modo.desenhar_tabuleiro()
            str_jog = self.list_jogadores[self.int_jogador_actual].str_jogador
              
            #selecionar se e o computador ou o jogador a jogar
            if(self.list_jogadores[self.int_jogador_actual].int_tipo == Modo.MODO_JOGADOR_PC):
                print "Jogador %s(Computador):" % str_jog 
                self.ai_concluir_jogada()
                int_quadrados = self.cls_modo.actualizar_tabuleiro(str_jog)

                int_estado, int_flag, str_vencedor = \
                         self.cls_modo.obter_estado_tabuleiro()

                if(int_estado == Modo.ESTADO_TABULEIRO_GAMEOVER):
                    self.cls_modo.desenhar_tabuleiro()
                    if(int_flag == Modo.FLAG_EMPATE):
                        print "Fim do jogo, os jogadores empataram"
                    elif(int_flag == Modo.FLAG_VENCEDOR):
                        print "Fim do jogo. O vencedor foi o jogador ", \
                            str_vencedor
                    return False

                #se o jogador completou quadrados, ganha uma nova jogada
                if(int_quadrados):
                    self.int_estado_jogada = JOGADA_EM_ESPERA
                else:
                    self.int_estado_jogada = JOGADA_JOGADOR_SEGUINTE
            else:
                str_coordenadas = raw_input( \
                    str.format("Jogador %s: segmento entre que pontos?(x1,y1)" \
                    % str_jog + "(x2,y2)"))

                int_x1, int_y1, int_x2, int_y2 = \
                    self.ler_coordenadas(str_coordenadas,str_jog)

                bool_validade, str_erro = \
                    self.cls_modo.set_coordenadas(int_x1,int_y1,int_x2,int_y2)

                if(bool_validade):
                     #verifica o estado do tabuleiro e atribui novos quadrados 
                     #se o jogador os completou com a nova jogada.
                     #verifica tambem se o tabuleiro foi completado e retorna o 
                     #vencedor.
                     int_quadrados = self.cls_modo.actualizar_tabuleiro(str_jog)
                 
                     int_estado, int_flag, str_vencedor = \
                         self.cls_modo.obter_estado_tabuleiro()

                     if(int_estado == Modo.ESTADO_TABULEIRO_GAMEOVER):
                         self.cls_modo.desenhar_tabuleiro()
                         if(int_flag == Modo.FLAG_EMPATE):
                             print "Fim do jogo, os jogadores empataram"
                         elif(int_flag == Modo.FLAG_VENCEDOR):
                             print "Fim do jogo. O vencedor foi o jogador ", \
                                 str_vencedor
                         return False

                     #se o jogador completou quadrados, ganha uma nova jogada
                     if(int_quadrados):
                         self.int_estado_jogada = JOGADA_EM_ESPERA
                     else:
                         self.int_estado_jogada = JOGADA_JOGADOR_SEGUINTE

                else:
                    print str_erro
        elif(self.int_estado_jogada == JOGADA_JOGADOR_SEGUINTE):
            self.obter_jogador_seguinte()
            self.int_estado_jogada = JOGADA_EM_ESPERA
        return True