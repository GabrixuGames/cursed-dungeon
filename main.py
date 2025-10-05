import pygame
import time
import os
from src.object.mainChar import MainChar
from levels.start_game import start_game_name, start_game_weapons
from src.others import slow_print, resource_path
from levels.game_menu import game_menu



# Configuración de la ventana
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FONT_SIZE = 20
FPS = 60

main_menu_sound = pygame.mixer.Sound(resource_path("src\sounds\main_menu_entrance.mp3"))
main_menu_sound.set_volume(0.15)  # Ajusta el volumen según sea necesario
main_menu_sound.play(-1)  # Reproduce el sonido en bucle



def init_pygame():
    """Inicializa Pygame y configura la ventana."""
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    font_text = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 25)
    pygame.display.set_caption("Cursed Dungeon")
    font_ascii = pygame.font.SysFont("Courier", FONT_SIZE)
    font_title = pygame.font.Font(resource_path("src/assets/fonts/Viking.ttf"), 120)
    return screen, font_text, font_ascii, font_title

# Creación de una clase para manejar el menú principal
class MainMenu:
    def __init__(self, screen, font_text, font_title, main_menu_sound):
        self.screen = screen
        self.font_text = font_text
        self.font_title = pygame.font.Font(resource_path("src/assets/fonts/Viking.ttf"), 80)  # Tamaño reducido
        self.main_menu_sound = main_menu_sound

    def display(self):
        """Dibuja el menú principal en la pantalla."""
        self.screen.fill((0, 0, 0))
        title = "CURSED DUNGEON"
        title_surface = self.font_title.render(title, True, (255, 255, 255))
        title_x = (WINDOW_WIDTH - title_surface.get_width()) // 2
        title_y = 100
        self.screen.blit(title_surface, (title_x, title_y))

        opciones = [
            "1. Iniciar partida.",
            "2. Continuar.",
            "3. Salir."
        ]

        total_height = len(opciones) * 40
        start_y = (WINDOW_HEIGHT - total_height) // 2

        for i, opcion in enumerate(opciones):
            text_surface = self.font_text.render(opcion, True, (255, 255, 255))
            text_width = text_surface.get_width()
            x = (WINDOW_WIDTH - text_width) // 2
            y = start_y + i * 40
            self.screen.blit(text_surface, (x, y))

        pygame.display.flip()

    def handle_events(self):
        """Maneja los eventos del menú principal."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "new_game"
                elif event.key == pygame.K_2:
                    return "continue"
                elif event.key == pygame.K_3:
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
            name = start_game_name(screen, font_text)
            start_weapon = start_game_weapons(screen, font_text)
            mainChar = MainChar(name)
            mainChar.setWeapon(start_weapon)
            screen.fill((0, 0, 0))
            slow_print(screen, font_text, f"Muy bien {mainChar.name}, comenzarás tu aventura con {mainChar.weapon['name']}", 100, 100)
            pygame.display.flip()
            time.sleep(2)
            main_menu_sound.stop()
            game_menu(WINDOW_WIDTH, WINDOW_HEIGHT, mainChar, screen, font_text, font_ascii)  # Llamar al menú de partida

        elif action == "continue":
            if os.path.exists("save.json"):
                screen.fill((0, 0, 0))
                loading_message = "Cargando partida..."
                text_surface = font_text.render(loading_message, True, (255, 255, 255))
                text_x = (WINDOW_WIDTH - text_surface.get_width()) // 2
                text_y = (WINDOW_HEIGHT - text_surface.get_height()) // 2
                screen.blit(text_surface, (text_x, text_y))
                pygame.display.flip()
                time.sleep(1.5)
                mainChar = MainChar("")
                mainChar.load_game()
                main_menu_sound.stop()
                game_menu(WINDOW_WIDTH, WINDOW_HEIGHT, mainChar, screen, font_text, font_ascii)  # Llamar al menú de partida
            else:
                slow_print(screen, font_text, "No hay partida guardada.", 100, 100)
                pygame.display.flip()
                time.sleep(2)

        elif action == "quit":
            pygame.quit()
            return

    pygame.quit()


if __name__ == "__main__":
    main()