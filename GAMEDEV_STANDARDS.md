# GAMEDEV_STANDARDS.md - Estándares de Desarrollo de Juegos

## 🎮 Estándares Específicos para Pygame con Arte ASCII

### ⚠️ Filosofía de Diseño: ASCII Art Game

Este proyecto utiliza **arte ASCII** para toda la representación visual:
- Personajes renderizados con caracteres
- Enemigos como arte ASCII
- UI dibujada con caracteres y símbolos
- Animaciones mediante transición de frames ASCII
- Estética retro/roguelike

**NO se usan**:
- ❌ Sprites PNG/imágenes
- ❌ Spritesheets tradicionales
- ❌ Texturas bitmap

**SÍ se usan**:
- ✅ Fuentes monoespaciadas para renderizado consistente
- ✅ Caracteres Unicode (│, ─, ┌, └, █, etc.)
- ✅ Efectos de color mediante pygame.font.render()
- ✅ Audio para feedback (música y efectos de sonido)

---

## 📁 Estructura de Assets

```
src/assets/
├── fonts/              # Fuentes TTF monoespaciadas
│   ├── main.ttf       # Fuente principal para texto
│   └── ascii.ttf      # Fuente para arte ASCII
└── sounds/            # Audio files (WAV/OGG/MP3)
    ├── combat/
    │   ├── hit.mp3
    │   ├── miss.mp3
    │   └── battle_start.mp3
    ├── ui/
    │   ├── click.mp3
    │   └── menu_select.mp3
    └── music/
        ├── main_menu.mp3
        └── ambience_sound.mp3
```

### Nomenclatura de Assets

```python
# Fuentes
font_main.ttf             # Fuente de texto normal
font_ascii_art.ttf        # Fuente para arte ASCII (monoespaciada)

# Sonidos
sfx_combat_hit.mp3        # Efecto de sonido
music_main_menu.mp3       # Música de fondo
ambience_dungeon.mp3      # Ambiente
```

---

## 🎨 Sistema de Renderizado ASCII

---

## 🎨 Sistema de Renderizado ASCII

### Renderizado de Personajes

```python
def draw_character(screen, font_ascii, x, y, character_art, color=(255, 255, 255)):
    """
    Renderiza arte ASCII multi-línea en pantalla.
    
    Args:
        screen: Surface de pygame
        font_ascii: Fuente monoespaciada para ASCII art
        x, y: Coordenadas de inicio
        character_art: Lista de strings (cada string es una línea)
        color: Color RGB para el personaje
    """
    line_spacing = 20  # Espaciado entre líneas
    
    for i, line in enumerate(character_art):
        text_surface = font_ascii.render(line, True, color)
        screen.blit(text_surface, (x, y + i * line_spacing))


# Ejemplo de arte ASCII para personaje
PLAYER_IDLE = [
    "  O  ",
    " /|\\ ",
    " / \\ "
]

PLAYER_ATTACK = [
    "  O  ",
    " /|--",  # Brazo extendido
    " / \\ "
]

ENEMY_GOBLIN = [
    " ._. ",
    "((o))",
    " /^\\ "
]
```

### Caché de Texto Renderizado

```python
class ASCIITextCache:
    """Cachea surfaces de texto ASCII para performance."""
    
    def __init__(self, max_size: int = 200):
        self.cache: Dict[str, pygame.Surface] = {}
        self.max_size = max_size
    
    def get_text(self, text: str, font: pygame.font.Font, 
                 color: Tuple[int, int, int]) -> pygame.Surface:
        """Obtener texto del caché o renderizar."""
        # Crear key único
        key = f"{text}_{font.get_height()}_{color}"
        
        if key not in self.cache:
            # Limpiar caché si está lleno
            if len(self.cache) >= self.max_size:
                # Eliminar el primer elemento (FIFO)
                self.cache.pop(next(iter(self.cache)))
            
            # Renderizar y cachear
            self.cache[key] = font.render(text, True, color)
        
        return self.cache[key]
    
    def clear(self):
        """Limpiar caché completamente."""
        self.cache.clear()

# Uso global
ascii_cache = ASCIITextCache()
text_surface = ascii_cache.get_text("HP: 100", font, (255, 255, 255))
screen.blit(text_surface, (10, 10))
```

