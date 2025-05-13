import pygame
import numpy as np
from blob_base2 import Blob
from stable_baselines3 import PPO
from environement_ppo import BlobEnv

# === CONFIG VISUELLE ===
GRID_SIZE = 20
WIDTH, HEIGHT = 600, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
VIOLET = (138, 43, 226)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Food or Poison - PPO vs Human")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28, bold=True)
small_font = pygame.font.SysFont("arial", 16)

env = BlobEnv()
model = PPO.load("ppo_blob")

# === UI ===
def draw_text_centered(text, y, font_obj=font, color=WHITE):
    label = font_obj.render(text, True, color)
    text_rect = label.get_rect(center=(WIDTH // 2, y))
    win.blit(label, text_rect)

def bouton(x, y, w, h, label, mouse, click):
    rect = pygame.Rect(x, y, w, h)
    survol = rect.collidepoint(mouse)
    pygame.draw.rect(win, YELLOW, rect)
    pygame.draw.rect(win, VIOLET, rect, 3)
    draw_text_centered(label, y + h // 2, font_obj=small_font, color=BLACK)
    return survol and click[0]

def accueil():
    while True:
        win.fill(BLACK)
        draw_text_centered("Bienvenue dans mon jeu Food or Poison", 120)
        draw_text_centered("Créé par Bibata Sombie", 570, font_obj=small_font)

        mx, my = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if bouton(200, 250, 200, 60, "👤 Jouer (Humain)", (mx, my), click):
            return "human"
        if bouton(200, 340, 200, 60, "🤖 Observer (PPO)", (mx, my), click):
            return "ppo"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()

        pygame.display.update()
        clock.tick(30)

# === DESSIN DES ENTITÉS ===
def draw_robot(surface, x, y, size):
    center_x = x * size + size // 2
    center_y = y * size + size // 2
    pygame.draw.circle(surface, GRAY, (center_x, center_y), size // 2)
    pygame.draw.line(surface, BLACK, (center_x, y * size), (center_x, y * size + size), 2)
    pygame.draw.line(surface, BLACK, (x * size, center_y), (x * size + size, center_y), 2)
    pygame.draw.circle(surface, BLACK, (center_x - 5, center_y - 5), 2)
    pygame.draw.circle(surface, BLACK, (center_x + 5, center_y - 5), 2)

def draw_enemy(win, blob):
    x, y = blob.x * GRID_SIZE, blob.y * GRID_SIZE
    center = (x + GRID_SIZE // 2, y + GRID_SIZE // 2)
    pygame.draw.circle(win, RED, center, GRID_SIZE // 2)
    pygame.draw.line(win, BLACK, (x + 5, y + 5), (x + GRID_SIZE - 5, y + GRID_SIZE - 5), 2)
    pygame.draw.line(win, BLACK, (x + GRID_SIZE - 5, y + 5), (x + 5, y + GRID_SIZE - 5), 2)

def draw_food(win, blob):
    x, y = blob.x * GRID_SIZE, blob.y * GRID_SIZE
    center = (x + GRID_SIZE // 2, y + GRID_SIZE // 2)
    pygame.draw.circle(win, GREEN, center, GRID_SIZE // 2)
    pygame.draw.rect(win, (0, 180, 0), (center[0] - 2, y + 2, 4, 6))

def draw_window(player, food, enemy, score, mode):
    win.fill(BLACK)
    draw_food(win, food)
    draw_enemy(win, enemy)
    draw_robot(win, player.x, player.y, GRID_SIZE)
    win.blit(font.render(f"Score: {int(score)}", True, WHITE), (10, 10))
    win.blit(font.render(f"Mode: {'Humain' if mode == 'human' else 'PPO'}", True, WHITE), (10, 50))
    pygame.display.update()

def afficher_message_fin(message, color):
    win.fill(BLACK)
    draw_text_centered(message, HEIGHT // 2, color=color)
    pygame.display.update()
    pygame.time.delay(3000)

# === MAIN GAME LOOP ===
mode = accueil()
running = True
score = 0
episode_num = 1
reward_log = []
food_count = 0
enemy_hits = 0

if mode == "human":
    player = Blob(GRAY, (WIDTH, HEIGHT), GRID_SIZE, GRID_SIZE)
    food = Blob(GREEN, (WIDTH, HEIGHT), GRID_SIZE, GRID_SIZE)
    enemy = Blob(RED, (WIDTH, HEIGHT), GRID_SIZE, GRID_SIZE)
else:
    obs, _ = env.reset()
    player, food, enemy = env.player, env.food, env.enemy

while running:
    clock.tick(10)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    if mode == "human":
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_LEFT]: player.move(x=-1); moved = True
        elif keys[pygame.K_RIGHT]: player.move(x=1); moved = True
        elif keys[pygame.K_UP]: player.move(y=-1); moved = True
        elif keys[pygame.K_DOWN]: player.move(y=1); moved = True

        if moved:
            score -= 1

        if player.Rect.colliderect(food.Rect):
            score += 250
            food_count += 1
            food = Blob(GREEN, (WIDTH, HEIGHT), GRID_SIZE, GRID_SIZE)
        elif player.Rect.colliderect(enemy.Rect):
            score -= 250
            enemy_hits += 1
            enemy = Blob(RED, (WIDTH, HEIGHT), GRID_SIZE, GRID_SIZE)

    else:
        action, _ = model.predict(obs)
        obs, reward, terminated, truncated, _ = env.step(action)
        score += reward
        player, food, enemy = env.player, env.food, env.enemy

        if reward == 250:
            food_count += 1
        elif reward == -250:
            enemy_hits += 1

        if food_count >= 5:
            afficher_message_fin("🎉 Bravo ! 5 nourritures collectées !", GREEN)
            running = False
        elif enemy_hits >= 4:
            afficher_message_fin("💀 Game Over : 4 ennemis touchés !", RED)
            running = False

        if terminated or truncated:
            reward_log.append(score)
            with open("ppo_rewards.txt", "a") as f:
                f.write(f"{episode_num},{score}\n")
            episode_num += 1
            pygame.time.delay(500)
            obs, _ = env.reset()
            score = 0

    draw_window(player, food, enemy, score, mode)

pygame.quit()
