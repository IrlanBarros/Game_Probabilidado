import pygame
import sys
import random

pygame.init()

# Definindo a largura e altura da tela
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0)
pygame.display.set_caption("Probabilidado")

# Definindo as cores
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
NUM_RODADAS = 5

REGRAS = [
    "Bem-vindo ao Probabilidado!",
    "Cada jogador começa com 15 fichas.",
    "A cada rodada dois dados secretos (não viciados) são lançados.",
    "O número das faces que saírem nos dados são usados como parâmetro",
    "para o par ordenado, exemplo:",
    "Dado 1: 5; dado 2: 4. O par ordenado então é (5, 4).",
    "Acerte o quadrante, cor ou posição exata dos dados no tabuleiro.",
    "Você pode apostar em quadrantes, cores ou par ordenado.",
    "Quadrantes: Aposte no quadrante onde os dados cairão.",
    "Cores: Aposte na cor da célula selecionada.",
    "Apostar: não clique em nada! Digite a quantiddade de fichas e aperte enter.",
    "Para apostar em quadrante ou cor, aposte nos botões da lateral.",
    "Par ordenado: Aposte nas coordenadas exatas dos dados.",
    "Os ganhos variam conforme a probabilidade do evento e o",
    "numero de fichas apostadas.",
    "Pressione ENTER para continuar."
]

