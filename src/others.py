import os, time, sys, pygame



def slow_print(screen, font_ascii, text, x, y, color=(255, 255, 255)):
    # Inicializa la posición de X
    current_x = x
    for char in text:
        draw_text(screen, font_ascii, char, current_x, y, color)
        pygame.display.flip()
        current_x += font_ascii.size(char)[0]  # Obtener el ancho real del carácter
        time.sleep(0.05)


def resource_path(relative_path):
    """Consigue la ruta absoluta al recurso, funciona empaquetado o no."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def draw_text(screen, font, text, x, y, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def mostrar_popup(screen, font, mensaje, WINDOW_WIDTH, WINDOW_HEIGHT, width=500, height=150):
    # Dibuja un rectángulo semitransparente sobre la pantalla
    popup_surface = pygame.Surface((width, height))
    popup_surface.set_alpha(230)  # Transparencia (0-255)
    popup_surface.fill((30, 30, 30))  # Color del cuadro

    # Borde opcional
    pygame.draw.rect(popup_surface, (255, 255, 255), popup_surface.get_rect(), 2)

    # Renderiza el texto
    text_surface = font.render(mensaje, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))

    popup_surface.blit(text_surface, text_rect)

    # Posición centrada en la pantalla principal
    x = (WINDOW_WIDTH - width) // 2
    y = (WINDOW_HEIGHT - height) // 2
    screen.blit(popup_surface, (x, y))
    pygame.display.update()

    time.sleep(2)  # Pausa para mostrar el mensaje

BACKGROUND = [
    "-----------------------------------------------",
    "                                            ",
    "####  ######    ###########  #####  ### #####",
    " ###   ##  #     #####  ##    ###    #   ### ",
    "           #      ##                      # ",
    "                                            ",
    "                                            ",
    "                                            ",
    "                                            ",
    "                                            ",
    "                                            ",
    "----------------------------------------------",
]

def draw_custom_dungeon(screen, font_ascii, offset):
    screen_width, screen_height = screen.get_size()
    line_height = 20
    background_height = len(BACKGROUND) * line_height
    start_y = (screen_height - background_height) // 2
    for i, line in enumerate(BACKGROUND):
        repeated_line = (line * ((screen_width // len(line)) + 3))
        y_position = start_y + i * line_height
        draw_text(screen, font_ascii, repeated_line, -offset, y_position, (200, 200, 200))