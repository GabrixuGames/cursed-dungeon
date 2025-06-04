import pygame, copy, random, time
from src.object.enemy import load_enemies
from src.others import resource_path, draw_text, slow_print, draw_custom_dungeon
from src.animations.walking import dungeon_walking, draw_dungeon_static
from src.animations.animations import play_combat_intro




background_sound = pygame.mixer.Sound("src/sounds/ambience_sound.mp3")  # Ajusta la ruta
background_sound.set_volume(0.05)  # Ajusta el volumen según sea necesario
battle_start_sound = pygame.mixer.Sound(resource_path("src/sounds/battle_start.mp3"))
battle_start_sound.set_volume(0.5)  # Ajusta el volumen según sea necesario


def draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy):
    screen.fill((0, 0, 0))
    draw_custom_dungeon(screen, font_ascii, offset=0)  # Dibuja el fondo de la mazmora
    draw_text(screen, font_text, f"Salud: {mainChar.getHealth()}/{inicial_player_health} HP", 50, 200)
    draw_text(screen, font_text, f"{enemy.getName()}: {enemy.getHealth()}/{hud_enemy_hp} HP", 750, 200)


def dungeon(mainChar, screen, font_ascii, font_text_combat):
    clock = pygame.time.Clock()
    player_x = screen.get_width() // 2 - 300
    player_y = 360
    enemies_valid = load_enemies(resource_path("src/db/enemyDb.json"), mainChar)
    random.shuffle(enemies_valid)
    number_of_enemies = max(1, random.randint(mainChar.getLevel() - 2, mainChar.getLevel() + 3)) if mainChar.getLevel() <= 15 else random.randint(12, 18)
    enemies_to_defeat = [copy.deepcopy(random.choice(enemies_valid)) for _ in range(number_of_enemies)]
    enemies_defeaten = 0
    inicial_player_health = mainChar.getHealth()
    steps_walked = 0
    steps_until_combat = random.randint(10, 20)
    offset = 0  # Offset inicial del fondo
    char_offset = 0  # Offset inicial del personaje

    background_sound.play(-1)


    draw_dungeon_static(screen, font_text_combat, font_ascii, inicial_player_health, mainChar, offset)

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
            offset, steps_made, char_offset = dungeon_walking(screen, font_text_combat, font_ascii, inicial_player_health, mainChar, offset, char_offset)
            steps_walked += steps_made
            print(f"Steps walked: {steps_walked}, Steps until combat: {steps_until_combat}")

            if steps_walked >= steps_until_combat:
                enemy_instance = enemies_to_defeat[enemies_defeaten]
                battle_start_sound.play()
                time.sleep(1)
                play_combat_intro(screen, font_ascii)
                combat_result = run_combat(mainChar, screen, font_ascii, font_text_combat, player_x, player_y, inicial_player_health, enemy_instance)
                if combat_result == "defeat":
                    background_sound.stop()
                    return
                enemies_defeaten += 1
                steps_walked = 0
                steps_until_combat = random.randint(10, 20)

                if enemies_defeaten == len(enemies_to_defeat):
                    y_offset =+ 30
                    slow_print(screen, font_text_combat, "¡Has derrotado a todos los enemigos de la mazmorra!", 50, y_offset)
                    time.sleep(2)
                    background_sound.stop()
                    return

        clock.tick(60)



def run_combat(mainChar, screen, font_ascii, font_text_combat, player_x, player_y, inicial_player_health, enemy_instance):
    clock = pygame.time.Clock()
    player_attack_speed = mainChar.getWeapon()["attack_ratio"]
    enemy_attack_speed = enemy_instance.getAttackRate()
    player_evade = mainChar.getEvadeChance()
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

        draw_combat_scene(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance)

        # Comprobar si jugador puede atacar (basado en el ataque por segundo)
        if current_time - last_player_attack >= 1000 / player_attack_speed:
            evade_chance = random.uniform(0, 100)

            # Aplicar efectos activos que dañan salud
            for active_state in player_active_states[:]:
                if "health" in active_state["effect"]:
                    inicial_player_health -= active_state["effect"]["health"]
                    y_offset += 30
                    draw_text(screen, font_text_combat, f"Pierdes {active_state['effect']['health']} puntos de salud debido al {active_state['name']}.", 50, y_offset)
                    player_active_states.remove(active_state)

            if evade_chance < enemy_evade:
                enemy_instance.evade(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance, y_offset)
            else:
                mainChar.player_attack(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance, y_offset)
            
            if enemy_instance.getHealth() <= 0:
                mainChar.player_victory(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance, y_offset)

                if mainChar.getExperience() >= mainChar.getToNextLevel():
                    y_offset += 30
                    mainChar.next_level(screen, font_text_combat, y_offset)

                pygame.display.flip()
                pygame.time.wait(1000)
                break
            last_player_attack = current_time

        # Comprobar si enemigo puede atacar
        if current_time - last_enemy_attack >= 1000 / enemy_attack_speed:
            evade_chance = random.uniform(0, 100)

            if evade_chance < player_evade:
                mainChar.player_evade(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance, y_offset)
            else:
                enemy_instance.attack(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance, y_offset)

                if enemy_instance.getState():
                    apply_effect_chance = random.uniform(0, 100)
                    if apply_effect_chance < enemy_instance.state[0]["chance"]:
                        enemy_instance.apply_state(enemy_instance, screen, font_text_combat, y_offset)
                        player_active_states.append(enemy_instance.getState())

            last_enemy_attack = current_time

        # Revisar condiciones de derrota/victoria

        if mainChar.getHealth() <= 0:
            slow_print(screen, font_text_combat, "Te has quedado sin puntos de salud...", 50, y_offset)
            y_offset += 30
            slow_print(screen, font_text_combat, f"El {enemy_instance.getName()} te ha derrotado...", 50, y_offset)
            exp_lost = mainChar.getExperience() * 0.20
            mainChar.setExperience(mainChar.getExperience() - exp_lost)
            y_offset += 30
            slow_print(screen, font_text_combat, f"Has perdido {round(exp_lost)} experiencia.", 50, y_offset)
            mainChar.setHealth(inicial_player_health)
            pygame.display.flip()
            pygame.time.wait(2000)
            return "defeat"


        pygame.display.flip()
        clock.tick(60)  # Limitar a 60 FPS
        
    offset = 0
    draw_dungeon_static(screen, font_text_combat, font_ascii, inicial_player_health, mainChar, offset)
    return "victory"
    
