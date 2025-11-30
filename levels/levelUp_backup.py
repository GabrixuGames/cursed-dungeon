import pygame, time, os
from src.others import resource_path, mostrar_popup, fade_out
from config import Colors, MenuConfig, TransitionConfig, AudioConfig

# Absolute path to the sound file, relative to this file
sound_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'sounds', 'menu_bonfire_sound.mp3')
game_menu_sound = pygame.mixer.Sound(sound_path)
game_menu_sound.set_volume(AudioConfig.SFX_VOLUME)


def show_level_up_menu(WINDOW_WIDTH, WINDOW_HEIGHT, main_character, screen, font_text, font_ascii):
    def display_level_up_menu(screen, font_text, main_character, selection):
        """Draw the level-up menu centered on the screen."""
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
        
        # Calculate start position to vertically center the menu
        total_height = (len(options_info) + len(selectable_options)) * MenuConfig.OPTION_SPACING
        start_y = (WINDOW_HEIGHT - total_height) // 2

        # Mostrar información no seleccionable
        for i, option in enumerate(options_info):
            text_surface = font_text.render(option, True, Colors.WHITE)
            text_width = text_surface.get_width()
            x = (WINDOW_WIDTH - text_width) // 2  # Center horizontally
            y = start_y + i * MenuConfig.OPTION_SPACING  # line spacing
            screen.blit(text_surface, (x, y))
        
        # Mostrar opciones seleccionables
        for i, option in enumerate(selectable_options):
            color = Colors.YELLOW if i == selection else Colors.WHITE
            text_surface = font_text.render(option, True, color)
            text_width = text_surface.get_width()
            x = (WINDOW_WIDTH - text_width) // 2  # Center horizontally
            y = start_y + (len(options_info) + i) * MenuConfig.OPTION_SPACING  # line spacing
            screen.blit(text_surface, (x, y))
            
        pygame.display.flip()

    def menu_juego(screen, font_text, font_ascii, mainChar):
        """Handle the level-up menu interactions."""
        seleccion = 0
        opciones_seleccionables = ["Vida", "Daño", "Evasion", "Salir"]
        
        # Mostrar el menú inicial directamente
        mostrar_menu_juego(screen, font_text, mainChar, seleccion)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False  # Salir del juego
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(opciones_seleccionables)
                        mostrar_menu_juego(screen, font_text, mainChar, seleccion)
                    elif event.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(opciones_seleccionables)
                        mostrar_menu_juego(screen, font_text, mainChar, seleccion)
                    elif event.key == pygame.K_RETURN:
                        if seleccion == 0:  # Vida
                            if mainChar.getAtributes() > 0:
                                mainChar.setHealth(mainChar.getHealth() + MenuConfig.HEALTH_INCREASE)
                                mainChar.setAtributes(mainChar.getAtributes() - 1)
                                mostrar_popup(screen, font_text, f"Vida aumentada a {mainChar.getHealth()}.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                time.sleep(TransitionConfig.MESSAGE_DELAY / 1000)
                                mostrar_menu_juego(screen, font_text, mainChar, seleccion)  # redraw the menu after
                            else:
                                mostrar_popup(screen, font_text, f"No tienes puntos de atributo suficentes.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                time.sleep(TransitionConfig.MESSAGE_DELAY / 1000)
                                mostrar_menu_juego(screen, font_text, mainChar, seleccion)  # redraw the menu after
                        elif seleccion == 1:  # Daño
                            if mainChar.getAtributes() > 0:
                                mainChar.setDamage(mainChar.getDamage() + MenuConfig.DAMAGE_INCREASE)
                                mainChar.setAtributes(mainChar.getAtributes() - 1)
                                mostrar_popup(screen, font_text, f"Daño aumentado a {mainChar.getDamage()}.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                time.sleep(TransitionConfig.MESSAGE_DELAY / 1000)
                                mostrar_menu_juego(screen, font_text, mainChar, seleccion)  # Redibujar el menú después
                            else:
                                mostrar_popup(screen, font_text, f"No tienes puntos de atributo suficentes.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                time.sleep(TransitionConfig.MESSAGE_DELAY / 1000)
                                mostrar_menu_juego(screen, font_text, mainChar, seleccion)  # Redibujar el menú después
                        elif seleccion == 2:  # Evasion
                            if mainChar.getAtributes() > 0:
                                mainChar.setEvadeChance(mainChar.getEvadeChance() + MenuConfig.EVASION_INCREASE)
                                mainChar.setAtributes(mainChar.getAtributes() - 1)
                                mostrar_popup(screen, font_text, f"Evasion aumentada a {mainChar.getEvadeChance()}.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                pygame.display.flip()
                                time.sleep(TransitionConfig.MESSAGE_DELAY / 1000)
                                mostrar_menu_juego(screen, font_text, mainChar, seleccion)  # Redibujar el menú después
                            else:
                                mostrar_popup(screen, font_text, f"No tienes puntos de atributo suficentes.", WINDOW_WIDTH, WINDOW_HEIGHT, MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                                pygame.display.flip()
                                time.sleep(TransitionConfig.MESSAGE_DELAY / 1000)
                                mostrar_menu_juego(screen, font_text, mainChar, seleccion)  # Redibujar el menú después
                        elif seleccion == 3:  # Salir
                            fade_out(screen, TransitionConfig.NORMAL_FADE)
                            return True  # Salir del menú del juego
                    
    menu_juego(screen, font_text, font_ascii, mainChar)