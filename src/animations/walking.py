import pygame
from src.others import draw_text
from src.animations.animations import frames_walking_left, frames_walking_right
from src.others import draw_custom_dungeon

import os
sound_path = os.path.join(os.path.dirname(__file__), '..', 'sounds', 'steps_sound.mp3')
steps_sound = pygame.mixer.Sound(sound_path)

def draw_dungeon_static(screen, font_text_combat, font_ascii, inicial_player_health, main_character, offset, char_offset=0):
    screen.fill((0, 0, 0))
    draw_custom_dungeon(screen, font_ascii, offset, 0)  # Sin animación en estado estático

    x_char = screen.get_width() // 2 - 300 + char_offset
    # Calcular y_char para que los pies del muñeco estén sobre la línea 12 (igual que en walking)
    background_height = 14 * 28  # líneas del fondo * line_height
    start_y_background = (screen.get_height() - background_height) // 2
    # Los pies deben estar sobre la línea 12, así que el muñeco termina en la línea 12
    y_char = start_y_background + (12 * 28) - 120  # Ajustado para que los pies estén en línea 12
    
    # Usar frame estático (sin efectos para estado idle)
    frame_lines = frames_walking_right[0].splitlines()
    for i, line in enumerate(frame_lines):
        draw_text(screen, font_ascii, line, x_char, y_char + i * 30)  # Mismo espaciado que walking

    # UI positions (fixed) to avoid jumps when text changes
    UI_NAME_X = 50
    UI_NAME_Y = 30
    UI_PROMPT_Y = 60

    # Show current character health in current/max format
    draw_text(screen, font_text_combat, f"{main_character.getName()} - Health: {main_character.getHealth()}/{inicial_player_health} HP", UI_NAME_X, UI_NAME_Y)
    draw_text(screen, font_text_combat, "Press A or D to move through the dungeon.", UI_NAME_X, UI_PROMPT_Y)

    pygame.display.flip()

from src.animations.animations import frames_walking_right, frames_walking_left

