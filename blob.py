import numpy as np

# Ces valeurs doivent être cohérentes avec celles du jeu
WIDTH = 600
HEIGHT = 600
GRID_SIZE = 40

class Blob:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.max_x = WIDTH // grid_size
        self.max_y = HEIGHT // grid_size
        self.x = np.random.randint(0, self.max_x)
        self.y = np.random.randint(0, self.max_y)

    def __str__(self):
        return f"Blob({self.x}, {self.y})"

    def __sub__(self, other):
        return (self.x - other.x, self.y - other.y)

    def move(self, x=False, y=False):
        # Mouvement directionnel ou aléatoire
        if x is False:
            self.x += np.random.randint(-1, 2)
        else:
            self.x += x

        if y is False:
            self.y += np.random.randint(-1, 2)
        else:
            self.y += y

        # Contrainte des bords
        self.x = max(0, min(self.x, self.max_x - 1))
        self.y = max(0, min(self.y, self.max_y - 1))
