import pygame
import time
import os
from src.object.main_character import MainCharacter
from levels.start_game import get_character_name, select_starting_weapon
from src.others import slow_print, resource_path, fade_out, fade_in
from levels.game_menu import game_menu
from config import DisplayConfig, AudioConfig, FontConfig, Colors, MenuConfig, TransitionConfig, GameConfig

# Import new performance and UX systems
from src.display_manager import init_display_manager, get_display_manager, get_resource_cache
from src.settings_manager import init_settings, get_settings
from src.input_manager import get_input_manager, get_keyboard_shortcuts, get_help_system



# Configuración de la ventana
WINDOW_WIDTH = DisplayConfig.WINDOW_WIDTH
WINDOW_HEIGHT = DisplayConfig.WINDOW_HEIGHT
FONT_SIZE = FontConfig.SMALL_SIZE
FPS = DisplayConfig.FPS

# Initialize systems
settings = init_settings()
resource_cache = get_resource_cache()

# Load audio with volume settings
try:
    main_menu_sound = resource_cache.get_sound(resource_path(AudioConfig.MAIN_MENU_MUSIC))
    if main_menu_sound:
        main_menu_sound.set_volume(settings.get_volume("music"))
        main_menu_sound.play(-1)  # Reproduce el sonido en bucle
except Exception as e:
    print(f"Warning: Could not load main menu music: {e}")
    main_menu_sound = None



def init_pygame():
    """Inicializa Pygame y configura la ventana con manejo de errores."""
    try:
        pygame.init()
        
        # Check if pygame initialized successfully
        if not pygame.get_init():
            raise RuntimeError("Pygame failed to initialize")

        # Get display settings from settings manager
        settings = get_settings()
        resolution = settings.get("display", "resolution")
        fullscreen = settings.get("display", "fullscreen")
        
        if fullscreen:
            screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
        else:
            screen = pygame.display.set_mode(resolution)
        
        # Initialize display manager for performance optimization
        display_manager = init_display_manager(screen)
        
        # Load fonts with fallbacks using resource cache
        cache = get_resource_cache()
        try:
            font_text = cache.get_font(resource_path(FontConfig.MAIN_FONT), FontConfig.MEDIUM_SIZE)
        except (FileNotFoundError, OSError):
            print(f"Warning: Could not load main font, using system default")
            font_text = cache.get_font(None, FontConfig.MEDIUM_SIZE)
            
        try:
            font_title = cache.get_font(resource_path(FontConfig.TITLE_FONT), FontConfig.TITLE_SIZE)
        except (FileNotFoundError, OSError):
            print(f"Warning: Could not load title font, using system default")
            font_title = cache.get_font(None, FontConfig.TITLE_SIZE)
            
        try:
            font_ascii = cache.get_font(None, FONT_SIZE)  # System font
        except Exception:
            print(f"Warning: Could not load mono font, using default")
            font_ascii = cache.get_font(None, FONT_SIZE)
        
        pygame.display.set_caption(DisplayConfig.CAPTION)
        
        return screen, font_text, font_ascii, font_title, display_manager
        
    except pygame.error as e:
        print(f"Pygame error during initialization: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error initializing Pygame: {e}")
        raise

# Creación de una clase para manejar el menú principal
class MainMenu:
    def __init__(self, screen, font_text, font_title, main_menu_sound):
        self.screen = screen
        # Crear fuente más grande específicamente para el menú principal
        try:
            self.font_text = pygame.font.Font(resource_path(FontConfig.MAIN_FONT), 30)  # Tamaño perfecto
        except:
            self.font_text = pygame.font.Font(None, 30)  # Fallback con tamaño 30
        
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

        # Espaciado más grande específicamente para el menú principal
        main_menu_spacing = 55  # Más espacioso que MenuConfig.OPTION_SPACING (40)
        total_height = len(opciones) * main_menu_spacing
        start_y = (WINDOW_HEIGHT - total_height) // 2

        for i, opcion in enumerate(opciones):
            color = Colors.YELLOW if i == self.seleccion else Colors.WHITE
            text_surface = self.font_text.render(opcion, True, color)
            text_width = text_surface.get_width()
            x = (WINDOW_WIDTH - text_width) // 2
            y = start_y + i * main_menu_spacing
            self.screen.blit(text_surface, (x, y))

        # Dibujar línea de controles centrada debajo del menú
        controls_text = "| ↑/↓ seleccionar | Enter entrar | Esc salir |"
        # Crear fuente más pequeña para los controles
        try:
            small_font = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 18)
        except:
            small_font = pygame.font.Font(None, 18)
        
        controls_surface = small_font.render(controls_text, True, Colors.GRAY)
        controls_x = (WINDOW_WIDTH - controls_surface.get_width()) // 2
        controls_y = start_y + total_height + 50  # 50px debajo del último elemento
        self.screen.blit(controls_surface, (controls_x, controls_y))

        pygame.display.flip()

    def handle_events(self):
        """Maneja los eventos del menú principal."""
        for event in pygame.event.get():
            action = self.handle_single_event(event)
            if action:
                return action
        return None
    
    def handle_single_event(self, event):
        """Maneja un solo evento del menú principal."""
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
            elif event.key == pygame.K_ESCAPE:
                return "quit"  # Escape sale del juego desde el menú principal
        return None



