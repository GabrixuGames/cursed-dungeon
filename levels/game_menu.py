import pygame, time
from src.others import slow_print, resource_path, fade_out
from levels.shop import shop
from levels.levelUp import level_up_menu
from levels.dungeon_combat import dungeon
from src.animations.animations_game_menu import precalculate_bonfire_frames

game_menu_sound = pygame.mixer.Sound(resource_path("src\\sounds\\menu_bonfire_sound.mp3"))
game_menu_sound.set_volume(0.25)


def game_menu(WINDOW_WIDTH, WINDOW_HEIGHT, mainChar, screen, font_text, font_ascii_menu):
    def mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii_menu, bonfire_frames, current_frame):
        """Dibuja el menú del juego con la opción seleccionada resaltada y la animación."""
        screen.fill((0, 0, 0))

        # Calcular posiciones centradas para el recuadro
        recuadro_x = screen.get_width() // 2 - 350
        recuadro_y = screen.get_height() // 2 - 200
        recuadro_width = 700
        recuadro_height = 400

        # Dibujar borde del recuadro (sin fondo)
        pygame.draw.rect(screen, (200, 200, 200), (recuadro_x, recuadro_y, recuadro_width, recuadro_height), 2)

        # Calcular posiciones para el texto y la animación
        texto_x = recuadro_x + 50
        texto_y = recuadro_y + 100  # Subir el texto del menú
        animacion_x = recuadro_x + recuadro_width // 2 - 100  # Mover aún más a la derecha
        animacion_y = recuadro_y + recuadro_height // 2 - 100  # Bajar un poco más

        # Dibujar opciones del menú alineadas a la izquierda
        for i, opcion in enumerate(opciones):
            color = (255, 255, 0) if i == seleccion else (255, 255, 255)
            text_surface = font_text.render(opcion, True, color)
            screen.blit(text_surface, (texto_x, texto_y + i * 40))

        # Escalar la animación para hacerla más grande
        bonfire_frame = pygame.transform.scale(bonfire_frames[current_frame], (300, 300))
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
        FRAME_DURATION = 600  # ms (ajustado para una animación ligeramente más lenta)

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
                            fade_out(screen, 600)
                            game_menu_sound.stop()
                            dungeon(mainChar, screen, font_ascii, font_text)
                            # Al regresar de la mazmorra, restaurar música y mostrar menú
                            game_menu_sound.play(-1)
                            mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                        elif seleccion == 1:
                            fade_out(screen, 600)
                            shop(mainChar, screen, font_text, screen.get_width(), screen.get_height())
                            # Al regresar de la tienda, restaurar música y mostrar menú
                            game_menu_sound.play(-1)
                            mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                        elif seleccion == 2:
                            fade_out(screen, 600)
                            level_up_menu(screen.get_width(), screen.get_height(), mainChar, screen, font_text, font_ascii)
                            # Al regresar del level up, restaurar música y mostrar menú
                            game_menu_sound.play(-1)
                            mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                        elif seleccion == 3:
                            fade_out(screen, 500)
                            screen.fill((0, 0, 0))
                            slow_print(screen, font_text, "Partida guardada.", 10, 200)
                            pygame.time.wait(2000)
                            mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii, bonfire_frames, current_frame)
                        elif seleccion == 4:
                            fade_out(screen, 800)
                            return True

            # Actualizar frame de animación de forma independiente
            now = pygame.time.get_ticks()
            if now - frame_timer >= FRAME_DURATION:
                frame_timer = now
                current_frame = (current_frame + 1) % len(bonfire_frames)
                mostrar_menu_juego(screen, font_text, mainChar, opciones, seleccion, font_ascii, bonfire_frames, current_frame)

            clock.tick(30)

    menu_juego(screen, font_text, font_ascii_menu, mainChar)
