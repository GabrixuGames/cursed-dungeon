import pygame
from src.others import slow_print, draw_text
from src.object.wepons import cargar_armas
from src.others import resource_path

def start_game_name(screen, font_text, prompt="Introduce el nombre de tu personaje:"):
    nombre = ""
    escribiendo = True
    clock = pygame.time.Clock()
    screen.fill((0, 0, 0))
    text_width = len(prompt) * 12.5  # 15 es el ancho estimado por carácter en slow_print
    x = (screen.get_width() - text_width) // 2
    y = screen.get_height()  // 2
    slow_print(screen, font_text, prompt, x, y - 100)
    prompt_mostrado = True  # Para evitar repetir el slow_print

    while escribiendo:
        screen.fill((0, 0, 0))

        # Redibujar el prompt después del slow_print
        draw_text(screen, font_text, prompt, x, y - 100)

        # Renderizar el nombre escrito hasta ahora
        nombre_surface = font_text.render(nombre, True, (255, 255, 255))
        nombre_x = (screen.get_width() - nombre_surface.get_width()) // 2
        nombre_y = y - 100 + 40
        screen.blit(nombre_surface, (nombre_x, nombre_y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    escribiendo = False
                elif event.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 15:
                        nombre += event.unicode

        clock.tick(30)

    return nombre


def start_game_weapons(screen, font_text):
    screen.fill((0, 0, 0))
    pygame.display.flip()

    slow_print(screen, font_text, "Selecciona tu arma:", 50, 100)

    weapons_list = cargar_armas(resource_path("src\db\weaponsDb.json"))
    weapons_show = weapons_list[:4]
    opciones = []
    
    y_offset = 150
    for i, weapon in enumerate(weapons_show):
        texto = f"{i + 1}. {weapon['name']} - Daño: {weapon['damage']} | Velocidad: {weapon['attack_ratio']}"
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