class Jogador:
    def __init__(self, nome):
        self.nome = nome
        self.fichas = 15  # Cada jogador começa com 15 fichas
        self.apostas = {'quadrante': 0, 'vermelho': 0,
                        'verde': 0, 'azul': 0, 'par_ordenado': 0}
        self.num_rodadas = 0

    def fazer_aposta(self, tipo, valor):
        global mensagem_jogo
        self.fichas -= valor
        self.apostas[tipo] += valor
        self.num_rodadas += 1
        mensagem_jogo = f"{self.nome} apostou {valor} fichas em {
            tipo}."           

    def reset_apostas(self):
        self.apostas = {'quadrante': 0, 'vermelho': 0,
                        'verde': 0, 'azul': 0, 'par_ordenado': 0}

    def ganhar_fichas(self, ganho, aposta):
        self.fichas = self.fichas + ganho + aposta
        print(f"{self.nome} ganhou {ganho} fichas. Fichas atuais: {self.fichas}")


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
            [0, 1, 3, 2, 2, 3, 1, 7]  # ,
            # [8, 8, 8, 8, 8, 8, 8, 8]
        ]
        self.input_active = True
        self.input_rect = pygame.Rect(WIDTH - 350, HEIGHT - 400, 200, 50)
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
                # Centraliza na célula
                screen.blit(text, (x + 25, y + self.tamanho // 2 - 10))
                pygame.draw.rect(
                    screen, BLACK, (x, y, self.tamanho + 120, self.tamanho), 1)
                continue
            # Define a cor conforme o valor
            if casa_tabuleiro == 1:
                cor = RED
            elif casa_tabuleiro == 2:
                cor = GREEN
            elif casa_tabuleiro == 3:
                cor = BLUE
            elif casa_tabuleiro in (4, 5, 6, 7):
                pygame.draw.rect(
                    screen, cor, (x, y, self.tamanho + 120, self.tamanho))
                pygame.draw.rect(
                    screen, BLACK, (x, y, self.tamanho + 120, self.tamanho), 1)
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

                # pygame.draw.rect(screen, cor, (x, y, self.tamanho + 120, self.tamanho))
            # Desenha o quadrado colorido
            if casa_tabuleiro != 4:
                pygame.draw.rect(
                    screen, cor, (x, y, self.tamanho, self.tamanho))
                pygame.draw.rect(
                    screen, BLACK, (x, y, self.tamanho, self.tamanho), 1)
                if casa_tabuleiro == 1:
                    pygame.draw.rect(
                        screen, cor, (x, y, self.tamanho, self.tamanho))
                    pygame.draw.rect(
                        screen, BLACK, (x, y, self.tamanho, self.tamanho), 1)
                    font = pygame.font.SysFont(None, 40)
                    if number_line == 2 and number_col == 5:
                        text = font.render(
                            "Q" + str(number_line-1), True, WHITE)
                        screen.blit(text, (x + 25, y + self.tamanho // 2 - 10))
                    if number_line == 2 and number_col == 2:
                        text = font.render("Q" + str(number_line), True, WHITE)
                        screen.blit(text, (x + 25, y + self.tamanho // 2 - 10))
                    if number_line == 5 and number_col == 2:
                        text = font.render(
                            "Q" + str(number_line-2), True, WHITE)
                        screen.blit(text, (x + 25, y + self.tamanho // 2 - 10))
                    if number_line == 5 and number_col == 5:
                        text = font.render(
                            "Q" + str(number_line-1), True, WHITE)
                        screen.blit(text, (x + 25, y + self.tamanho // 2 - 10))
    # Função para desenhar a numeração das colunas

    def draw_column_numbers(self, screen):
        font = pygame.font.SysFont(None, 40)
        # Pula a primeira coluna (coluna das linhas)
        for i in range(1, len(self.tabuleiro[0]) - 1):
            x = i * self.tamanho
            text = font.render(str(i), True, BLACK)
            # Alinhar o texto no centro da célula
            screen.blit(text, (x + self.tamanho // 2 - 10, 30))

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
                    # Apenas casas coloridas e a última coluna são clicáveis
                    if casa_tabuleiro in (4, 5, 6, 7):
                        print(f"Clique em casa ({number_col}, {number_line})")
                        return casa_tabuleiro, number_col, number_line
                # Evitar cliques em casas de numeração (linha 0 ou coluna 0)
                if number_line == 0 or number_col == 0:
                    continue
                # Verifica se o clique está dentro de uma casa colorida
                if x < mouse_x < x + self.tamanho and y < mouse_y < y + self.tamanho:
                    # Apenas casas coloridas e a última coluna são clicáveis
                    if casa_tabuleiro in (1, 2, 3):
                        print(f"Clique em casa ({number_col}, {number_line})")
                        return casa_tabuleiro, number_col, number_line
        return None

    def toggle_input(self):
        self.input_active = not self.input_active
        self.input_text = ''
# Inicializa o cenário com o tamanho adequado
tam = (600 // 7)
cenario = Cenario(tam)
jogadores = [Jogador("Jogador 1"), Jogador("Jogador 2")]
jogador_atual = 0
rodada_atual = 1
mensagem_jogo = "Seja bem vindo ao Probabilidado!"
empate = False

def lancar_dados():
    dado1 = random.randint(1, 6)
    dado2 = random.randint(1, 6)
    print(f"Dados: ({dado1}, {dado2})")
    return dado1, dado2

def input_aposta():
    # Tenta converter a entrada de texto para um número inteiro
    if cenario.input_text.isdigit():
        # Converte a entrada em um inteiro
        valor_aposta = int(cenario.input_text)
    else:
        valor_aposta = 0  # Retorna 0 se a entrada não for um número válido
# Desativa o modo de entrada após obter o valor
    cenario.input_text = ''  # Limpa o campo de texto após a entrada
    return valor_aposta  # Retorna o valor da aposta

def exibir_mensagem(screen, mensagem):
    font = pygame.font.SysFont(None, 30)
    texto_surface = font.render(mensagem, True, BLACK)
    if mensagem == "Seja bem vindo ao Probabilidado!":
        screen.blit(texto_surface, (WIDTH - 390, HEIGHT - 680))
    else:
        screen.blit(texto_surface, (WIDTH - 470, HEIGHT - 680))

def processar_aposta(dado1, dado2, aposta):
    global mensagem_jogo
    valor_dado1, valor_dado2 = dado1, dado2
    v_dados = valor_dado1, valor_dado2
    pos = pygame.mouse.get_pos()
    casa_tabuleiro, number_col, number_line = cenario.check_click(pos)
    pos_casa = number_line, number_col
    resultado_click = cenario.check_click(pos)
    if resultado_click:
        # cenario.toggle_input()
        if casa_tabuleiro == 4:
            aposta_quadrante(number_line, valor_dado1,
                            valor_dado2, jogador_atual, aposta)
            # mensagem_jogo = "Aposta no quadrante realizada!"
        elif casa_tabuleiro in (5, 6, 7):
            cores = {5: 'azul', 6: 'vermelho', 7: 'verde'}
            aposta_cor(casa_tabuleiro, valor_dado1, valor_dado2,
                    jogador_atual, cores[casa_tabuleiro], aposta)
            # mensagem_jogo = f"Aposta na cor {cores[casa_tabuleiro]} realizada!"
        else:
            aposta_par_ordenado(v_dados, pos_casa, aposta)
            # mensagem_jogo = "Aposta no par ordenado realizada!"
    return None

def aposta_quadrante(linha, dado1, dado2, jogador, aposta):
    global mensagem_jogo
    if jogadores[jogador_atual].fichas >= aposta:
        jogadores[jogador_atual].fazer_aposta('quadrante', aposta)
        number_line = linha
        v_dado1, v_dado2 = dado1, dado2
        if number_line == 0:
            if v_dado1 > 0 and v_dado1 < 4 and v_dado2 > 3 and v_dado2 < 7:
                jogadores[jogador_atual].ganhar_fichas(aposta * 3, aposta)
                print("Venceu, aposta no quadrante 1!!")
                mensagem_jogo = "Acertou, aposta no quadrante 1!!"
        elif number_line == 1:
            if v_dado1 > 0 and v_dado1 < 4 and v_dado2 > 0 and v_dado2 < 4:
                jogadores[jogador_atual].ganhar_fichas(aposta * 3, aposta)
                print("Acertou, aposta no quadrante 2!!")
                mensagem_jogo = "Acertou, aposta no quadrante 2!!"
        elif number_line == 2:
            if v_dado1 > 3 and v_dado1 < 7 and v_dado2 > 0 and v_dado2 < 4:
                jogadores[jogador_atual].ganhar_fichas(aposta * 3, aposta)
                print("Acertou, aposta no quadrante 3!!")
                mensagem_jogo = "Acertou, aposta no quadrante 3!!"
        elif number_line == 3:
            if v_dado1 > 3 and v_dado1 < 7 and v_dado2 > 3 and v_dado2 < 7:
                jogadores[jogador_atual].ganhar_fichas(aposta * 3, aposta)
                print("Acertou, aposta no quadrante 4!!")
                mensagem_jogo = "Acertou, aposta no quadrante 4!!"
    else:
        mensagem_jogo = f"{jogadores[jogador_atual].nome} não tem fichas suficientes para apostar {aposta}."

def aposta_cor(casa, dado1, dado2, jogador, cor, aposta):
    global mensagem_jogo
    if jogadores[jogador_atual].fichas >= aposta:
        jogadores[jogador_atual].fazer_aposta(cor, aposta)
        casa_tabuleiro = casa
        v_dado1, v_dado2 = dado1, dado2
        if casa_tabuleiro == 5:
            casa_dado = cenario.tabuleiro[v_dado1][v_dado2]
            if casa_dado == 3:
                jogadores[jogador_atual].ganhar_fichas(aposta, aposta)
                print("Acertou com aposta na cor azul!")
                mensagem_jogo = "Acertou com aposta na cor azul!"
        elif casa_tabuleiro == 6:
            casa_dado = cenario.tabuleiro[v_dado1][v_dado2]
            if casa_dado == 1:
                jogadores[jogador_atual].ganhar_fichas(aposta * 2, aposta)
                print("Acertou com aposta na cor vermelha!")
                mensagem_jogo = "Acertou com aposta na cor vermelha!"
        elif casa_tabuleiro == 7:
            casa_dado = cenario.tabuleiro[v_dado1][v_dado2]
            if casa_dado == 2:
                jogadores[jogador_atual].ganhar_fichas(aposta * 4, aposta)
                print("Acertou com aposta na cor verde!")
                mensagem_jogo = "Acertou com aposta na cor verde!"
    else:
        mensagem_jogo = f"{jogadores[jogador_atual].nome} não tem fichas suficientes para apostar {aposta}."

def aposta_par_ordenado(v_dados, pos_casa, aposta):
    global mensagem_jogo
    if jogadores[jogador_atual].fichas >= aposta:
        jogadores[jogador_atual].fazer_aposta('par_ordenado', aposta)
        if v_dados == pos_casa:
            jogadores[jogador_atual].ganhar_fichas(aposta * 5, aposta)
            print("Acertou com aposta em par ordenado!")
            mensagem_jogo = "Acertou com aposta em par ordenado!"
    else:
        mensagem_jogo = f"{jogadores[jogador_atual].nome} não tem fichas suficientes para apostar {aposta}."

def exibir_vencedor(vencedor, empate):
    while True:
        screen.fill((WHITE))
        font = pygame.font.SysFont(None, 60)
        if not empate:
            texto_vencedor = font.render(f"Parabéns, {vencedor.nome}! Você venceu com {vencedor.fichas} fichas!", True, BLACK)
        else:
            texto_vencedor = font.render(f"{jogadores[0].nome} e {jogadores[1].nome} empataram com {jogadores[0].fichas} fichas!", True, BLACK)
        screen.blit(texto_vencedor, (WIDTH // 2 - texto_vencedor.get_width() // 2, HEIGHT // 2 - 50))

        font_opcoes = pygame.font.SysFont(None, 40)
        opcao_reiniciar = font_opcoes.render("Pressione R para jogar novamente", True, (0, 200, 0))
        opcao_sair = font_opcoes.render("Pressione S para sair", True, (200, 0, 0))
        screen.blit(opcao_reiniciar, (WIDTH // 2 - opcao_reiniciar.get_width() // 2, HEIGHT // 2 + 50))
        screen.blit(opcao_sair, (WIDTH // 2 - opcao_sair.get_width() // 2, HEIGHT // 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reiniciar_jogo()
                    return True  # Reiniciar o jogo
                elif event.key == pygame.K_s:
                    pygame.quit()
                    sys.exit()

def exibir_info_jogador(screen):
    font = pygame.font.SysFont(None, 40)
    for idx, jogador in enumerate(jogadores):
        if idx == 0:
            text = font.render(f"{jogador.nome}:", True, BLUE)
        else:
            text = font.render(f"{jogador.nome}:", True, RED)
        text2 = font.render(f" {jogador.fichas} fichas", True, BLACK)
        screen.blit(text, (20, HEIGHT - 100 + idx * 40))
        screen.blit(text2, (20 + text.get_width(), HEIGHT - 100 + idx * 40))

def exibir_local_aposta(screen):
    font = pygame.font.SysFont(None, 30)
    texto_surface = font.render("Sua aposta aparece aqui:", True, BLACK)
    screen.blit(texto_surface, (WIDTH - 370, HEIGHT - 425))

def exibir_vez_jogador(screen):
    font = pygame.font.SysFont(None, 45)
    if jogador_atual == 0:
        texto_surface = font.render(f"Vez do jogador {jogadores[jogador_atual].nome}", True, BLUE)
    else:
        texto_surface = font.render(f"Vez do jogador {jogadores[jogador_atual].nome}", True, RED)
    screen.blit(texto_surface, (WIDTH - 460, HEIGHT - 300))

pos = [None, None]
dado1, dado2 = lancar_dados()
jogo_comecou = False

def solicitar_nomes():
    nomes = []
    font = pygame.font.SysFont(None, 48)
    input_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 25, 400, 50)
    for i in range(2):
        nome = ""
        while True:
            screen.fill((WHITE))
            text_surface = font.render(f"Insira o nome do Jogador {i + 1}:", True, BLACK)
            screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, HEIGHT // 2 - 100))
            pygame.draw.rect(screen, BLACK, input_rect, 2)
            if i == 0:
                input_surface = font.render(nome, True, BLUE)
            else:
                input_surface = font.render(nome, True, RED)
            screen.blit(input_surface, (input_rect.x + 10, input_rect.y + 10))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        nomes.append(nome.strip() or f"Jogador {i + 1}")
                        break
                    elif event.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    else:
                        nome += event.unicode
            else:
                continue
            break
    return nomes

# Pedir os nomes ao iniciar
nomes_jogadores = solicitar_nomes()
jogadores = [Jogador(nomes_jogadores[0]), Jogador(nomes_jogadores[1])]

def reiniciar_jogo():
    """
    Função para resetar o estado do jogo para o início.
    """
    global jogo_comecou, jogadores, jogador_atual, rodada_atual, mensagem_jogo, dado1, dado2, acabou, nomes_jogadores, empate

    jogo_comecou = False
    nomes_jogadores = solicitar_nomes()
    jogadores = [Jogador(nomes_jogadores[0]), Jogador(nomes_jogadores[1])]
    jogador_atual = 0
    rodada_atual = 1
    mensagem_jogo = "Seja bem vindo ao Probabilidado!"
    dado1, dado2 = lancar_dados()
    empate = False

# Loop principal do jogo
while True:
    # Variáveis de controle do jogo
    screen.fill(WHITE)  # Limpa a tela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Controle da fase inicial (regras)
        if not jogo_comecou:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                jogo_comecou = True  # Transição para iniciar o jogo

        # Controle do jogo ativo
        elif jogo_comecou:
            # Verificar término das rodadas
            if jogadores[0].num_rodadas >= NUM_RODADAS and jogadores[1].num_rodadas >= NUM_RODADAS or jogadores[jogador_atual].fichas == 0:
                vencedor = max(jogadores, key=lambda jogador: jogador.fichas)
                if jogadores[0].fichas == jogadores[1].fichas:
                    empate = True
                    if not exibir_vencedor(vencedor, empate):  # Opção de reinício ou saída
                        break
                else:
                    if not exibir_vencedor(vencedor, empate):  # Opção de reinício ou saída
                        break

            # Processar eventos relacionados ao jogo
            if event.type == pygame.MOUSEBUTTONUP and not cenario.input_active:
                cenario.toggle_input()
                processar_aposta(dado1, dado2, aposta)
                jogador_atual = 0 if jogador_atual == 1 else 1  # Trocar jogador
                dado1, dado2 = lancar_dados()

            elif event.type == pygame.KEYDOWN and cenario.input_active:
                if event.key == pygame.K_RETURN:
                    aposta = input_aposta()
                    cenario.toggle_input()
                    print(f"Aposta recebida: {aposta}")
                elif event.key == pygame.K_BACKSPACE:
                    cenario.input_text = cenario.input_text[:-1]
                else:
                    cenario.input_text += event.unicode

    # Exibição condicional de telas
    if not jogo_comecou:
        # Tela de regras
        font = pygame.font.SysFont(None, 48)
        for i, linha in enumerate(REGRAS):
            texto = font.render(linha, True, BLACK)
            screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, 30 + i * 40))
    else:
        # Tela do jogo
        cenario.paint_board(screen)
        exibir_mensagem(screen, mensagem_jogo)
        exibir_info_jogador(screen)
        exibir_local_aposta(screen)
        exibir_vez_jogador(screen)

        if cenario.input_active:
            pygame.draw.rect(screen, BLACK, cenario.input_rect, 2)  # Retângulo para entrada
            font = pygame.font.SysFont(None, 40)
            input_surface = font.render(cenario.input_text, True, BLACK)
            screen.blit(input_surface, (WIDTH - 270, HEIGHT - 390))

    # Atualiza a tela
    pygame.display.flip()
