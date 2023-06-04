import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from jugador import Jugador
from enemigos import Enemigos
from balas import Balas, BalasEnemigos
from explosion import Explosion

pygame.init()
width, height = 800, 600
window = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption('Juego Space Invaders')

gluPerspective(45, (width / height), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

fondo = pygame.image.load('imagenes/espacio.jpg')
laser_sonido = pygame.mixer.Sound('laser.wav')
explosion_sonido = pygame.mixer.Sound('explosion.wav')
golpe_sonido = pygame.mixer.Sound('golpe.wav')

explosion_list = []
for i in range(1, 13):
    explosion = pygame.image.load(f'explosion/{i}.jpg')
    explosion_list.append(explosion)

run = True
fps = 60
clock = pygame.time.Clock()
score = 0
vida = 100
blanco = (255, 255, 255)
negro = (0, 0, 0)

grupo_jugador = pygame.sprite.Group()
grupo_enemigos = pygame.sprite.Group()
grupo_balas_jugador = pygame.sprite.Group()
grupo_balas_enemigos = pygame.sprite.Group()

player = Jugador(width, height, grupo_jugador, grupo_balas_jugador)
grupo_jugador.add(player)
grupo_balas_jugador.add(player)

for x in range(10):
    enemigo = Enemigos(width, height, grupo_enemigos, grupo_jugador)
    grupo_enemigos.add(enemigo)
    grupo_jugador.add(enemigo)

while run:
    clock.tick(fps)

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

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)

    glPushMatrix()
    glTranslatef(0.0, 0.0, 0)

    grupo_jugador.draw(window)

    colicion1 = pygame.sprite.groupcollide(
        grupo_enemigos, grupo_balas_jugador, True, True
    )
    for i in colicion1:
        score += 10
        enemigo = Enemigos(width, height, grupo_enemigos, grupo_jugador)
        grupo_enemigos.add(enemigo)
        grupo_jugador.add(enemigo)

        explo = Explosion(i.rect.center)
        grupo_jugador.add(explo)
        explosion_sonido.set_volume(0.3)
        explosion_sonido.play()

    colicion2 = pygame.sprite.spritecollide(player, grupo_balas_enemigos, True)
    for j in colicion2:
        player.vida -= 10
        if player.vida <= 0:
            run = False
        explo1 = Explosion(j.rect.center)
        grupo_jugador.add(explo1)
        golpe_sonido.play()

    hits = pygame.sprite.spritecollide(player, grupo_enemigos, False)
    for hit in hits:
        player.vida -= 100
        enemigos = Enemigos(width, height, grupo_enemigos, grupo_jugador)
        grupo_jugador.add(enemigos)
        grupo_enemigos.add(enemigos)
        if player.vida <= 0:
            run = False

    pygame.display.flip()

pygame.quit()
