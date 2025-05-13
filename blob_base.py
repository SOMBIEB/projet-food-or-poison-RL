import pygame
import numpy as np

class Blob:
    def __init__(self, color, size, step, length):
        self.Size_x = size[0]
        self.Size_y = size[1]
        self.color = color
        self.Step = step
        self.Length = length
        self.x = np.random.randint(0, self.Size_x)
        self.y = np.random.randint(0, self.Size_y)
        self.Rect = pygame.Rect(self.x, self.y, self.Length, self.Length)

    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)

    def collide(self, other):
        return self.Rect.colliderect(other)

    def action(self, choice):
        if choice == 0:
            self.move(-self.Step, 0)
        elif choice == 1:
            self.move(self.Step, 0)
        elif choice == 2:
            self.move(0, -self.Step)
        elif choice == 3:
            self.move(0, self.Step)

    def move(self, x=False, y=False):
        if not x:
            self.x += np.random.randint(-self.Step, 2 * self.Step)
        else:
            self.x += x

        if not y:
            self.y += np.random.randint(-self.Step, 2 * self.Step)
        else:
            self.y += y

        self.check_borders()
        self.Rect.x = self.x
        self.Rect.y = self.y

    def check_borders(self):
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0
        if self.x > self.Size_x - self.Length:
            self.x = self.Size_x - self.Length
        if self.y > self.Size_y - self.Length:
            self.y = self.Size_y - self.Length

    def draw(self, Win):
        # Robot stylisé en traits simples
        head = pygame.Rect(self.x + self.Length // 4, self.y, self.Length // 2, self.Length // 2)
        body = pygame.Rect(self.x + self.Length // 3, self.y + self.Length // 2, self.Length // 3, self.Length // 2)
        pygame.draw.rect(Win, self.color, head)   # tête
        pygame.draw.rect(Win, self.color, body)   # corps