### Dibujo de UI con Caracteres

```python
def draw_box(screen, font, x, y, width, height, 
             border_color=(255, 255, 255), fill_color=(0, 0, 0)):
    """Dibuja un cuadro ASCII."""
    # Caracteres de box drawing
    TOP_LEFT = "┌"
    TOP_RIGHT = "┐"
    BOTTOM_LEFT = "└"
    BOTTOM_RIGHT = "┘"
    HORIZONTAL = "─"
    VERTICAL = "│"
    
    char_width = font.size(HORIZONTAL)[0]
    char_height = font.get_height()
    
    cols = width // char_width
    rows = height // char_height
    
    # Fondo
    if fill_color:
        pygame.draw.rect(screen, fill_color, (x, y, width, height))
    
    # Línea superior
    screen.blit(font.render(TOP_LEFT, True, border_color), (x, y))
    for i in range(1, cols - 1):
        screen.blit(font.render(HORIZONTAL, True, border_color), 
                   (x + i * char_width, y))
    screen.blit(font.render(TOP_RIGHT, True, border_color), 
               (x + (cols - 1) * char_width, y))
    
    # Lados
    for i in range(1, rows - 1):
        screen.blit(font.render(VERTICAL, True, border_color), 
                   (x, y + i * char_height))
        screen.blit(font.render(VERTICAL, True, border_color), 
                   (x + (cols - 1) * char_width, y + i * char_height))
    
    # Línea inferior
    screen.blit(font.render(BOTTOM_LEFT, True, border_color), 
               (x, y + (rows - 1) * char_height))
    for i in range(1, cols - 1):
        screen.blit(font.render(HORIZONTAL, True, border_color), 
                   (x + i * char_width, y + (rows - 1) * char_height))
    screen.blit(font.render(BOTTOM_RIGHT, True, border_color), 
               (x + (cols - 1) * char_width, y + (rows - 1) * char_height))


def draw_health_bar(screen, font, x, y, current, maximum, width=200):
    """Barra de vida usando caracteres ASCII."""
    # Calcular ratio
    ratio = max(0.0, min(1.0, current / maximum)) if maximum > 0 else 0
    filled = int((width / 10) * ratio)  # Cada █ representa ~10px
    empty = (width // 10) - filled
    
    # Dibujar barra
    bar = "█" * filled + "░" * empty
    text_surface = font.render(bar, True, (255, 255, 255))
    screen.blit(text_surface, (x, y))
    
    # Números
    hp_text = f"{current}/{maximum}"
    hp_surface = font.render(hp_text, True, (255, 255, 255))
    screen.blit(hp_surface, (x, y + 20))
```

---

## 🎬 Sistema de Animaciones ASCII

### Animaciones por Frame

```python
class ASCIIAnimation:
    """Animación de arte ASCII por frames."""
    
    def __init__(self, frames: List[List[str]], frame_duration: float = 0.1):
        """
        Args:
            frames: Lista de frames, cada frame es lista de strings
            frame_duration: Duración de cada frame en segundos
        """
        self.frames = frames
        self.frame_duration = frame_duration
        self.current_frame = 0
        self.time_accumulator = 0.0
        self.playing = True
        self.loop = True
    
    def update(self, dt: float):
        """Actualizar animación."""
        if not self.playing:
            return
        
        self.time_accumulator += dt
        
        if self.time_accumulator >= self.frame_duration:
            self.time_accumulator = 0.0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.playing = False
    
    def get_current_frame(self) -> List[str]:
        """Obtener frame actual."""
        return self.frames[self.current_frame]
    
    def reset(self):
        """Reiniciar animación."""
        self.current_frame = 0
        self.time_accumulator = 0.0
        self.playing = True


# Ejemplo: Animación de ataque
ATTACK_FRAMES = [
    # Frame 1: Preparación
    [
        "  O  ",
        " /|\\ ",
        " / \\ "
    ],
    # Frame 2: Golpe
    [
        "  O  ",
        " /|--",
        " / \\ "
    ],
    # Frame 3: Retroceso
    [
        "  O  ",
        "--|\\ ",
        " / \\ "
    ],
]

# Uso
attack_anim = ASCIIAnimation(ATTACK_FRAMES, frame_duration=0.15)

# En game loop
def update(dt):
    attack_anim.update(dt)
    current_frame = attack_anim.get_current_frame()
    draw_character(screen, font, x, y, current_frame)
```

