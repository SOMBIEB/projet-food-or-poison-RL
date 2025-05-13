import pygame
import matplotlib.pyplot as plt
from blob_base import Blob
import numpy as np
import time

# Paramètres globaux
Episodes = 30000
Move_Penalty = 1
Enemy_Penalty = 250
Food_Reward = 250
Eps = 0.95
Eps_Decay = 0.9998
Lr = 0.1
Gamma = 0.95

# Fonction de discrétisation de l'espace
def binning(Size, numsamples):
    Width_chunk = np.linspace(-Size[0], Size[0], numsamples)
    Height_chunk = np.linspace(-Size[1], Size[1], numsamples)
    return Width_chunk, Height_chunk

# Encodage d'un état
def get_discrete_state(state, binning):
    x1_dis = np.digitize(state[0][0], binning[0])
    y1_dis = np.digitize(state[0][1], binning[1])
    x2_dis = np.digitize(state[1][0], binning[0])
    y2_dis = np.digitize(state[1][1], binning[1])
    return ((x1_dis, y1_dis), (x2_dis, y2_dis))

# Création de la Q-table
def create_Q_Table(Width_chunk, Height_chunk):
    print("Creating Q_Table")
    Q_table = {}
    for x1 in range(-len(Width_chunk)+1, len(Width_chunk)+1):
        for y1 in range(-len(Height_chunk)+1, len(Height_chunk)+1):
            for x2 in range(-len(Width_chunk)+1, len(Width_chunk)+1):
                for y2 in range(-len(Height_chunk)+1, len(Height_chunk)+1):
                    Q_table[((x1, y1), (x2, y2))] = [np.random.uniform(-5, 0) for _ in range(4)]
    print("Q_Table created")
    return Q_table

# Courbe de récompenses
def plot(moving_avg):
    plt.plot(range(len(moving_avg)), moving_avg)
    plt.ylabel("reward")
    plt.xlabel("episode")
    plt.show()

# Entraînement Q-Learning
def QLearning(Win, Q_table, Episodes, Size, colors, Width_chunk, Height_chunk, launched):
    global Eps

    if launched:
        return

    Eps_rewards = []
    show = False
    Win.fill((0, 0, 0))  # fond noir

    for episode in range(Episodes):
        Player = Blob(colors["blue"], Size, Size[0]//15, 15)
        Enemy = Blob(colors["red"], Size, Size[0]//15, 15)
        Food = Blob(colors["green"], Size, Size[0]//15, 15)
        Ep_rewards = 0

        if episode % 20 == 0:
            print(f"ep : {episode}")
            print(f"ep mean : {np.mean(Eps_rewards[-20:]) if len(Eps_rewards) >= 20 else 0}")
            show = True
        else:
            show = False

        for _ in range(200):
            obs = (Player - Food, Player - Enemy)
            obs_dis = get_discrete_state(obs, (Width_chunk, Height_chunk))

            if np.random.random() > Eps:
                action = np.argmax(Q_table[obs_dis])
            else:
                action = np.random.randint(0, 4)

            Player.action(action)

            if Player.collide(Enemy.Rect):
                reward = -Enemy_Penalty
            elif Player.collide(Food.Rect):
                reward = Food_Reward
            else:
                reward = -Move_Penalty

            new_obs = (Player - Food, Player - Enemy)
            new_obs_dis = get_discrete_state(new_obs, (Width_chunk, Height_chunk))

            max_future_q = np.max(Q_table[new_obs_dis])
            current_q = Q_table[obs_dis][action]

            if reward in [Food_Reward, -Enemy_Penalty]:
                new_q = reward
            else:
                new_q = (1 - Lr) * current_q + Lr * (reward + Gamma * max_future_q)

            Q_table[obs_dis][action] = new_q

            if show:
                Win.fill((0, 0, 0))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                draw_enemy(Win, Enemy)
                draw_food(Win, Food)
                draw_robot(Win, Player)
                pygame.display.update()
                time.sleep(0.1)

            Ep_rewards += reward
            if reward in [Food_Reward, -Enemy_Penalty]:
                break

        Eps_rewards.append(Ep_rewards)
        Eps *= Eps_Decay

    moving_avg = np.convolve(Eps_rewards, np.ones(100) / 100, mode="valid")
    plot(moving_avg)

# === Fonctions graphiques personnalisées ===

def draw_robot(surface, blob):
    x, y, size = blob.x, blob.y, blob.Length
    center_x = x + size // 2
    center_y = y + size // 2

    pygame.draw.circle(surface, (180, 180, 180), (center_x, center_y), size // 2)
    pygame.draw.line(surface, (0, 0, 0), (center_x, y), (center_x, y + size), 2)
    pygame.draw.line(surface, (0, 0, 0), (x, center_y), (x + size, center_y), 2)
    pygame.draw.circle(surface, (0, 0, 0), (center_x - 5, center_y - 5), 2)
    pygame.draw.circle(surface, (0, 0, 0), (center_x + 5, center_y - 5), 2)

def draw_food(surface, blob):
    x, y, size = blob.x, blob.y, blob.Length
    pygame.draw.circle(surface, (0, 255, 0), (x + size // 2, y + size // 2), size // 2)
    pygame.draw.rect(surface, (0, 180, 0), (x + size // 2 - 2, y + 2, 4, 6))

def draw_enemy(surface, blob):
    x, y, size = blob.x, blob.y, blob.Length
    pygame.draw.circle(surface, (255, 0, 0), (x + size // 2, y + size // 2), size // 2)
    pygame.draw.line(surface, (0, 0, 0), (x + 5, y + 5), (x + size - 5, y + size - 5), 2)
    pygame.draw.line(surface, (0, 0, 0), (x + size - 5, y + 5), (x + 5, y + size - 5), 2)
