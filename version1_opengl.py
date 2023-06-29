import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

pygame.init()
pygame.mixer.init()

width = 800
height = 600

fondo = pygame.image.load('imagenes/espacio.jpg')
laser_sonido = pygame.mixer.Sound('laser.wav')
explosion_sonido = pygame.mixer.Sound('explosion.wav')
golpe_sonido = pygame.mixer.Sound('golpe.wav')

explosion_list = []
for i in range(1, 13):
    explosion = pygame.image.load(f'explosion/{i}.png')
    explosion_list.append(explosion)

#window = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Juego Space Invaders')
#glViewport(0, 0, width, height)
glViewport(0, 0, width, height)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, width, height, 0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

run = True
fps = 60
clock = pygame.time.Clock()
score = 0
vida = 100
blanco = (255, 255, 255)
negro = (0, 0, 0)


def texto_puntuacion(frame, text, size, x, y):
    font = pygame.font.SysFont('Small Fonts', size, bold=True)
    text_frame = font.render(text, True, blanco, negro)
    text_rect = text_frame.get_rect()
    text_rect.midtop = (x, y)
    frame.blit(text_frame, text_rect)


def barra_vida(frame, x, y, nivel):
    longitud = 100
    alto = 20
    fill = int((nivel / 100) * longitud)
    border = pygame.Rect(x, y, longitud, alto)
    fill = pygame.Rect(x, y, fill, alto)
    pygame.draw.rect(frame, (255, 0, 55), fill)
    pygame.draw.rect(frame, negro, border, 4)