### Efectos Visuales con ASCII

```python
def screen_shake(intensity: int = 5, duration: float = 0.2) -> Iterator[Tuple[int, int]]:
    """Generador para screen shake offset."""
    import random
    import time
    
    start_time = time.time()
    while time.time() - start_time < duration:
        offset_x = random.randint(-intensity, intensity)
        offset_y = random.randint(-intensity, intensity)
        yield (offset_x, offset_y)
    
    yield (0, 0)  # Volver a posición original


def create_damage_popup(damage: int, is_critical: bool = False) -> Dict:
    """Crear popup de daño flotante."""
    return {
        'text': str(damage),
        'color': (255, 0, 0) if is_critical else (255, 255, 255),
        'x': 0,
        'y': 0,
        'velocity_y': -2,  # Flota hacia arriba
        'lifetime': 1.0,
        'elapsed': 0.0
    }


def update_damage_popups(popups: List[Dict], dt: float):
    """Actualizar popups de daño."""
    for popup in popups[:]:
        popup['elapsed'] += dt
        popup['y'] += popup['velocity_y']
        
        # Fade out
        alpha = int(255 * (1.0 - popup['elapsed'] / popup['lifetime']))
        popup['color'] = (*popup['color'][:3], alpha)
        
        # Remover si expiró
        if popup['elapsed'] >= popup['lifetime']:
            popups.remove(popup)
```

---

## 🎨 Paletas de Color para ASCII Art

### Colores Temáticos

```python
# Colores base
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# UI
UI_BG = (20, 20, 30)
UI_BORDER = (100, 100, 120)
UI_TEXT = (220, 220, 220)

# Combate
HP_COLOR = (200, 50, 50)      # Rojo para vida
MP_COLOR = (50, 50, 200)      # Azul para maná
STAMINA_COLOR = (50, 200, 50) # Verde para stamina

# Estados
POISON_COLOR = (150, 50, 200)  # Púrpura
BURN_COLOR = (255, 100, 0)     # Naranja
FROZEN_COLOR = (100, 200, 255) # Azul claro

# Feedback
DAMAGE_COLOR = (255, 50, 50)
HEAL_COLOR = (50, 255, 50)
CRITICAL_COLOR = (255, 255, 0)
MISS_COLOR = (150, 150, 150)
```

### Aplicar Efectos de Color

```python
def apply_status_effect_color(base_art: List[str], 
                              status: str) -> Tuple[List[str], Tuple[int, int, int]]:
    """
    Modificar arte ASCII según estado.
    
    Returns:
        Tupla de (arte_modificado, color)
    """
    if status == "poisoned":
        return (base_art, POISON_COLOR)
    elif status == "burning":
        # Añadir efecto de fuego
        modified = base_art.copy()
        modified.append("  ^^ ")  # Llamas
        return (modified, BURN_COLOR)
    elif status == "frozen":
        # Añadir cristales de hielo
        modified = ["*" + line + "*" for line in base_art]
        return (modified, FROZEN_COLOR)
    
    return (base_art, WHITE)
```

---

## 🔄 Game Loop Architecture

### Estructura Básica (Sin cambios - Aplica igual para ASCII)

