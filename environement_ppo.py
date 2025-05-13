# environement_ppo.py
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from blob_base2 import Blob

class BlobEnv(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self):
        super().__init__()
        self.size = 15
        self.grid_size = 600
        self.grid_step = self.grid_size // self.size
        self.length = self.grid_step

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(low=-self.size, high=self.size, shape=(4,), dtype=np.int32)

        self.player = None
        self.food = None
        self.enemy = None

    def reset(self, *, seed=None, options=None):
        super().reset(seed=seed)
        self.player = Blob((180, 180, 180), (self.grid_size, self.grid_size), self.grid_step, self.length)
        self.food = Blob((0, 255, 0), (self.grid_size, self.grid_size), self.grid_step, self.length)
        self.enemy = Blob((255, 0, 0), (self.grid_size, self.grid_size), self.grid_step, self.length)

        return self.get_obs(), {}

    def get_obs(self):
        return np.array([
            self.player.x - self.food.x,
            self.player.y - self.food.y,
            self.player.x - self.enemy.x,
            self.player.y - self.enemy.y
        ], dtype=np.int32)

    def step(self, action):
        self.player.action(action)

        reward = -1
        terminated = False

        if self.player.collide(self.food.Rect):
            reward = 250
            terminated = True
        elif self.player.collide(self.enemy.Rect):
            reward = -250
            terminated = True

        return self.get_obs(), reward, terminated, False, {}

    def get_blobs(self):
        return self.player, self.food, self.enemy
