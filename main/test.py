import pygame
import math

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Line Around Circle")
background_color = (255, 255, 255)
line_color = (0, 0, 0)

# Parametry okręgu
center_x = SCREEN_WIDTH // 2
center_y = SCREEN_HEIGHT // 2
radius = 100

# Parametry linii
line_length = 150

# Kąt początkowy
angle = 0

# Prędkość kątowa
angle_speed = 0.05

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Wypełnienie tła
    screen.fill(background_color)

    # Obliczanie końcowych punktów linii
    end_x = center_x + radius * math.cos(angle)
    end_y = center_y + radius * math.sin(angle)

    # Rysowanie linii
    pygame.draw.line(screen, line_color, (center_x, center_y), (end_x, end_y), 2)

    # Aktualizacja wyświetlacza
    pygame.display.flip()

    # Aktualizacja kąta
    angle += angle_speed

    # Ograniczenie prędkości odświeżania
    pygame.time.Clock().tick(60)

pygame.quit()