```python
class Game:
    def __init__(self):
        """Inicialización única del juego."""
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "MENU"
        
        # Cargar fuentes para ASCII art
        self.font_text = pygame.font.Font("fonts/main.ttf", 24)
        self.font_ascii = pygame.font.Font("fonts/ascii.ttf", 20)
        
    def run(self):
        """Game loop principal."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time en segundos
            
            # 1. Procesar eventos
            self.handle_events()
            
            # 2. Actualizar lógica
            self.update(dt)
            
            # 3. Renderizar
            self.render()
            
            # 4. Actualizar display
            pygame.display.flip()
    
    def handle_events(self):
        """Procesar inputs del usuario."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.current_state.handle_event(event)
    
    def update(self, dt):
        """Actualizar lógica del juego con delta time."""
        self.current_state.update(dt)
    
    def render(self):
        """Renderizar frame actual."""
        self.screen.fill((0, 0, 0))
        self.current_state.render(self.screen, self.font_text, self.font_ascii)
```

### Delta Time Pattern (Crítico para animaciones)

```python
# ✅ BIEN: Movimiento independiente de framerate
def update(self, dt):
    """dt en segundos (ej: 0.016 para 60 FPS)."""
    self.position.x += self.velocity.x * dt * 100  # 100 píxeles/segundo
    self.animation_timer += dt

# ❌ MAL: Movimiento dependiente de framerate
def update(self):
    self.position.x += self.velocity.x  # Varía según FPS
```

### Fixed Timestep para Física

```python
class PhysicsGame:
    def __init__(self):
        self.accumulator = 0.0
        self.fixed_dt = 1.0 / 60.0  # 60 updates/segundo
    
    def run(self):
        while self.running:
            frame_time = self.clock.tick(FPS) / 1000.0
            self.accumulator += frame_time
            
            # Fixed update para física
            while self.accumulator >= self.fixed_dt:
                self.fixed_update(self.fixed_dt)
                self.accumulator -= self.fixed_dt
            
            # Variable update para renderizado
            self.render()
```

---

## 🎨 Sistema de Renderizado

### Optimización con Dirty Rects

```python
# ✅ BIEN: Solo actualizar áreas que cambiaron
dirty_rects = []
for sprite in self.sprites:
    if sprite.dirty:
        dirty_rects.append(sprite.rect)
        self.screen.blit(sprite.image, sprite.rect)
        sprite.dirty = False

pygame.display.update(dirty_rects)

# ❌ MAL para juegos pequeños, pero simple
pygame.display.flip()  # Actualiza toda la pantalla
```

### Surface Caching

```python
class TextCache:
    """Cachear renders de texto para performance."""
    def __init__(self):
        self._cache: Dict[str, pygame.Surface] = {}
    
    def get_text(self, text: str, font: pygame.font.Font, 
                 color: Tuple[int, int, int]) -> pygame.Surface:
        """Obtener texto del caché o renderizar."""
        key = f"{text}_{font.get_height()}_{color}"
        
        if key not in self._cache:
            self._cache[key] = font.render(text, True, color)
        
        return self._cache[key]
    
    def clear(self):
        """Limpiar caché cuando sea necesario."""
        self._cache.clear()

# Uso
text_cache = TextCache()
text_surface = text_cache.get_text("HP: 100", font, WHITE)
screen.blit(text_surface, (10, 10))
```

### Sprite Groups

```python
# ✅ BIEN: Usar sprite groups de pygame
class Game:
    def __init__(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
    
    def update(self, dt):
        self.all_sprites.update(dt)
        
        # Detección de colisiones optimizada
        hits = pygame.sprite.groupcollide(
            self.projectiles, 
            self.enemies,
            True,  # Eliminar proyectil
            False  # No eliminar enemigo aún
        )
        
        for projectile, enemy_list in hits.items():
            for enemy in enemy_list:
                enemy.take_damage(projectile.damage)
    
    def render(self):
        self.all_sprites.draw(self.screen)  # Batch rendering
```

---

## 🎯 State Machine Pattern

### Implementación de Estados

