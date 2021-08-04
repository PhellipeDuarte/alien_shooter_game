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
        return not(self.y <= height and self.y >= 0)

    # Método para verificar se o disparo colide com alguma nave
    def collision(self, obj):
        return collide(obj, self)

# Classe abstrata "Nave"
class Ship:
    def __init__(self, x, y, health=100):
        self.COOLDOWN = 30
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
    def move_lasers(self, vel , obj):
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

# Classe do player, herda da classe abstrata "Nave"
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

    # Método que desenha a barra de vida do player na tela
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
    
    # Método que mostra a barra de vida do player
    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

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
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

# Função que analisa as colisões dos projéteis
def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

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
    laser_vel = 5

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
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player.x + player_vel > 0:
            player.x -= player_vel

        # Indo para a direita
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player.x + player_vel < WIDTH - player.get_width():
            player.x += player_vel

        # Indo para cima
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.y + player_vel > 0:
            player.y -= player_vel

        # Indo para baixo
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.y + player_vel < HEIGHT - player.get_height():
            player.y += player_vel

        # Clicando espaço para atirar
        if keys[pygame.K_SPACE] or keys[pygame.K_LSHIFT]:
            player.shoot()

        # Usa o método mover
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            # Forma de tiro dos inimigos
            if random.randrange(0, 2*FPS) == 1:
                enemy.shoot()
            
            # Condicional que percebe se algum inimigo colidiu com a nave aliada
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

            # Condicional que percebe se algum inimigo passou pela nave aliada
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)


        player.move_lasers(-laser_vel, enemies)

main()