def dungeon_walking(screen, font_text_combat, font_ascii, inicial_player_health, main_character, offset, char_offset=0, delay=100, steps_walked=0, steps_until_combat=None, force_steps=0):
    clock = pygame.time.Clock()
    running = True
    current_frame = 0
    last_update = pygame.time.get_ticks()
    step_count = 0
    # steps made during this call
    steps_made = 0
    last_direction = "right"  # Valor inicial para elegir la animación
    
    # Sistema de efectos ambientales mejorado (uno a la vez)
    current_effect = None
    effect_timer = 0
    effect_cooldown = 0  # Tiempo de espera entre efectos
    effect_x = 0
    effect_y = 0
    effect_color = (255, 255, 255)

    # Maximum character displacement before moving the background (relative to window)
    screen_w = screen.get_width()
    # Start moving the background earlier (player doesn't need to reach window edge)
    # lower threshold from 35% to 25% of screen width so the background starts moving sooner
    char_max_offset = max(120, int(screen_w * 0.25))
    # Extended: additional range the character can use when background is at its limit
    char_max_offset_extended = max(200, int(screen_w * 0.40))
    char_max_offset_a = char_max_offset
    # Rango máximo razonable para offset del fondo (evita que el fondo se vaya fuera de vista)
    max_offset = screen_w * 2
    min_offset = -max_offset
    # Background step (más suave que el step del jugador)
    step_player = 15
    step_bg = 8
    # Grace: allow a couple of frames without keypress before ending walking animation
    no_key_grace = 3
    no_key_frames = 0
    
    # Contador para animaciones del fondo
    frame_counter = 0

    steps_sound.play(-1)

    while running:
        now = pygame.time.get_ticks()
        frame_counter += 1  # Incrementar contador de frames
        
        # Procesar efectos ambientales independientemente del movimiento
        import random
        
        # Decrementar timers
        if effect_timer > 0:
            effect_timer -= 1
        if effect_cooldown > 0:
            effect_cooldown -= 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                steps_sound.stop()
                pygame.quit()
                return offset, step_count, char_offset

        keys = pygame.key.get_pressed()
        if not (keys[pygame.K_d] or keys[pygame.K_a]):
            no_key_frames += 1
            if no_key_frames > no_key_grace:
                running = False
        else:
            no_key_frames = 0

            if now - last_update >= delay:
                current_frame = (current_frame + 1) % len(frames_walking_right)  # Asumen mismo largo
                step_count += 1
                steps_made += 1
                # step counters updated (debug prints removed in cleanup)
                last_update = now

                # Permitir forzar pasos en pruebas
                if force_steps > 0:
                    steps_made += force_steps

                # If the total steps goal is reached, interrupt for combat
                if steps_until_combat is not None and (steps_walked + steps_made) >= steps_until_combat:
                    # reached steps threshold: stop walking and signal combat
                    steps_sound.stop()
                    return offset, steps_made, char_offset, True

                if keys[pygame.K_d]:  # Mover a la derecha
                    last_direction = "right"
                    if char_offset < char_max_offset:
                        char_offset += step_player
                    else:
                        # si el fondo puede moverse, muévelo con paso más suave
                        if offset < max_offset:
                            offset += step_bg
                            if offset > max_offset:
                                offset = max_offset
                        else:
                            # fondo en límite: permitir rango extendido al personaje
                            if char_offset < char_max_offset_extended:
                                char_offset += step_player

                elif keys[pygame.K_a]:  # Mover a la izquierda
                    last_direction = "left"
                    if char_offset > -char_max_offset_a:
                        char_offset -= step_player
                    else:
                        # si el fondo puede moverse, muévelo con paso más suave
                        if offset > min_offset:
                            offset -= step_bg
                            if offset < min_offset:
                                offset = min_offset
                        else:
                            # fondo en límite: permitir rango extendido al personaje
                            if char_offset > -char_max_offset_extended:
                                char_offset -= step_player

        # Generar nuevos efectos solo si no hay uno activo y el cooldown ha terminado
        if effect_timer <= 0 and effect_cooldown <= 0 and random.randint(1, 120) == 1:
            effect_type = random.choice(['wind', 'wind', 'dust', 'leaves'])
            effect_timer = 45  # duración del efecto
            effect_cooldown = random.randint(180, 360)  # cooldown hasta próximo efecto
            
            if effect_type == 'wind':
                wind_patterns = ["~", "~~", "~~~", "~~~~"]
                current_effect = random.choice(wind_patterns)
                effect_x = random.randint(100, screen.get_width() - 200)
                effect_y = random.randint(100, 300)
                effect_color = (200, 200, 255)
            elif effect_type == 'dust':
                dust_patterns = [".", "..", "...", "° °", "· ·"]
                current_effect = random.choice(dust_patterns)
                effect_x = random.randint(100, screen.get_width() - 200)
                effect_y = random.randint(400, screen.get_height() - 100)
                effect_color = (139, 129, 76)
            else:  # leaves
                leaf_patterns = ["*", "o", "°", "·"]
                current_effect = random.choice(leaf_patterns)
                effect_x = random.randint(100, screen.get_width() - 200)
                effect_y = random.randint(200, 400)
                effect_color = (34, 139, 34)

        # Draw background and character
        screen.fill((0, 0, 0))
        draw_custom_dungeon(screen, font_ascii, offset, frame_counter)

        x_char = screen.get_width() // 2 - 300 + char_offset
        # Calcular y_char para que los pies del muñeco estén sobre la línea 12
        background_height = 14 * 28  # líneas del fondo * line_height
        start_y_background = (screen.get_height() - background_height) // 2
        # Los pies deben estar sobre la línea 12, así que el muñeco termina en la línea 12
        y_char = start_y_background + (12 * 28) - 120  # Ajustado para que los pies estén en línea 12

        # Select appropriate frames according to direction
        if last_direction == "right":
            frame_lines = frames_walking_right[current_frame]
        else:
            frame_lines = frames_walking_left[current_frame]

        if not isinstance(frame_lines, list):
            frame_lines = frame_lines.splitlines()

        # Dibujar el personaje con espaciado vertical generoso
        for i, line in enumerate(frame_lines):
            draw_text(screen, font_ascii, line, x_char, y_char + i * 30)  # Aumentado de 25 a 30
        
        # Dibujar efecto activo
        if current_effect and effect_timer > 0:
            # Las hojas se mueven lentamente
            if effect_color == (34, 139, 34):  # Es una hoja
                effect_x += 0.5  # Movimiento sutil
            
            draw_text(screen, font_ascii, current_effect, int(effect_x), int(effect_y), effect_color)
        
        # Limpiar efecto cuando termine
        if effect_timer <= 0:
            current_effect = None

        # Ensure char_offset stays within extended range
        if char_offset > char_max_offset_extended:
            char_offset = char_max_offset_extended
        if char_offset < -char_max_offset_extended:
            char_offset = -char_max_offset_extended

        # UI positions (match draw_dungeon_static) to avoid jumps
        UI_NAME_X = 50
        UI_NAME_Y = 30
        UI_PROMPT_Y = 60

        # Always show the name and current health while walking
        draw_text(screen, font_text_combat, f"{main_character.getName()} - Health: {main_character.getHealth()}/{inicial_player_health} HP", UI_NAME_X, UI_NAME_Y)
        # Show the prompt in the same position as static state for consistency
        draw_text(screen, font_text_combat, "Press A or D to move through the dungeon.", UI_NAME_X, UI_PROMPT_Y)

        pygame.display.flip()
        clock.tick(60)
    steps_sound.stop()
    return offset, step_count, char_offset





