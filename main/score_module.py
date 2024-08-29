import pygame
from config import SCREEN_HEIGHT, SCREEN_WIDTH, SCORE_PADDING, SCORE_LENGTH
class score:
    def __init__(self, screen, score_font, score_color):
        self.screen= screen
        self.score_font = score_font
        self.score_color = score_color
        self.score=0
        self.x= SCREEN_WIDTH - SCORE_PADDING
        self.y = SCORE_PADDING
        self.score_length = SCORE_LENGTH

    def draw(self):
        text = "0"*(self.score_length - len(str(self.score))) + str(self.score)
        img = self.score_font.render( text, True, self.score_color)
        text_width, text_height = img.get_size()
        top_left_position = (self.x - text_width, self.y)
        self.screen.blit(img, top_left_position)
    def update(self, points):
        self.score+=points
    def reset(self):
        self.score=0