```python
from abc import ABC, abstractmethod
from typing import Dict

class GameState(ABC):
    """Clase base para estados del juego."""
    
    @abstractmethod
    def enter(self):
        """Llamado al entrar al estado."""
        pass
    
    @abstractmethod
    def exit(self):
        """Llamado al salir del estado."""
        pass
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        """Procesar evento."""
        pass
    
    @abstractmethod
    def update(self, dt: float):
        """Actualizar lógica."""
        pass
    
    @abstractmethod
    def render(self, screen: pygame.Surface):
        """Renderizar estado."""
        pass


class MenuState(GameState):
    """Estado del menú principal."""
    
    def enter(self):
        print("Entering menu...")
        self.selected_option = 0
    
    def exit(self):
        print("Exiting menu...")
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = max(0, self.selected_option - 1)
            elif event.key == pygame.K_DOWN:
                self.selected_option = min(2, self.selected_option + 1)
            elif event.key == pygame.K_RETURN:
                return f"OPTION_{self.selected_option}"
        return None
    
    def update(self, dt):
        # Animaciones del menú
        pass
    
    def render(self, screen):
        # Dibujar opciones del menú
        pass


class StateManager:
    """Gestor de estados del juego."""
    
    def __init__(self):
        self.states: Dict[str, GameState] = {}
        self.current_state: GameState = None
        self.current_state_name: str = None
    
    def add_state(self, name: str, state: GameState):
        """Registrar un nuevo estado."""
        self.states[name] = state
    
    def change_state(self, name: str):
        """Cambiar al estado especificado."""
        if self.current_state:
            self.current_state.exit()
        
        self.current_state = self.states[name]
        self.current_state_name = name
        self.current_state.enter()
    
    def handle_event(self, event):
        """Delegar evento al estado actual."""
        if self.current_state:
            return self.current_state.handle_event(event)
        return None
    
    def update(self, dt):
        """Actualizar estado actual."""
        if self.current_state:
            self.current_state.update(dt)
    
    def render(self, screen):
        """Renderizar estado actual."""
        if self.current_state:
            self.current_state.render(screen)
```

---

## 💥 Sistema de Partículas ASCII

### Particle Class

```python
class ASCIIParticle:
    """Partícula ASCII para efectos visuales."""
    
    CHARS = ["*", "+", "·", "o", "°", "•"]  # Caracteres de partícula
    
    def __init__(self, x: float, y: float, vx: float, vy: float,
                 lifetime: float, color: Tuple[int, int, int], 
                 char: str = None):
        self.x = x
        self.y = y
        self.vx = vx  # Velocidad en X
        self.vy = vy  # Velocidad en Y
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.char = char or random.choice(self.CHARS)
        self.alive = True
    
    def update(self, dt: float):
        """Actualizar posición y vida."""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 200 * dt  # Gravedad
        self.lifetime -= dt
        
        if self.lifetime <= 0:
            self.alive = False
    
    def render(self, screen: pygame.Surface, font: pygame.font.Font):
        """Renderizar partícula ASCII."""
        if self.alive:
            # Fade out basado en lifetime
            alpha_ratio = self.lifetime / self.max_lifetime
            # Pygame font no soporta alpha, usar color más oscuro
            faded_color = tuple(int(c * alpha_ratio) for c in self.color)
            
            text_surface = font.render(self.char, True, faded_color)
            screen.blit(text_surface, (int(self.x), int(self.y)))


class ASCIIParticleSystem:
    """Sistema de gestión de partículas ASCII."""
    
    def __init__(self, font: pygame.font.Font, max_particles: int = 100):
        self.font = font
        self.particles: List[ASCIIParticle] = []
        self.max_particles = max_particles
    
    def emit(self, x: float, y: float, count: int = 10, 
             color: Tuple[int, int, int] = (255, 255, 255)):
        """Emitir partículas desde una posición."""
        import random
        import math
        
        for _ in range(count):
            if len(self.particles) >= self.max_particles:
                break
            
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            particle = ASCIIParticle(
                x, y, vx, vy,
                lifetime=random.uniform(0.5, 1.5),
                color=color
            )
            self.particles.append(particle)
    
    def update(self, dt: float):
        """Actualizar todas las partículas."""
        # Actualizar y eliminar muertas
        self.particles = [p for p in self.particles if p.alive]
        
        for particle in self.particles:
            particle.update(dt)
    
    def render(self, screen: pygame.Surface):
        """Renderizar todas las partículas."""
        for particle in self.particles:
            particle.render(screen, self.font)

# Uso
particle_system = ASCIIParticleSystem(font_ascii)

# En combate, al hacer daño
particle_system.emit(enemy_x + 20, enemy_y + 20, count=15, color=(255, 0, 0))

# En game loop
particle_system.update(dt)
particle_system.render(screen)
```

