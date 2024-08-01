from time import sleep
from config import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    PADDDLE_HEIGHT,
    PADDLE_SPEED,
    BLOCK_TYPES,
    FPS,
    BALL_RADIUS,
    BALL_MAX_SPEED,
    BALL_MIN_SPEED,
    COLLIDE_TRESHOLD,
)
from colors import (
    bg_color,
    paddle_color,
    paddle_outline_color,
    ball_color,
    ball_outline_color,
    main_text_color,
    aim_color,
)
import pygame
from block_module import block
from fonts import game_font
from util import draw_text, draw_text_centered
from aim_module import aim

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()

run = True


cols = 6
rows = 6


class wall:
    def __init__(self):
        self.width = SCREEN_WIDTH // cols
        self.height = 40

    def create_wall(self):
        self.blocks = {}
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
                self.blocks[(x, y)] = brick

    # narazie tak potem to zodyfikuje żeby bloki były mniejsze i użyje vectora 2d w blokach tez

    def draw_wall(self):
        for block in self.blocks.values():
            pygame.draw.rect(screen, block.color, block.rect)
            pygame.draw.rect(screen, bg_color, (block.rect), 2)


class paddle:
    def __init__(self):
        self.height = PADDDLE_HEIGHT
        self.width = SCREEN_WIDTH // 8
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height * 2
        self.speed = PADDLE_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0
    def reset(self):
        self.height = PADDDLE_HEIGHT
        self.width = SCREEN_WIDTH // 8
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height * 2
        self.speed = PADDLE_SPEED
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.direction = 0
    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        elif key[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_color, self.rect)
        pygame.draw.rect(screen, paddle_outline_color, self.rect, 2)


class ball:
    def __init__(self, x, y):
        self.rad = BALL_RADIUS
        self.x = x - BALL_RADIUS
        self.y = y - BALL_RADIUS * 2
        self.rect = pygame.Rect(self.x, self.y, self.rad * 2, self.rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.game_over = 0
        self.max_speed = BALL_MAX_SPEED
        self.min_speed = BALL_MIN_SPEED
    def reset(self, x , y):
        self.rad = BALL_RADIUS
        self.x = x - BALL_RADIUS
        self.y = y - BALL_RADIUS * 2
        self.rect = pygame.Rect(self.x, self.y, self.rad * 2, self.rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.game_over = 0
        self.max_speed = BALL_MAX_SPEED
        self.min_speed = BALL_MIN_SPEED

    def set_speed(self, speed_x, speed_y):
        self.speed_x=speed_x
        self.speed_y=speed_y
    def draw(self):
        pygame.draw.circle(
            screen,
            ball_color,
            (self.rect.x + self.rad, self.rect.y + self.rad),
            self.rad,
        )
        pygame.draw.circle(
            screen,
            ball_outline_color,
            (self.rect.x + self.rad, self.rect.y + self.rad),
            self.rad,
            2,
        )

    def colision_with_paddle(self, paddle):
        if self.rect.colliderect(paddle):
            print(abs(self.rect.bottom - paddle.rect.top))
            if (
                abs(self.rect.bottom - paddle.rect.top) < COLLIDE_TRESHOLD
                and self.speed_y > 0
        
            ):
                print("hej")
                self.speed_x = max(
                    min(abs(self.speed_x + paddle.direction), self.max_speed),
                    self.min_speed,
                ) * (self.speed_x // abs(self.speed_x))
                self.speed_y *= -1
            else:
                self.speed_x *= -1

    def collision_with_wall(self, wall):
        for key in list(wall.keys()):
            block = wall[key]
            if self.rect.colliderect(block):
                if (
                    abs(self.rect.top - block.rect.bottom) < COLLIDE_TRESHOLD
                    and self.speed_y < 0
                ) or (
                    abs(self.rect.bottom - block.rect.top) < COLLIDE_TRESHOLD
                    and self.speed_y > 0
                ):
                    self.speed_y *= -1
                if (
                    abs(self.rect.left - block.rect.right) < COLLIDE_TRESHOLD
                    and self.speed_x < 0
                ) or (
                    abs(self.rect.right - block.rect.left) < COLLIDE_TRESHOLD
                    and self.speed_x > 0
                ):
                    self.speed_x *= -1
                if block.take_hit():
                    del wall[key]
                    del block

    def move(self, paddle, wall):

        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1
        if self.rect.bottom > SCREEN_HEIGHT:
            self.game_over = -1
        self.colision_with_paddle(paddle)
        self.collision_with_wall(wall.blocks)
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if len(wall.blocks) == 0:
            self.game_over = 1
        return self.game_over


player_paddle = paddle()

game_ball = ball(player_paddle.x + player_paddle.width // 2, player_paddle.rect.top)
game_wall = wall()
player_aim = aim(
    100,
    game_ball.rect.x + game_ball.rad,
    game_ball.rect.y + game_ball.rad,
    screen,
    aim_color
)
game_wall.create_wall()
game_start = False
game_over = 0
while run:

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                run = False
                print("Bye")
                break
            case pygame.KEYDOWN:
                if not game_start and event.key == pygame.K_SPACE and game_over==0:
                    game_start = True
                    speed_x,speed_y=player_aim.calculate_speed(game_ball.max_speed)
                    game_ball.set_speed(speed_x,speed_y)
                    print("Start Game")
                elif not game_start and event.key == pygame.K_SPACE:
                    game_ball.reset(player_paddle.x + player_paddle.width // 2, player_paddle.rect.top)
                    player_paddle.reset()
                    game_wall.create_wall()
                    game_over=0
    screen.fill(bg_color)
    game_wall.draw_wall()
    player_paddle.draw()
    game_ball.draw()
    if game_start:
        player_paddle.move()
        game_over = game_ball.move(player_paddle, game_wall)
        if game_over != 0:
            game_start = False
    if game_over == -1:
        draw_text_centered(
            screen,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            "GAME OVER PRESS SPACE TO TRY AGAIN",
            game_font,
            main_text_color,
        )
    elif game_over == 1:
        draw_text_centered(
            screen,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            "YOU WON PRESS SPACE TO PLAY AGAIN",
            game_font,
            main_text_color,
        )
    elif game_over == 0 and not game_start:
        draw_text_centered(
            screen,
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            "PRESS SPACE TO START GAME",
            game_font,
            main_text_color,
        )
        player_aim.move()
        player_aim.draw()

    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
