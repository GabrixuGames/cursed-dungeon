import pygame, copy, random, time
from src.object.enemy import load_enemies
from src.others import resource_path, draw_text, slow_print, draw_custom_dungeon, blocking_message, combat_message_box
from src.animations.walking import dungeon_walking, draw_dungeon_static
from src.animations.animations import play_combat_intro




background_sound = pygame.mixer.Sound("src/sounds/ambience_sound.mp3")  # Ajusta la ruta
background_sound.set_volume(0.05)  # Ajusta el volumen según sea necesario
battle_start_sound = pygame.mixer.Sound(resource_path("src/sounds/battle_start.mp3"))
battle_start_sound.set_volume(0.5)  # Ajusta el volumen según sea necesario


def draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy):
    screen.fill((0, 0, 0))
    draw_custom_dungeon(screen, font_ascii, offset=0)  # Dibuja el fondo de la mazmora
    # UI simétrica: jugador a la izquierda, enemigo a la derecha
    UI_LEFT_X = 50
    UI_Y = 170  # name Y (a bit higher)
    # Calcular posición derecha exacta usando el ancho del texto
    enemy_text = f"{enemy.getName()}"
    enemy_text_width = font_text.size(enemy_text)[0]
    margin = 50
    UI_RIGHT_X = max(UI_LEFT_X + 200, screen.get_width() - margin - enemy_text_width)

    # Draw simple health bars under the names (white fill per aesthetic)
    BAR_WIDTH = 200
    BAR_HEIGHT = 16
    BAR_Y = UI_Y + 40  # increase gap so bars sit below the names

    # Player bar (left)
    player_hp = main_character.getHealth()
    player_max = inicial_player_health
    player_ratio = max(0.0, min(1.0, player_hp / player_max)) if player_max > 0 else 0
    player_bar_x = UI_LEFT_X
    pygame.draw.rect(screen, (80, 80, 80), (player_bar_x, BAR_Y, BAR_WIDTH, BAR_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (player_bar_x, BAR_Y, int(BAR_WIDTH * player_ratio), BAR_HEIGHT))

    # Enemy bar (right)
    enemy_hp = enemy.getHealth()
    enemy_max = hud_enemy_hp if hud_enemy_hp > 0 else enemy.getHealth()
    enemy_ratio = max(0.0, min(1.0, enemy_hp / enemy_max)) if enemy_max > 0 else 0
    enemy_bar_x = UI_RIGHT_X
    pygame.draw.rect(screen, (80, 80, 80), (enemy_bar_x, BAR_Y, BAR_WIDTH, BAR_HEIGHT))
    pygame.draw.rect(screen, (255, 255, 255), (enemy_bar_x, BAR_Y, int(BAR_WIDTH * enemy_ratio), BAR_HEIGHT))

    # Draw names + numeric HP on top of bars so they are not obscured
    draw_text(screen, font_text, f"{main_character.getName()}", UI_LEFT_X, UI_Y)
    draw_text(screen, font_text, enemy_text, UI_RIGHT_X, UI_Y)

    # Draw active toasts (short messages)
    try:
        from src.others import toast_manager
        toast_manager.draw(screen, font_text)
    except Exception:
        pass

    # Draw persistent combat message box last so it stays visible
    try:
        from src.others import combat_message_box
        # draw the persistent box (new draw_box returns multiple coords)
        try:
            combat_message_box.draw_box(screen, font_text)
        except TypeError:
            # backward compatibility
            combat_message_box.draw_box(screen, font_text)
    except Exception:
        pass


def dungeon(main_character, screen, font_ascii, font_text_combat):
    clock = pygame.time.Clock()
    player_x = screen.get_width() // 2 - 300
    player_y = 360
    enemies_valid = load_enemies(resource_path("src/db/enemyDb.json"), main_character)
    random.shuffle(enemies_valid)
    number_of_enemies = max(1, random.randint(main_character.getLevel() - 2, main_character.getLevel() + 3)) if main_character.getLevel() <= 15 else random.randint(12, 18)
    enemies_to_defeat = [copy.deepcopy(random.choice(enemies_valid)) for _ in range(number_of_enemies)]
    enemies_defeated = 0
    inicial_player_health = main_character.getHealth()
    steps_walked = 0
    steps_until_combat = random.randint(10, 20)
    offset = 0  # Offset inicial del fondo
    char_offset = 0  # Offset inicial del personaje

    background_sound.play(-1)


    draw_dungeon_static(screen, font_text_combat, font_ascii, inicial_player_health, main_character, offset, char_offset)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                background_sound.stop()
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        # Solo llamamos a dungeon_walking si se pulsa A o D
        if keys[pygame.K_d] or keys[pygame.K_a]:
            res = dungeon_walking(screen, font_text_combat, font_ascii, inicial_player_health, main_character, offset, char_offset, delay=100, steps_walked=steps_walked, steps_until_combat=steps_until_combat)
            # res puede ser (offset, steps_made, char_offset) o (offset, steps_made, char_offset, True)
            if isinstance(res, tuple) and len(res) >= 3:
                offset, steps_made, char_offset = res[0], res[1], res[2]
                steps_walked += steps_made

                # Si la función indicó interrumpir para combate, entra inmediatamente
                if len(res) == 4 and res[3] is True:
                    enemy_instance = enemies_to_defeat[enemies_defeated]
                    battle_start_sound.play()
                    time.sleep(1)
                    play_combat_intro(screen, font_ascii)
                    # pass current offsets so the combat can preserve/return them
                    combat_result = run_combat(main_character, screen, font_ascii, font_text_combat, player_x, player_y, inicial_player_health, enemy_instance, offset, char_offset)
                    # combat_result is a tuple (result_flag, offset, char_offset)
                    if isinstance(combat_result, tuple):
                        result_flag, offset, char_offset = combat_result
                        if result_flag == "defeat":
                            background_sound.stop()
                            return
                    else:
                        # If unexpected, stop the dungeon
                        background_sound.stop()
                        return

                    enemies_defeated += 1
                    steps_walked = 0
                    # reset steps until next combat: 999 para testing
                    steps_until_combat = random.randint(999, 999)

                    if enemies_defeated == len(enemies_to_defeat):
                        y_offset =+ 30
                        slow_print(screen, font_text_combat, "¡Has derrotado a todos los enemigos de la mazmorra!", 50, y_offset)
                        time.sleep(2)
                        # After showing the dungeon clear message, wait for user to press a key
                        try:
                            combat_message_box.show(screen, font_text_combat, "Presiona una tecla para continuar...", wait_for_key=True)
                        except Exception:
                            blocking_message(screen, font_text_combat, "Presiona una tecla para continuar...", 50, y_offset + 26, wait_for_key=True)
                        background_sound.stop()
                        return

        clock.tick(60)



def run_combat(main_character, screen, font_ascii, font_text_combat, player_x, player_y, inicial_player_health, enemy_instance, offset=0, char_offset=0):
    clock = pygame.time.Clock()
    player_attack_speed = main_character.getWeapon()["attack_ratio"]
    enemy_attack_speed = enemy_instance.getAttackRate()
    player_evade = main_character.getEvadeChance()
    enemy_evade = enemy_instance.getEvadeChance()
    player_active_states = []
    hud_enemy_hp = enemy_instance.getHealth()
    y_offset = 500

    last_player_attack = pygame.time.get_ticks()
    last_enemy_attack = pygame.time.get_ticks()

    while True:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "defeat"

        draw_combat_scene(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)

        # Comprobar si jugador puede atacar (basado en el ataque por segundo)
        if current_time - last_player_attack >= 1000 / player_attack_speed:
            evade_chance = random.uniform(0, 100)

            # Aplicar efectos activos que dañan salud al personaje (usar main_character)
            for active_state in player_active_states[:]:
                if "health" in active_state.get("effect", {}):
                    # Reducir la salud actual del personaje
                    main_character.setHealth(main_character.getHealth() + active_state["effect"]["health"])  # effect health es negativo en los JSON
                    # Show styled blocking message so it is readable over background
                    state_text = f"Pierdes {active_state['effect']['health']} puntos de salud debido al {active_state.get('state', active_state.get('name', 'un estado'))}."
                    try:
                        combat_message_box.show(screen, font_text_combat, state_text, timeout=1000)
                    except Exception:
                        draw_text(screen, font_text_combat, state_text, 50, y_offset + 30)
                    player_active_states.remove(active_state)

            # Enemy may evade or be hit; these functions now return message strings
            if evade_chance < enemy_evade:
                msg = enemy_instance.evade(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance, y_offset)
            else:
                msg = main_character.player_attack(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance, y_offset)

            if msg:
                try:
                    combat_message_box.show(screen, font_text_combat, msg, timeout=900)
                except Exception:
                    blocking_message(screen, font_text_combat, msg, 50, y_offset + 30, timeout=900)
                pygame.time.wait(200)
            
            if enemy_instance.getHealth() <= 0:
                victory_msg = main_character.player_victory(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance, y_offset)
                # Show the victory message typed and wait a bit for the player to read
                if victory_msg:
                    # Support either a single string or a list of strings
                    if isinstance(victory_msg, (list, tuple)):
                        # show two lines slightly lower and styled; second line waits for key
                        left_x = 50
                        base_y = y_offset + 10
                        try:
                            # show first victory line briefly, then show rewards line without blocking
                            combat_message_box.show(screen, font_text_combat, victory_msg[0], timeout=1400)
                            combat_message_box.show(screen, font_text_combat, victory_msg[1], timeout=1400)
                        except Exception:
                            blocking_message(screen, font_text_combat, victory_msg[0], left_x, base_y, timeout=1400, bg_color=(0,0,0,200), border_color=(200,200,200))
                            # show rewards line with timeout (do not wait for key here)
                            blocking_message(screen, font_text_combat, victory_msg[1], left_x, base_y + 26, timeout=1400, bg_color=(0,0,0,200), border_color=(200,200,200))
                        # After victory messages, show explicit 'press any key to continue' prompt
                        try:
                            combat_message_box.show(screen, font_text_combat, "Presiona una tecla para continuar...", wait_for_key=True)
                        except Exception:
                            blocking_message(screen, font_text_combat, "Presiona una tecla para continuar...", 50, base_y + 56, wait_for_key=True)
                    else:
                        blocking_message(screen, font_text_combat, victory_msg, 50, y_offset, timeout=1600)

                if main_character.getExperience() >= main_character.getToNextLevel():
                    y_offset += 30
                    main_character.next_level(screen, font_text_combat, y_offset)

                pygame.display.flip()
                pygame.time.wait(800)
                break
            last_player_attack = current_time

        # Comprobar si enemigo puede atacar
        if current_time - last_enemy_attack >= 1000 / enemy_attack_speed:
            evade_chance = random.uniform(0, 100)

            if evade_chance < player_evade:
                msg = main_character.player_evade(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance, y_offset)
                if msg:
                    try:
                        combat_message_box.show(screen, font_text_combat, msg, timeout=700)
                    except Exception:
                        blocking_message(screen, font_text_combat, msg, 50, y_offset + 30, timeout=700)
            else:
                msg = enemy_instance.attack(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance, y_offset)
                if msg:
                    try:
                        combat_message_box.show(screen, font_text_combat, msg, timeout=900)
                    except Exception:
                        blocking_message(screen, font_text_combat, msg, 50, y_offset + 30, timeout=900)

                if enemy_instance.getState():
                    apply_effect_chance = random.uniform(0, 100)
                    if apply_effect_chance < enemy_instance.state[0]["chance"]:
                        # apply_state expects the main character as the first argument and now returns a message
                        state_msg = enemy_instance.apply_state(main_character, screen, font_text_combat, y_offset)
                        if main_character.getState():
                            player_active_states.append(main_character.getState())
                        if state_msg:
                            try:
                                combat_message_box.show(screen, font_text_combat, state_msg, timeout=1000)
                            except Exception:
                                blocking_message(screen, font_text_combat, state_msg, 50, y_offset + 30, timeout=1000)

            last_enemy_attack = current_time

        # Revisar condiciones de derrota/victoria

        if main_character.getHealth() <= 0:
            slow_print(screen, font_text_combat, "Te has quedado sin puntos de salud...", 50, y_offset, clear_area=True)
            y_offset += 30
            slow_print(screen, font_text_combat, f"El {enemy_instance.getName()} te ha derrotado...", 50, y_offset, clear_area=True)
            exp_lost = main_character.getExperience() * 0.20
            main_character.setExperience(main_character.getExperience() - exp_lost)
            y_offset += 30
            slow_print(screen, font_text_combat, f"Has perdido {round(exp_lost)} experiencia.", 50, y_offset, clear_area=True)
            main_character.setHealth(inicial_player_health)
            pygame.display.flip()
            pygame.time.wait(2000)
            return "defeat"


        pygame.display.flip()
        clock.tick(60)  # Limitar a 60 FPS
        
    # After combat, return control and preserve the last offsets so the player appears
    # where they left off instead of resetting to initial position.
    return "victory", offset, char_offset
    