---

## 🎵 Sistema de Audio (Compatible con ASCII Art)

### Audio Manager

```python
class AudioManager:
    """Gestor centralizado de audio del juego."""
    
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        
    def load_sound(self, name: str, path: str):
        """Cargar efecto de sonido."""
        try:
            self.sounds[name] = pygame.mixer.Sound(path)
            self.sounds[name].set_volume(self.sfx_volume)
        except pygame.error as e:
            print(f"Error loading sound {name}: {e}")
    
    def play_sound(self, name: str, loops: int = 0):
        """Reproducir efecto de sonido."""
        if name in self.sounds:
            self.sounds[name].play(loops)
    
    def load_music(self, path: str):
        """Cargar música de fondo."""
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
        except pygame.error as e:
            print(f"Error loading music: {e}")
    
    def play_music(self, loops: int = -1, fade_ms: int = 0):
        """Reproducir música (loops=-1 para loop infinito)."""
        pygame.mixer.music.play(loops, fade_ms=fade_ms)
    
    def stop_music(self, fade_ms: int = 1000):
        """Detener música con fade out."""
        pygame.mixer.music.fadeout(fade_ms)
    
    def set_music_volume(self, volume: float):
        """Ajustar volumen de música (0.0 a 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume: float):
        """Ajustar volumen de efectos (0.0 a 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

# Uso
audio = AudioManager()
audio.load_sound("hit", "src/sounds/combat/hit.wav")
audio.load_music("src/sounds/music/battle.ogg")

# En combate
audio.play_sound("hit")
audio.play_music(loops=-1, fade_ms=500)
```

---

## 🎬 Sistema de Animaciones

### Sprite Animation

```python
class AnimatedSprite:
    """Sprite con soporte para animaciones por frames."""
    
    def __init__(self, spritesheet_path: str, frame_width: int, 
                 frame_height: int, animation_speed: float = 0.1):
        # Cargar spritesheet
        self.spritesheet = pygame.image.load(spritesheet_path).convert_alpha()
        
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.animation_speed = animation_speed
        
        # Extraer frames
        self.frames: List[pygame.Surface] = []
        self._extract_frames()
        
        # Estado de animación
        self.current_frame = 0
        self.animation_timer = 0.0
        self.playing = True
        self.loop = True
    
    def _extract_frames(self):
        """Extraer frames individuales del spritesheet."""
        sheet_width = self.spritesheet.get_width()
        sheet_height = self.spritesheet.get_height()
        
        for y in range(0, sheet_height, self.frame_height):
            for x in range(0, sheet_width, self.frame_width):
                frame = self.spritesheet.subsurface(
                    pygame.Rect(x, y, self.frame_width, self.frame_height)
                )
                self.frames.append(frame)
    
    def update(self, dt: float):
        """Actualizar animación."""
        if not self.playing:
            return
        
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.playing = False
    
    def get_current_frame(self) -> pygame.Surface:
        """Obtener frame actual."""
        return self.frames[self.current_frame]
    
    def reset(self):
        """Reiniciar animación."""
        self.current_frame = 0
        self.animation_timer = 0.0
        self.playing = True
```

### Multi-Animation Sprite

