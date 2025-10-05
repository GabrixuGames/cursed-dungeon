import pygame
from src.others import slow_print, draw_text, resource_path
from src.object.wepons import cargar_armas
from config import Colors, MenuConfig, DisplayConfig, FontConfig, TransitionConfig

def get_character_name(screen, font_text, prompt="Introduce el nombre de tu personaje:"):
    name = ""
    typing = True
    clock = pygame.time.Clock()
    screen.fill(Colors.BLACK)
    text_width = len(prompt) * FontConfig.ESTIMATED_CHAR_WIDTH  # estimated character width used by slow_print
    x = (screen.get_width() - text_width) // 2
    y = screen.get_height()  // 2
    slow_print(screen, font_text, prompt, x, y - MenuConfig.TITLE_Y_OFFSET)

    while typing:
        screen.fill(Colors.BLACK)

        # Redraw the prompt after slow_print
        draw_text(screen, font_text, prompt, x, y - MenuConfig.TITLE_Y_OFFSET)

        # Render the name typed so far
        name_surface = font_text.render(name, True, Colors.WHITE)
        name_x = (screen.get_width() - name_surface.get_width()) // 2
        name_y = y - MenuConfig.TITLE_Y_OFFSET + MenuConfig.OPTION_SPACING
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
                    if len(name) < MenuConfig.MAX_NAME_LENGTH:
                        name += event.unicode

        clock.tick(MenuConfig.MENU_FPS)

    return name


def select_starting_weapon(screen, font_text):
    screen.fill(Colors.BLACK)
    pygame.display.flip()

    # Centrar el slow_print
    titulo = "Selecciona tu arma:"
    titulo_width = len(titulo) * FontConfig.ESTIMATED_CHAR_WIDTH  # estimación del ancho del carácter usado por slow_print
    titulo_x = (screen.get_width() - titulo_width) // 2
    slow_print(screen, font_text, titulo, titulo_x, MenuConfig.TITLE_Y_OFFSET)

    try:
        weapons_list = cargar_armas(resource_path("src/db/weaponsDb.json"))
        if not weapons_list:
            raise ValueError("La lista de armas está vacía o no se pudo cargar.")
    except Exception as e:
        slow_print(screen, font_text, f"Error al cargar armas: {e}", MenuConfig.MENU_PADDING, MenuConfig.TITLE_Y_OFFSET + MenuConfig.OPTION_SPACING)
        pygame.display.flip()
        pygame.time.wait(TransitionConfig.MESSAGE_DELAY)
        pygame.quit()
        exit()

    weapons_show = weapons_list[:MenuConfig.MAX_WEAPONS_SHOW]
    selection = 0

    def display_weapons():
        screen.fill(Colors.BLACK)
        
        # Título centrado (redibujado)
        titulo = "Selecciona tu arma:"
        titulo_surface = font_text.render(titulo, True, Colors.WHITE)
        titulo_x = (screen.get_width() - titulo_surface.get_width()) // 2
        screen.blit(titulo_surface, (titulo_x, MenuConfig.TITLE_Y_OFFSET))
        
        # Opciones de armas centradas
        y_offset = MenuConfig.WEAPON_SELECTION_Y_OFFSET
        for i, weapon in enumerate(weapons_show):
            color = Colors.YELLOW if i == selection else Colors.WHITE
            texto = f"{weapon['name']} - Damage: {weapon['damage']} | Speed: {weapon['attack_ratio']}"
            text_surface = font_text.render(texto, True, color)
            text_x = (screen.get_width() - text_surface.get_width()) // 2
            screen.blit(text_surface, (text_x, y_offset + i * MenuConfig.WEAPON_OPTION_SPACING))
        
        pygame.display.flip()

    selecting = True
    while selecting:
        display_weapons()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selection = (selection - 1) % len(weapons_show)
                elif event.key == pygame.K_DOWN:
                    selection = (selection + 1) % len(weapons_show)
                elif event.key == pygame.K_RETURN:
                    selecting = False
                    return weapons_show[selection]
