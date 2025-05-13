import pygame
import numpy as np
from blob_base2 import Blob
from stable_baselines3 import PPO
from environement_ppo import BlobEnv

# === CONFIG VISUELLE ===
GRID_SIZE = 40
WIDTH, HEIGHT = 600, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🎥 PPO - Observation Multi-Épisodes")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 28, bold=True)

def draw_robot(surface, x, y, size):
    center_x = x * size + size // 2
    center_y = y * size + size // 2
    pygame.draw.circle(surface, GRAY, (center_x, center_y), size // 2)
    pygame.draw.line(surface, BLACK, (center_x, center_y - size // 2), (center_x, center_y + size // 2), 2)
    pygame.draw.line(surface, BLACK, (center_x - size // 2, center_y), (center_x + size // 2, center_y), 2)
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

def draw_window(player, food, enemy, score, episode):
    win.fill(BLACK)
    draw_food(win, food)
    draw_enemy(win, enemy)
    draw_robot(win, player.x, player.y, GRID_SIZE)
    win.blit(font.render(f"Score: {int(score)}", True, WHITE), (10, 10))
    win.blit(font.render(f"Episode: {episode}", True, WHITE), (10, 50))
    pygame.display.update()

# === CHARGEMENT DU MODÈLE PPO
env = BlobEnv()
model = PPO.load("ppo_blob")

# === BOUCLE DE PLUSIEURS ÉPISODES
NUM_EPISODES = 5
for episode in range(1, NUM_EPISODES + 1):
    obs, _ = env.reset()
    score = 0
    done = False

    while not done:
        clock.tick(8)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); exit()

        action, _ = model.predict(obs)
        obs, reward, terminated, truncated, _ = env.step(action)
        score += reward
        player, food, enemy = env.player, env.food, env.enemy
        draw_window(player, food, enemy, score, episode)

        done = terminated or truncated

    pygame.time.delay(1000)

pygame.quit()
