import pygame
import numpy as np

class Blob:
    def __init__(self, color, size, step, length):
        self.Size_x = size[0]
        self.Size_y = size[1]
        self.color = color
        self.Step = step  
        self.Length = length  

        self.x = np.random.randint(0, self.Size_x // self.Step)
        self.y = np.random.randint(0, self.Size_y // self.Step)

        self.Rect = pygame.Rect(self.x * self.Step, self.y * self.Step, self.Length, self.Length)

    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)

    def collide(self, other):
        return self.Rect.colliderect(other)

    def action(self, choice):
        if choice == 0:
            self.move(x=-1, y=0)
        elif choice == 1:
            self.move(x=1, y=0)
        elif choice == 2:
            self.move(x=0, y=-1)
        elif choice == 3:
            self.move(x=0, y=1)

    def move(self, x=0, y=0):
        self.x += x
        self.y += y
        self.check_borders()
        self.Rect.x = self.x * self.Step
        self.Rect.y = self.y * self.Step

    def check_borders(self):
        max_x = self.Size_x // self.Step - 1
        max_y = self.Size_y // self.Step - 1
        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))

    def draw(self, Win):
        draw_x = self.x * self.Step
        draw_y = self.y * self.Step

        head = pygame.Rect(draw_x + self.Length // 4, draw_y, self.Length // 2, self.Length // 2)
        body = pygame.Rect(draw_x + self.Length // 3, draw_y + self.Length // 2, self.Length // 3, self.Length // 2)
        
        pygame.draw.rect(Win, self.color, head)
        pygame.draw.rect(Win, self.color, body)
