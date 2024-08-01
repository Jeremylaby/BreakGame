def draw_text(screen, x, y ,text, font, text_color):
    img = font.render(text, True, text_color)
    screen.blit(img,(x,y))
def draw_text_centered(screen, x, y ,text, font, text_color):

    text_img = font.render(text, True, text_color)
    text_rect = text_img.get_rect(center=(x, y))
    screen.blit(text_img, text_rect)