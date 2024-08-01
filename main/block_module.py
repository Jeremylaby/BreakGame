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
    def update_color(self):
        self.color=block_color_dict[self.strenght]
    def take_hit(self):
        if self.strenght==1:
            return True
        else:
            self.strenght-=1
            self.update_color()