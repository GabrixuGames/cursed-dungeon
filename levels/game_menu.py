import pygame, time
from src.others import slow_print, resource_path, fade_out, show_popup
from levels.shop import shop
from levels.level_up import show_level_up_menu
from levels.dungeon_combat import dungeon
from src.animations.animations_game_menu import precalculate_bonfire_frames
from config import Colors, MenuConfig, TransitionConfig, AudioConfig

game_menu_sound = pygame.mixer.Sound(resource_path("src/sounds/menu_bonfire_sound.mp3"))
game_menu_sound.set_volume(AudioConfig.SFX_VOLUME)


def game_menu(WINDOW_WIDTH, WINDOW_HEIGHT, main_character, screen, font_text, font_ascii_menu):
    def mostrar_menu_juego(screen, font_text, main_character, opciones, seleccion, font_ascii_menu, bonfire_frames, current_frame):
        """Dibuja el menú del juego con la opción seleccionada resaltada y la animación."""
        screen.fill(Colors.BLACK)

        # Calcular posiciones centradas para el recuadro
        recuadro_x = screen.get_width() // 2 - MenuConfig.GAME_MENU_BOX_WIDTH // 2
        recuadro_y = screen.get_height() // 2 - MenuConfig.GAME_MENU_BOX_HEIGHT // 2
        recuadro_width = MenuConfig.GAME_MENU_BOX_WIDTH
        recuadro_height = MenuConfig.GAME_MENU_BOX_HEIGHT

        # Dibujar borde del recuadro (sin fondo)
        pygame.draw.rect(screen, Colors.LIGHT_GRAY, (recuadro_x, recuadro_y, recuadro_width, recuadro_height), 2)

        # Calcular posiciones para el texto y la animación
        texto_x = recuadro_x + MenuConfig.MENU_PADDING
        texto_y = recuadro_y + MenuConfig.TITLE_Y_OFFSET  # Subir el texto del menú
        
        # Posicionar la fogata más cerca del texto del menú
        bonfire_x = texto_x + 335  # Posición ajustada 15px más a la izquierda
        bonfire_y = recuadro_y + (recuadro_height - MenuConfig.BONFIRE_SIZE[1]) // 2  # Centrada verticalmente

        # Dibujar opciones del menú alineadas a la izquierda
        for i, opcion in enumerate(opciones):
            if i == seleccion:
                # Opción seleccionada: color amarillo, entre > < y ligeramente más grande
                color = Colors.YELLOW
                # Crear fuente más grande para la opción seleccionada
                try:
                    big_font = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 27)  # Solo 2px más grande que 25
                except:
                    big_font = pygame.font.Font(None, 27)
                
                # Formatear con el símbolo >
                formatted_text = f"> {opcion}"
                text_surface = big_font.render(formatted_text, True, color)
                # Centrar la opción seleccionada horizontalmente
                selected_x = texto_x - 10  # Pequeño ajuste hacia la izquierda
                screen.blit(text_surface, (selected_x, texto_y + i * MenuConfig.OPTION_SPACING - 2))
            else:
                # Opciones no seleccionadas: tamaño normal, color blanco
                color = Colors.WHITE
                text_surface = font_text.render(opcion, True, color)
                screen.blit(text_surface, (texto_x, texto_y + i * MenuConfig.OPTION_SPACING))

        # Dibujar línea de controles debajo del recuadro
        controls_text = "| ↑/↓ seleccionar | Enter entrar | Esc salir |"
        # Crear fuente más pequeña para los controles
        try:
            small_font = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 18)
        except:
            small_font = pygame.font.Font(None, 18)
        
        controls_surface = small_font.render(controls_text, True, Colors.GRAY)
        controls_x = recuadro_x + (recuadro_width - controls_surface.get_width()) // 2  # Centrado con el recuadro
        controls_y = recuadro_y + recuadro_height + 10  # Debajo del recuadro
        screen.blit(controls_surface, (controls_x, controls_y))

        # La animación ya está en el tamaño correcto, no necesita escalado
        bonfire_frame = bonfire_frames[current_frame]
        screen.blit(bonfire_frame, (bonfire_x, bonfire_y))

        pygame.display.flip()

    def menu_juego(screen, font_text, font_ascii, main_character):
        game_menu_sound.play(-1)
        clock = pygame.time.Clock()
        opciones = [
            "Ir a la mazmorra",
            "Tienda",
            "Subir nivel",
            "Guardar partida",
            "Salir"
        ]
        seleccion = 0
        current_frame = 0

        # Precalcular cuadros de la animación de la fogata
        # Crear una fuente más grande específicamente para la fogata
        try:
            big_font_ascii = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 20)
        except:
            big_font_ascii = pygame.font.Font(None, 60)  # Fuente del sistema como fallback
        
        bonfire_frames = precalculate_bonfire_frames(big_font_ascii)
        frame_timer = 0
        FRAME_DURATION = MenuConfig.ANIMATION_FRAME_DURATION  # ms (ajustado para una animación ligeramente más lenta)

        # Mostrar el menú inicial
        mostrar_menu_juego(screen, font_text, main_character, opciones, seleccion, font_ascii, bonfire_frames, current_frame)

        while True:
            # Procesar eventos de entrada primero para evitar retrasos en la navegación
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(opciones)
                        mostrar_menu_juego(screen, font_text, main_character, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                    elif event.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(opciones)
                        mostrar_menu_juego(screen, font_text, main_character, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                    elif event.key == pygame.K_ESCAPE:
                        # Escape vuelve al menú principal
                        fade_out(screen, TransitionConfig.LONG_FADE)
                        return True
                    elif event.key == pygame.K_RETURN:
                        if seleccion == 0:
                            fade_out(screen, TransitionConfig.NORMAL_FADE)
                            game_menu_sound.stop()
                            dungeon(main_character, screen, font_ascii, font_text)
                            # Al regresar de la mazmorra, restaurar música y mostrar menú
                            game_menu_sound.play(-1)
                            mostrar_menu_juego(screen, font_text, main_character, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                        elif seleccion == 1:
                            fade_out(screen, TransitionConfig.NORMAL_FADE)
                            shop(main_character, screen, font_text, screen.get_width(), screen.get_height())
                            # Al regresar de la tienda, restaurar música y mostrar menú
                            game_menu_sound.play(-1)
                            mostrar_menu_juego(screen, font_text, main_character, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                        elif seleccion == 2:
                            fade_out(screen, TransitionConfig.NORMAL_FADE)
                            show_level_up_menu(screen.get_width(), screen.get_height(), main_character, screen, font_text, font_ascii)
                            # Al regresar del level up, restaurar música y mostrar menú
                            game_menu_sound.play(-1)
                            mostrar_menu_juego(screen, font_text, main_character, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                        elif seleccion == 3:
                            # Guardar partida y mostrar popup
                            main_character.save_game()
                            show_popup(screen, font_text, "Partida guardada exitosamente!", screen.get_width(), screen.get_height(), MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                            mostrar_menu_juego(screen, font_text, main_character, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                        elif seleccion == 4:
                            fade_out(screen, TransitionConfig.LONG_FADE)
                            return True

            # Actualizar frame de animación de forma independiente
            now = pygame.time.get_ticks()
            if now - frame_timer >= FRAME_DURATION:
                frame_timer = now
                current_frame = (current_frame + 1) % len(bonfire_frames)
                mostrar_menu_juego(screen, font_text, main_character, opciones, seleccion, font_ascii, bonfire_frames, current_frame)

            clock.tick(MenuConfig.MENU_FPS)

    menu_juego(screen, font_text, font_ascii_menu, main_character)
