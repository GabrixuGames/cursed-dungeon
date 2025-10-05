import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import pygame
from src.object.wepons import cargar_armas
from src.others import resource_path
from src.others import mostrar_popup

def confirmar_compra(screen, font, mensaje, WINDOW_WIDTH, WINDOW_HEIGHT):
    """Muestra un mensaje de confirmación y espera la respuesta del jugador."""
    opciones = ["Sí", "No"]
    seleccion = 0

    while True:
        screen.fill((0, 0, 0))
        texto = font.render(mensaje, True, (255, 255, 255))
        screen.blit(texto, ((WINDOW_WIDTH - texto.get_width()) // 2, WINDOW_HEIGHT // 3))

        for i, opcion in enumerate(opciones):
            color = (255, 255, 0) if i == seleccion else (255, 255, 255)
            texto_opcion = font.render(opcion, True, color)
            screen.blit(texto_opcion, ((WINDOW_WIDTH - texto_opcion.get_width()) // 2, WINDOW_HEIGHT // 2 + i * 40))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif event.key == pygame.K_RETURN:
                    return seleccion == 0

def shop(mainChar, screen, font, WINDOW_WIDTH, WINDOW_HEIGHT):
    """Show the shop in the Pygame window."""
    try:
        weapons_list = cargar_armas(resource_path("src/db/weaponsDb.json"))
        if not weapons_list:
            raise ValueError("La lista de armas está vacía o no se pudo cargar.")
    except Exception as e:
        mostrar_popup(screen, font, f"Error al cargar armas: {e}", WINDOW_WIDTH, WINDOW_HEIGHT, 500, 150)
        pygame.display.flip()
        pygame.time.wait(2000)
        return False

    random.shuffle(weapons_list)
    weapons_show = weapons_list[:5]
    running = True

    opciones = [
        "¡Bienvenido a la tienda!",
        f"Dinero: {mainChar.getMoney()}",
        "Elige un arma (sustituirá al actual):"
    ]

    for i, weapon in enumerate(weapons_show):
        opciones.append(f"{i + 1}. {weapon['name']} - Daño: {weapon['damage']} | Velocidad: {weapon['attack_ratio']} | Precio: {weapon['price']}")

    opciones.append(f"{len(weapons_show) + 1}. Salir")

    total_height = len(opciones) * 30
    start_y = (screen.get_height() - total_height) // 2

    while running:
        screen.fill((0, 0, 0))
        for i, opcion in enumerate(opciones):
            text_surface = font.render(opcion, True, (255, 255, 255))
            text_width = text_surface.get_width()
            x = (screen.get_width() - text_width) // 2
            y = start_y + i * 40
            screen.blit(text_surface, (x, y))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                if pygame.K_1 <= event.key <= pygame.K_9:
                    selected = event.key - pygame.K_1
                    if 0 <= selected < len(weapons_show):
                        selected_weapon = weapons_show[selected]
                        if mainChar.getMoney() >= selected_weapon['price']:
                            if confirmar_compra(screen, font, f"¿Comprar {selected_weapon['name']} por {selected_weapon['price']}?", WINDOW_WIDTH, WINDOW_HEIGHT):
                                mainChar.setWeapon(selected_weapon)
                                mainChar.setMoney(mainChar.getMoney() - selected_weapon['price'])
                                mostrar_popup(screen, font, f"Has comprado {selected_weapon['name']}.", WINDOW_WIDTH, WINDOW_HEIGHT, 500, 150)
                                pygame.display.flip()
                                pygame.time.wait(2000)
                                running = False
                        else:
                            mostrar_popup(screen, font, "No tienes suficiente dinero.", WINDOW_WIDTH, WINDOW_HEIGHT, 500, 150)
                            pygame.display.flip()
                            pygame.time.wait(2000)
                    elif selected == len(weapons_show):
                        running = False
                        return False
