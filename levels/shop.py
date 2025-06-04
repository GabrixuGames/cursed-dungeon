import random
import pygame
from src.object.wepons import cargar_armas
from src.others import resource_path
from src.others import mostrar_popup

def shop(mainChar, screen, font, WINDOW_WIDTH, WINDOW_HEIGHT):
    """Muestra la tienda en la ventana de Pygame."""
    # Cargar armas y seleccionar aleatoriamente 5
    weapons_list = cargar_armas(resource_path("src/db/weaponsDb.json"))
    random.shuffle(weapons_list)
    weapons_show = weapons_list[:5]
    running = True
    
    # Mostrar encabezado de la tienda solo una vez
    opciones = [
        "¡Bienvenido a la tienda!",
        f"Dinero: {mainChar.getMoney()}",
        "Elige un arma (sustituirá al actual):"
    ]

    # Mostrar las armas disponibles con formato mejorado
    for i, weapon in enumerate(weapons_show):
        opciones.append(f"{i + 1}. {weapon['name']} - Daño: {weapon['damage']} | Velocidad: {weapon['attack_ratio']} | Precio: {weapon['price']}")

    # Opción para salir
    opciones.append(f"{len(weapons_show) + 1}. Salir")

    # Calcular la posición inicial para centrar verticalmente
    total_height = len(opciones) * 30  # Espaciado entre líneas
    start_y = (screen.get_height() - total_height) // 2

    # Bucle principal de la tienda
    while running:
        # Dibujar las opciones en la pantalla solo si es necesario
        screen.fill((0, 0, 0))  # Limpiar la pantalla solo antes de dibujar el menú
        for i, opcion in enumerate(opciones):
            text_surface = font.render(opcion, True, (255, 255, 255))
            text_width = text_surface.get_width()
            x = (screen.get_width() - text_width) // 2  # Centrar horizontalmente
            y = start_y + i * 40  # Espaciado entre líneas
            screen.blit(text_surface, (x, y))

        pygame.display.flip()

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Salir del juego

            if event.type == pygame.KEYDOWN:
                # Convertir la tecla presionada en un número
                if pygame.K_1 <= event.key <= pygame.K_9:
                    selected = event.key - pygame.K_1  # Convertir la tecla en índice (0-8)
                    if 0 <= selected < len(weapons_show):
                        selected_weapon = weapons_show[selected]
                        if mainChar.getMoney() >= selected_weapon['price']:
                            # Compra exitosa
                            mainChar.setWeapon(selected_weapon)
                            mainChar.setMoney(mainChar.getMoney() - selected_weapon['price'])
                            # Mostrar mensaje de compra exitosa
                            mostrar_popup(screen, font, f"Has comprado {selected_weapon['name']}.", WINDOW_WIDTH, WINDOW_HEIGHT, 500, 150)
                            pygame.display.flip()
                            pygame.time.wait(2000)  # Esperar 2 segundos
                            running = False  # Salir de la tienda
                        else:
                            # Mostrar mensaje de dinero insuficiente
                            mostrar_popup(screen, font, "No tienes suficiente dinero.", WINDOW_WIDTH, WINDOW_HEIGHT, 500, 150)
                            pygame.display.flip()
                            pygame.time.wait(2000)  # Esperar 2 segundos
                    else:
                        # Si se selecciona la opción para salir
                        if selected == len(weapons_show):  # Salir
                            running = False  # Salir de la tienda
                            return False  # Salir del juego
