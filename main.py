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

def mostrar_menu_principal(screen, font_text, font_title):
    """Dibuja el menú principal en la pantalla, centrado."""
    screen.fill((0, 0, 0))
    # Título con fuente diferente
    font_title = pygame.font.Font("src/assets/fonts/Viking.ttf", 60)
    title = "CURSED DUNGEON"
    title_surface = font_title.render(title, True, (255, 255, 255))
    title_width = title_surface.get_width()
    title_height = title_surface.get_height()

    
    # Opciones con la fuente regular
    opciones = [
        "1. Iniciar partida.",
        "2. Continuar.",
        "3. Salir."
    ]

    title_x = (WINDOW_WIDTH - title_width) // 2
    title_y = (WINDOW_HEIGHT - len(opciones)) - 500
    screen.blit(title_surface, (title_x, title_y))
    


    # Calcular la posición inicial para centrar verticalmente
    total_height = len(opciones) * 40  # Espaciado entre líneas
    start_y = (WINDOW_HEIGHT - total_height) // 2

    for i, opcion in enumerate(opciones):
        text_surface = font_text.render(opcion, True, (255, 255, 255))
        text_width = text_surface.get_width()
        x = (WINDOW_WIDTH - text_width) // 2  # Centrar horizontalmente
        y = start_y + i * 40  # Espaciado entre líneas
        screen.blit(text_surface, (x, y))
    pygame.display.flip()



def main():
    """Función principal."""
    screen, font_text, font_ascii, font_title = init_pygame()
    clock = pygame.time.Clock()


    # Menú principal
    mainChar = None
    mostrar_menu_principal(screen, font_text, font_title)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # Iniciar nueva partida
                    name = start_game_name(screen, font_text)  # Se añade la lista de armas
                    start_weapon = start_game_weapons(screen, font_text)  # Se añade la lista de armas # Simular entrada de texto
                    mainChar = MainChar(name)
                    mainChar.setWeapon(start_weapon)
                    screen.fill((0, 0, 0))
                    text_surface = font_text.render(f"Muy bien {mainChar.name}, comenzarás tu aventura con {mainChar.weapon["name"]}", True, (255, 255, 255))
                    text_width = text_surface.get_width()
                    text_height = text_surface.get_height()

                    x = (screen.get_width() - text_width) // 2
                    y = (screen.get_height() - text_height) // 2

                    slow_print(screen, font_text, f"Muy bien {mainChar.name}, comenzarás tu aventura con {mainChar.weapon["name"]}", x, y - 100)

                    pygame.display.flip()
                    time.sleep(2)
                    main_menu_sound.stop()  # Detener el sonido del menú principal
                    
                elif event.key == pygame.K_2:
                    if os.path.exists("save.json"):
                        # Limpiar la pantalla y mostrar "Cargando..."
                        screen.fill((0, 0, 0))  # Limpiar la pantalla
                        text_surface = font_text.render("Cargando partida...", True, (255, 255, 255))
                        text_width = text_surface.get_width()
                        text_height = text_surface.get_height()

                        x = (screen.get_width() - text_width) // 2
                        y = (screen.get_height() - text_height) // 2

                        slow_print(screen, font_text, "Cargando partida...", x, y)
                        pygame.display.flip()
                        time.sleep(1.5)  # Simular tiempo de carga
                        
                        # Cargar la partida
                        mainChar = MainChar("")
                        mainChar.load_game()
                        main_menu_sound.stop()
                        game_menu(WINDOW_WIDTH, WINDOW_HEIGHT, mainChar, screen, font_text, font_ascii)
                        break
                    else:
                        slow_print(screen, font_text, "No hay partida guardada.", 10, 150)
                        pygame.display.flip()
                        time.sleep(2)
                elif event.key == pygame.K_3:
                    pygame.quit()
                    return
            # Aquí manejamos los eventos del ratón sin bloquear el cierre de la ventana
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    # Este bloque ya no interfiere con el evento de la ventana
                    continue

        if mainChar:
            break


    pygame.quit()


if __name__ == "__main__":
    main()