import pygame
from src.others import draw_text
from src.animations.animations import frames_walking_left, frames_walking_right
from levels.dungeon_combat import draw_custom_dungeon

steps_sound = pygame.mixer.Sound("src/sounds/steps_sound.mp3")

def draw_dungeon_static(screen, font_text_combat, font_ascii, inicial_player_health, mainChar, offset):
    screen.fill((0, 0, 0))
    draw_custom_dungeon(screen, font_ascii, offset)

    x_char = screen.get_width() // 2 - 300
    y_char = 380
    frame_lines = frames_walking_right[0] if isinstance(frames_walking_right[0], list) else frames_walking_right[0].splitlines()
    for i, line in enumerate(frame_lines):
        draw_text(screen, font_ascii, line, x_char, y_char + i * 20)

    draw_text(screen, font_text_combat, f"{mainChar.getName()} - Salud: {inicial_player_health}", 50, 30)
    draw_text(screen, font_text_combat, "Presiona A o D para moverte por la mazmorra.", 50, 60)

    pygame.display.flip()

from src.animations.animations import frames_walking_right, frames_walking_left

def dungeon_walking(screen, font_text_combat, font_ascii, inicial_player_health, mainChar, offset, char_offset=0, delay=100):
    clock = pygame.time.Clock()
    running = True
    current_frame = 0
    last_update = pygame.time.get_ticks()
    step_count = 0
    last_direction = "right"  # Valor inicial para elegir la animación

    char_max_offset = 400
    char_max_offset_a = screen.get_width() // 2 - 500

    steps_sound.play(-1)

    while running:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                steps_sound.stop()
                pygame.quit()
                return offset, step_count, char_offset

        keys = pygame.key.get_pressed()
        if not (keys[pygame.K_d] or keys[pygame.K_a]):
            running = False

        if now - last_update >= delay:
            current_frame = (current_frame + 1) % len(frames_walking_right)  # Asumen mismo largo
            step_count += 1
            last_update = now

            if keys[pygame.K_d]:  # Mover a la derecha
                last_direction = "right"
                if char_offset < char_max_offset:
                    char_offset += 15
                else:
                    offset += 15

            elif keys[pygame.K_a]:  # Mover a la izquierda
                last_direction = "left"
                if char_offset > -char_max_offset_a:
                    char_offset -= 15
                else:
                    offset -= 15

        # Dibujar fondo y personaje
        screen.fill((0, 0, 0))
        draw_custom_dungeon(screen, font_ascii, offset)

        x_char = screen.get_width() // 2 - 300 + char_offset
        y_char = 380

        # Seleccionar los frames correctos según la dirección
        if last_direction == "right":
            frame_lines = frames_walking_right[current_frame]
        else:
            frame_lines = frames_walking_left[current_frame]

        if not isinstance(frame_lines, list):
            frame_lines = frame_lines.splitlines()

        for i, line in enumerate(frame_lines):
            draw_text(screen, font_ascii, line, x_char, y_char + i * 20)

        draw_text(screen, font_text_combat, f"Pasos en esta animación: {step_count}", 10, 10)

        pygame.display.flip()
        clock.tick(60)

    steps_sound.stop()
    return offset, step_count, char_offset





