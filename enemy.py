import pygame
from laser import Laser
from ship import Ship
from constants import RED_SPACE_SHIP, RED_LASER, GREEN_SPACE_SHIP, GREEN_LASER, BLUE_SPACE_SHIP, BLUE_LASER

# Classe dos inimigos, herda da classe abstrata "Nave"
class Enemy(Ship):
    COLOR_MAP = {
        "red":(RED_SPACE_SHIP, RED_LASER),
        "green":(GREEN_SPACE_SHIP, GREEN_LASER),
        "blue":(BLUE_SPACE_SHIP, BLUE_LASER),
    }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    # Método que realiza a movimentação do inimigo
    def move(self, vel):
        self.y += vel
    
    # Método que realiza o tiro dos inimigos
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
