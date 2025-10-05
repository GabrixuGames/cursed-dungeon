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

    slow_print(screen, font_text, "Selecciona tu arma:", 50, 100)

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
    opciones = []

    y_offset = 150
    for i, weapon in enumerate(weapons_show):
        texto = f"{i + 1}. {weapon['name']} - Damage: {weapon['damage']} | Speed: {weapon['attack_ratio']}"
        opciones.append(texto)
        slow_print(screen, font_text, texto, 50, y_offset)
        y_offset += 40

    seleccionando = True
    while seleccionando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                    index = event.key - pygame.K_1
                    seleccionando = False
                    return weapons_show[index]
