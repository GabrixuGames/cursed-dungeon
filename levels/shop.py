import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import pygame
from src.object.weapons import load_weapons
from src.others import resource_path, show_popup, fade_out
from config import Colors, MenuConfig, TransitionConfig
from config import Colors, MenuConfig, TransitionConfig

def confirm_purchase(screen, font, mensaje, WINDOW_WIDTH, WINDOW_HEIGHT):
    """Muestra un mensaje de confirmación y espera la respuesta del jugador."""
    options = ["Sí", "No"]
    selection = 0

    while True:
        screen.fill(Colors.BLACK)
        texto = font.render(mensaje, True, Colors.WHITE)
        screen.blit(texto, ((WINDOW_WIDTH - texto.get_width()) // 2, WINDOW_HEIGHT // 3))

        for i, option in enumerate(options):
            color = Colors.YELLOW if i == selection else Colors.WHITE
            texto_opcion = font.render(option, True, color)
            screen.blit(texto_opcion, ((WINDOW_WIDTH - texto_opcion.get_width()) // 2, WINDOW_HEIGHT // 2 + i * MenuConfig.OPTION_SPACING))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selection = (selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selection = (selection + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    return selection == 0

def shop(main_character, screen, font, WINDOW_WIDTH, WINDOW_HEIGHT):
    """Show the shop in the Pygame window."""
    try:
        weapons_list = load_weapons(resource_path("src/db/weaponsDb.json"))
        if not weapons_list:
            raise ValueError("La lista de armas está vacía o no se pudo cargar.")
    except Exception as e:
        show_popup(screen, font, f"Error al cargar armas: {e}", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
        pygame.display.flip()
        pygame.time.wait(TransitionConfig.MESSAGE_DELAY)
        return False

    random.shuffle(weapons_list)
    weapons_show = weapons_list[:5]
    running = True
    selection = 0

    # Crear las opciones del menú
    options_info = [
        "¡Bienvenido a la tienda!",
        f"Dinero: {main_character.getMoney()}",
        "Elige un arma (sustituirá al actual):"
    ]
    
    selectable_options = []
    for i, weapon in enumerate(weapons_show):
        selectable_options.append(f"{weapon['name']} - Daño: {weapon['damage']} | Velocidad: {weapon['attack_ratio']} | Precio: {weapon['price']}")

    selectable_options.append("Salir")

    def display_shop():
        screen.fill(Colors.BLACK)
        
        # Mostrar información no seleccionable
        y_offset = MenuConfig.MENU_PADDING
        for option in options_info:
            text_surface = font.render(option, True, Colors.WHITE)
            text_width = text_surface.get_width()
            x = (screen.get_width() - text_width) // 2
            screen.blit(text_surface, (x, y_offset))
            y_offset += MenuConfig.OPTION_SPACING
        
        y_offset += MenuConfig.SECTION_SPACING  # Espacio extra antes de las opciones
        
        # Mostrar opciones seleccionables
        for i, option in enumerate(selectable_options):
            color = Colors.YELLOW if i == selection else Colors.WHITE
            text_surface = font.render(option, True, color)
            text_width = text_surface.get_width()
            x = (screen.get_width() - text_width) // 2
            screen.blit(text_surface, (x, y_offset + i * MenuConfig.OPTION_SPACING))

        pygame.display.flip()

    # Mostrar el menú inicial directamente
    display_shop()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selection = (selection - 1) % len(selectable_options)
                    display_shop()
                elif event.key == pygame.K_DOWN:
                    selection = (selection + 1) % len(selectable_options)
                    display_shop()
                elif event.key == pygame.K_RETURN:
                    if selection < len(weapons_show):  # Seleccionó un arma
                        selected_weapon = weapons_show[selection]
                        if main_character.getMoney() >= selected_weapon['price']:
                            if confirm_purchase(screen, font, f"¿Comprar {selected_weapon['name']} por {selected_weapon['price']}?", WINDOW_WIDTH, WINDOW_HEIGHT):
                                main_character.setWeapon(selected_weapon)
                                main_character.setMoney(main_character.getMoney() - selected_weapon['price'])
                                show_popup(screen, font, f"Has comprado {selected_weapon['name']}.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                pygame.display.flip()
                                pygame.time.wait(TransitionConfig.MESSAGE_DELAY)
                                fade_out(screen, TransitionConfig.NORMAL_FADE)
                                running = False
                        else:
                            show_popup(screen, font, "No tienes suficiente dinero.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                            pygame.display.flip()
                            pygame.time.wait(TransitionConfig.MESSAGE_DELAY)
                    else:  # Seleccionó salir
                        fade_out(screen, TransitionConfig.NORMAL_FADE)
                        running = False
                        return False
