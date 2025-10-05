# src/animations/animations_game_menu.py

import pygame
from src.others import draw_text

def draw_character(surface, font_ascii, x, y, character, color=(255, 255, 255)):
    for i, line in enumerate(character.splitlines()):
        draw_text(surface, font_ascii, line, x, y + i * 20, color)

def precalculate_bonfire_frames(font_ascii):
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
    precalculated_frames = []
    for frame in frames:
        frame_surface = pygame.Surface((300, 250), pygame.SRCALPHA)  # Tamaño aproximado + transparencia
        frame_surface.fill((0, 0, 0, 0))  # Limpia con fondo transparente
        draw_character(frame_surface, font_ascii, 0, 0, frame)
        precalculated_frames.append(frame_surface)
    return precalculated_frames


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