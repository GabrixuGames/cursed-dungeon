import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
import pygame
from src.object.weapons import load_weapons
from src.object.item import load_items
from src.inventory_system import get_inventory_manager
from src.others import resource_path, show_popup, fade_out
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
    """
    Show the shop in the Pygame window with tabs for Weapons and Items.
    
    Args:
        main_character: MainCharacter instance
        screen: Pygame screen
        font: Pygame font
        WINDOW_WIDTH: Window width
        WINDOW_HEIGHT: Window height
    """
    # Cargar armas
    try:
        weapons_list = load_weapons(resource_path("src/db/weaponsDb.json"))
        if not weapons_list:
            raise ValueError("La lista de armas está vacía o no se pudo cargar.")
    except Exception as e:
        show_popup(screen, font, f"Error al cargar armas: {e}", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
        pygame.display.flip()
        pygame.time.wait(TransitionConfig.MESSAGE_DELAY)
        return False
    
    # Cargar items
    try:
        items_db = load_items(resource_path("src/db/itemsDb.json"))
        if not items_db:
            raise ValueError("La lista de items está vacía o no se pudo cargar.")
        # Convertir dict a lista para mostrar
        items_list = list(items_db.values())
    except Exception as e:
        show_popup(screen, font, f"Error al cargar items: {e}", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
        pygame.display.flip()
        pygame.time.wait(TransitionConfig.MESSAGE_DELAY)
        items_list = []
    
    # Inicializar inventario si no existe
    if not hasattr(main_character, 'inventory_manager') or main_character.inventory_manager is None:
        main_character.inventory_manager = get_inventory_manager()
        try:
            main_character.inventory_manager.load_item_database()
        except:
            pass
    
    # Estado de la tienda
    current_tab = 0  # 0 = Armas, 1 = Items
    tabs = ["Armas", "Items"]
    running = True
    selection = 0
    
    # Preparar armas para mostrar
    random.shuffle(weapons_list)
    weapons_show = weapons_list[:5]
    
    # Preparar items para mostrar (solo items comunes y poco comunes, aleatorio)
    common_items = [item for item in items_list if item.rarity in ["common", "uncommon"]]
    random.shuffle(common_items)
    items_show = common_items[:8]  # Mostrar 8 items

    
    def display_shop():
        """Renderiza la tienda con pestañas y contenido."""
        screen.fill(Colors.BLACK)
        
        # Dibujar pestañas en la parte superior
        tab_width = 150
        tab_height = 40
        tab_y = 50
        tab_start_x = (WINDOW_WIDTH - (len(tabs) * tab_width + 20)) // 2
        
        for i, tab in enumerate(tabs):
            tab_x = tab_start_x + i * (tab_width + 20)
            tab_color = Colors.YELLOW if i == current_tab else Colors.DARK_GRAY
            border_color = Colors.WHITE if i == current_tab else Colors.LIGHT_GRAY
            
            # Dibujar fondo de pestaña
            pygame.draw.rect(screen, tab_color, (tab_x, tab_y, tab_width, tab_height))
            pygame.draw.rect(screen, border_color, (tab_x, tab_y, tab_width, tab_height), 2)
            
            # Dibujar texto de pestaña
            tab_text = font.render(tab, True, Colors.BLACK if i == current_tab else Colors.WHITE)
            text_x = tab_x + (tab_width - tab_text.get_width()) // 2
            text_y = tab_y + (tab_height - tab_text.get_height()) // 2
            screen.blit(tab_text, (text_x, text_y))
        
        # Información del jugador
        info_y = tab_y + tab_height + 20
        money_text = font.render(f"Dinero: {main_character.getMoney()} oro", True, Colors.WHITE)
        screen.blit(money_text, (50, info_y))
        
        # Mostrar slots de inventario
        inv_slots = main_character.inventory_manager.get_total_slots_used()
        inv_max = main_character.inventory_manager.max_slots
        inv_text = font.render(f"Inventario: {inv_slots}/{inv_max}", True, Colors.WHITE)
        screen.blit(inv_text, (WINDOW_WIDTH - inv_text.get_width() - 50, info_y))
        
        # Área de contenido
        content_y = info_y + 50
        
        if current_tab == 0:  # Pestaña de Armas
            display_weapons_tab(content_y)
        else:  # Pestaña de Items
            display_items_tab(content_y)
        
        # Controles
        controls_text = "| ←/→ cambiar pestaña | ↑/↓ seleccionar | Enter comprar | Esc salir |"
        try:
            small_font = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 18)
        except:
            small_font = pygame.font.Font(None, 18)
        
        controls_surface = small_font.render(controls_text, True, Colors.GRAY)
        controls_x = (WINDOW_WIDTH - controls_surface.get_width()) // 2
        controls_y = WINDOW_HEIGHT - 30
        screen.blit(controls_surface, (controls_x, controls_y))
        
        pygame.display.flip()
    
    def display_weapons_tab(start_y):
        """Muestra la pestaña de armas."""
        title = font.render("Armas Disponibles:", True, Colors.WHITE)
        screen.blit(title, ((WINDOW_WIDTH - title.get_width()) // 2, start_y))
        
        # Crear lista de opciones
        selectable_options = []
        for weapon in weapons_show:
            selectable_options.append(f"{weapon['name']} - Daño: {weapon['damage']} | Vel: {weapon['attack_ratio']} | {weapon['price']} oro")
        selectable_options.append("Volver")
        
        # Mostrar opciones
        option_y = start_y + 50
        for i, option in enumerate(selectable_options):
            if i == selection:
                color = Colors.YELLOW
                try:
                    big_font = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 27)
                except:
                    big_font = pygame.font.Font(None, 27)
                formatted_text = f"> {option}"
                text_surface = big_font.render(formatted_text, True, color)
            else:
                color = Colors.WHITE
                text_surface = font.render(option, True, color)
            
            text_x = (WINDOW_WIDTH - text_surface.get_width()) // 2
            screen.blit(text_surface, (text_x, option_y + i * 40))
    
    def display_items_tab(start_y):
        """Muestra la pestaña de items."""
        # Dividir en dos columnas: Tienda | Inventario
        col_width = WINDOW_WIDTH // 2
        
        # Columna izquierda: Items en venta
        left_title = font.render("Items en Venta:", True, Colors.WHITE)
        screen.blit(left_title, (col_width // 4, start_y))
        
        # Columna derecha: Inventario del jugador
        right_title = font.render("Tu Inventario:", True, Colors.WHITE)
        screen.blit(right_title, (col_width + col_width // 4, start_y))
        
        # Línea divisoria vertical
        pygame.draw.line(screen, Colors.LIGHT_GRAY, (col_width, start_y + 30), (col_width, WINDOW_HEIGHT - 60), 2)
        
        # Crear lista de opciones
        selectable_options = []
        for item in items_show:
            selectable_options.append(f"{item.get_display_name()} - {item.price} oro")
        selectable_options.append("Volver")
        
        # Mostrar items en venta
        option_y = start_y + 50
        for i, option in enumerate(selectable_options):
            if i == selection:
                color = Colors.YELLOW
                try:
                    big_font = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 27)
                except:
                    big_font = pygame.font.Font(None, 27)
                formatted_text = f"> {option}"
                text_surface = big_font.render(formatted_text, True, color)
                
                # Mostrar descripción del item seleccionado
                if i < len(items_show):
                    selected_item = items_show[i]
                    try:
                        desc_font = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 20)
                    except:
                        desc_font = pygame.font.Font(None, 20)
                    desc_text = desc_font.render(selected_item.description, True, Colors.GRAY)
                    screen.blit(desc_text, (50, option_y + len(selectable_options) * 40 + 20))
            else:
                color = Colors.WHITE
                text_surface = font.render(option, True, color)
            
            screen.blit(text_surface, (50, option_y + i * 40))
        
        # Mostrar inventario del jugador en la columna derecha
        player_items = main_character.inventory_manager.get_all_items()
        inv_y = option_y
        
        if not player_items:
            empty_text = font.render("(vacío)", True, Colors.GRAY)
            screen.blit(empty_text, (col_width + 50, inv_y))
        else:
            for item, quantity in player_items[:10]:  # Mostrar primeros 10
                item_text = font.render(f"{item.get_display_name()} x{quantity}", True, Colors.WHITE)
                screen.blit(item_text, (col_width + 50, inv_y))
                inv_y += 35
            
            if len(player_items) > 10:
                more_text = font.render(f"... y {len(player_items) - 10} más", True, Colors.GRAY)
                screen.blit(more_text, (col_width + 50, inv_y))

    # Crear las opciones del menú (legacy - ya no se usa)
    options_info = [
        "¡Bienvenido a la tienda!",
        f"Dinero: {main_character.getMoney()}",
        "Elige un arma (sustituirá al actual):"
    ]
    
    selectable_options = []
    for i, weapon in enumerate(weapons_show):
        selectable_options.append(f"{weapon['name']} - Daño: {weapon['damage']} | Velocidad: {weapon['attack_ratio']} | Precio: {weapon['price']}")

    selectable_options.append("Salir")

    def display_shop_legacy():
        """Legacy display function - deprecated"""
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
                # Cambiar de pestaña
                if event.key == pygame.K_LEFT:
                    current_tab = (current_tab - 1) % len(tabs)
                    selection = 0  # Reset selection
                    display_shop()
                elif event.key == pygame.K_RIGHT:
                    current_tab = (current_tab + 1) % len(tabs)
                    selection = 0  # Reset selection
                    display_shop()
                # Navegación en la pestaña actual
                elif event.key == pygame.K_UP:
                    if current_tab == 0:  # Armas
                        max_options = len(weapons_show) + 1  # +1 por "Volver"
                    else:  # Items
                        max_options = len(items_show) + 1
                    selection = (selection - 1) % max_options
                    display_shop()
                elif event.key == pygame.K_DOWN:
                    if current_tab == 0:  # Armas
                        max_options = len(weapons_show) + 1
                    else:  # Items
                        max_options = len(items_show) + 1
                    selection = (selection + 1) % max_options
                    display_shop()
                elif event.key == pygame.K_ESCAPE:
                    # Escape sale de la tienda
                    fade_out(screen, TransitionConfig.NORMAL_FADE)
                    running = False
                elif event.key == pygame.K_RETURN:
                    # Procesar compra según la pestaña
                    if current_tab == 0:  # Armas
                        if selection < len(weapons_show):
                            selected_weapon = weapons_show[selection]
                            if main_character.getMoney() >= selected_weapon['price']:
                                if confirm_purchase(screen, font, f"¿Comprar {selected_weapon['name']} por {selected_weapon['price']}?", WINDOW_WIDTH, WINDOW_HEIGHT):
                                    main_character.setWeapon(selected_weapon)
                                    main_character.setMoney(main_character.getMoney() - selected_weapon['price'])
                                    show_popup(screen, font, f"Has comprado {selected_weapon['name']}.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                    pygame.display.flip()
                                    pygame.time.wait(TransitionConfig.MESSAGE_DELAY)
                                    display_shop()
                            else:
                                show_popup(screen, font, "No tienes suficiente dinero.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                pygame.display.flip()
                                pygame.time.wait(TransitionConfig.MESSAGE_DELAY)
                                display_shop()
                        else:  # Volver
                            fade_out(screen, TransitionConfig.NORMAL_FADE)
                            running = False
                    
                    else:  # Items
                        if selection < len(items_show):
                            selected_item = items_show[selection]
                            if main_character.getMoney() >= selected_item.price:
                                # Verificar si hay espacio en el inventario
                                if main_character.inventory_manager.is_full() and not main_character.inventory_manager.has_item(selected_item.id):
                                    show_popup(screen, font, "Inventario lleno.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                    pygame.display.flip()
                                    pygame.time.wait(TransitionConfig.MESSAGE_DELAY)
                                    display_shop()
                                else:
                                    if confirm_purchase(screen, font, f"¿Comprar {selected_item.name} por {selected_item.price}?", WINDOW_WIDTH, WINDOW_HEIGHT):
                                        success, msg = main_character.inventory_manager.add_item(selected_item.id, 1)
                                        if success:
                                            main_character.setMoney(main_character.getMoney() - selected_item.price)
                                            show_popup(screen, font, f"Has comprado {selected_item.name}.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                        else:
                                            show_popup(screen, font, msg, WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                        pygame.display.flip()
                                        pygame.time.wait(TransitionConfig.MESSAGE_DELAY)
                                        display_shop()
                            else:
                                show_popup(screen, font, "No tienes suficiente dinero.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                pygame.display.flip()
                                pygame.time.wait(TransitionConfig.MESSAGE_DELAY)
                                display_shop()
                        else:  # Volver
                            fade_out(screen, TransitionConfig.NORMAL_FADE)
                            running = False
    
    return True
