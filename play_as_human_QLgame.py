import pygame
from blob import Blob
import numpy as np
import random

# === Initialisation ===
pygame.init()

# === Constantes ===
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 10
PLAYER_COLOR = (0, 0, 255)
FOOD_COLOR = (0, 255, 0)
ENEMY_COLOR = (255, 0, 0)
FONT = pygame.font.SysFont("comicsans", 30)

# === Récompenses Q-Learning simulées ===
MOVE_PENALTY = 1
FOOD_REWARD = 250
ENEMY_PENALTY = 250

# === Fenêtre ===
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Food or Poison - Mode Humain Q-Rules")
clock = pygame.time.Clock()

# === Création des entités ===
player = Blob(GRID_SIZE)
food = Blob(GRID_SIZE)
enemy = Blob(GRID_SIZE)
score = 0
food_hits = 0
enemy_hits = 0

# === Robot stylisé ===
def draw_robot(surface, x, y, size):
    center_x = x * size + size // 2
    center_y = y * size + size // 2
    pygame.draw.circle(surface, (180, 180, 180), (center_x, center_y), size // 2)
    pygame.draw.line(surface, (0, 0, 0), (center_x, y * size), (center_x, y * size + size), 2)
    pygame.draw.line(surface, (0, 0, 0), (x * size, center_y), (x * size + size, center_y), 2)
    pygame.draw.circle(surface, (0, 0, 0), (center_x - 5, center_y - 5), 2)
    pygame.draw.circle(surface, (0, 0, 0), (center_x + 5, center_y - 5), 2)

# === Affichage ===
def redraw_window():
    win.fill((0, 0, 0))
    pygame.draw.rect(win, FOOD_COLOR, (food.x * GRID_SIZE, food.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(win, ENEMY_COLOR, (enemy.x * GRID_SIZE, enemy.y * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    draw_robot(win, player.x, player.y, GRID_SIZE)
    text = FONT.render(f"Score: {score}", 1, (255, 255, 255))
    win.blit(text, (10, 10))
    pygame.display.update()

# === Boucle principale ===
run = True
while run:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_LEFT]:
        player.move(x=-1, y=0)
        moved = True
    elif keys[pygame.K_RIGHT]:
        player.move(x=1, y=0)
        moved = True
    elif keys[pygame.K_UP]:
        player.move(x=0, y=-1)
        moved = True
    elif keys[pygame.K_DOWN]:
        player.move(x=0, y=1)
        moved = True

    if moved:
        score -= MOVE_PENALTY

    # Vérifications des collisions
    if player.x == food.x and player.y == food.y:
        score += FOOD_REWARD
        food_hits += 1
        print(f"🍏 Nourriture attrapée ! Total = {food_hits} fois")
        food = Blob(GRID_SIZE)  # nouvelle position

    elif player.x == enemy.x and player.y == enemy.y:
        score -= ENEMY_PENALTY
        enemy_hits += 1
        print(f"💀 Ennemi rencontré ! Total = {enemy_hits} fois")
        enemy = Blob(GRID_SIZE)  # nouvelle position

    # Fin de jeu
    if enemy_hits >= 5:
        print("🚫 GAME OVER : Trop d'ennemis rencontrés.")
        run = False

    if food_hits >= 5:
        print("🎉 NIVEAU SUPÉRIEUR ATTEINT !")
        run = False

    redraw_window()

pygame.quit()
