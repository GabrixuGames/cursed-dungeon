import pygame
from src.others import slow_print, draw_text, resource_path
from src.object.wepons import cargar_armas

def start_game_name(screen, font_text, prompt="Introduce el nombre de tu personaje:"):
    name = ""
    typing = True
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    text_width = len(prompt) * 12.5  # estimated character width used by slow_print
    x = (screen.get_width() - text_width) // 2
    y = screen.get_height()  // 2
    slow_print(screen, font_text, prompt, x, y - 100)

    while typing:
        screen.fill((0, 0, 0))

        # Redraw the prompt after slow_print
        draw_text(screen, font_text, prompt, x, y - 100)

        # Render the name typed so far
        name_surface = font_text.render(name, True, (255, 255, 255))
        name_x = (screen.get_width() - name_surface.get_width()) // 2
        name_y = y - 100 + 40
        screen.blit(name_surface, (name_x, name_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 15:
                        name += event.unicode

        clock.tick(30)

    return name


def start_game_weapons(screen, font_text):
    screen.fill((0, 0, 0))
    pygame.display.flip()

    # Centrar el slow_print
    titulo = "Selecciona tu arma:"
    titulo_width = len(titulo) * 12.5  # estimación del ancho del carácter usado por slow_print
    titulo_x = (screen.get_width() - titulo_width) // 2
    slow_print(screen, font_text, titulo, titulo_x, 100)

    try:
        weapons_list = cargar_armas(resource_path("src/db/weaponsDb.json"))
        if not weapons_list:
            raise ValueError("La lista de armas está vacía o no se pudo cargar.")
    except Exception as e:
        slow_print(screen, font_text, f"Error al cargar armas: {e}", 50, 150)
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()
        exit()

    weapons_show = weapons_list[:4]
    seleccion = 0

    def mostrar_armas():
        screen.fill((0, 0, 0))
        
        # Título centrado (redibujado)
        titulo = "Selecciona tu arma:"
        titulo_surface = font_text.render(titulo, True, (255, 255, 255))
        titulo_x = (screen.get_width() - titulo_surface.get_width()) // 2
        screen.blit(titulo_surface, (titulo_x, 100))
        
        # Opciones de armas centradas
        y_offset = 180
        for i, weapon in enumerate(weapons_show):
            color = (255, 255, 0) if i == seleccion else (255, 255, 255)
            texto = f"{weapon['name']} - Damage: {weapon['damage']} | Speed: {weapon['attack_ratio']}"
            text_surface = font_text.render(texto, True, color)
            text_x = (screen.get_width() - text_surface.get_width()) // 2
            screen.blit(text_surface, (text_x, y_offset + i * 50))
        
        pygame.display.flip()

    seleccionando = True
    while seleccionando:
        mostrar_armas()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(weapons_show)
                elif event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(weapons_show)
                elif event.key == pygame.K_RETURN:
                    seleccionando = False
                    return weapons_show[seleccion]