class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('imagenes/A1.png').convert_alpha()
        pygame.display.set_icon(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.centery = height - 50
        self.velocidad_x = 0
        self.vida = 100

    def update(self):
        self.velocidad_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.velocidad_x = -5
        elif keystate[pygame.K_RIGHT]:
            self.velocidad_x = 5

        self.rect.x += self.velocidad_x
        if self.rect.right > width:
            self.rect.right = width
        elif self.rect.left < 0:
            self.rect.left = 0

    def disparar(self):
        bala = Balas(self.rect.centerx, self.rect.top)
        grupo_jugador.add(bala)
        grupo_balas_jugador.add(bala)
        laser_sonido.play()


class Enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/naves.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1, width - 50)
        self.rect.y = 10
        self.velocidad_y = random.randrange(-5, 20)

    def update(self):
        self.time = random.randrange(-1, pygame.time.get_ticks() // 5000)
        self.rect.x += self.time
        if self.rect.x >= width:
            self.rect.x = 0
            self.rect.y += 50

    def disparar_enemigos(self):
        bala = Balas_enemigos(self.rect.centerx, self.rect.bottom)
        grupo_jugador.add(bala)
        grupo_balas_enemigos.add(bala)
        laser_sonido.play()


class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/B2.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.velocidad = -18

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.bottom < 0:
            self.kill()


class Balas_enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('imagenes/B1.png').convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = random.randrange(10, width)
        self.velocidad_y = 4

    def update(self):
        self.rect.y += self.velocidad_y
        if self.rect.bottom > height:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = explosion_list[0]
        img_scale = pygame.transform.scale(self.image, (20, 20))
        self.rect = img_scale.get_rect()
        self.rect.center = position
        self.time = pygame.time.get_ticks()
        self.velocidad_explo = 30
        self.frames = 0

    def update(self):
        tiempo = pygame.time.get_ticks()
        if tiempo - self.time > self.velocidad_explo:
            self.time = tiempo
            self.frames += 1
            if self.frames == len(explosion_list):
                self.kill()
            else:
                position = self.rect.center
                self.image = explosion_list[self.frames]
                self.rect = self.image.get_rect()
                self.rect.center = position

#Clase para graficar triangulos                
class Triangulo(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad_x, velocidad_y):
        super().__init__()
        self.image = pygame.image.load("imagenes/A1.png")  # Ruta de la imagen de la nave
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        if self.rect.left > width:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = width

        if self.rect.bottom < 0:
            self.rect.top = height
        elif self.rect.top > height:
            self.rect.bottom = 0
# Crear un grupo para los triángulos
grupo_triangulos = pygame.sprite.Group()


class Meteorito(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad_x,velocidad_y):
        super().__init__()
        self.image = pygame.image.load("imagenes/meteorito.png")  # Ruta de la imagen del meteorito
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocidad_y = velocidad_y
        self.velocidad_x = velocidad_x

    def update(self):
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        if self.rect.left > width:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = width

        if self.rect.bottom < 0:
            self.rect.top = height
        elif self.rect.top > height:
            self.rect.bottom = 0
grupo_meteoritos = pygame.sprite.Group()

# Crear instancias de triángulos y agregarlos al grupo
triangulo1 = Triangulo(200, 200, 2, 3)
triangulo2 = Triangulo(400, 300, -4, -2)
triangulo3 = Triangulo(250, 150, 1, 1)
triangulo4 = Triangulo(450, 350, -3, 3)
grupo_triangulos.add(triangulo1, triangulo2,triangulo3,triangulo4)




# Crear instancias de meteoritos y agregarlos al grupo
meteorito1 = Meteorito(200, 200, 2,1)
meteorito2 = Meteorito(400, 300, 3,1)
grupo_meteoritos.add(meteorito1, meteorito2)

#funciones de pygame para el juego
grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()

player = Jugador()
grupo_jugador.add(player)
grupo_balas_jugador.add(player)

for x in range(10):
    enemigo = Enemigos(10, 10)
    grupo_enemigos.add(enemigo)
    grupo_jugador.add(enemigo)

while run:
    clock.tick(fps)
    window.blit(fondo, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.disparar()

    grupo_jugador.update()
    grupo_enemigos.update()
    grupo_balas_jugador.update()
    grupo_balas_enemigos.update()
    grupo_triangulos.update()
    grupo_meteoritos.update()

    grupo_jugador.draw(window)
    #Nueva linea
    grupo_triangulos.draw(window)
    grupo_meteoritos.draw(window)
    # Colisiones: balas_jugador - enemigo
    colision1 = pygame.sprite.groupcollide(grupo_enemigos, grupo_balas_jugador, True, True)
    for i in colision1:
        score += 10
        enemigo.disparar_enemigos()
        enemigo = Enemigos(300, 10)
        grupo_enemigos.add(enemigo)
        grupo_jugador.add(enemigo)

        explo = Explosion(i.rect.center)
        grupo_jugador.add(explo)
        explosion_sonido.set_volume(0.3)
        explosion_sonido.play()
        if score >= 300:
            pygame.init()
            pygame.font.init()
            mensaje_font = pygame.font.SysFont("Comic Sans MS", 50)
            mensaje_texto = mensaje_font.render("!Victoria, lograr puedes.", True, blanco)
            window.blit(mensaje_texto, (width // 2 - mensaje_texto.get_width() // 2, height // 2 - mensaje_texto.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(2000)
            pygame.mixer.music.stop()
            pygame.quit()

    # Colisiones: jugador - balas_enemigo
    colision2 = pygame.sprite.spritecollide(player, grupo_balas_enemigos, True)
    for j in colision2:
        player.vida -= 10
        if player.vida <= 0:
            run = False
            pygame.init()
            pygame.font.init()
            mensaje_font = pygame.font.SysFont("Comic Sans MS", 50)
            mensaje_texto = mensaje_font.render("¡Perdiste, Confía en tus habilidades, confía en la Fuerza.!", True, blanco)
            window.blit(mensaje_texto, (width // 2 - mensaje_texto.get_width() // 2, height // 2 - mensaje_texto.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(2000)
        explo1 = Explosion(j.rect.center)
        grupo_jugador.add(explo1)
        golpe_sonido.play()

    # Colisiones: jugador - enemigo
    hits = pygame.sprite.spritecollide(player, grupo_enemigos, False)
    for hit in hits:
        player.vida -= 100
        enemigos = Enemigos(10, 10)
        grupo_jugador.add(enemigos)
        grupo_enemigos.add(enemigos)
        if player.vida <= 0:
            run = False
            pygame.init()
            pygame.font.init()
            mensaje_font = pygame.font.SysFont("Comic Sans MS", 50)
            mensaje_texto = mensaje_font.render("¡Perdiste!", True, blanco)
            window.blit(mensaje_texto, (width // 2 - mensaje_texto.get_width() // 2, height // 2 - mensaje_texto.get_height() // 2))
            pygame.display.update()
            pygame.time.wait(2000)

    # Resto del código


    # Indicador y Score
    texto_puntuacion(window, ('  SCORE: ' + str(score) + '       '), 30, width - 85, 2)
    barra_vida(window, width - 285, 0, player.vida)

    pygame.display.flip()

pygame.quit()

glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glLoadIdentity()

glBegin(GL_TRIANGLES)
glVertex2f(100, 100)
glVertex2f(200, 100)
glVertex2f(150, 200)
glEnd()

pygame.display.flip()
pygame.time.wait(10)