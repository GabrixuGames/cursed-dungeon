import pygame
import time
import os
from src.object.mainChar import MainChar
from levels.start_game import get_character_name, select_starting_weapon
from src.others import slow_print, resource_path, fade_out, fade_in
from levels.game_menu import game_menu
from config import DisplayConfig, AudioConfig, FontConfig, Colors, MenuConfig, TransitionConfig, GameConfig



# Configuración de la ventana
WINDOW_WIDTH = DisplayConfig.WINDOW_WIDTH
WINDOW_HEIGHT = DisplayConfig.WINDOW_HEIGHT
FONT_SIZE = FontConfig.SMALL_SIZE
FPS = DisplayConfig.FPS

main_menu_sound = pygame.mixer.Sound(resource_path(AudioConfig.MAIN_MENU_MUSIC))
main_menu_sound.set_volume(AudioConfig.MAIN_MENU_VOLUME)
main_menu_sound.play(-1)  # Reproduce el sonido en bucle



def init_pygame():
    """Inicializa Pygame y configura la ventana."""
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    font_text = pygame.font.Font(resource_path(FontConfig.MAIN_FONT), FontConfig.MEDIUM_SIZE)
    pygame.display.set_caption(DisplayConfig.CAPTION)
    font_ascii = pygame.font.SysFont(FontConfig.MONO_FONT, FONT_SIZE)
    font_title = pygame.font.Font(resource_path(FontConfig.TITLE_FONT), FontConfig.TITLE_SIZE)
    return screen, font_text, font_ascii, font_title

# Creación de una clase para manejar el menú principal
class MainMenu:
    def __init__(self, screen, font_text, font_title, main_menu_sound):
        self.screen = screen
        self.font_text = font_text
        self.font_title = pygame.font.Font(resource_path(FontConfig.TITLE_FONT), FontConfig.LARGE_SIZE)
        self.main_menu_sound = main_menu_sound
        self.seleccion = 0

    def display(self):
        """Dibuja el menú principal en la pantalla."""
        self.screen.fill(Colors.BLACK)
        title = "CURSED DUNGEON"
        title_surface = self.font_title.render(title, True, Colors.WHITE)
        title_x = (WINDOW_WIDTH - title_surface.get_width()) // 2
        title_y = MenuConfig.TITLE_Y_OFFSET
        self.screen.blit(title_surface, (title_x, title_y))

        opciones = [
            "Iniciar partida",
            "Continuar",
            "Salir"
        ]

        total_height = len(opciones) * MenuConfig.OPTION_SPACING
        start_y = (WINDOW_HEIGHT - total_height) // 2

        for i, opcion in enumerate(opciones):
            color = Colors.YELLOW if i == self.seleccion else Colors.WHITE
            text_surface = self.font_text.render(opcion, True, color)
            text_width = text_surface.get_width()
            x = (WINDOW_WIDTH - text_width) // 2
            y = start_y + i * MenuConfig.OPTION_SPACING
            self.screen.blit(text_surface, (x, y))

        pygame.display.flip()

    def handle_events(self):
        """Maneja los eventos del menú principal."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.seleccion = (self.seleccion - 1) % 3
                elif event.key == pygame.K_DOWN:
                    self.seleccion = (self.seleccion + 1) % 3
                elif event.key == pygame.K_RETURN:
                    if self.seleccion == 0:
                        return "new_game"
                    elif self.seleccion == 1:
                        return "continue"
                    elif self.seleccion == 2:
                        return "quit"
        return None



def main():
    """Función principal."""
    screen, font_text, font_ascii, font_title = init_pygame()
    clock = pygame.time.Clock()

    main_menu = MainMenu(screen, font_text, font_title, main_menu_sound)
    mainChar = None

    while True:
        main_menu.display()
        action = main_menu.handle_events()

        if action == "new_game":
            # Transición suave antes de ir a la creación de personaje
            fade_out(screen, TransitionConfig.NORMAL_FADE)
            
            name = get_character_name(screen, font_text)
            start_weapon = select_starting_weapon(screen, font_text)
            main_character = MainChar(name)
            main_character.setWeapon(start_weapon)
            
            # Preparar la pantalla de confirmación
            screen.fill(Colors.BLACK)
            slow_print(screen, font_text, f"Muy bien {main_character.name}, comenzarás tu aventura con {main_character.weapon['name']}", MenuConfig.MENU_PADDING, MenuConfig.TITLE_Y_OFFSET)
            pygame.display.flip()
            time.sleep(2)
            
            # Transición al menú del juego
            fade_out(screen, TransitionConfig.NORMAL_FADE)
            main_menu_sound.stop()
            game_menu(DisplayConfig.WINDOW_WIDTH, DisplayConfig.WINDOW_HEIGHT, main_character, screen, font_text, font_ascii)

        elif action == "continue":
            if os.path.exists(GameConfig.SAVE_FILE):
                # Transición suave antes de cargar
                fade_out(screen, TransitionConfig.NORMAL_FADE)
                
                screen.fill(Colors.BLACK)
                loading_message = "Cargando partida..."
                text_surface = font_text.render(loading_message, True, Colors.WHITE)
                text_x = (DisplayConfig.WINDOW_WIDTH - text_surface.get_width()) // 2
                text_y = (DisplayConfig.WINDOW_HEIGHT - text_surface.get_height()) // 2
                screen.blit(text_surface, (text_x, text_y))
                pygame.display.flip()
                time.sleep(1.5)
                
                main_character = MainChar("")
                main_character.load_game()
                
                # Transición al menú del juego
                fade_out(screen, TransitionConfig.NORMAL_FADE)
                main_menu_sound.stop()
                game_menu(DisplayConfig.WINDOW_WIDTH, DisplayConfig.WINDOW_HEIGHT, main_character, screen, font_text, font_ascii)
            else:
                # Mensaje de error con transición suave
                fade_out(screen, TransitionConfig.SHORT_FADE)
                screen.fill(Colors.BLACK)
                slow_print(screen, font_text, "No hay partida guardada.", MenuConfig.MENU_PADDING, MenuConfig.TITLE_Y_OFFSET)
                pygame.display.flip()
                time.sleep(2)
                fade_out(screen, TransitionConfig.SHORT_FADE)

        elif action == "quit":
            fade_out(screen, TransitionConfig.LONG_FADE)
            pygame.quit()
            return

    pygame.quit()


if __name__ == "__main__":
    main()