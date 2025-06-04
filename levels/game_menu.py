import pygame, time
from src.others import slow_print, resource_path
from levels.shop import shop
from levels.levelUp import level_up_menu
from levels.dungeon_combat import dungeon
from src.animations.animations_game_menu import animation_bonfire_1_get_frame

game_menu_sound = pygame.mixer.Sound(resource_path("src\\sounds\\menu_bonfire_sound.mp3"))
game_menu_sound.set_volume(0.25)


def game_menu(WINDOW_WIDTH, WINDOW_HEIGHT, mainChar, screen, font_text, font_ascii_menu):
    def mostrar_menu_juego(screen, font_text, mainChar):
        font_ascii_menu = pygame.font.SysFont("Courier", 60)
        opciones = [
            f"{mainChar.getName()} - Nivel: {mainChar.getLevel()} - Experiencia: {mainChar.getExperience()} - Dinero: {round(mainChar.getMoney(), 2)}",
            f"{mainChar.getWeapon()['name']}",
            "1. Ir a la mazmorra.",
            "2. Tienda.",
            "3. Subir nivel.",
            "4. Guardar partida.",
            "5. Salir."
        ]
        total_height = len(opciones) * 40
        start_y = (WINDOW_HEIGHT // 2) - 150
        text_x = WINDOW_WIDTH // 2 - 500

        for i, opcion in enumerate(opciones):
            text_surface = font_text.render(opcion, True, (255, 255, 255))
            screen.blit(text_surface, (text_x, start_y + i * 40))

    def menu_juego(screen, font_text, font_ascii, mainChar):
        game_menu_sound.play(-1)
        clock = pygame.time.Clock()
        frame_timer = 0
        current_frame = 0
        FRAME_DURATION = 300  # ms

        while True:
            screen.fill((0, 0, 0))
            mostrar_menu_juego(screen, font_text, mainChar)

            # Actualizar frame si ha pasado suficiente tiempo
            now = pygame.time.get_ticks()
            if now - frame_timer >= FRAME_DURATION:
                frame_timer = now
                current_frame = (current_frame + 1) % 4

            # Obtener frame de fogata como surface y dibujarlo
            bonfire_frame = animation_bonfire_1_get_frame(font_ascii_menu, current_frame)
            screen.blit(bonfire_frame, (WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        game_menu_sound.stop()
                        dungeon(mainChar, screen, font_ascii, font_text)
                    elif event.key == pygame.K_2:
                        shop(mainChar, screen, font_text, WINDOW_WIDTH, WINDOW_HEIGHT)
                    elif event.key == pygame.K_3:
                        level_up_menu(WINDOW_WIDTH, WINDOW_HEIGHT, mainChar, screen, font_text, font_ascii)
                    elif event.key == pygame.K_4:
                        mainChar.save_game()
                        slow_print(screen, font_text, "Partida guardada.", 10, 200)
                        time.sleep(2)
                    elif event.key == pygame.K_5:
                        return True

    menu_juego(screen, font_text, font_ascii_menu, mainChar)
