import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Explosion:
    def __init__(self, position):
        self.position = position
        self.frame_index = 0
        self.frame_delay = 3
        self.frame_count = 12
        self.frame_width = 64
        self.frame_height = 64
        self.texture = self.load_texture()

    def load_texture(self):
        texture_surface = pygame.image.load('explosion.jpg')
        texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
        width = texture_surface.get_width()
        height = texture_surface.get_height()

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

        return texture_id

    def update(self):
        if self.frame_index < self.frame_count * self.frame_delay:
            self.frame_index += 1

    def draw(self):
        frame = self.frame_index // self.frame_delay
        frame_x = (frame % 4) * self.frame_width
        frame_y = (frame // 4) * self.frame_height

        glPushMatrix()
        glTranslatef(self.position[0] - self.frame_width / 2, self.position[1] - self.frame_height / 2, 0)

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glColor4f(1, 1, 1, 1)

        glBegin(GL_QUADS)
        glTexCoord2f(frame_x / self.frame_width, frame_y / self.frame_height)
        glVertex3f(0, 0, 0)

        glTexCoord2f((frame_x + self.frame_width) / self.frame_width, frame_y / self.frame_height)
        glVertex3f(self.frame_width, 0, 0)

        glTexCoord2f((frame_x + self.frame_width) / self.frame_width, (frame_y + self.frame_height) / self.frame_height)
        glVertex3f(self.frame_width, self.frame_height, 0)

        glTexCoord2f(frame_x / self.frame_width, (frame_y + self.frame_height) / self.frame_height)
        glVertex3f(0, self.frame_height, 0)
        glEnd()

        glDisable(GL_TEXTURE_2D)

        glPopMatrix()

