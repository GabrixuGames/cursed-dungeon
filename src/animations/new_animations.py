"""
Sistema de animaciones mejorado para Cursed Dungeon
Todas las animaciones rediseñadas con arte ASCII cohesivo
"""

import pygame, random, os
from src.others import draw_text

pygame.mixer.init()
sound_dir = os.path.join(os.path.dirname(__file__), '..', 'sounds')
player_atack_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'player_atack.mp3'))
player_atack_sound.set_volume(0.75)
enemy_atack_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'monster_atack.mp3'))
enemy_atack_sound.set_volume(0.4)
enemy_die_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'monster_died.wav'))
enemy_die_sound.set_volume(0.5)
atack_fail_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'atack_fail.mp3'))
atack_fail_sound.set_volume(0.6)

def draw_character(screen, font_ascii, x, y, character, color=(255, 255, 255)):
    """Dibuja un personaje ASCII con espaciado consistente"""
    for i, line in enumerate(character.splitlines()):
        draw_text(screen, font_ascii, line, x, y + i * 28, color)

def draw_side_by_side(screen, font_ascii, player_x, player_y, player_art, enemy_art, player_color=(255, 255, 255), enemy_color=(255, 100, 100)):
    """Dibuja jugador y enemigo lado a lado"""
    # Jugador a la izquierda
    draw_character(screen, font_ascii, player_x, player_y, player_art, player_color)
    # Enemigo a la derecha (posición fija para consistencia)
    enemy_x = player_x + 350
    draw_character(screen, font_ascii, enemy_x, player_y, enemy_art, enemy_color)

# ===== ARTE ASCII MEJORADO =====

# JUGADOR - Estados normales
PLAYER_IDLE = r"""
    ╭─╮
    │ │
    ╰─╯
     │
   ╱─┼─╲
  ╱  │  ╲
 ╱   │   ╲
│    │    │
╰─╮ ╱╲ ╭─╯
  │╱  ╲│
  ╱    ╲
 ╱      ╲
"""

PLAYER_ATTACK_1 = r"""
    ╭─╮
    │ │
    ╰─╯     ⚔
     │    ╱
   ╱─┼─╲╱
  ╱  │  ╲
 ╱   │   ╲
│    │    │
╰─╮ ╱╲ ╭─╯
  │╱  ╲│
  ╱    ╲
 ╱      ╲
"""

PLAYER_ATTACK_2 = r"""
    ╭─╮
    │ │      ⚔═══
    ╰─╯    ╱
     │   ╱
   ╱─┼─╲
  ╱  │  ╲
 ╱   │   ╲
│    │    │
╰─╮ ╱╲ ╭─╯
  │╱  ╲│
  ╱    ╲
 ╱      ╲
"""

PLAYER_ATTACK_3 = r"""
    ╭─╮   ★ ⚔
    │ │    ╲
    ╰─╯     ╲
     │       ╲
   ╱─┼─╲     ╲
  ╱  │  ╲
 ╱   │   ╲
│    │    │
╰─╮ ╱╲ ╭─╯
  │╱  ╲│
  ╱    ╲
 ╱      ╲
"""

PLAYER_DEFEND = r"""
    ╭─╮
    │ │
    ╰─╯
     │
  ┌──┼──┐
 ╱   │   ╲
╱    │    ╲
│    │    │
╰─╮ ╱╲ ╭─╯
  │╱  ╲│
  ╱    ╲
 ╱      ╲
"""

PLAYER_HURT = r"""
    ╭─╮  ×
    │×│
    ╰─╯
     │
   ╱─┼─╲
  ╱  │  ╲
 ╱   │   ╲ ×
│    │    │
╰─╮ ╱╲ ╭─╯
  │╱  ╲│
  ╱    ╲
 ╱      ╲
"""

PLAYER_VICTORY = r"""
    ╭─╮  ★
    │^│   ★
    ╰─╯
     │
   ╲─┼─╱
    ╲│╱
     ╲╱   ★
  ╲   │   ╱
   ╲ ╱╲ ╱
    ╱  ╲
   ╱    ╲
  ╱      ╲
"""