```python
class Character:
    """Personaje con múltiples animaciones."""
    
    def __init__(self):
        self.animations: Dict[str, List[pygame.Surface]] = {
            "idle": self._load_animation("idle", 4),
            "walk": self._load_animation("walk", 8),
            "attack": self._load_animation("attack", 6),
        }
        
        self.current_animation = "idle"
        self.current_frame = 0
        self.animation_speed = 0.1
        self.animation_timer = 0.0
    
    def _load_animation(self, name: str, frame_count: int) -> List[pygame.Surface]:
        """Cargar frames de una animación."""
        frames = []
        for i in range(frame_count):
            path = f"assets/sprites/player/{name}_{i:02d}.png"
            frame = pygame.image.load(path).convert_alpha()
            frames.append(frame)
        return frames
    
    def set_animation(self, name: str):
        """Cambiar animación actual."""
        if name != self.current_animation:
            self.current_animation = name
            self.current_frame = 0
            self.animation_timer = 0.0
    
    def update(self, dt: float):
        """Actualizar animación."""
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            frames = self.animations[self.current_animation]
            self.current_frame = (self.current_frame + 1) % len(frames)
    
    def render(self, screen: pygame.Surface, x: int, y: int):
        """Renderizar frame actual."""
        frames = self.animations[self.current_animation]
        screen.blit(frames[self.current_frame], (x, y))
```

---

## ⚔️ Combat System Patterns

### Damage Calculation

```python
from typing import Dict, Optional
from enum import Enum

class DamageType(Enum):
    """Tipos de daño."""
    PHYSICAL = "physical"
    MAGICAL = "magical"
    TRUE = "true"  # Ignora defensas

class CombatCalculator:
    """Calculador de daño y efectos de combate."""
    
    @staticmethod
    def calculate_damage(attacker_damage: int, 
                        defender_defense: int,
                        damage_type: DamageType = DamageType.PHYSICAL,
                        critical_chance: float = 0.0) -> Dict[str, any]:
        """
        Calcular daño final.
        
        Returns:
            Dict con keys: 'damage', 'is_critical', 'blocked'
        """
        import random
        
        # Check crítico
        is_critical = random.random() < critical_chance
        damage = attacker_damage
        
        if is_critical:
            damage *= 2
        
        # Aplicar defensa
        if damage_type == DamageType.PHYSICAL:
            damage_reduction = defender_defense * 0.5
            final_damage = max(1, damage - damage_reduction)
        elif damage_type == DamageType.MAGICAL:
            damage_reduction = defender_defense * 0.3
            final_damage = max(1, damage - damage_reduction)
        else:  # TRUE damage
            final_damage = damage
        
        return {
            'damage': int(final_damage),
            'is_critical': is_critical,
            'type': damage_type
        }
    
    @staticmethod
    def calculate_hit_chance(attacker_accuracy: int,
                            defender_evasion: int) -> float:
        """Calcular probabilidad de impacto."""
        base_hit = 0.85  # 85% base
        accuracy_bonus = attacker_accuracy * 0.01
        evasion_penalty = defender_evasion * 0.01
        
        hit_chance = base_hit + accuracy_bonus - evasion_penalty
        return max(0.05, min(0.95, hit_chance))  # Entre 5% y 95%
```

### Status Effects

```python
class StatusEffect:
    """Efecto de estado (buff/debuff)."""
    
    def __init__(self, effect_type: str, value: int, 
                 duration: float, stacks: int = 1):
        self.type = effect_type  # "poison", "burn", "strength", etc.
        self.value = value
        self.duration = duration
        self.max_duration = duration
        self.stacks = stacks
    
    def update(self, dt: float) -> bool:
        """
        Actualizar duración.
        
        Returns:
            True si el efecto sigue activo, False si expiró
        """
        self.duration -= dt
        return self.duration > 0
    
    def apply(self, target: 'Character') -> Optional[int]:
        """
        Aplicar efecto al objetivo.
        
        Returns:
            Daño/curación causado (si aplica)
        """
        if self.type == "poison":
            target.health -= self.value * self.stacks
            return -self.value * self.stacks
        elif self.type == "regeneration":
            heal = self.value * self.stacks
            target.health = min(target.max_health, target.health + heal)
            return heal
        elif self.type == "strength":
            # Buff aplicado pasivamente
            return None
        
        return None

class StatusEffectManager:
    """Gestor de efectos de estado de un personaje."""
    
    def __init__(self):
        self.active_effects: List[StatusEffect] = []
    
    def add_effect(self, effect: StatusEffect):
        """Añadir nuevo efecto (stackeable si aplica)."""
        # Buscar si ya existe el mismo tipo
        existing = next((e for e in self.active_effects 
                        if e.type == effect.type), None)
        
        if existing:
            # Stackear o refrescar duración
            existing.stacks += 1
            existing.duration = max(existing.duration, effect.duration)
        else:
            self.active_effects.append(effect)
    
    def update(self, dt: float, target: 'Character') -> List[Dict]:
        """
        Actualizar todos los efectos activos.
        
        Returns:
            Lista de eventos (daño/curación causados)
        """
        events = []
        
        # Actualizar y aplicar efectos
        for effect in self.active_effects[:]:
            damage = effect.apply(target)
            
            if damage is not None:
                events.append({
                    'type': effect.type,
                    'value': damage
                })
            
            # Remover si expiró
            if not effect.update(dt):
                self.active_effects.remove(effect)
        
        return events
    
    def get_stat_modifier(self, stat_name: str) -> float:
        """Obtener modificador total de una estadística."""
        modifier = 1.0
        
        for effect in self.active_effects:
            if effect.type == "strength" and stat_name == "damage":
                modifier += 0.2 * effect.stacks
            elif effect.type == "weakness" and stat_name == "damage":
                modifier -= 0.2 * effect.stacks
        
        return max(0.1, modifier)  # Mínimo 10%
```

