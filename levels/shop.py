import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import pygame
from src.object.wepons import cargar_armas
from src.others import resource_path, mostrar_popup, fade_out

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
    seleccion = 0

    # Crear las opciones del menú
    opciones_info = [
        "¡Bienvenido a la tienda!",
        f"Dinero: {mainChar.getMoney()}",
        "Elige un arma (sustituirá al actual):"
    ]
    
    opciones_seleccionables = []
    for i, weapon in enumerate(weapons_show):
        opciones_seleccionables.append(f"{weapon['name']} - Daño: {weapon['damage']} | Velocidad: {weapon['attack_ratio']} | Precio: {weapon['price']}")

    opciones_seleccionables.append("Salir")

    def mostrar_tienda():
        screen.fill((0, 0, 0))
        
        # Mostrar información no seleccionable
        y_offset = 50
        for opcion in opciones_info:
            text_surface = font.render(opcion, True, (255, 255, 255))
            text_width = text_surface.get_width()
            x = (screen.get_width() - text_width) // 2
            screen.blit(text_surface, (x, y_offset))
            y_offset += 40
        
        y_offset += 20  # Espacio extra antes de las opciones
        
        # Mostrar opciones seleccionables
        for i, opcion in enumerate(opciones_seleccionables):
            color = (255, 255, 0) if i == seleccion else (255, 255, 255)
            text_surface = font.render(opcion, True, color)
            text_width = text_surface.get_width()
            x = (screen.get_width() - text_width) // 2
            screen.blit(text_surface, (x, y_offset + i * 40))

        pygame.display.flip()

    # Mostrar el menú inicial directamente
    mostrar_tienda()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones_seleccionables)
                    mostrar_tienda()
                elif event.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones_seleccionables)
                    mostrar_tienda()
                elif event.key == pygame.K_RETURN:
                    if seleccion < len(weapons_show):  # Seleccionó un arma
                        selected_weapon = weapons_show[seleccion]
                        if mainChar.getMoney() >= selected_weapon['price']:
                            if confirmar_compra(screen, font, f"¿Comprar {selected_weapon['name']} por {selected_weapon['price']}?", WINDOW_WIDTH, WINDOW_HEIGHT):
                                mainChar.setWeapon(selected_weapon)
                                mainChar.setMoney(mainChar.getMoney() - selected_weapon['price'])
                                mostrar_popup(screen, font, f"Has comprado {selected_weapon['name']}.", WINDOW_WIDTH, WINDOW_HEIGHT, 500, 150)
                                pygame.display.flip()
                                pygame.time.wait(2000)
                                fade_out(screen, 600)
                                running = False
                        else:
                            mostrar_popup(screen, font, "No tienes suficiente dinero.", WINDOW_WIDTH, WINDOW_HEIGHT, 500, 150)
                            pygame.display.flip()
                            pygame.time.wait(2000)
                    else:  # Seleccionó salir
                        fade_out(screen, 600)
                        running = False
                        return False
