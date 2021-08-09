from laser import Laser
from constants import HEIGHT

# Classe abstrata "Nave"
class Ship:
    def __init__(self, x, y, health=100):
        self.COOLDOWN = 60
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    # Método para desenhar a nave na tela
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    # Método para mover os disparos
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    # Método para contar o cooldown dos tiros
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    # Método para reduzir o cooldown dos tiros
    def reduce_cooldown(self):
        self.COOLDOWN = self.COOLDOWN / 3

    # Método para realizar o tiro das naves
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    # Métodos para receber o tamanho da imagem da nave
    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()
