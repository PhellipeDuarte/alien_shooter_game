import pygame
import os
import time 
import random
pygame.font.init()

# Setando a janela principal
WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Carregando as imagens

# Naves inimigas
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))

# Nave do player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# Lasers atirados pelas naves
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

# Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background_black.png")), (WIDTH, HEIGHT))

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
        return self.y <= height and self.y >= 0

    # Método para verificar se o disparo colide com alguma nave
    def collison(self, obj):
        return collide(obj, self)

# Classe abstrata "Nave"
class Ship:
    def __init__(self, x, y, health=100):
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
    
    # Métodos para receber o tamanho da imagem da nave
    def get_width(self):
        return self.ship_img.get_width()
    
    def get_height(self):
        return self.ship_img.get_height()

# Classe do player, herda da classe abstrata "Nave"
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

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

# Função que analisa as colisões dos projéteis
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    
    return obj1.mask.overlap(obj2, (offset_x, offset_y)) != None

# Definindo o loop principal de execução
def main():
    run = True
    FPS = 300
    level = 0
    lives = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 90)
    player_vel = 4
    enemy_vel = 2

    enemies = []
    wave_lenght = 5

    player = Player(425, 700)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    # Função que atualiza a tela no tempo de clock (300 vezez por segundo)
    def redraw_window():
        WIN.blit(BG, (0, 0))

        # Escrevendo o texto na tela
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        # Desenhando os inimigos na tela
        for enemy in enemies:
            enemy.draw(WIN)
        
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("Você perdeu!!", 1, (255, 255, 255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()


        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS*3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_lenght += 2
            for i in range(wave_lenght):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()

        # Indo para a esquerda
        if keys[pygame.K_a] and player.x + player_vel > 0:
            player.x -= player_vel

        # Indo para a direita
        if keys[pygame.K_d] and player.x + player_vel < WIDTH - player.get_width():
            player.x += player_vel

        # Indo para cima
        if keys[pygame.K_w] and player.y + player_vel > 0:
            player.y -= player_vel

        # Indo para baixo
        if keys[pygame.K_s] and player.y + player_vel < HEIGHT - player.get_height():
            player.y += player_vel

        # Usa o método mover
        for enemy in enemies:
            enemy.move(enemy_vel)
            
            # Condicional que percebe se algum inimigo passou pela nave aliada
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        

main()
