from config import SCREEN_WIDTH
from main.block_module import block
import pygame
BLOCK_TYPES =3
cols = 6 
rows = 6
class wall():
    def __init__(self):
        self.width = SCREEN_WIDTH//cols
        self.height = 40
    def create_wall(self):
        self.blocks =[]
        for row in rows:
            for col in cols:
                x = col*self.width
                y = row*self.height
                if row<=rows//BLOCK_TYPES:
                    rect = block(3,x,y,self.width,self.height)
                elif row <= (rows//BLOCK_TYPES)*2:
                    rect = block(2,x,y,self.width,self.height)
                else:
                    rect = block(2,x,y,self.width,self.height)
                self.blocks.append(rect)
    def draw_wall(self):
        for block in self.blocks:
            pygame.draw.rect(screen)