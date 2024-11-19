import pygame, sys, random

pygame.init()

# Definindo a largura e altura da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0)

# Definindo as cores
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NUM_RODADAS = 5

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.fichas = 15  # Cada jogador começa com 15 fichas
        self.apostas = {'quadrante': 0, 'vermelho': 0, 'verde': 0, 'azul': 0, 'par_ordenado': 0}
        self.resultado_rodada = ""
    def fazer_aposta(self, tipo, valor):
        if self.fichas >= valor:
            self.fichas -= valor
            self.apostas[tipo] += valor
            print(f"{self.nome} fez uma aposta de {valor} em {tipo}. Fichas restantes: {self.fichas}")
        else:
            print(f"{self.nome} não tem fichas suficientes para apostar {valor}.")

    def reset_apostas(self):
        self.apostas = {'quadrante': 0, 'vermelho': 0, 'verde': 0, 'azul': 0, 'par_ordenado': 0}

    def ganhar_fichas(self, ganho):
        self.fichas += ganho

class Cenario:
    def __init__(self, tamanho):
        self.tamanho = tamanho
        # 0 - Numeração das casas
        # 1 - Vermelho
        # 2 - Verde
        # 3 - Azul
        # 4 - Aposta no quadrante
        # 5 - Aposta no Azul
        # 6 - Aposta no Vermelho
        # 7 - Aposta no Verde
        self.tabuleiro = [
            [0, 0, 0, 0, 0, 0, 0, 4],
            [0, 1, 3, 2, 2, 3, 1, 4],
            [0, 3, 1, 3, 3, 1, 3, 4],
            [0, 2, 3, 1, 1, 3, 2, 4],
            [0, 2, 3, 1, 1, 3, 2, 5],
            [0, 3, 1, 3, 3, 1, 3, 6],
            [0, 1, 3, 2, 2, 3, 1, 7]#,
            #[8, 8, 8, 8, 8, 8, 8, 8]
        ]
        self.input_active = True
        self.input_rect = pygame.Rect(300, 250, 200, 50)
        self.input_text = ''

    # Função que desenha cada linha do tabuleiro
    def paint_line(self, screen, number_line, line):
        for number_col, casa_tabuleiro in enumerate(line):
            x = number_col * self.tamanho
            y = number_line * self.tamanho
            cor = WHITE
            
            # Desenha o número da linha (coluna 0)
            if casa_tabuleiro == 0 and number_col == 0:
                font = pygame.font.SysFont(None, 40)
                text = font.render(str(number_line), True, BLACK)
                screen.blit(text, (x + 25, y + self.tamanho // 2 - 10))  # Centraliza na célula
                pygame.draw.rect(screen, BLACK, (x, y, self.tamanho + 120, self.tamanho), 1)
                continue
            # Define a cor conforme o valor
            if casa_tabuleiro == 1:
                cor = RED
            elif casa_tabuleiro == 2:
                cor = GREEN
            elif casa_tabuleiro == 3:
                cor = BLUE
            elif casa_tabuleiro in (4, 5, 6, 7):
                pygame.draw.rect(screen, cor, (x, y, self.tamanho + 120, self.tamanho))
                pygame.draw.rect(screen, BLACK, (x, y, self.tamanho + 120, self.tamanho), 1)
                font = pygame.font.SysFont(None, 40)
                if casa_tabuleiro == 4:
                    text = font.render("Q" + str(number_line + 1), True, BLACK)
                    screen.blit(text, (x + 75, y + self.tamanho // 2 - 10))
                    break
                if casa_tabuleiro == 5:
                    text = font.render("Azul", True, BLUE)
                elif casa_tabuleiro == 6:
                    text = font.render("Vermelho", True, RED)
                elif casa_tabuleiro == 7:
                    text = font.render("Verde", True, GREEN)
                screen.blit(text, (x + 25, y + self.tamanho // 2 - 10))
                continue
            
                #pygame.draw.rect(screen, cor, (x, y, self.tamanho + 120, self.tamanho))
            # Desenha o quadrado colorido
            if casa_tabuleiro != 4:
                pygame.draw.rect(screen, cor, (x, y, self.tamanho, self.tamanho))
                pygame.draw.rect(screen, BLACK, (x, y, self.tamanho, self.tamanho), 1)
                if casa_tabuleiro == 1:
                    pygame.draw.rect(screen, cor, (x, y, self.tamanho, self.tamanho))
                    pygame.draw.rect(screen, BLACK, (x, y, self.tamanho, self.tamanho), 1)
                    font = pygame.font.SysFont(None, 40)
                    if number_line == 2 and number_col == 5:
                        text = font.render("Q" + str(number_line-1), True, WHITE)
                        screen.blit(text, (x + 25, y + self.tamanho // 2 - 10))
                    if number_line == 2 and number_col == 2: 
                        text = font.render("Q" + str(number_line), True, WHITE)
                        screen.blit(text, (x + 25, y + self.tamanho // 2 - 10))
                    if number_line == 5 and number_col == 2:
                        text = font.render("Q" + str(number_line-2), True, WHITE)
                        screen.blit(text, (x + 25, y + self.tamanho // 2 - 10))
                    if number_line == 5 and number_col == 5:
                        text = font.render("Q" + str(number_line-1), True, WHITE)
                        screen.blit(text, (x + 25, y + self.tamanho // 2 - 10))
    # Função para desenhar a numeração das colunas
    def draw_column_numbers(self, screen):
        font = pygame.font.SysFont(None, 40)
        for i in range(1, len(self.tabuleiro[0]) - 1):  # Pula a primeira coluna (coluna das linhas)
            x = i * self.tamanho
            text = font.render(str(i), True, BLACK)
            screen.blit(text, (x + self.tamanho // 2 - 10, 30))  # Alinhar o texto no centro da célula

    # Função para desenhar o tabuleiro completo
    def paint_board(self, screen):
        for number_line, line in enumerate(self.tabuleiro):
            self.paint_line(screen, number_line, line)
        self.draw_column_numbers(screen)  # Desenhar números das colunas

    def check_click(self, pos):
        mouse_x, mouse_y = pos
        for number_line, line in enumerate(self.tabuleiro):
            for number_col, casa_tabuleiro in enumerate(line):
                x = number_col * self.tamanho
                y = number_line * self.tamanho
                if x < mouse_x < x + self.tamanho + 120 and y < mouse_y < y + self.tamanho:
                    if casa_tabuleiro in (4, 5, 6, 7):  # Apenas casas coloridas e a última coluna são clicáveis
                        print(f"Clique em casa ({number_col}, {number_line})")
                        return casa_tabuleiro, number_col, number_line
                # Evitar cliques em casas de numeração (linha 0 ou coluna 0)
                if number_line == 0 or number_col == 0:
                    continue
                # Verifica se o clique está dentro de uma casa colorida
                if x < mouse_x < x + self.tamanho and y < mouse_y < y + self.tamanho:
                    if casa_tabuleiro in (1, 2, 3):  # Apenas casas coloridas e a última coluna são clicáveis
                        print(f"Clique em casa ({number_col}, {number_line})")
                        return casa_tabuleiro, number_col, number_line
        return None
    def toggle_input(self):
        self.input_active = not self.input_active
        self.input_text = ''

class GerenteDeRodadas:
    def _init_(self, jogadores):
        self.jogadores = jogadores
        self.rodada_atual = 1
    
    def lancar_dados(self):
        dado1 = random.randint(1, 6)
        dado2 = random.randint(1, 6)
        return dado1, dado2

# Inicializa o cenário com o tamanho adequado
tam = (600 // 7)
cenario = Cenario(tam)
jogadores = [Jogador("Jogador 1"), Jogador("Jogador 2")]
jogador_atual = 0
rodada_atual = 1

def lancar_dados():
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    print(f"Dados: ({dado1}, {dado2})")
    return dado1, dado2

def input_aposta():
    # Tenta converter a entrada de texto para um número inteiro
    if cenario.input_text.isdigit():
        valor_aposta = int(cenario.input_text)  # Converte a entrada em um inteiro
    else:
        valor_aposta = 0  # Retorna 0 se a entrada não for um número válido
# Desativa o modo de entrada após obter o valor
    cenario.input_text = ''  # Limpa o campo de texto após a entrada
    return valor_aposta  # Retorna o valor da aposta


def processar_aposta(dado1, dado2, aposta):
    valor_dado1, valor_dado2 = dado1, dado2
    v_dados = valor_dado1, valor_dado2
    pos = pygame.mouse.get_pos()
    casa_tabuleiro, number_col, number_line = cenario.check_click(pos)
    pos_casa = number_col, number_line
    resultado_click = cenario.check_click(pos)
    if resultado_click:
        #cenario.toggle_input()
        if casa_tabuleiro == 4:
            aposta_quadrante(number_line, valor_dado1, valor_dado2, jogador_atual, aposta)
        elif casa_tabuleiro in (5, 6, 7):
            cores = {5: 'azul', 6: 'vermelho', 7: 'verde'}
            aposta_cor(casa_tabuleiro, valor_dado1, valor_dado2, jogador_atual, cores[casa_tabuleiro], aposta)
        else:
            aposta_par_ordenado(v_dados, pos_casa, aposta)
    return None

def aposta_quadrante(linha, dado1, dado2, jogador, aposta):
    jogadores[jogador_atual].fazer_aposta('quadrante', aposta)
    number_line = linha
    v_dado1, v_dado2 = dado1, dado2
    if number_line == 0:
        if v_dado2 > 0 and v_dado2 < 4 and v_dado1 > 3 and v_dado1 < 7:
            jogadores[jogador_atual].ganhar_fichas(aposta * 4)
            print("Venceu, aposta no quadrante 1!!")
    elif number_line == 1:
        if v_dado2 > 0 and v_dado2 < 4 and v_dado1 > 0 and v_dado1 < 4:
            jogadores[jogador_atual].ganhar_fichas(aposta * 4)
            print("Venceu, aposta no quadrante 2!!")
    elif number_line == 2:
        if v_dado2 > 3 and v_dado2 < 7 and v_dado1 > 0 and v_dado1 < 4:
            jogadores[jogador_atual].ganhar_fichas(aposta * 4)
            print("Venceu, aposta no quadrante 3!!")
    elif number_line == 3:
        if v_dado2 > 3 and v_dado2 < 7 and v_dado1 > 3 and v_dado1 < 7:
            jogadores[jogador_atual].ganhar_fichas(aposta * 4)
            print("Venceu, aposta no quadrante 4!!")

def aposta_cor(casa, dado1, dado2, jogador, cor, aposta):
    jogadores[jogador_atual].fazer_aposta(cor, aposta)
    casa_tabuleiro = casa
    v_dado1, v_dado2 = dado1, dado2
    if casa_tabuleiro == 5:
        casa_dado = cenario.tabuleiro[v_dado1][v_dado2]
        if casa_dado == 3:
            jogadores[jogador_atual].ganhar_fichas(aposta * 2)
            print("Venceu com aposta na cor azul!")
    elif casa_tabuleiro == 6:
        casa_dado = cenario.tabuleiro[v_dado1][v_dado2]
        if casa_dado == 1:
            jogadores[jogador_atual].ganhar_fichas(aposta * 3)
            print("Venceu com aposta na cor vermelha!")
    elif casa_tabuleiro == 7:
        casa_dado = cenario.tabuleiro[v_dado1][v_dado2]
        if casa_dado == 2:
            jogadores[jogador_atual].ganhar_fichas(aposta * 5)
            print("Venceu com aposta na cor verde!")
            
def aposta_par_ordenado(v_dados, pos_casa, aposta):
    jogadores[jogador_atual].fazer_aposta('par_ordenado', aposta)
    if v_dados == pos_casa:
        print("Venceu com aposta em par ordenado!")

def alternar_jogador():
    global jogador_atual
    jogador_atual = (jogador_atual + 1) % len(jogadores)

def exibir_info_jogador(screen):
    jogador = jogadores[jogador_atual]
    font = pygame.font.SysFont(None, 40)
    text = font.render(f"{jogador.nome}: {jogador.fichas} fichas", True, BLACK)
    screen.blit(text, (20, HEIGHT - 60))

def mostrar_resultado_rodada(screen):
    jogador = jogadores[jogador_atual]
    font = pygame.font.SysFont(None, 40)
    resultado = font.render(f"Resultado: {jogador.resultado_rodada}", True, BLACK)
    screen.blit(resultado, (20, HEIGHT - 100))

pos = [None, None]
dado1, dado2 = lancar_dados()

# Loop principal do jogo
while True:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP and not cenario.input_active:
            cenario.toggle_input()
            processar_aposta(dado1, dado2, aposta)
        elif event.type == pygame.KEYDOWN and cenario.input_active:
            if event.key == pygame.K_RETURN:
                aposta = input_aposta()
                cenario.toggle_input()
                
                print(f"Aposta recebida: {aposta}")
            elif event.key == pygame.K_BACKSPACE:
                cenario.input_text = cenario.input_text[:-1]
            else:
                cenario.input_text += event.unicode
    # Preenche a tela com cor preta

    # Desenha o tabuleiro e os números
    cenario.paint_board(screen)

    #exibir_info_jogador(screen)
    #mostrar_resultado_rodada(screen)


    if cenario.input_active:
        pygame.draw.rect(screen, BLACK, cenario.input_rect, 2)  # Desenha o retângulo
        font = pygame.font.SysFont(None, 40)
        input_surface = font.render(cenario.input_text, True, BLACK)
        screen.blit(input_surface, (cenario.input_rect.x + 5, cenario.input_rect.y + 5))
    # Atualiza a tela
    pygame.display.flip()