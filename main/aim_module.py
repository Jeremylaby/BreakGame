import pygame
import math
from config import AIM_MIN_ANGLE, AIM_MAX_ANGLE, AIM_SPEED


class aim:
    def __init__(
        self,
        radius,
        start_x,
        start_y,
        screen,
        aim_color,
    ):
        self.radius = radius
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = start_x
        self.end_y = start_y
        self.angle = AIM_MIN_ANGLE
        self.angle_speed = AIM_SPEED
        self.max_angle = AIM_MAX_ANGLE
        self.min_angle = AIM_MIN_ANGLE
        self.screen = screen
        self.aim_color = aim_color

    def draw(self):

        angle_rad = math.radians(self.angle)
        self.end_x = self.start_x + self.radius * math.cos(angle_rad)
        self.end_y = self.start_y + self.radius * math.sin(angle_rad)
        pygame.draw.line(
            self.screen,
            self.aim_color,
            (self.start_x, self.start_y),
            (self.end_x, self.end_y),
            2,
        )

    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.angle -= self.angle_speed
            if self.angle < self.min_angle:
                self.angle = self.min_angle
        elif key[pygame.K_RIGHT]:
            self.angle += self.angle_speed
            if self.angle > self.max_angle:
                self.angle = self.max_angle

    def calculate_speed(self, max_speed):
        angle_rad = math.radians(self.angle)
        speed_y=max_speed* math.sin(angle_rad)
        speed_x = math.cos(angle_rad)*max_speed
        return speed_x,speed_y
