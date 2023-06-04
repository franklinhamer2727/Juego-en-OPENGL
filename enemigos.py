import pygame
import random
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Enemigos(pygame.sprite.Sprite):
    def __init__(self, width, height, grupo_enemigos, grupo_jugador):
        super().__init__()  # Llamada al constructor de la clase base
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.grupo_enemigos = grupo_enemigos
        self.grupo_jugador = grupo_jugador
        self.width = width
        self.height = height
        self.x = random.randint(0, width - 64)
        self.y = random.randint(50, 200)
        self.velocidad = 2

    def update(self):
        self.y += self.velocidad

        if self.y > self.height:
            self.x = random.randint(0, self.width - 64)
            self.y = random.randint(50, 200)

        if pygame.sprite.spritecollide(self, self.grupo_jugador, False):
            self.y = self.height + 100

    def dibujar(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)

        glBegin(GL_QUADS)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(64, 0, 0)
        glVertex3f(64, 64, 0)
        glVertex3f(0, 64, 0)
        glEnd()

        glPopMatrix()
