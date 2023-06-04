import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Balas:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 5

    def update(self):
        self.y -= self.velocidad

    def dibujar(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)

        glBegin(GL_QUADS)
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(8, 0, 0)
        glVertex3f(8, 16, 0)
        glVertex3f(0, 16, 0)
        glEnd()

        glPopMatrix()


class BalasEnemigos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 3

    def update(self):
        self.y += self.velocidad

    def dibujar(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)

        glBegin(GL_QUADS)
        glColor3f(1, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(8, 0, 0)
        glVertex3f(8, 16, 0)
        glVertex3f(0, 16, 0)
        glEnd()

        glPopMatrix()