PLAYER_DEAD = r"""
      ×
    ╭─╮
    │×│
    ╰─╯
    ╱│╲
   ╱ │ ╲   ×
  ╱  │  ╲
════════════
    ╱╲
   ╱  ╲
  ╱    ╲
"""

# ENEMIGO - Estados
ENEMY_IDLE = r"""
     ▄▄▄
   ╱     ╲
  │  ◉ ◉  │
  │    ∩   │
   ╲  ═══ ╱
    ╲     ╱
     │▄▄▄│
     │███│
   ╱─┴───┴─╲
  ╱  │   │  ╲
 ╱   │   │   ╲
│    │   │    │
╰─╮ ╱╲ ╱╲ ╭─╯
  │╱  ╲╱  ╲│
"""

ENEMY_ATTACK_1 = r"""
     ▄▄▄
   ╱     ╲
  │  ◉ ◉  │  ★
  │    ∩   │
   ╲  ╤╤╤ ╱
    ╲╱ │ ╲╱
     │▄▄▄│
     │███│
   ╱─┴───┴─╲
  ╱  │   │  ╲
 ╱   │   │   ╲
│    │   │    │
╰─╮ ╱╲ ╱╲ ╭─╯
  │╱  ╲╱  ╲│
"""

ENEMY_ATTACK_2 = r"""
     ▄▄▄      ⚡
   ╱     ╲   ╱
  │  ◉ ◉  │ ╱
  │    ∩   │╱
   ╲  ▼▼▼ ╱
    ╲     ╱
     │▄▄▄│
     │███│
   ╱─┴───┴─╲
  ╱  │   │  ╲  ⚡
 ╱   │   │   ╲
│    │   │    │
╰─╮ ╱╲ ╱╲ ╭─╯
  │╱  ╲╱  ╲│
"""

ENEMY_HURT = r"""
     ▄×▄
   ╱  ×  ╲
  │  ◉ ◉  │
  │    ∩   │
   ╲  ─── ╱
    ╲ ××× ╱
     │▄▄▄│
     │███│
   ╱─┴───┴─╲
  ╱  │ × │  ╲
 ╱   │   │   ╲
│    │   │    │
╰─╮ ╱╲ ╱╲ ╭─╯
  │╱  ╲╱  ╲│
"""

ENEMY_DYING = r"""
     ▄×▄
   ╱  ×  ╲
  │  × ×  │
  │    ∩   │    ×
   ╲  ~~~ ╱
    ╲ ××× ╱
     │▄××│
     │×××│  ×
   ╱─┴───┴─╲
  ╱  │ × │  ╲
 ╱   │ × │   ╲
│    │ × │    │
╰─╮ ╱╲×╱╲ ╭─╯
  │╱ ×╲╱× ╲│
"""

ENEMY_DEAD = r"""
      × × ×
     ××▄××
   ╱  ×××  ╲
  │  × × ×  │
  │    ×    │
   ╲  ××× ╱
    ╲××××╱
     │×××│
════════════
   ╱ × │ × ╲
  ╱ ×  │  × ╲
═══════════════
    ╲×╱ ╲×╱
"""

# ===== FUNCIONES DE ANIMACIÓN =====

def animation_player_attack(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance):
    """Animación de ataque del jugador mejorada"""
    from levels.dungeon_combat import draw_combat_scene
    
    player_atack_sound.play()
    
    # Secuencia de animación de ataque
    frames = [PLAYER_ATTACK_1, PLAYER_ATTACK_2, PLAYER_ATTACK_3, PLAYER_IDLE]
    enemy_frames = [ENEMY_IDLE, ENEMY_HURT, ENEMY_HURT, ENEMY_IDLE]
    
    for i, (player_frame, enemy_frame) in enumerate(zip(frames, enemy_frames)):
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)
        
        # Color del enemigo cambia cuando recibe daño
        enemy_color = (255, 100, 100) if i == 2 else (255, 150, 150)
        
        draw_side_by_side(screen, font_ascii, player_x, player_y, player_frame, enemy_frame, 
                         player_color=(255, 255, 255), enemy_color=enemy_color)
        
        pygame.display.flip()
        pygame.time.wait(200 if i == 2 else 150)  # Pausa más larga en el impacto