def main():
    """Función principal con manejo de errores y nuevos sistemas."""
    try:
        screen, font_text, font_ascii, font_title, display_manager = init_pygame()
        clock = pygame.time.Clock()
        
        # Initialize enhanced input systems
        input_manager = get_input_manager()
        shortcuts = get_keyboard_shortcuts()
        help_system = get_help_system()
        settings = get_settings()

        main_menu = MainMenu(screen, font_text, font_title, main_menu_sound)
        
        # Show FPS if enabled in settings
        show_fps = settings.get("gameplay", "show_fps")
        fps_font = font_ascii

        while True:
            # Handle events with enhanced input system
            events_to_process = []
            shortcut_handled = False
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    settings.save_settings()
                    pygame.quit()
                    return
                
                # Update keyboard shortcuts
                shortcuts.update_modifiers(event)
                
                # Handle keyboard shortcuts first
                if event.type == pygame.KEYDOWN:
                    shortcut_action = shortcuts.get_shortcut(event)
                    
                    if shortcut_action == "quit_confirm":
                        # Show confirmation dialog
                        from src.input_manager import ConfirmationDialog
                        confirm_dialog = ConfirmationDialog(
                            "¿Seguro que quieres salir del juego?",
                            lambda: pygame.quit(),
                            None
                        )
                        
                        # Simple confirmation loop
                        confirming = True
                        while confirming:
                            for conf_event in pygame.event.get():
                                result = confirm_dialog.handle_input(conf_event)
                                if result:
                                    if result == "confirmed":
                                        settings.save_settings()
                                        pygame.quit()
                                        return
                                    confirming = False
                                    break
                            
                            main_menu.display()
                            confirm_dialog.draw(screen, font_text)
                            display_manager.update()
                            clock.tick(FPS)
                        shortcut_handled = True
                        break
                    
                    elif shortcut_action == "help":
                        help_system.show_help()
                        
                        # Help system loop
                        while help_system.active:
                            for help_event in pygame.event.get():
                                if help_event.type == pygame.QUIT:
                                    settings.save_settings()
                                    pygame.quit()
                                    return
                                help_system.handle_input(help_event)
                            
                            main_menu.display()
                            help_system.draw(screen, font_text)
                            display_manager.update()
                            clock.tick(FPS)
                        shortcut_handled = True
                        break
                    
                    elif shortcut_action == "toggle_mute":
                        muted = settings.toggle_mute()
                        # Update audio volumes
                        if main_menu_sound:
                            volume = 0.0 if muted else settings.get_volume("music")
                            main_menu_sound.set_volume(volume)
                        shortcut_handled = True
                        break
                    
                    elif shortcut_action == "toggle_fullscreen":
                        current_fullscreen = settings.get("display", "fullscreen")
                        settings.set("display", "fullscreen", not current_fullscreen)
                        # Would need restart to apply - show message
                        print("Fullscreen toggle will apply on restart")
                        shortcut_handled = True
                        break
                
                # If no shortcut was handled, add event to be processed by menu
                if not shortcut_handled:
                    events_to_process.append(event)
            
            # Skip menu processing if shortcut was handled
            if shortcut_handled:
                continue
            
            # Regular menu display and logic
            main_menu.display()
            
            # Show FPS if enabled
            if show_fps:
                fps_text = f"FPS: {int(clock.get_fps())}"
                fps_surface = fps_font.render(fps_text, True, Colors.YELLOW)
                screen.blit(fps_surface, (10, 10))
            
            # Optimized display update
            display_manager.update()
            
            # Process menu events with the filtered event list
            action = None
            for event in events_to_process:
                menu_action = main_menu.handle_single_event(event)
                if menu_action:
                    action = menu_action
                    break

            if action == "new_game":
                try:
                    # Stop main menu music
                    if main_menu_sound:
                        main_menu_sound.stop()
                    
                    # Transición suave antes de ir a la creación de personaje
                    fade_out(screen, TransitionConfig.NORMAL_FADE)
                    
                    name = get_character_name(screen, font_text)
                    start_weapon = select_starting_weapon(screen, font_text)
                    main_character = MainCharacter(name)
                    main_character.setWeapon(start_weapon)
                    
                    # Preparar la pantalla de confirmación
                    screen.fill(Colors.BLACK)
                    
                    # Use fast text if skip animations is enabled
                    if settings.get("gameplay", "skip_animations"):
                        display_manager.fast_text(font_text, f"Muy bien {main_character.name}, comenzarás tu aventura con {main_character.weapon['name']}", (MenuConfig.MENU_PADDING, MenuConfig.TITLE_Y_OFFSET))
                        display_manager.update()
                        time.sleep(1)
                    else:
                        slow_print(screen, font_text, f"Muy bien {main_character.name}, comenzarás tu aventura con {main_character.weapon['name']}", MenuConfig.MENU_PADDING, MenuConfig.TITLE_Y_OFFSET)
                        display_manager.update()
                        time.sleep(2)
                    
                    # Transición al menú del juego
                    fade_out(screen, TransitionConfig.NORMAL_FADE)
                    game_menu(DisplayConfig.WINDOW_WIDTH, DisplayConfig.WINDOW_HEIGHT, main_character, screen, font_text, font_ascii)
                    
                    # Restart main menu music
                    if main_menu_sound:
                        main_menu_sound.play(-1)
                    
                except Exception as e:
                    print(f"Error during new game creation: {e}")
                    # Return to main menu on error
                    if main_menu_sound:
                        main_menu_sound.play(-1)

            elif action == "continue":
                try:
                    if os.path.exists(GameConfig.SAVE_FILE):
                        # Stop main menu music
                        if main_menu_sound:
                            main_menu_sound.stop()
                        
                        # Transición suave antes de cargar
                        fade_out(screen, TransitionConfig.NORMAL_FADE)
                        
                        screen.fill(Colors.BLACK)
                        loading_message = "Cargando partida..."
                        
                        # Crear fuente más grande para el mensaje de carga
                        try:
                            loading_font = pygame.font.Font(resource_path(FontConfig.MAIN_FONT), 50)
                        except:
                            loading_font = pygame.font.Font(None, 50)
                        
                        text_surface = loading_font.render(loading_message, True, Colors.WHITE)
                        text_x = (DisplayConfig.WINDOW_WIDTH - text_surface.get_width()) // 2
                        text_y = (DisplayConfig.WINDOW_HEIGHT - text_surface.get_height()) // 2
                        screen.blit(text_surface, (text_x, text_y))
                        display_manager.update(force=True)
                        time.sleep(1.5)
                        
                        main_character = MainCharacter("")
                        load_success = main_character.load_game()
                        
                        if load_success:
                            # Transición al menú del juego
                            fade_out(screen, TransitionConfig.NORMAL_FADE)
                            game_menu(DisplayConfig.WINDOW_WIDTH, DisplayConfig.WINDOW_HEIGHT, main_character, screen, font_text, font_ascii)
                            
                            # Restart main menu music
                            if main_menu_sound:
                                main_menu_sound.play(-1)
                        else:
                            # Error loading save file
                            fade_out(screen, TransitionConfig.SHORT_FADE)
                            screen.fill(Colors.BLACK)
                            slow_print(screen, font_text, "Error cargando partida. Archivo corrupto o inválido.", MenuConfig.MENU_PADDING, MenuConfig.TITLE_Y_OFFSET)
                            display_manager.update(force=True)
                            time.sleep(3)
                            fade_out(screen, TransitionConfig.SHORT_FADE)
                            
                            # Restart main menu music
                            if main_menu_sound:
                                main_menu_sound.play(-1)
                    else:
                        # Mensaje de error con transición suave
                        fade_out(screen, TransitionConfig.SHORT_FADE)
                        screen.fill(Colors.BLACK)
                        slow_print(screen, font_text, "No hay partida guardada.", MenuConfig.MENU_PADDING, MenuConfig.TITLE_Y_OFFSET)
                        display_manager.update(force=True)
                        time.sleep(2)
                        fade_out(screen, TransitionConfig.SHORT_FADE)
                        
                except Exception as e:
                    print(f"Error during continue game: {e}")
                    # Return to main menu on error
                    fade_out(screen, TransitionConfig.SHORT_FADE)
                    screen.fill(Colors.BLACK)
                    slow_print(screen, font_text, "Error inesperado al cargar la partida.", MenuConfig.MENU_PADDING, MenuConfig.TITLE_Y_OFFSET)
                    display_manager.update(force=True)
                    time.sleep(2)
                    fade_out(screen, TransitionConfig.SHORT_FADE)
                    
                    # Restart main menu music
                    if main_menu_sound:
                        main_menu_sound.play(-1)

            elif action == "quit":
                settings.save_settings()
                fade_out(screen, TransitionConfig.LONG_FADE)
                pygame.quit()
                return
            
            # Apply FPS limit from settings
            fps_limit = settings.get("display", "fps_limit") or FPS
            clock.tick(fps_limit)
                
    except KeyboardInterrupt:
        print("Game interrupted by user")
        settings.save_settings()
        pygame.quit()
        return
        
    except Exception as e:
        print(f"Critical error in main game loop: {e}")
        try:
            settings.save_settings()
            pygame.quit()
        except:
            pass
        raise

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame terminated by user")
    except Exception as e:
        print(f"\nCritical error: {e}")
        print("Please report this error if it persists")
        import traceback
        traceback.print_exc()
    finally:
        try:
            pygame.quit()
        except:
            pass