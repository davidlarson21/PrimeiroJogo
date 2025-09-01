import pygame as pg

# Define os estados do jogo como constantes para facilitar a leitura
ESTADO_MENU = 0
ESTADO_JOGANDO = 1

# Inicializa o Pygame e o mixer de som
pg.init()
pg.mixer.init()

# --- Configurações da tela ---
LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pg.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pg.display.set_caption("Space Arcade")

# --- Cores ---
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# --- Carregar Assets (Imagens e Músicas) ---

# Imagens
largura_desejada_nave = 90
altura_desejada_nave = 90

imagem_nave_original = pg.image.load('./asset/Spaceship.png').convert_alpha()
imagem_nave = pg.transform.scale(imagem_nave_original, (largura_desejada_nave, altura_desejada_nave))

imagem_fundo_menu_original = pg.image.load('./asset/GalaxyMenu.jpg').convert()
imagem_fundo_menu = pg.transform.scale(imagem_fundo_menu_original, (LARGURA_TELA, ALTURA_TELA))

imagem_fundo_jogo_original = pg.image.load('./asset/InGameBg.jpg').convert()
imagem_fundo_jogo = pg.transform.scale(imagem_fundo_jogo_original, (LARGURA_TELA, ALTURA_TELA))

# Músicas
musica_menu = './asset/soundBg.mp3'
musica_jogo = './asset/StarWarsSoundtrack.mp3'

# Fontes
fonte_titulo = pg.font.Font(None, 80)  # None usa a fonte padrão, 80 é o tamanho
fonte_botao = pg.font.Font(None, 50)

# --- Atributos do Jogo ---
nave_x = LARGURA_TELA / 2 - largura_desejada_nave / 2
nave_y = ALTURA_TELA - altura_desejada_nave - 10
velocidade_nave = 2

# --- Variáveis de Estado do Jogo e do Botão ---
estado_atual = ESTADO_MENU
botao_rect = pg.Rect(LARGURA_TELA / 2 - 75, ALTURA_TELA / 2 + 50, 150, 50)  # Posição e tamanho do botão

# --- Inicia a música do menu ---
pg.mixer.music.load(musica_menu)
pg.mixer.music.play(-1)  # -1 para tocar em loop

# --- Loop principal do jogo ---
rodando = True
while rodando:
    # --- Processa os eventos ---
    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            rodando = False

        # Lógica do clique do mouse no menu
        if estado_atual == ESTADO_MENU:
            if evento.type == pg.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):
                    estado_atual = ESTADO_JOGANDO

                    # Para a música do menu e começa a do jogo
                    pg.mixer.music.stop()
                    pg.mixer.music.load(musica_jogo)
                    pg.mixer.music.play(-1)

    # --- Lógica do Jogo ---
    if estado_atual == ESTADO_JOGANDO:
        # 1. Captura as teclas pressionadas para mover a nave
        teclas = pg.key.get_pressed()
        if teclas[pg.K_LEFT]:
            nave_x -= velocidade_nave
        if teclas[pg.K_RIGHT]:
            nave_x += velocidade_nave
        if teclas[pg.K_UP]:
            nave_y -= velocidade_nave
        if teclas[pg.K_DOWN]:
            nave_y += velocidade_nave

        # 2. Garante que a nave não saia da tela
        if nave_x < 0:
            nave_x = 0
        if nave_x > LARGURA_TELA - largura_desejada_nave:
            nave_x = LARGURA_TELA - largura_desejada_nave
        if nave_y < 0:
            nave_y = 0
        if nave_y > ALTURA_TELA - altura_desejada_nave:
            nave_y = ALTURA_TELA - altura_desejada_nave

    # --- Desenha na Tela ---

    # Lógica do Menu
    if estado_atual == ESTADO_MENU:
        tela.blit(imagem_fundo_menu, (0, 0))

        # Renderiza e desenha o título
        titulo_texto = fonte_titulo.render("Space Arcade", True, BRANCO)
        titulo_rect = titulo_texto.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2 - 50))
        tela.blit(titulo_texto, titulo_rect)

        # Desenha o botão
        pg.draw.rect(tela, (50, 50, 50), botao_rect, border_radius=10)
        pg.draw.rect(tela, BRANCO, botao_rect, 2, border_radius=10)  # Borda do botão

        # Renderiza e desenha o texto do botão
        texto_botao = fonte_botao.render("Play", True, BRANCO)
        texto_botao_rect = texto_botao.get_rect(center=botao_rect.center)
        tela.blit(texto_botao, texto_botao_rect)

    # Lógica do Jogo
    elif estado_atual == ESTADO_JOGANDO:
        tela.blit(imagem_fundo_jogo, (0, 0))
        tela.blit(imagem_nave, (nave_x, nave_y))

    # --- Atualiza a tela ---
    pg.display.flip()

# Encerra o Pygame
pg.quit()