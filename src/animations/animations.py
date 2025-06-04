import pygame, random
from src.others import draw_text

pygame.mixer.init()  # Inicializa el mezclador de sonido
player_atack_sound = pygame.mixer.Sound("src\sounds\player_atack.mp3")  # Ajusta la ruta
player_atack_sound.set_volume(0.75)  # Ajusta el volumen según sea necesario
enemy_atack_sound = pygame.mixer.Sound("src\sounds\monster_atack.mp3")  # Ajusta la ruta
enemy_atack_sound.set_volume(0.4)  # Ajusta el volumen según sea necesario 
enemy_die_sound = pygame.mixer.Sound("src\sounds\monster_died.wav")  # Ajusta la ruta
enemy_die_sound.set_volume(0.5)  # Ajusta el volumen según sea necesario
atack_fail_sound = pygame.mixer.Sound("src/sounds/atack_fail.mp3")  # Ajusta la ruta
atack_fail_sound.set_volume(0.6)  # Ajusta el volumen según sea necesario
steps_sound = pygame.mixer.Sound("src\sounds\steps_sound.mp3")
steps_sound.set_volume(0.2)

def draw_character(screen, font_ascii, x, y, character, color=(255, 255, 255)):
    for i, line in enumerate(character.splitlines()):
        draw_text(screen, font_ascii, line, x, y + i * 20, color)

# Animación de ataque del jugador
def animation_player_atack(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, mainChar, enemy_real):
    frames = [
        """
        
                 O     __o     
                /|\\___  /|   
                / \\     / \\   
        """,
        """
        
                 O |   __o     
                /|¯¯     /|   
                / \\     / \\   
        """,
        """
        
                 O     __o     
                /|\\/    /|   
                / \\     / \\   
        """,
        """
        
                 O      __o     
                /|\\___   /|   
                / \\     / \\   
        """,
        """
        
                 O     __o     
                /|\\___  /|   
                / \\     / \\   
        """
    ]

    player_atack_sound.play()

    from levels.dungeon_combat import draw_combat_scene
    for frame in frames:
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, mainChar, enemy_real)
        draw_character(screen, font_ascii, player_x, player_y, frame, (255, 255, 255))  # Dibuja el frame actual del jugador
        pygame.display.flip()
        pygame.time.wait(150)

# Animación de ataque del enemigo
def animation_enemy_atack(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, mainChar, enemy_real):
    frames_enemy = [
        """
        
                 O     __o     
                /|\\___  /|   
                / \\     / \\   
        """,
        """
        
                 O     __o     
                /|\\___   |   
                / \\     / \\   
        """,
        """
        
                 O      \ o     
               /|\\___   /|   
                / \\     / \\   
        """,
        """
        
                 O     __o     
               /|\\___   /|   
                / \\     / \\   
        """,
        """
        
                 O     _\\o     
                /|\\___   |   
                / \\     / \\   
        """
    ]

    enemy_atack_sound.play()

    from levels.dungeon_combat import draw_combat_scene
    for frame in frames_enemy:
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, mainChar, enemy_real)
        draw_character(screen, font_ascii, player_x, player_y, frame, (255, 255, 255))  # Dibuja el frame actual del enemigo
        pygame.display.flip()
        pygame.time.wait(150)

# Animación de evasión del jugador
def animation_player_evade(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, mainChar, enemy_real):
    frames_evade_player = [
        """
        
                 O     __o     
                /|\\___  /|   
                / \\     / \\   
        """,
        """
        
                 O     __o     
                /||__    |   
                | \\     / \\   
        """,
        """
        
                 O      \o     
               _||\\     /|   
                / |     / \\   
        """,
        """
        
                 O     __o     
             ___/|\\     /|   
                / \\     / \\   
        """,
        """
        
                 O     _\\o     
                /|\\___   |   
                / \\     / \\   
        """
    ]

    atack_fail_sound.play()

    from levels.dungeon_combat import draw_combat_scene
    for frame in frames_evade_player:
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, mainChar, enemy_real)
        draw_character(screen, font_ascii, player_x, player_y, frame, (255, 255, 255))  # Dibuja el frame actual del jugador
        pygame.display.flip()
        pygame.time.wait(150)

