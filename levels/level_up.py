import pygame, time, os
from src.others import resource_path, show_popup, fade_out
from config import Colors, MenuConfig, TransitionConfig, AudioConfig

# Absolute path to the sound file, relative to this file
sound_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'sounds', 'menu_bonfire_sound.mp3')
game_menu_sound = pygame.mixer.Sound(sound_path)
game_menu_sound.set_volume(AudioConfig.SFX_VOLUME)


def show_level_up_menu(WINDOW_WIDTH, WINDOW_HEIGHT, main_character, screen, font_text, font_ascii):
    def display_level_up_menu(screen, font_text, main_character, selection):
        """Draw the level-up menu centered on the screen with a bordered box."""
        game_menu_sound.play(-1)  # Play sound in loop
        screen.fill(Colors.BLACK)
        
        options_info = [
            "Aqui pudes subir tus estadisticas usando los puntos de atributos disponibles.",
            f"{main_character.getName()} - Nivel: {main_character.getLevel()} - Atributos: {main_character.getAtributes()}",
            f"Vida: {main_character.getHealth()} - Daño: {main_character.getDamage()} - Evasion: {main_character.getEvadeChance()}",
            ""  # Línea vacía para separar
        ]
        
        selectable_options = [
            "Vida",
            "Daño",
            "Evasion",
            "Salir"
        ]
        
        # Calcular el ancho necesario basado en el texto más largo
        max_width = 0
        all_texts = options_info + selectable_options
        
        for text in all_texts:
            if text:  # Ignorar líneas vacías
                text_surface = font_text.render(text, True, Colors.WHITE)
                max_width = max(max_width, text_surface.get_width())
        
        # Añadir padding extra para los símbolos > < y el texto más grande
        recuadro_width = max_width + 150  # Padding generoso
        
        # Calcular altura necesaria
        total_lines = len(options_info) + len(selectable_options)
        recuadro_height = total_lines * MenuConfig.OPTION_SPACING + 100  # Padding vertical
        
        # Calcular posiciones centradas para el recuadro (más arriba)
        recuadro_x = screen.get_width() // 2 - recuadro_width // 2
        recuadro_y = screen.get_height() // 4 - recuadro_height // 4  # Más arriba que el centro

        # Dibujar borde del recuadro (sin fondo)
        pygame.draw.rect(screen, Colors.LIGHT_GRAY, (recuadro_x, recuadro_y, recuadro_width, recuadro_height), 2)
        
        # Calcular la altura total del contenido
        total_content_height = (len(options_info) + len(selectable_options)) * MenuConfig.OPTION_SPACING
        
        # Centrar el contenido verticalmente dentro del recuadro
        content_start_y = recuadro_y + (recuadro_height - total_content_height) // 2

        # Mostrar información no seleccionable
        for i, option in enumerate(options_info):
            text_surface = font_text.render(option, True, Colors.WHITE)
            # Centrar dentro del recuadro
            text_width = text_surface.get_width()
            x = recuadro_x + (recuadro_width - text_width) // 2
            y = content_start_y + i * MenuConfig.OPTION_SPACING
            screen.blit(text_surface, (x, y))
        
        # Mostrar opciones seleccionables
        for i, option in enumerate(selectable_options):
            if i == selection:
                # Opción seleccionada: color amarillo, entre > < y ligeramente más grande
                color = Colors.YELLOW
                try:
                    big_font = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 27)  # Solo 2px más grande que 25
                except:
                    big_font = pygame.font.Font(None, 27)
                
                formatted_text = f"> {option}"
                text_surface = big_font.render(formatted_text, True, color)
                text_width = text_surface.get_width()
                x = recuadro_x + (recuadro_width - text_width) // 2
                y = content_start_y + (len(options_info) + i) * MenuConfig.OPTION_SPACING - 2
                screen.blit(text_surface, (x, y))
            else:
                color = Colors.WHITE
                text_surface = font_text.render(option, True, color)
                text_width = text_surface.get_width()
                x = recuadro_x + (recuadro_width - text_width) // 2
                y = content_start_y + (len(options_info) + i) * MenuConfig.OPTION_SPACING
                screen.blit(text_surface, (x, y))
        
        # Dibujar línea de controles debajo del recuadro
        controls_text = "| ↑/↓ seleccionar | Enter entrar | Esc salir |"
        try:
            small_font = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 18)
        except:
            small_font = pygame.font.Font(None, 18)
        
        controls_surface = small_font.render(controls_text, True, Colors.GRAY)
        controls_x = recuadro_x + (recuadro_width - controls_surface.get_width()) // 2
        controls_y = recuadro_y + recuadro_height + 10  # Debajo del recuadro
        screen.blit(controls_surface, (controls_x, controls_y))
            
        pygame.display.flip()

    def level_up_game_loop(screen, font_text, font_ascii, main_character):
        """Handle the level-up menu interactions."""
        selection = 0
        selectable_options = ["Vida", "Daño", "Evasion", "Salir"]
        
        # Mostrar el menú inicial directamente
        display_level_up_menu(screen, font_text, main_character, selection)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False  # Salir del juego
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        selection = (selection - 1) % len(selectable_options)
                        display_level_up_menu(screen, font_text, main_character, selection)
                    elif event.key == pygame.K_DOWN:
                        selection = (selection + 1) % len(selectable_options)
                        display_level_up_menu(screen, font_text, main_character, selection)
                    elif event.key == pygame.K_ESCAPE:
                        # Escape sale del menú de level up
                        fade_out(screen, TransitionConfig.NORMAL_FADE)
                        return True
                    elif event.key == pygame.K_RETURN:
                        if selection == 0:  # Vida
                            if main_character.getAtributes() > 0:
                                main_character.setHealth(main_character.getHealth() + MenuConfig.HEALTH_INCREASE)
                                main_character.setAtributes(main_character.getAtributes() - 1)
                                show_popup(screen, font_text, f"Vida aumentada a {main_character.getHealth()}.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                time.sleep(TransitionConfig.MESSAGE_DELAY / 1000)
                                display_level_up_menu(screen, font_text, main_character, selection)  # redraw the menu after
                            else:
                                show_popup(screen, font_text, f"No tienes puntos de atributo suficentes.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                time.sleep(TransitionConfig.MESSAGE_DELAY / 1000)
                                display_level_up_menu(screen, font_text, main_character, selection)  # redraw the menu after
                        elif selection == 1:  # Daño
                            if main_character.getAtributes() > 0:
                                main_character.setDamage(main_character.getDamage() + MenuConfig.DAMAGE_INCREASE)
                                main_character.setAtributes(main_character.getAtributes() - 1)
                                show_popup(screen, font_text, f"Daño aumentado a {main_character.getDamage()}.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                time.sleep(TransitionConfig.MESSAGE_DELAY / 1000)
                                display_level_up_menu(screen, font_text, main_character, selection)  # Redibujar el menú después
                            else:
                                show_popup(screen, font_text, f"No tienes puntos de atributo suficentes.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                time.sleep(TransitionConfig.MESSAGE_DELAY / 1000)
                                display_level_up_menu(screen, font_text, main_character, selection)  # Redibujar el menú después
                        elif selection == 2:  # Evasion
                            if main_character.getAtributes() > 0:
                                main_character.setEvadeChance(main_character.getEvadeChance() + MenuConfig.EVASION_INCREASE)
                                main_character.setAtributes(main_character.getAtributes() - 1)
                                show_popup(screen, font_text, f"Evasion aumentada a {main_character.getEvadeChance()}.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                pygame.display.flip()
                                time.sleep(TransitionConfig.MESSAGE_DELAY / 1000)
                                display_level_up_menu(screen, font_text, main_character, selection)  # Redibujar el menú después
                            else:
                                show_popup(screen, font_text, f"No tienes puntos de atributo suficentes.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                pygame.display.flip()
                                time.sleep(TransitionConfig.MESSAGE_DELAY / 1000)
                                display_level_up_menu(screen, font_text, main_character, selection)  # Redibujar el menú después
                        elif selection == 3:  # Salir
                            fade_out(screen, TransitionConfig.NORMAL_FADE)
                            return True  # Salir del menú del juego
                    
    level_up_game_loop(screen, font_text, font_ascii, main_character)