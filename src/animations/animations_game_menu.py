# src/animations/animations_game_menu.py

import pygame,time
from src.others import draw_text

def draw_character(surface, font_ascii, x, y, character, color=(255, 255, 255)):
    for i, line in enumerate(character.splitlines()):
        draw_text(surface, font_ascii, line, x, y + i * 20, color)

def animation_bonfire_1_get_frame(font_ascii, frame_index):
    frames = [
        """
                  ¦
                 ¦
             O    ¦
            /\\_  ¦
            \\/\\  /\\
        ---------------------
        """,
        """
                 ¦
                  ¦
             O   ¦ 
            /\\_   ¦
            \\/\\  /\\
        ---------------------
        """,
        """
                  ¦
                 ¦
             O    ¦
            /\\_  ¦
            \\/\\  /\\
        ---------------------
        """,
        """
                 ¦
                  ¦
             O   ¦
            /\\_   ¦   
            \\/\\  /\\
        ---------------------    
        """
    ]
    frame_surface = pygame.Surface((300, 250), pygame.SRCALPHA)  # Tamaño aproximado + transparencia
    frame_surface.fill((0, 0, 0, 0))  # Limpia con fondo transparente
    draw_character(frame_surface, font_ascii, 0, 0, frames[frame_index % len(frames)])
    time.sleep(0.8)  # Añadir un pequeño retraso para la animación
    return frame_surface


"""
          ________________
          |              | 
          |      O       |
          |     /|\      |
          ----------------
          |              |
    


          ________________
          |              | 
          |     O__      |
          |     |\       |
          ----------------
          |              |
    
          ________________
          |              | 
          |      O       |
          |   __/|\      |
          ----------------
          |              |
    
          ________________
          |              | 
          |    | O       |
          |    ¯¯|\      |
          ----------------
          |              |
"""