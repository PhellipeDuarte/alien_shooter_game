import pygame
import os
import time 
import random
from collide import collide
from enemy import Enemy
from player import Player
from constants import WIDTH, HEIGHT, WIN, BG

pygame.font.init()

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
