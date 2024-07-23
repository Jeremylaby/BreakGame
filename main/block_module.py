import pygame
from colors import block_color_dict


class block:
    def __init__(self, strenght, x, y, width, height):
        self.strenght = strenght
        # self.x=x
        # self.y=y
        # self.width = width
        # self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.color = block_color_dict[strenght]