---

## 🔍 Debugging y Profiling

### FPS Counter

```python
class FPSCounter:
    """Contador de FPS para debugging."""
    
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.clock = pygame.time.Clock()
        self.fps_history: List[float] = []
        self.max_history = 60
    
    def update(self):
        """Actualizar contador."""
        fps = self.clock.get_fps()
        self.fps_history.append(fps)
        
        if len(self.fps_history) > self.max_history:
            self.fps_history.pop(0)
    
    def render(self, screen: pygame.Surface, x: int = 10, y: int = 10):
        """Renderizar FPS en pantalla."""
        if self.fps_history:
            avg_fps = sum(self.fps_history) / len(self.fps_history)
            text = f"FPS: {avg_fps:.1f}"
            
            color = (0, 255, 0)  # Verde
            if avg_fps < 30:
                color = (255, 0, 0)  # Rojo
            elif avg_fps < 50:
                color = (255, 255, 0)  # Amarillo
            
            surface = self.font.render(text, True, color)
            screen.blit(surface, (x, y))
```

### Debug Overlay

```python
class DebugOverlay:
    """Overlay de información de debugging."""
    
    def __init__(self, font: pygame.font.Font):
        self.font = font
        self.enabled = False
        self.info: Dict[str, any] = {}
    
    def toggle(self):
        """Toggle overlay."""
        self.enabled = not self.enabled
    
    def set_info(self, key: str, value: any):
        """Actualizar información."""
        self.info[key] = value
    
    def render(self, screen: pygame.Surface):
        """Renderizar overlay."""
        if not self.enabled:
            return
        
        y = 10
        for key, value in self.info.items():
            text = f"{key}: {value}"
            surface = self.font.render(text, True, (255, 255, 0))
            screen.blit(surface, (10, y))
            y += 20
```

---

## ✅ Best Practices Checklist

### Performance
- [ ] Usar delta time para animaciones y movimiento
- [ ] Cachear surfaces cuando sea posible
- [ ] Usar sprite groups para batch rendering
- [ ] Limitar número de partículas activas
- [ ] Optimizar colisiones con spatial partitioning si es necesario

### Code Quality
- [ ] Type hints en todas las funciones
- [ ] Docstrings en clases y métodos públicos
- [ ] Separar lógica de renderizado
- [ ] Usar constantes para valores mágicos
- [ ] Manejar errores de carga de recursos

### Game Feel
- [ ] Screen shake en impactos
- [ ] Partículas en efectos importantes
- [ ] Sound effects bien timeados
- [ ] Feedback visual inmediato
- [ ] Transiciones suaves entre estados

### Testing
- [ ] Test de game loop básico
- [ ] Test de sistemas de combate
- [ ] Test de save/load
- [ ] Playtesting frecuente
- [ ] Verificar balance de dificultad

---

**Última actualización**: Enero 2026 - v0.5
**Creado por**: GameDevSenior