def animation_enemy_attack(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance):
    """Animación de ataque del enemigo mejorada"""
    from levels.dungeon_combat import draw_combat_scene
    
    enemy_atack_sound.play()
    
    # Secuencia de animación de ataque
    enemy_frames = [ENEMY_IDLE, ENEMY_ATTACK_1, ENEMY_ATTACK_2, ENEMY_IDLE]
    player_frames = [PLAYER_IDLE, PLAYER_DEFEND, PLAYER_HURT, PLAYER_IDLE]
    
    for i, (enemy_frame, player_frame) in enumerate(zip(enemy_frames, player_frames)):
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)
        
        # Color del jugador cambia cuando recibe daño
        player_color = (255, 100, 100) if i == 2 else (255, 255, 255)
        
        draw_side_by_side(screen, font_ascii, player_x, player_y, player_frame, enemy_frame, 
                         player_color=player_color, enemy_color=(255, 150, 150))
        
        pygame.display.flip()
        pygame.time.wait(200 if i == 2 else 150)  # Pausa más larga en el impacto

def animation_player_evade(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance):
    """Animación de evasión del jugador"""
    from levels.dungeon_combat import draw_combat_scene
    
    atack_fail_sound.play()
    
    # Secuencia de evasión
    enemy_frames = [ENEMY_IDLE, ENEMY_ATTACK_1, ENEMY_ATTACK_2, ENEMY_IDLE]
    player_frames = [PLAYER_IDLE, PLAYER_DEFEND, PLAYER_DEFEND, PLAYER_IDLE]
    
    for i, (enemy_frame, player_frame) in enumerate(zip(enemy_frames, player_frames)):
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)
        
        # El jugador se mueve ligeramente durante la evasión
        offset_x = 15 if i == 2 else 0
        
        draw_character(screen, font_ascii, player_x - offset_x, player_y, player_frame, (255, 255, 255))
        draw_character(screen, font_ascii, player_x + 350, player_y, enemy_frame, (255, 150, 150))
        
        pygame.display.flip()
        pygame.time.wait(150)

def animation_enemy_evade(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance):
    """Animación de evasión del enemigo"""
    from levels.dungeon_combat import draw_combat_scene
    
    atack_fail_sound.play()
    
    # Secuencia de evasión
    frames = [PLAYER_ATTACK_1, PLAYER_ATTACK_2, PLAYER_ATTACK_3, PLAYER_IDLE]
    enemy_frames = [ENEMY_IDLE, ENEMY_IDLE, ENEMY_IDLE, ENEMY_IDLE]
    
    for i, (player_frame, enemy_frame) in enumerate(zip(frames, enemy_frames)):
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)
        
        # El enemigo se mueve durante la evasión
        offset_x = 25 if i == 2 else 0
        
        draw_character(screen, font_ascii, player_x, player_y, player_frame, (255, 255, 255))
        draw_character(screen, font_ascii, player_x + 350 + offset_x, player_y, enemy_frame, (255, 150, 150))
        
        pygame.display.flip()
        pygame.time.wait(150)

def animation_victory(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance):
    """Animación de victoria épica"""
    from levels.dungeon_combat import draw_combat_scene
    
    enemy_die_sound.play()
    
    # Secuencia de muerte del enemigo y celebración
    enemy_death_sequence = [ENEMY_HURT, ENEMY_DYING, ENEMY_DYING, ENEMY_DEAD]
    player_victory_sequence = [PLAYER_IDLE, PLAYER_IDLE, PLAYER_VICTORY, PLAYER_VICTORY]
    
    for i, (enemy_frame, player_frame) in enumerate(zip(enemy_death_sequence, player_victory_sequence)):
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)
        
        # Efectos de color
        enemy_color = (100, 100, 100) if i >= 2 else (255, 100, 100)  # Se oscurece al morir
        player_color = (255, 255, 100) if i >= 2 else (255, 255, 255)  # Dorado en victoria
        
        draw_side_by_side(screen, font_ascii, player_x, player_y, player_frame, enemy_frame, 
                         player_color=player_color, enemy_color=enemy_color)
        
        pygame.display.flip()
        pygame.time.wait(300 if i >= 2 else 200)

