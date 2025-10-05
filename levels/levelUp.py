import pygame, time, os
from src.others import resource_path, mostrar_popup

# Absolute path to the sound file, relative to this file
sound_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'sounds', 'menu_bonfire_sound.mp3')
game_menu_sound = pygame.mixer.Sound(sound_path)
game_menu_sound.set_volume(0.25)


def level_up_menu(WINDOW_WIDTH, WINDOW_HEIGHT, mainChar, screen, font_text, font_ascii):
    def mostrar_menu_juego(screen, font_text, mainChar):
        """Draw the level-up menu centered on the screen."""
        game_menu_sound.play(-1)  # Play sound in loop
        screen.fill((0, 0, 0))
        opciones = [
            "Aqui pudes subir tus estadisticas usando los puntos de atributos disponibles.",
            f"{mainChar.getName()} - Nivel: {mainChar.getLevel()} - Atributos: {mainChar.getAtributes()}",
            f"Vida: {mainChar.getHealth()} - Daño: {mainChar.getDamage()} - Evasion: {mainChar.getEvadeChance()}",
            "1. Vida",
            "2. Daño.",
            "3. Evasion.",
            "4. Salir."
        ]
        # Calculate start position to vertically center the menu
        total_height = len(opciones) * 40  # spacing between lines
        start_y = (WINDOW_HEIGHT - total_height) // 2

        for i, opcion in enumerate(opciones):
            text_surface = font_text.render(opcion, True, (255, 255, 255))
            text_width = text_surface.get_width()
            x = (WINDOW_WIDTH - text_width) // 2  # Center horizontally
            y = start_y + i * 40  # line spacing
            screen.blit(text_surface, (x, y))
        pygame.display.flip()

    def menu_juego(screen, font_text, font_ascii, mainChar):
        """Handle the level-up menu interactions."""
        mostrar_menu_juego(screen, font_text, mainChar)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False  # Salir del juego
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        if mainChar.getAtributes() > 0:
                            mainChar.setHealth(mainChar.getHealth() + 10)
                            mainChar.setAtributes(mainChar.getAtributes() - 1)
                            mostrar_popup(screen, font_text, f"Vida aumentada a {mainChar.getHealth()}.", WINDOW_WIDTH, WINDOW_HEIGHT, 500, 150)
                            time.sleep(2)
                            mostrar_menu_juego(screen, font_text, mainChar)  # redraw the menu after
                        else:
                            mostrar_popup(screen, font_text, f"No tienes puntos de atributo suficentes.", 500, 150)
                            time.sleep(2)
                            mostrar_menu_juego(screen, font_text, mainChar)  # redraw the menu after
                    elif event.key == pygame.K_2:
                        if mainChar.getAtributes() > 0:
                            mainChar.setDamage(mainChar.getDamage() + 1)
                            mainChar.setAtributes(mainChar.getAtributes() - 1)
                            mostrar_popup(screen, font_text, f"Daño aumentado a {mainChar.getDamage()}.", WINDOW_WIDTH, WINDOW_HEIGHT, 500, 150)
                            time.sleep(2)
                            mostrar_menu_juego(screen, font_text, mainChar)  # Redibujar el menú después
                        else:
                            mostrar_popup(screen, font_text, f"No tienes puntos de atributo suficentes.", WINDOW_WIDTH, WINDOW_HEIGHT, 500, 150)
                            time.sleep(2)
                            mostrar_menu_juego(screen, font_text, mainChar)  # Redibujar el menú después
                    elif event.key == pygame.K_3:
                        if mainChar.getAtributes() > 0:
                            mainChar.setEvadeChance(mainChar.getEvadeChance() + 1)
                            mainChar.setAtributes(mainChar.getAtributes() - 1)
                            mostrar_popup(screen, font_text, f"Evasion aumentada a {mainChar.getEvadeChance()}.", WINDOW_WIDTH, WINDOW_HEIGHT, 500, 150)
                            pygame.display.flip()
                            time.sleep(2)
                            mostrar_menu_juego(screen, font_text, mainChar)  # Redibujar el menú después
                        else:
                            mostrar_popup(screen, font_text, f"No tienes puntos de atributo suficentes.", WINDOW_WIDTH, WINDOW_HEIGHT, 500, 150)
                            pygame.display.flip()
                            time.sleep(2)
                            mostrar_menu_juego(screen, font_text, mainChar)  # Redibujar el menú después
                    elif event.key == pygame.K_4:
                        return True  # Salir del menú del juego
                    
    menu_juego(screen, font_text, font_ascii, mainChar)