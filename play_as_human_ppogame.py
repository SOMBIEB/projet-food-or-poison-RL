import pygame
import numpy as np
from blob_base2 import Blob

# === Paramètres visuels ===
GRID_SIZE = 40
WIDTH, HEIGHT = 600, 600

# === Couleurs utilisées ===
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# === Initialisation de Pygame ===
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Food or Poison - Mode Humain")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28, bold=True)

# === Fonctions d'affichage ===
def draw_robot(surface, x, y, size):
    """Dessine un robot stylisé"""
    center_x = x * size + size // 2
    center_y = y * size + size // 2
    pygame.draw.circle(surface, GRAY, (center_x, center_y), size // 2)
    pygame.draw.line(surface, BLACK, (center_x, center_y - size // 2), (center_x, center_y + size // 2), 2)
    pygame.draw.line(surface, BLACK, (center_x - size // 2, center_y), (center_x + size // 2, center_y), 2)
    pygame.draw.circle(surface, BLACK, (center_x - 5, center_y - 5), 2)
    pygame.draw.circle(surface, BLACK, (center_x + 5, center_y - 5), 2)

def draw_enemy(win, blob):
    """Dessine un ennemi en rouge avec une croix"""
    x, y = blob.x * GRID_SIZE, blob.y * GRID_SIZE
    center = (x + GRID_SIZE // 2, y + GRID_SIZE // 2)
    pygame.draw.circle(win, RED, center, GRID_SIZE // 2)
    pygame.draw.line(win, BLACK, (x + 5, y + 5), (x + GRID_SIZE - 5, y + GRID_SIZE - 5), 2)
    pygame.draw.line(win, BLACK, (x + GRID_SIZE - 5, y + 5), (x + 5, y + GRID_SIZE - 5), 2)

def draw_food(win, blob):
    """Dessine une nourriture en vert avec une tige"""
    x, y = blob.x * GRID_SIZE, blob.y * GRID_SIZE
    center = (x + GRID_SIZE // 2, y + GRID_SIZE // 2)
    pygame.draw.circle(win, GREEN, center, GRID_SIZE // 2)
    pygame.draw.rect(win, (0, 180, 0), (center[0] - 2, y + 2, 4, 6))

def draw_window(player, food, enemy, score):
    """Affiche l'état actuel du jeu"""
    win.fill(BLACK)
    draw_food(win, food)
    draw_enemy(win, enemy)
    draw_robot(win, player.x, player.y, GRID_SIZE)
    win.blit(font.render(f"Score: {int(score)}", True, WHITE), (10, 10))
    win.blit(font.render("Mode: Humain", True, WHITE), (10, 50))
    pygame.display.update()

def draw_text_centered(text, y, font_obj=font, color=WHITE):
    label = font_obj.render(text, True, color)
    text_rect = label.get_rect(center=(WIDTH // 2, y))
    win.blit(label, text_rect)

def afficher_message_fin(message, color):
    win.fill(BLACK)
    draw_text_centered(message, HEIGHT // 2, color=color)
    pygame.display.update()
    pygame.time.delay(3000)

# === Initialisation du jeu ===
player = Blob(GRAY, (WIDTH, HEIGHT), GRID_SIZE, GRID_SIZE)
food = Blob(GREEN, (WIDTH, HEIGHT), GRID_SIZE, GRID_SIZE)
enemy = Blob(RED, (WIDTH, HEIGHT), GRID_SIZE, GRID_SIZE)

score = 0
food_count = 0
enemy_hits = 0
running = True

# === Boucle principale ===
while running:
    clock.tick(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    keys = pygame.key.get_pressed()
    moved = False

    # Déplacement du joueur
    if keys[pygame.K_LEFT]: player.move(x=-1); moved = True
    elif keys[pygame.K_RIGHT]: player.move(x=1); moved = True
    elif keys[pygame.K_UP]: player.move(y=-1); moved = True
    elif keys[pygame.K_DOWN]: player.move(y=1); moved = True

    if moved:
        score -= 1

    # Collisions
    if player.Rect.colliderect(food.Rect):
        score += 250
        food_count += 1
        food = Blob(GREEN, (WIDTH, HEIGHT), GRID_SIZE, GRID_SIZE)

    elif player.Rect.colliderect(enemy.Rect):
        score -= 250
        enemy_hits += 1
        enemy = Blob(RED, (WIDTH, HEIGHT), GRID_SIZE, GRID_SIZE)

    # Affichage
    draw_window(player, food, enemy, score)

    # Conditions de fin de partie
    if food_count >= 5:
        afficher_message_fin("🎉 Bravo ! 5 nourritures collectées !", GREEN)
        running = False
    elif enemy_hits >= 4:
        afficher_message_fin("💀 Game Over : 4 ennemis touchés !", RED)
        running = False

# === Fermeture du jeu ===
pygame.quit()