# Animación de evasión del enemigo
def animation_enemy_evade(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, mainChar, enemy_real):
    frames_enemy_evade = [
        """
        
                 O     __o     
                /|\\___  /|   
                / \\     / \\   
        """,
        """
        
                 O |   __o     
                /|¯¯     /|   
                / \\     | |   
        """,
        """
        
                 O      __o     
                /|\\/     /|   
                / \\      / \\   
        """,
        """
        
                 O      __o     
                /|\\___  /|   
                / \\     | |   
        """,
        """
        
                 O     __o     
                /|\\___  /|   
                / \\     / \\   
        """
    ]

    atack_fail_sound.play()

    from levels.dungeon_combat import draw_combat_scene
    for frame in frames_enemy_evade:
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, mainChar, enemy_real)
        draw_character(screen, font_ascii, player_x, player_y, frame, (255, 255, 255))  # Dibuja el frame actual del enemigo
        pygame.display.flip()
        pygame.time.wait(150)

# Animación de victoria del jugador
def animation_victory(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, mainChar, enemy_real):
    frames_victory = [
        """
        
                 O     __o     
                /|\\___  /|   
                / \\     / \\   
        """,
        """
        
               __O__|     o     
                 |       /|   
                / \\     <   
        """,
        """
                  \\ 
                \O/           
                 |       \o  
                / \\     __|  
        """,
        """
                  \\ 
                \O/          
                 |        
                / \\   _\\__o/ 
        """
    ]

    enemy_die_sound.play()

    from levels.dungeon_combat import draw_combat_scene
    for frame in frames_victory:
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, mainChar, enemy_real)
        draw_character(screen, font_ascii, player_x, player_y, frame, (255, 255, 255))  # Dibuja el frame actual del jugador
        pygame.display.flip()
        pygame.time.wait(150)



frames_walking_right = [
    """
         O         
        /|\\___    
        / \\        
    """,
    """
         O        
        /|\\___    
         |        
    """
]

frames_walking_left = [
    """
         O         
     ___/|\\   
        / \\        
    """,
    """
         O        
     ___/|\\    
         |        
    """
]


def play_combat_intro(screen, font_ascii, delay=500):
    combat_intro_frames = [
        [
            " " * 20 + "    ",
            " " * 20 + "    ",
            " " * 15 + "¡ALERTA! UN ENEMIGO APARECIÓ",
            " " * 20 + "    ",
            " " * 20 + "    ",
        ],
        [
            " " * 20 + "**************",
            " " * 20 + "*            *",
            " " * 15 + "* ¡ALERTA! UN ENEMIGO APARECIÓ *",
            " " * 20 + "*            *",
            " " * 20 + "**************",
        ],
        [
            " " * 15 + "╔════════════════════════════╗",
            " " * 15 + "║                            ║",
            " " * 15 + "║ ¡ALERTA! UN ENEMIGO APARECIÓ ║",
            " " * 15 + "║                            ║",
            " " * 15 + "╚════════════════════════════╝",
        ],
        [
            " " * 15 + "╔════════════════════════════╗",
            " " * 15 + "║   PREPÁRATE PARA LUCHAR    ║",
            " " * 15 + "║                            ║",
            " " * 15 + "║     [Presiona una tecla]   ║",
            " " * 15 + "╚════════════════════════════╝",
        ],
    ]

    screen_width, screen_height = screen.get_size()
    line_height = 25
    enemy_atack_sound.play()
    # Mostrar cada frame menos el último con delay
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
        pygame.time.delay(delay)

    # Mostrar el último frame y mantenerlo
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

    # Esperar a que el usuario presione una tecla SIN borrar pantalla
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False

