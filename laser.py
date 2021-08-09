import pygame
from collide import collide

# Classe Laser que representa os disparos das naves
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    # Método para desenhar o laser na tela
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    # Método para mover o laser na tela
    def move(self, vel):
        self.y += vel

    # Método para verificar se o disparo está fora da tela
    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    # Método para verificar se o disparo colide com alguma nave
    def collision(self, obj):
        return collide(obj, self)
