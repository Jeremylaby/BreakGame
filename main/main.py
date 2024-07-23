from config import SCREEN_HEIGHT, SCREEN_WIDTH
from colors import bg_color
import pygame
from block_module import block

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout")
run = True


BLOCK_TYPES = 3
cols = 6
rows = 6


class wall:
    def __init__(self):
        self.width = SCREEN_WIDTH // cols
        self.height = 40

    def create_wall(self):
        self.blocks = []
        for row in range(rows):
            for col in range(cols):
                x = col * self.width
                y = row * self.height
                if row < rows // BLOCK_TYPES:
                    brick = block(3, x, y, self.width, self.height)
                elif row < (rows // BLOCK_TYPES) * 2:
                    brick = block(2, x, y, self.width, self.height)
                else:
                    brick = block(1, x, y, self.width, self.height)
                self.blocks.append(brick)

    def draw_wall(self):
        for block in self.blocks:
            pygame.draw.rect(screen, block.color, block.rect)
            pygame.draw.rect(screen, bg_color, (block.rect),2)


wall = wall()
wall.create_wall()
while run:
    screen.fill(bg_color)
    wall.draw_wall()
    pygame.display.flip()
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                run = False
                print("Bye")
                break
pygame.quit()
