import pygame, copy, random, time
from typing import List, Dict
from src.object.enemy import load_enemies
from src.others import resource_path, draw_text, slow_print, draw_custom_dungeon, blocking_message, combat_message_box
from src.animations.walking import dungeon_walking, draw_dungeon_static
from src.animations.animations import play_combat_intro




background_sound = pygame.mixer.Sound("src/sounds/ambience_sound.mp3")  # Ajusta la ruta
background_sound.set_volume(0.05)  # Ajusta el volumen según sea necesario
battle_start_sound = pygame.mixer.Sound(resource_path("src/sounds/battle_start.mp3"))
battle_start_sound.set_volume(0.5)  # Ajusta el volumen según sea necesario


def draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy):
    """
    Dibuja la escena de combate mejorada.
    
    Mejoras FASE 5:
    - Nombres y barras reposicionadas más arriba (Y=80)
    - Barra de maná añadida para el jugador
    - Mejor espaciado y legibilidad
    - Números de HP/MP visibles
    
    Agente: FrontendSenior
    """
    screen.fill((0, 0, 0))
    draw_custom_dungeon(screen, font_ascii, offset=0)
    
    # === CONSTANTES DE UI ===
    UI_LEFT_X = 50
    NAME_Y = 80
    TEXT_SPACING = 26
    
    # === JUGADOR (IZQUIERDA) ===
    # Nombre del jugador
    player_name = main_character.getName()
    player_level = main_character.getLevel()
    player_name_text = f"{player_name} (Nv.{player_level})"
    draw_text(screen, font_text, player_name_text, UI_LEFT_X, NAME_Y, (220, 220, 255))
    
    # HP del jugador (solo texto)
    hp_y = NAME_Y + TEXT_SPACING
    player_hp = main_character.getHealth()
    player_max_hp = inicial_player_health
    hp_text = f"HP: {int(player_hp)}/{int(player_max_hp)}"
    draw_text(screen, font_text, hp_text, UI_LEFT_X, hp_y, (255, 255, 255))

    # MP del jugador (solo texto)
    if hasattr(main_character, 'skill_manager') and main_character.skill_manager:
        mp_y = hp_y + TEXT_SPACING
        player_mp = main_character.skill_manager.current_mana
        player_max_mp = main_character.skill_manager.max_mana
        mp_text = f"MP: {int(player_mp)}/{int(player_max_mp)}"
        draw_text(screen, font_text, mp_text, UI_LEFT_X, mp_y, (200, 220, 255))
    
    # === ENEMIGO (DERECHA) ===
    # Nombre del enemigo
    enemy_name = enemy.getName()
    enemy_text = f"{enemy_name}"
    enemy_text_width = font_text.size(enemy_text)[0]
    # HP del enemigo (solo texto)
    enemy_hp_y = NAME_Y + TEXT_SPACING
    enemy_hp = enemy.getHealth()
    enemy_max_hp = hud_enemy_hp if hud_enemy_hp > 0 else enemy.getHealth()
    enemy_hp_text = f"HP: {int(enemy_hp)}/{int(enemy_max_hp)}"
    enemy_hp_text_width = font_text.size(enemy_hp_text)[0]
    UI_RIGHT_X = screen.get_width() - 50 - max(enemy_text_width, enemy_hp_text_width)
    draw_text(screen, font_text, enemy_text, UI_RIGHT_X, NAME_Y, (255, 220, 220))
    draw_text(screen, font_text, enemy_hp_text, UI_RIGHT_X, enemy_hp_y, (255, 255, 255))
    
    # === TOASTS (NOTIFICACIONES TEMPORALES) ===
    try:
        from src.others import toast_manager
        toast_manager.draw(screen, font_text)
    except Exception:
        pass

    # === COMBAT MESSAGE BOX (FONDO FIJO) ===
    message_box_rect = None
    try:
        from src.others import combat_message_box
        box_x, box_y, box_w, box_h, inner_x, inner_y, inner_w, inner_h = combat_message_box.draw_box(screen, font_text)
        message_box_rect = (inner_x, inner_y, inner_w, inner_h)
    except Exception:
        message_box_rect = None

    return message_box_rect


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
    # Rango dinámico de pasos antes del combate (más desafiante en niveles altos)
    min_steps = max(3, 8 - (main_character.getLevel() // 10))
    max_steps = max(5, 15 - (main_character.getLevel() // 8))
    steps_until_combat = random.randint(min_steps, max_steps)
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
    """
    Loop principal de combate por turnos.
    
    Agente: GameDevSenior - Refactorizado para sistema de turnos
    """
    from levels.combat_manager import create_combat_manager
    from levels.combat_menu import create_combat_menu
    
    clock = pygame.time.Clock()
    player_evade = main_character.getEvadeChance()
    enemy_evade = enemy_instance.getEvadeChance()
    hud_enemy_hp = enemy_instance.getHealth()
    y_offset = 500

    # Inicializar sistema de turnos
    combat_mgr = create_combat_manager(main_character, enemy_instance)
    combat_menu = create_combat_menu()

    # Asegurar inventario cargado para usar items en combate
    if not hasattr(main_character, 'inventory_manager') or main_character.inventory_manager is None:
        from src.inventory_system import get_inventory_manager
        main_character.inventory_manager = get_inventory_manager()
    if main_character.inventory_manager and not getattr(main_character.inventory_manager, "_item_db", None):
        try:
            main_character.inventory_manager.load_item_database()
        except Exception:
            pass
    
    # Resetear maná al inicio del combate
    if hasattr(main_character, 'skill_manager') and main_character.skill_manager:
        main_character.skill_manager.reset_mana()
    
    waiting_for_player_action = False
    action_to_execute = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "defeat"
            
            # Solo procesar input si es turno del jugador y estamos esperando
            if waiting_for_player_action:
                action = combat_menu.handle_input(event)
                
                if action == "navigate":
                    # Solo redibujar
                    pass
                elif action == "skill_menu":
                    # Abrir submenú de habilidades
                    skills_list = _get_available_skills(main_character)
                    combat_menu.open_submenu("skill", skills_list)
                elif action == "item_menu":
                    # Abrir submenú de items
                    items_list = _get_usable_items(main_character)
                    combat_menu.open_submenu("item", items_list)
                elif action == "back":
                    # Volver al menú principal
                    pass
                elif action:
                    # Acción válida seleccionada
                    action_to_execute = action
                    waiting_for_player_action = False

        # Dibujar escena de combate
        message_box_rect = draw_combat_scene(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)
        
        # Verificar si el combate ha terminado
        is_over, result = combat_mgr.is_combat_over()
        if is_over:
            if result == "victory":
                # TRACKING: Enemy defeated
                main_character.track_enemy_defeat()
                
                # TRACKING: Flawless combat (si no recibió daño)
                main_character.track_flawless_combat(inicial_player_health)
                
                victory_msg = main_character.player_victory(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance, y_offset)
                if victory_msg:
                    if isinstance(victory_msg, (list, tuple)):
                        try:
                            combat_message_box.show(screen, font_text_combat, victory_msg[0], timeout=1400)
                            combat_message_box.show(screen, font_text_combat, victory_msg[1], timeout=1400)
                        except Exception:
                            blocking_message(screen, font_text_combat, victory_msg[0], 50, y_offset + 10, timeout=1400)
                            blocking_message(screen, font_text_combat, victory_msg[1], 50, y_offset + 36, timeout=1400)
                        try:
                            combat_message_box.show(screen, font_text_combat, "Presiona una tecla para continuar...", wait_for_key=True)
                        except Exception:
                            blocking_message(screen, font_text_combat, "Presiona una tecla para continuar...", 50, y_offset + 56, wait_for_key=True)
                    else:
                        blocking_message(screen, font_text_combat, victory_msg, 50, y_offset, timeout=1600)

                if main_character.getExperience() >= main_character.getToNextLevel():
                    y_offset += 30
                    main_character.next_level(screen, font_text_combat, y_offset)

                pygame.display.flip()
                pygame.time.wait(800)
                return "victory", offset, char_offset
            
            elif result == "defeat":
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
            
            elif result == "flee":
                # TRACKING: Flee success
                main_character.track_flee()
                
                try:
                    combat_message_box.show(screen, font_text_combat, "Has escapado del combate.", timeout=1400)
                except Exception:
                    blocking_message(screen, font_text_combat, "Has escapado del combate.", 50, y_offset, timeout=1400)
                pygame.display.flip()
                pygame.time.wait(1000)
                return "victory", offset, char_offset  # Tratamos huida como victoria parcial
        
        # Obtener turno actual
        current_turn = combat_mgr.get_current_turn()
        
        # TURNO DEL JUGADOR
        if current_turn == "player" and not waiting_for_player_action and action_to_execute is None:
            # Procesar estados alterados antes de permitir acción
            state_msg = combat_mgr.process_player_state_effects()
            if state_msg:
                try:
                    combat_message_box.show(screen, font_text_combat, state_msg, timeout=1000)
                except Exception:
                    draw_text(screen, font_text_combat, state_msg, 50, y_offset + 30)
                pygame.display.flip()
                pygame.time.wait(1000)
            
            # Mostrar menú y esperar acción
            waiting_for_player_action = True
        
        # Ejecutar acción del jugador
        if action_to_execute:
            _execute_player_action(action_to_execute, main_character, enemy_instance, combat_mgr, 
                                  screen, font_ascii, font_text_combat, player_x, player_y, 
                                  inicial_player_health, hud_enemy_hp, y_offset, 
                                  player_evade, enemy_evade)
            
            action_to_execute = None
            combat_mgr.end_turn()
            pygame.display.flip()
            pygame.time.wait(500)  # Pausa breve entre turnos
        
        # TURNO DEL ENEMIGO
        elif current_turn == "enemy":
            # El enemigo ataca automáticamente
            evade_chance = random.uniform(0, 100)

            if evade_chance < player_evade:
                # TRACKING: Dodge successful
                main_character.track_dodge()
                
                msg = main_character.player_evade(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance, y_offset)
                if msg:
                    try:
                        combat_message_box.show(screen, font_text_combat, msg, timeout=700)
                    except Exception:
                        blocking_message(screen, font_text_combat, msg, 50, y_offset + 30, timeout=700)
            else:
                # TRACKING: Reset dodge streak (received damage)
                main_character.reset_dodge_streak()
                
                msg = enemy_instance.attack(screen, font_text_combat, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance, y_offset)
                if msg:
                    try:
                        combat_message_box.show(screen, font_text_combat, msg, timeout=900)
                    except Exception:
                        blocking_message(screen, font_text_combat, msg, 50, y_offset + 30, timeout=900)

                # Aplicar estados alterados
                if enemy_instance.getState():
                    apply_effect_chance = random.uniform(0, 100)
                    if apply_effect_chance < enemy_instance.state[0]["chance"]:
                        state_msg = enemy_instance.apply_state(main_character, screen, font_text_combat, y_offset)
                        if state_msg:
                            try:
                                combat_message_box.show(screen, font_text_combat, state_msg, timeout=1000)
                            except Exception:
                                blocking_message(screen, font_text_combat, state_msg, 50, y_offset + 30, timeout=1000)

            pygame.display.flip()
            pygame.time.wait(1000)  # Pausa para que el jugador vea el ataque del enemigo
            combat_mgr.end_turn()
        
        # Dibujar menú si es turno del jugador
        if current_turn == "player" and waiting_for_player_action:
            context = {
                "player": main_character,
                "enemy": enemy_instance,
                "combat_mgr": combat_mgr,
            }
            combat_menu.draw(screen, font_text_combat, inline_rect=message_box_rect, context=context)

        pygame.display.flip()
        clock.tick(60)


def _get_available_skills(main_character) -> List[Dict]:
    """
    Obtiene la lista de habilidades disponibles para el menú.
    
    Args:
        main_character: Instancia de MainCharacter
    
    Returns:
        Lista de diccionarios con información de habilidades
    """
    if not hasattr(main_character, 'skill_manager') or not main_character.skill_manager:
        return []
    
    skills_list = []
    skill_mgr = main_character.skill_manager
    
    for skill_id, skill in skill_mgr.skills_db.items():
        # Verificar si el jugador tiene el nivel requerido
        if main_character.getLevel() < skill.level_required:
            continue
        
        # Verificar si puede usar la habilidad
        can_use, reason = skill_mgr.can_use_skill(skill_id)
        
        skills_list.append({
            "id": skill_id,
            "name": skill.name,
            "description": skill.description,
            "mana_cost": skill.mana_cost,
            "damage_multiplier": skill.damage_multiplier,
            "skill_type": skill.skill_type,
            "available": can_use,
            "reason": reason if not can_use else ""
        })
    
    return skills_list


def _get_usable_items(main_character) -> List[Dict]:
    """
    Obtiene la lista de items usables en combate.
    
    Args:
        main_character: Instancia de MainCharacter
    
    Returns:
        Lista de diccionarios con información de items
    """
    if not hasattr(main_character, 'inventory_manager') or not main_character.inventory_manager:
        return []
    
    items_list = []
    inv_mgr = main_character.inventory_manager
    if not getattr(inv_mgr, "_item_db", None):
        try:
            inv_mgr.load_item_database()
        except Exception:
            return []
    
    # Obtener items usables en combate
    usable_items = inv_mgr.get_usable_items(context="combat")
    
    for item, quantity in usable_items:
        items_list.append({
            "id": item.id,
            "name": item.get_display_name(),
            "description": item.description,
            "quantity": quantity
        })
    
    return items_list


def _execute_player_action(action: str, player, enemy, combat_mgr, screen, font_ascii, font_text, 
                           player_x, player_y, inicial_player_health, hud_enemy_hp, y_offset, 
                           player_evade, enemy_evade):
    """
    Ejecuta la acción seleccionada por el jugador.
    
    Args:
        action: Acción a ejecutar
        player: MainCharacter
        enemy: Enemy
        combat_mgr: CombatManager
        screen: Superficie de pygame
        font_ascii: Fuente ASCII
        font_text: Fuente de texto
        player_x, player_y: Posiciones del jugador
        inicial_player_health: HP inicial del jugador
        hud_enemy_hp: HP inicial del enemigo
        y_offset: Offset vertical para mensajes
        player_evade: % de evasión del jugador
        enemy_evade: % de evasión del enemigo
    
    Agente: GameDevSenior
    """
    # ATACAR
    if action == "attack":
        evade_chance = random.uniform(0, 100)
        
        if evade_chance < enemy_evade:
            msg = enemy.evade(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, player, enemy, y_offset)
        else:
            msg = player.player_attack(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, player, enemy, y_offset)

        if msg:
            try:
                combat_message_box.show(screen, font_text, msg, timeout=900)
            except Exception:
                blocking_message(screen, font_text, msg, 50, y_offset + 30, timeout=900)
            pygame.time.wait(200)
    
    # HUIR
    elif action == "flee":
        success, msg = combat_mgr.attempt_flee()
        
        try:
            combat_message_box.show(screen, font_text, msg, timeout=1200)
        except Exception:
            blocking_message(screen, font_text, msg, 50, y_offset + 30, timeout=1200)
        
        pygame.display.flip()
        pygame.time.wait(1200)
        
        # Si falla la huida, el enemigo ataca gratis
        if not success:
            pygame.time.wait(500)
            enemy_msg = enemy.attack(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, player, enemy, y_offset)
            if enemy_msg:
                try:
                    combat_message_box.show(screen, font_text, f"¡El enemigo aprovecha! {enemy_msg}", timeout=1200)
                except Exception:
                    blocking_message(screen, font_text, f"¡El enemigo aprovecha! {enemy_msg}", 50, y_offset + 30, timeout=1200)
            pygame.display.flip()
            pygame.time.wait(1000)
    
    # USAR HABILIDAD
    elif action.startswith("use_skill:"):
        skill_id = action.split(":")[1]
        _use_skill(skill_id, player, enemy, screen, font_ascii, font_text, player_x, player_y, 
                  inicial_player_health, hud_enemy_hp, y_offset, enemy_evade)
    
    # USAR ITEM
    elif action.startswith("use_item:"):
        item_id = action.split(":")[1]
        _use_item(item_id, player, enemy, screen, font_text, y_offset)


def _use_skill(skill_id: str, player, enemy, screen, font_ascii, font_text, 
               player_x, player_y, inicial_player_health, hud_enemy_hp, y_offset, enemy_evade):
    """
    Ejecuta una habilidad del jugador.
    
    Args:
        skill_id: ID de la habilidad
        player: MainCharacter
        enemy: Enemy
        screen, font_ascii, font_text: Parámetros de renderizado
        player_x, player_y: Posiciones
        inicial_player_health, hud_enemy_hp: HP para HUD
        y_offset: Offset para mensajes
        enemy_evade: % de evasión del enemigo
    
    Agente: GameDevSenior
    """
    if not hasattr(player, 'skill_manager') or not player.skill_manager:
        return
    
    skill_mgr = player.skill_manager
    skill = skill_mgr.get_skill_info(skill_id)
    
    if not skill:
        return
    
    # Usar la habilidad (consume maná y activa cooldown)
    if not skill_mgr.use_skill(skill_id):
        msg = f"No puedes usar {skill.name}."
        try:
            combat_message_box.show(screen, font_text, msg, timeout=1000)
        except Exception:
            blocking_message(screen, font_text, msg, 50, y_offset + 30, timeout=1000)
        return
    
    # TRACKING: Skill used
    player.track_skill_use()
    
    # Aplicar efectos especiales (curación, buffs, etc.)
    effects = skill_mgr.apply_skill_effects(skill_id, player, enemy)
    
    # Calcular daño si es habilidad de ataque
    if skill.damage_multiplier > 0:
        # Verificar evasión
        evade_chance = random.uniform(0, 100)
        
        # Algunas habilidades ignoran evasión
        actual_evade = enemy_evade
        if "ignore_evade" in skill.effects:
            actual_evade *= (1 - skill.effects["ignore_evade"])
        
        if evade_chance < actual_evade:
            msg = f"¡{enemy.getName()} esquivó {skill.name}!"
            try:
                combat_message_box.show(screen, font_text, msg, timeout=900)
            except Exception:
                blocking_message(screen, font_text, msg, 50, y_offset + 30, timeout=900)
        else:
            # Calcular daño
            base_damage = player.getDamage()
            skill_damage = skill_mgr.calculate_skill_damage(skill_id, base_damage)
            
            # Aplicar daño
            enemy.setHealth(enemy.getHealth() - skill_damage)
            
            # Robo de vida si aplica
            if "lifesteal" in effects:
                heal_amount = int(skill_damage * effects["lifesteal"])
                player.setHealth(min(player.getHealth() + heal_amount, player._max_health))
                effects["heal"] = heal_amount
            
            # Mostrar animación de ataque
            from src.animations.animations import animation_player_atack
            animation_player_atack(screen, font_text, font_ascii, player_x, player_y, 
                                 inicial_player_health, hud_enemy_hp, player, enemy)
            
            # Mensaje de daño
            msg = f"¡{skill.name}! {skill_damage} de daño."
            try:
                combat_message_box.show(screen, font_text, msg, timeout=1000)
            except Exception:
                blocking_message(screen, font_text, msg, 50, y_offset + 30, timeout=1000)
    
    # Mensajes de efectos adicionales
    if "heal" in effects:
        msg = f"Recuperaste {effects['heal']} HP."
        try:
            combat_message_box.show(screen, font_text, msg, timeout=800)
        except Exception:
            draw_text(screen, font_text, msg, 50, y_offset + 50)
    
    pygame.display.flip()
    pygame.time.wait(500)


def _use_item(item_id: str, player, enemy, screen, font_text, y_offset):
    """
    Usa un item del inventario.
    
    Args:
        item_id: ID del item
        player: MainCharacter
        enemy: Enemy (puede ser objetivo)
        screen: Superficie de pygame
        font_text: Fuente de texto
        y_offset: Offset para mensajes
    
    Agente: GameDevSenior
    """
    if not hasattr(player, 'inventory_manager') or not player.inventory_manager:
        return
    
    inv_mgr = player.inventory_manager
    
    # Determinar el objetivo
    item = inv_mgr.get_item(item_id)
    if not item:
        return
    
    target = player if item.target == "self" else enemy
    
    # Usar el item
    success, msg = inv_mgr.use_item(item_id, target, context="combat")
    
    # TRACKING: Item used (solo si fue exitoso)
    if success:
        player.track_item_use()
    
    if msg:
        try:
            combat_message_box.show(screen, font_text, msg, timeout=1200)
        except Exception:
            blocking_message(screen, font_text, msg, 50, y_offset + 30, timeout=1200)
    
    pygame.display.flip()
    pygame.time.wait(800)


# Resto del código original se mantiene igual
    
