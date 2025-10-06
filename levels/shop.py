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
                elif event.key == pygame.K_ESCAPE:
                    return False  # Escape sale de la tienda
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
        
        # Calcular el ancho necesario basado en el texto más largo
        max_width = 0
        all_texts = options_info + selectable_options
        
        for text in all_texts:
            if text:  # Ignorar líneas vacías
                # Simular el texto con > para opciones seleccionables
                if text in selectable_options:
                    test_text = f"> {text}"
                    try:
                        big_font = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 27)  # Solo 2px más grande que 25
                        text_surface = big_font.render(test_text, True, Colors.WHITE)
                    except:
                        big_font = pygame.font.Font(None, 27)
                        text_surface = big_font.render(test_text, True, Colors.WHITE)
                else:
                    text_surface = font.render(text, True, Colors.WHITE)
                max_width = max(max_width, text_surface.get_width())
        
        # Añadir padding extra
        recuadro_width = max_width + 100  # Padding generoso
        
        # Calcular altura necesaria
        total_lines = len(options_info) + len(selectable_options)
        recuadro_height = total_lines * MenuConfig.OPTION_SPACING + MenuConfig.SECTION_SPACING + 120  # Padding vertical + espacio extra
        
        # Calcular posiciones centradas para el recuadro (más arriba)
        recuadro_x = screen.get_width() // 2 - recuadro_width // 2
        recuadro_y = screen.get_height() // 4 - recuadro_height // 4  # Más arriba que el centro

        # Dibujar borde del recuadro (sin fondo)
        pygame.draw.rect(screen, Colors.LIGHT_GRAY, (recuadro_x, recuadro_y, recuadro_width, recuadro_height), 2)
        
        # Calcular la altura total del contenido (incluyendo el espacio extra entre secciones)
        total_content_height = (len(options_info) + len(selectable_options)) * MenuConfig.OPTION_SPACING + MenuConfig.SECTION_SPACING
        
        # Centrar el contenido verticalmente dentro del recuadro
        content_start_y = recuadro_y + (recuadro_height - total_content_height) // 2
        
        # Mostrar información no seleccionable
        for i, option in enumerate(options_info):
            text_surface = font.render(option, True, Colors.WHITE)
            text_width = text_surface.get_width()
            x = recuadro_x + (recuadro_width - text_width) // 2
            y = content_start_y + i * MenuConfig.OPTION_SPACING
            screen.blit(text_surface, (x, y))
        
        # Espacio extra antes de las opciones seleccionables
        selectable_start_y = content_start_y + len(options_info) * MenuConfig.OPTION_SPACING + MenuConfig.SECTION_SPACING
        
        # Mostrar opciones seleccionables
        for i, option in enumerate(selectable_options):
            if i == selection:
                # Opción seleccionada: color amarillo, entre > < y ligeramente más grande
                color = Colors.YELLOW
                # Crear fuente más grande para la opción seleccionada
                try:
                    big_font = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 27)  # Solo 2px más grande que 25
                except:
                    big_font = pygame.font.Font(None, 27)
                
                # Formatear con el símbolo >
                formatted_text = f"> {option}"
                text_surface = big_font.render(formatted_text, True, color)
                text_width = text_surface.get_width()
                # Si el texto es muy ancho, usar la fuente normal
                if text_width > recuadro_width - 20:
                    text_surface = font.render(formatted_text, True, color)
                    text_width = text_surface.get_width()
                x = recuadro_x + (recuadro_width - text_width) // 2
                y = selectable_start_y + i * MenuConfig.OPTION_SPACING - 2
                screen.blit(text_surface, (x, y))
            else:
                # Opciones no seleccionadas: tamaño normal, color blanco
                color = Colors.WHITE
                text_surface = font.render(option, True, color)
                text_width = text_surface.get_width()
                x = recuadro_x + (recuadro_width - text_width) // 2
                y = selectable_start_y + i * MenuConfig.OPTION_SPACING
                screen.blit(text_surface, (x, y))

        # Dibujar línea de controles debajo del recuadro
        controls_text = "| ↑/↓ seleccionar | Enter entrar | Esc salir |"
        try:
            small_font = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 18)
        except:
            small_font = pygame.font.Font(None, 18)
        
        controls_surface = small_font.render(controls_text, True, Colors.GRAY)
        controls_x = recuadro_x + (recuadro_width - controls_surface.get_width()) // 2
        controls_y = recuadro_y + recuadro_height + 10
        screen.blit(controls_surface, (controls_x, controls_y))

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
                elif event.key == pygame.K_ESCAPE:
                    # Escape sale de la tienda
                    fade_out(screen, TransitionConfig.NORMAL_FADE)
                    running = False
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
