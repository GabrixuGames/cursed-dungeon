import pygame, time
from src.others import slow_print, resource_path, fade_out, show_popup
from levels.shop import shop
from levels.levelUp import show_level_up_menu
from levels.dungeon_combat import dungeon
from src.animations.animations_game_menu import precalculate_bonfire_frames
from config import Colors, MenuConfig, TransitionConfig, AudioConfig

game_menu_sound = pygame.mixer.Sound(resource_path("src\\sounds\\menu_bonfire_sound.mp3"))
game_menu_sound.set_volume(AudioConfig.SFX_VOLUME)


def game_menu(WINDOW_WIDTH, WINDOW_HEIGHT, mainChar, screen, font_text, font_ascii_menu):
    def mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii_menu, bonfire_frames, current_frame):
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
        animacion_x = recuadro_x + recuadro_width // 2 - MenuConfig.ANIMATION_OFFSET  # Mover aún más a la derecha
        animacion_y = recuadro_y + recuadro_height // 2 - MenuConfig.ANIMATION_OFFSET  # Bajar un poco más

        # Dibujar opciones del menú alineadas a la izquierda
        for i, opcion in enumerate(opciones):
            color = Colors.YELLOW if i == seleccion else Colors.WHITE
            text_surface = font_text.render(opcion, True, color)
            screen.blit(text_surface, (texto_x, texto_y + i * MenuConfig.OPTION_SPACING))

        # Escalar la animación para hacerla más grande
        bonfire_frame = pygame.transform.scale(bonfire_frames[current_frame], (MenuConfig.ANIMATION_SIZE, MenuConfig.ANIMATION_SIZE))
        screen.blit(bonfire_frame, (animacion_x, animacion_y))

        pygame.display.flip()

    def menu_juego(screen, font_text, font_ascii, mainChar):
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
        bonfire_frames = precalculate_bonfire_frames(font_ascii_menu)
        frame_timer = 0
        FRAME_DURATION = MenuConfig.ANIMATION_FRAME_DURATION  # ms (ajustado para una animación ligeramente más lenta)

        # Mostrar el menú inicial
        mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii, bonfire_frames, current_frame)

        while True:
            # Procesar eventos de entrada primero para evitar retrasos en la navegación
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(opciones)
                        mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                    elif event.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(opciones)
                        mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                    elif event.key == pygame.K_RETURN:
                        if seleccion == 0:
                            fade_out(screen, TransitionConfig.NORMAL_FADE)
                            game_menu_sound.stop()
                            dungeon(mainChar, screen, font_ascii, font_text)
                            # Al regresar de la mazmorra, restaurar música y mostrar menú
                            game_menu_sound.play(-1)
                            mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                        elif seleccion == 1:
                            fade_out(screen, TransitionConfig.NORMAL_FADE)
                            shop(mainChar, screen, font_text, screen.get_width(), screen.get_height())
                            # Al regresar de la tienda, restaurar música y mostrar menú
                            game_menu_sound.play(-1)
                            mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                        elif seleccion == 2:
                            fade_out(screen, TransitionConfig.NORMAL_FADE)
                            show_level_up_menu(screen.get_width(), screen.get_height(), mainChar, screen, font_text, font_ascii)
                            # Al regresar del level up, restaurar música y mostrar menú
                            game_menu_sound.play(-1)
                            mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                        elif seleccion == 3:
                            # Guardar partida y mostrar popup
                            mainChar.save_game()
                            show_popup(screen, font_text, "Partida guardada exitosamente!", screen.get_width(), screen.get_height(), MenuConfig.POPUP_WIDTH, MenuConfig.POPUP_HEIGHT)
                            mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                        elif seleccion == 4:
                            fade_out(screen, TransitionConfig.LONG_FADE)
                            return True

            # Actualizar frame de animación de forma independiente
            now = pygame.time.get_ticks()
            if now - frame_timer >= FRAME_DURATION:
                frame_timer = now
                current_frame = (current_frame + 1) % len(bonfire_frames)
                mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii, bonfire_frames, current_frame)

            clock.tick(MenuConfig.MENU_FPS)

    menu_juego(screen, font_text, font_ascii_menu, mainChar)