def animation_player_death(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance):
    """Animación de muerte del jugador"""
    from levels.dungeon_combat import draw_combat_scene
    
    # Secuencia de muerte
    death_sequence = [PLAYER_HURT, PLAYER_HURT, PLAYER_DEAD, PLAYER_DEAD]
    enemy_sequence = [ENEMY_ATTACK_2, ENEMY_IDLE, ENEMY_IDLE, ENEMY_IDLE]
    
    for i, (player_frame, enemy_frame) in enumerate(zip(death_sequence, enemy_sequence)):
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)
        
        # Color se desvanece
        player_color = (100, 100, 100) if i >= 2 else (255, 100, 100)
        
        draw_side_by_side(screen, font_ascii, player_x, player_y, player_frame, enemy_frame, 
                         player_color=player_color, enemy_color=(255, 150, 150))
        
        pygame.display.flip()
        pygame.time.wait(400)

def animation_status_effect_damage(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance):
    """Animación para daño por efectos de estado"""
    from levels.dungeon_combat import draw_combat_scene
    
    # Efecto de envenenamiento/quemadura
    for i in range(3):
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)
        
        # Parpadeo entre normal y herido
        player_frame = PLAYER_HURT if i % 2 == 0 else PLAYER_IDLE
        player_color = (100, 255, 100) if i % 2 == 0 else (255, 255, 255)  # Verde para veneno
        
        draw_side_by_side(screen, font_ascii, player_x, player_y, player_frame, ENEMY_IDLE, 
                         player_color=player_color, enemy_color=(255, 150, 150))
        
        pygame.display.flip()
        pygame.time.wait(200)

# ===== INTRO DE COMBATE MEJORADA =====

def play_combat_intro(screen, font_ascii):
    """Intro épica de combate con arte ASCII mejorado"""
    combat_intro_frames = [
        [
            "",
            "        ╔══════════════════════════════╗",
            "        ║                              ║", 
            "        ║         ⚔ COMBATE ⚔         ║",
            "        ║                              ║",
            "        ║        ¡Ha comenzado         ║",
            "        ║         la batalla!          ║",
            "        ║                              ║",
            "        ╚══════════════════════════════╝",
            "",
        ],
        [
            "",
            "        ╔══════════════════════════════╗",
            "        ║                              ║",
            "        ║         ⚔ COMBATE ⚔         ║", 
            "        ║                              ║",
            "        ║       PREPÁRATE PARA         ║",
            "        ║          LUCHAR              ║",
            "        ║                              ║",
            "        ║     [Presiona una tecla]     ║",
            "        ║                              ║",
            "        ╚══════════════════════════════╝",
        ],
    ]

    screen_width, screen_height = screen.get_size()
    line_height = 28
    enemy_atack_sound.play()
    
    # Mostrar frames de intro
    for frame in combat_intro_frames[:-1]:
        screen.fill((0, 0, 0))
        frame_height = len(frame) * line_height
        start_y = (screen_height - frame_height) // 2

        for i, line in enumerate(frame):
            text_width = font_ascii.size(line)[0]
            x = (screen_width - text_width) // 2
            y = start_y + i * line_height
            draw_text(screen, font_ascii, line, x, y, (255, 255, 255))
        pygame.display.flip()
        pygame.time.delay(800)

    # Mostrar el último frame y esperar
    last_frame = combat_intro_frames[-1]
    screen.fill((0, 0, 0))
    frame_height = len(last_frame) * line_height
    start_y = (screen_height - frame_height) // 2

    for i, line in enumerate(last_frame):
        text_width = font_ascii.size(line)[0]
        x = (screen_width - text_width) // 2
        y = start_y + i * line_height
        draw_text(screen, font_ascii, line, x, y, (255, 255, 255))
    pygame.display.flip()

    # Esperar tecla
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                waiting = False
            elif event.type == pygame.QUIT:
                waiting = False
        pygame.time.wait(50)

# ===== FUNCIONES DE COMPATIBILIDAD =====
# Mantener nombres anteriores para compatibilidad

def animation_player_atack(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance):
    return animation_player_attack(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)

def animation_enemy_atack(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance):
    return animation_enemy_attack(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)