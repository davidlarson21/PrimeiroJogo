import pygame as pg
import random

ESTADO_MENU = 0
ESTADO_JOGANDO = 1

pg.init()
pg.mixer.init()

LARGURA_TELA = 800
ALTURA_TELA = 600
tela = pg.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pg.display.set_caption("Space Arcade")

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

largura_nave = 90
altura_nave = 90
imagem_nave_original = pg.image.load('./asset/Spaceship.png').convert_alpha()
imagem_nave = pg.transform.scale(imagem_nave_original, (largura_nave, altura_nave))

largura_asteroide = 90
altura_asteroide = 80
imagem_asteroide_original = pg.image.load('./asset/Asteroid.png').convert_alpha()
imagem_asteroide = pg.transform.scale(imagem_asteroide_original, (largura_asteroide, altura_asteroide))

imagem_menu_original = pg.image.load('./asset/GalaxyMenu.jpg').convert()
imagem_menu = pg.transform.scale(imagem_menu_original, (LARGURA_TELA, ALTURA_TELA))

imagem_jogo_original = pg.image.load('./asset/InGameBg.jpg').convert()
imagem_jogo = pg.transform.scale(imagem_jogo_original, (LARGURA_TELA, ALTURA_TELA))

musica_menu = './asset/soundBg.mp3'
musica_jogo = './asset/StarWarsSoundtrack.mp3'

fonte_titulo = pg.font.Font(None, 80)
fonte_botao = pg.font.Font(None, 50)


class Nave(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = imagem_nave
        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA_TELA / 2
        self.rect.bottom = ALTURA_TELA - 10
        self.velocidade = 5

    def update(self, teclas):
        if teclas[pg.K_LEFT]:
            self.rect.x -= self.velocidade
        if teclas[pg.K_RIGHT]:
            self.rect.x += self.velocidade
        if teclas[pg.K_UP]:
            self.rect.y -= self.velocidade
        if teclas[pg.K_DOWN]:
            self.rect.y += self.velocidade

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGURA_TELA:
            self.rect.right = LARGURA_TELA
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > ALTURA_TELA:
            self.rect.bottom = ALTURA_TELA


class Asteroide(pg.sprite.Sprite):
    def __init__(self, x, y, velocidade_asteroide):
        super().__init__()
        self.image = imagem_asteroide
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocidade = velocidade_asteroide

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA_TELA:
            self.kill()


asteroides = pg.sprite.Group()
nave = Nave()
todos_os_sprites = pg.sprite.Group(nave)

velocidade_asteroide_base = 3
ultimo_spawn_asteroide = pg.time.get_ticks()
intervalo_spawn_asteroide = 1500

estado_atual = ESTADO_MENU
botao_rect = pg.Rect(LARGURA_TELA / 2 - 75, ALTURA_TELA / 2 + 50, 150, 50)

pg.mixer.music.load(musica_menu)
pg.mixer.music.play(-1)

clock = pg.time.Clock()
FPS = 60


def resetar_jogo():
    global estado_atual, ultimo_spawn_asteroide
    asteroides.empty()
    nave.rect.centerx = LARGURA_TELA / 2
    nave.rect.bottom = ALTURA_TELA - 10
    ultimo_spawn_asteroide = pg.time.get_ticks()
    estado_atual = ESTADO_MENU

    pg.mixer.music.stop()
    pg.mixer.music.load(musica_menu)
    pg.mixer.music.play(-1)


rodando = True
while rodando:
    clock.tick(FPS)

    for evento in pg.event.get():
        if evento.type == pg.QUIT:
            rodando = False

        if estado_atual == ESTADO_MENU:
            if evento.type == pg.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):
                    estado_atual = ESTADO_JOGANDO

                    pg.mixer.music.stop()
                    pg.mixer.music.load(musica_jogo)
                    pg.mixer.music.play(-1)

    if estado_atual == ESTADO_JOGANDO:
        teclas = pg.key.get_pressed()
        nave.update(teclas)

        agora = pg.time.get_ticks()
        if agora - ultimo_spawn_asteroide > intervalo_spawn_asteroide:
            x_aleatorio = random.randint(0, LARGURA_TELA - largura_asteroide)
            novo_asteroide = Asteroide(x_aleatorio, -altura_asteroide, velocidade_asteroide_base)
            asteroides.add(novo_asteroide)
            ultimo_spawn_asteroide = agora

        asteroides.update()

        if pg.sprite.spritecollideany(nave, asteroides):
            resetar_jogo()

    if estado_atual == ESTADO_MENU:
        tela.blit(imagem_menu, (0, 0))

        titulo_texto = fonte_titulo.render("Space Arcade", True, BRANCO)
        titulo_rect = titulo_texto.get_rect(center=(LARGURA_TELA / 2, ALTURA_TELA / 2 - 50))
        tela.blit(titulo_texto, titulo_rect)

        pg.draw.rect(tela, (50, 50, 50), botao_rect, border_radius=10)
        pg.draw.rect(tela, BRANCO, botao_rect, 2, border_radius=10)

        texto_botao = fonte_botao.render("Play", True, BRANCO)
        texto_botao_rect = texto_botao.get_rect(center=botao_rect.center)
        tela.blit(texto_botao, texto_botao_rect)

    elif estado_atual == ESTADO_JOGANDO:
        tela.blit(imagem_jogo, (0, 0))
        todos_os_sprites.draw(tela)
        asteroides.draw(tela)

    pg.display.flip()

pg.quit()
