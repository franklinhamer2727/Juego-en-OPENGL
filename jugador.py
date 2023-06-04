import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from balas import Balas, BalasEnemigos

class Jugador(pygame.sprite.Sprite):
    def __init__(self, width, height, grupo_jugador, grupo_balas_jugador):
        super().__init__()  # Llamada al constructor de la clase base
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.grupo_jugador = grupo_jugador
        self.grupo_balas_jugador = grupo_balas_jugador
        self.x = width // 2
        self.y = height - 50
        self.velocidad = 5
        self.vida = 100

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.x > 0:
            self.x -= self.velocidad
        if keys[K_RIGHT] and self.x < self.width - 64:
            self.x += self.velocidad

    def disparar(self):
        bala = Balas(self.x + 32, self.y, self.width, self.height)
        self.grupo_jugador.add(bala)
        self.grupo_balas_jugador.add(bala)

    def dibujar(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)

        glBegin(GL_TRIANGLES)
        glColor3f(1, 1, 1)
        glVertex3f(0, 32, 0)
        glVertex3f(-32, -32, 0)
        glVertex3f(32, -32, 0)
        glEnd()

        glPopMatrix()
