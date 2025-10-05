
import pygame, random, os
from src.others import draw_text

pygame.mixer.init()  # Initialize the sound mixer
sound_dir = os.path.join(os.path.dirname(__file__), '..', 'sounds')
player_atack_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'player_atack.mp3'))
player_atack_sound.set_volume(0.75)
enemy_atack_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'monster_atack.mp3'))
enemy_atack_sound.set_volume(0.4)
enemy_die_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'monster_died.wav'))
enemy_die_sound.set_volume(0.5)
atack_fail_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'atack_fail.mp3'))
atack_fail_sound.set_volume(0.6)
steps_sound = pygame.mixer.Sound(os.path.join(sound_dir, 'steps_sound.mp3'))
steps_sound.set_volume(0.2)

def draw_character(screen, font_ascii, x, y, character, color=(255, 255, 255)):
    for i, line in enumerate(character.splitlines()):
        draw_text(screen, font_ascii, line, x, y + i * 20, color)

# Player attack animation
def animation_player_atack(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, main_character, enemy_real):
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
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, main_character, enemy_real)
        draw_character(screen, font_ascii, player_x, player_y, frame, (255, 255, 255))  # draw current player frame
        pygame.display.flip()
        pygame.time.wait(150)

# Enemy attack animation
def animation_enemy_atack(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, main_character, enemy_real):
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
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, main_character, enemy_real)
        draw_character(screen, font_ascii, player_x, player_y, frame, (255, 255, 255))  # draw current enemy frame
        pygame.display.flip()
        pygame.time.wait(150)

# Player evade animation
def animation_player_evade(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, main_character, enemy_real):
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
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, main_character, enemy_real)
        draw_character(screen, font_ascii, player_x, player_y, frame, (255, 255, 255))  # draw current player frame
        pygame.display.flip()
        pygame.time.wait(150)

# Enemy evade animation
def animation_enemy_evade(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, main_character, enemy_real):
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
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, main_character, enemy_real)
        draw_character(screen, font_ascii, player_x, player_y, frame, (255, 255, 255))  # draw current enemy frame
        pygame.display.flip()
        pygame.time.wait(150)

# Player victory animation
def animation_victory(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, main_character, enemy_real):
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
        draw_combat_scene(screen, font_text, font_ascii, player_x, player_y, hud_player_hp, hud_enemy_hp, main_character, enemy_real)
        draw_character(screen, font_ascii, player_x, player_y, frame, (255, 255, 255))  # draw current player frame
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

