"""
Configuración global del juego Cursed Dungeon.
Todos los valores mágicos y constantes centralizados aquí.
"""

# ===== CONFIGURACIÓN DE VENTANA =====
class DisplayConfig:
    # Resolución estándar HD
    WINDOW_WIDTH = 1280
    WINDOW_HEIGHT = 720
    FPS = 60
    CAPTION = "Cursed Dungeon"

# ===== CONFIGURACIÓN DE COLORES =====
class Colors:
    # Colores básicos
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)  # Color de selección en menús
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    GRAY = (200, 200, 200)  # Bordes de menús
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (100, 100, 100)  # Para elementos deshabilitados
    
    # Colores de UI
    POPUP_BG = (30, 30, 30)
    POPUP_ALPHA = 230
    BLACK_ALPHA = (0, 0, 0, 180)

# ===== CONFIGURACIÓN DE FUENTES =====
class FontConfig:
    # Tamaños de fuente
    SMALL_SIZE = 20
    MEDIUM_SIZE = 25
    LARGE_SIZE = 80
    TITLE_SIZE = 120
    
    # Rutas de fuentes
    MAIN_FONT = "src/assets/fonts/texgyrebonum-regular.otf"
    TITLE_FONT = "src/assets/fonts/Viking.ttf"
    MONO_FONT = "src/assets/fonts/CascadiaCodeNF-Regular.ttf"  # ASCII Art optimizada
    
    # Font rendering constants
    ESTIMATED_CHAR_WIDTH = 12.5
    DEFAULT_HEIGHT = 20
    DEFAULT_CHAR_WIDTH = 8
    CLEAR_PADDING = 8
    BG_PADDING = 12
    BG_OFFSET = 4

# ===== CONFIGURACIÓN DE MENÚS =====
class MenuConfig:
    # Dimensiones del menú principal del juego
    GAME_MENU_WIDTH = 700
    GAME_MENU_HEIGHT = 400
    GAME_MENU_HALF_WIDTH = GAME_MENU_WIDTH // 2
    GAME_MENU_HALF_HEIGHT = GAME_MENU_HEIGHT // 2
    GAME_MENU_BOX_WIDTH = 700
    GAME_MENU_BOX_HEIGHT = 400
    
    # Espaciado entre opciones
    OPTION_SPACING = 40
    SECTION_SPACING = 20
    
    # Posicionamiento
    MENU_PADDING = 50
    TITLE_Y_OFFSET = 100
    MESSAGE_Y_POSITION = 200
    ANIMATION_OFFSET = 100
    
    # Animación de fogata
    BONFIRE_SIZE = (300, 200)  # Tamaño proporcional para fuente 20px
    BONFIRE_FRAME_DURATION = 600  # ms
    ANIMATION_FRAME_DURATION = 600  # ms
    ANIMATION_SIZE = 300
    
    # Popup dimensions
    POPUP_WIDTH = 500
    POPUP_HEIGHT = 150
    
    # Level up bonuses
    HEALTH_INCREASE = 10
    DAMAGE_INCREASE = 1
    EVASION_INCREASE = 1
    
    # Character creation
    MAX_NAME_LENGTH = 15
    MAX_WEAPONS_SHOW = 4
    
    # Weapon selection
    WEAPON_SELECTION_Y_OFFSET = 180
    WEAPON_OPTION_SPACING = 50
    
    # General settings
    MENU_FPS = 30
    
    # Toast system
    TOAST_X = 50
    TOAST_START_Y = 520
    TOAST_SPACING = 22
    TOAST_SLIDE_OFFSET = 10

# ===== CONFIGURACIÓN DE TRANSICIONES =====
class TransitionConfig:
    # Duraciones en milisegundos
    FAST_FADE = 500
    SHORT_FADE = 500
    NORMAL_FADE = 600
    SLOW_FADE = 800
    LONG_FADE = 800
    EXIT_FADE = 800
    
    # Message delays
    MESSAGE_DELAY = 2000  # ms
    TOAST_FADE_DURATION = 300  # ms
    EVENT_CHECK_DELAY = 20  # ms
    
    # Animation delays
    SLOW_PRINT_DELAY = 0.05  # seconds per character
    
    # FPS para transiciones suaves
    TRANSITION_FPS = 60
    FRAME_DELAY = 16  # ms (1000/60)

# ===== CONFIGURACIÓN DE ANIMACIONES =====
class AnimationConfig:
    # Velocidad de escritura
    SLOW_PRINT_DELAY = 0.05  # segundos por carácter
    
    # Timeouts
    MESSAGE_TIMEOUT = 1500  # ms
    POPUP_DISPLAY_TIME = 2000  # ms

# ===== CONFIGURACIÓN DE AUDIO =====
class AudioConfig:
    # Volúmenes (0.0 a 1.0)
    MAIN_MENU_VOLUME = 0.15
    GAME_MENU_VOLUME = 0.25
    SFX_VOLUME = 0.5
    
    # Rutas de audio
    MAIN_MENU_MUSIC = "src/sounds/main_menu_entrance.mp3"
    GAME_MENU_MUSIC = "src/sounds/menu_bonfire_sound.mp3"

# ===== CONFIGURACIÓN DE JUEGO =====
class GameConfig:
    # Sistema de guardado
    SAVE_FILE = "save.json"
    
    # Balanceamiento inicial
    STARTING_HEALTH = 150
    STARTING_DAMAGE = 10
    STARTING_EVADE = 5
    STARTING_MONEY = 0
    STARTING_LEVEL = 1
    
    # Progresión
    EXP_MULTIPLIER = 1.2
    LEVEL_BASE_EXP = 100

# ===== CONFIGURACIÓN DE POPUP =====
class PopupConfig:
    DEFAULT_WIDTH = 500
    DEFAULT_HEIGHT = 150
    BORDER_WIDTH = 2
    PADDING = 4

# ===== FUNCIONES HELPER =====
def get_centered_x(width, container_width=None):
    """Calcula X para centrar un elemento."""
    if container_width is None:
        container_width = DisplayConfig.WINDOW_WIDTH
    return (container_width - width) // 2

def get_centered_y(height, container_height=None):
    """Calcula Y para centrar un elemento."""
    if container_height is None:
        container_height = DisplayConfig.WINDOW_HEIGHT
    return (container_height - height) // 2

def get_menu_box_position():
    """Devuelve la posición del recuadro del menú del juego."""
    x = get_centered_x(MenuConfig.GAME_MENU_WIDTH)
    y = get_centered_y(MenuConfig.GAME_MENU_HEIGHT)
    return x, y