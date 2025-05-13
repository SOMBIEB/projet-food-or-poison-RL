import pygame
pygame.init()

from blob_base import Blob
from train_qlearning import QLearning, binning, create_Q_Table, Episodes

colors = {"blue": (180, 180, 180), "red": (255, 0, 0), "green": (0, 255, 0)}  # MàJ couleurs

Size = (600, 600)
Win = pygame.display.set_mode(Size)
pygame.display.set_caption("Food or Poison - Q-learning Observation")

def main(Win, Size, colors):
    run = True
    Width_chunk, Height_chunk = binning(Size, 15)
    Q_Table = create_Q_Table(Width_chunk, Height_chunk)
    launched = False

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                quit()

        if not launched:
            QLearning(Win, Q_Table, Episodes, Size, colors, Width_chunk, Height_chunk, launched)
            launched = True

main(Win, Size, colors)
