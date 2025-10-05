import os, time, sys, pygame
from config import Colors, TransitionConfig, FontConfig, MenuConfig



def slow_print(screen, font_ascii, text, x, y, color=Colors.WHITE, clear_area=True):
    """Draw text char-by-char. Optionally clear the message area first so lines don't overlap.

    Clears a horizontal strip starting at x,y using the font height.
    """
    # Clear the message area to avoid overlapping texts
    if clear_area:
        try:
            text_height = font_ascii.get_height()
            text_width = font_ascii.size(text)[0]
        except Exception:
            text_height = FontConfig.DEFAULT_HEIGHT
            text_width = len(text) * FontConfig.DEFAULT_CHAR_WIDTH
        clear_rect = (x, y, text_width + FontConfig.CLEAR_PADDING, text_height + FontConfig.CLEAR_PADDING // 2)
        screen.fill(Colors.BLACK, clear_rect)

    # Inicializa la posición de X
    current_x = x
    for char in text:
        draw_text(screen, font_ascii, char, current_x, y, color)
        pygame.display.flip()
        current_x += font_ascii.size(char)[0]  # Obtener el ancho real del carácter
        time.sleep(TransitionConfig.SLOW_PRINT_DELAY)


def blocking_message(screen, font_ascii, text, x, y, color=Colors.WHITE, clear_area=True, timeout=TransitionConfig.MESSAGE_DELAY, wait_for_key=False, bg_color=Colors.BLACK_ALPHA, border_color=None):
    """Type text (using slow_print) and then wait for keypress or timeout (ms).
    Returns when user pressed a key or timeout elapsed.
    """
    # Optionally draw a semi-transparent background rectangle to guarantee readability
    if clear_area:
        try:
            text_height = font_ascii.get_height()
            text_width = font_ascii.size(text)[0]
        except Exception:
            text_height = FontConfig.DEFAULT_HEIGHT
            text_width = len(text) * FontConfig.DEFAULT_CHAR_WIDTH
        bg = pygame.Surface((text_width + FontConfig.BG_PADDING, text_height + FontConfig.BG_PADDING), pygame.SRCALPHA)
        # Normalize bg_color to RGBA
        if len(bg_color) == 3:
            bg_rgba = (bg_color[0], bg_color[1], bg_color[2], 180)
        else:
            bg_rgba = bg_color
        bg.fill(bg_rgba)
        screen.blit(bg, (x - FontConfig.BG_OFFSET, y - FontConfig.BG_OFFSET // 2))
        # Optional border
        if border_color:
            try:
                rect = pygame.Rect(x - 4, y - 2, text_width + 12, text_height + 8)
                pygame.draw.rect(screen, border_color, rect, 1)
            except Exception:
                pass

    # Type the text
    slow_print(screen, font_ascii, text, x, y, color=color, clear_area=False)
    # Wait for key or timeout (or force waiting for key if requested)
    start = pygame.time.get_ticks()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return
            if ev.type == pygame.KEYDOWN:
                return
        if not wait_for_key and pygame.time.get_ticks() - start >= timeout:
            return
        pygame.time.wait(TransitionConfig.EVENT_CHECK_DELAY)


def resource_path(relative_path):
    """Consigue la ruta absoluta al recurso, funciona empaquetado o no."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def draw_text(screen, font, text, x, y, color=Colors.WHITE):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def show_popup(screen, font, mensaje, WINDOW_WIDTH, WINDOW_HEIGHT, width=500, height=150):
    # Dibuja un rectángulo semitransparente sobre la pantalla
    popup_surface = pygame.Surface((width, height))
    popup_surface.set_alpha(230)  # Transparencia (0-255)
    popup_surface.fill(Colors.POPUP_BG)  # Color del cuadro

    # Borde opcional
    pygame.draw.rect(popup_surface, Colors.WHITE, popup_surface.get_rect(), 2)

    # Renderiza el texto
    text_surface = font.render(mensaje, True, Colors.WHITE)
    text_rect = text_surface.get_rect(center=(width // 2, height // 2))

    popup_surface.blit(text_surface, text_rect)

    # Posición centrada en la pantalla principal
    x = (WINDOW_WIDTH - width) // 2
    y = (WINDOW_HEIGHT - height) // 2
    screen.blit(popup_surface, (x, y))
    pygame.display.update()

    time.sleep(TransitionConfig.MESSAGE_DELAY / 1000)  # Pausa para mostrar el mensaje


class Toast:
    def __init__(self, text, duration=TransitionConfig.MESSAGE_DELAY, color=Colors.WHITE):
        self.text = text
        self.duration = duration
        self.color = color
        self.start = None
        self.alpha = 255
        self.y_offset = 0


class ToastManager:
    def __init__(self):
        self.toasts = []

    def add(self, text, duration=TransitionConfig.MESSAGE_DELAY):
        t = Toast(text, duration)
        t.start = int(time.time() * 1000)
        self.toasts.append(t)

    def add(self, text, duration=TransitionConfig.MESSAGE_DELAY, color=Colors.WHITE):
        t = Toast(text, duration, color)
        t.start = int(time.time() * 1000)
        self.toasts.append(t)

    def draw(self, screen, font, x=MenuConfig.TOAST_X, start_y=MenuConfig.TOAST_START_Y, spacing=MenuConfig.TOAST_SPACING):
        now = int(time.time() * 1000)
        alive = []
        y = start_y
        for t in self.toasts:
            elapsed = now - t.start
            if elapsed < t.duration:
                # fade out in last 300ms
                fade_start = max(0, t.duration - TransitionConfig.TOAST_FADE_DURATION)
                if elapsed >= fade_start:
                    alpha = int(255 * (1 - (elapsed - fade_start) / max(1, t.duration - fade_start)))
                else:
                    alpha = 255
                # slide up a bit as it ages
                t.y_offset = int( -MenuConfig.TOAST_SLIDE_OFFSET * (elapsed / t.duration))

                # render text to surface to support alpha and draw a semi-transparent bg
                text_surface = font.render(t.text, True, t.color)
                text_w, text_h = text_surface.get_size()
                bg_surf = pygame.Surface((text_w + FontConfig.BG_PADDING, text_h + FontConfig.BG_PADDING // 2), pygame.SRCALPHA)
                # semi-transparent black background
                bg_color = Colors.BLACK_ALPHA
                bg_surf.fill(bg_color)
                # apply fade by multiplying alpha
                try:
                    bg_surf.set_alpha(alpha)
                except Exception:
                    pass
                # blit text onto bg
                bg_surf.blit(text_surface, (4, 2))
                # finally blit the composed surface
                screen.blit(bg_surf, (x, y + t.y_offset))
                y += spacing
                alive.append(t)
        self.toasts = alive


# Background caching: pre-render the ASCII dungeon to a surface for faster blits
def make_dungeon_surface(font_ascii):
    # Render one repetition of the BACKGROUND to a surface
    sample_line = BACKGROUND[0]
    pattern_px_width = font_ascii.size(sample_line)[0] if sample_line else 800
    line_height = font_ascii.get_height()
    surf = pygame.Surface((pattern_px_width, len(BACKGROUND) * line_height), pygame.SRCALPHA)
    for i, line in enumerate(BACKGROUND):
        y = i * line_height
        draw_text(surf, font_ascii, line, 0, y, (200, 200, 200))
    return surf


# Module-level toast manager
toast_manager = ToastManager()

# Cached dungeon surface (set to None by default, created lazily)
_dungeon_surface_cache = None

def get_dungeon_surface(font_ascii):
    global _dungeon_surface_cache
    if _dungeon_surface_cache is None:
        try:
            _dungeon_surface_cache = make_dungeon_surface(font_ascii)
        except Exception:
            _dungeon_surface_cache = None
    return _dungeon_surface_cache


class CombatMessageBox:
    """A persistent fixed-size message box drawn above the bottom of the screen.
    It is drawn every frame (draw_box) so it remains visible. Defaults tuned to be
    slightly lower and a bit taller than before.
    """
    def __init__(self, left=None, margin_bottom=80, width=600, height=110):
        # left: x position of the box. If None, box will be centered horizontally.
        # margin_bottom: distance from bottom of screen (higher -> box is higher)
        # width: fixed width of the box in pixels
        self.left = left
        self.margin_bottom = margin_bottom
        self.width = width
        self.height = height

    def draw_box(self, screen, font):
        sw, sh = screen.get_size()
        # Determine box width
        box_w = max(200, min(self.width, sw - 40)) if hasattr(self, 'width') else max(200, sw - 300)
        box_h = self.height
        # Center horizontally if left is None
        if self.left is None:
            box_x = (sw - box_w) // 2
        else:
            box_x = self.left
        box_y = sh - box_h - self.margin_bottom
        # background
        bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
        bg.fill((0, 0, 0, 200))
        screen.blit(bg, (box_x, box_y))
        # border
        pygame.draw.rect(screen, (200,200,200), (box_x, box_y, box_w, box_h), 1)
        # interior coords
        inner_x = box_x + 8
        inner_y = box_y + 8
        inner_w = box_w - 16
        inner_h = box_h - 16
        return box_x, box_y, box_w, box_h, inner_x, inner_y, inner_w, inner_h

    def show(self, screen, font, text, timeout=1400, wait_for_key=False, bg_color=(0,0,0,200), border_color=(200,200,200)):
        # compute box (draw_box returns box coords and inner coords)
        box_x, box_y, box_w, box_h, inner_x, inner_y, inner_w, inner_h = self.draw_box(screen, font)
        line_h = font.get_height()
        max_lines = max(1, inner_h // line_h)

        # wrap words into lines that fit inner_w
        words = text.split(' ')
        lines = []
        cur = ''
        for w in words:
            trial = (cur + ' ' + w).strip() if cur else w
            if font.size(trial)[0] <= inner_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)

        # Only keep the last max_lines lines of the wrapped text
        if len(lines) > max_lines:
            lines = lines[-max_lines:]

        # Animate each line character by character; clear inner area before drawing each frame
        for li, line in enumerate(lines):
            for i in range(1, len(line) + 1):
                # clear inner area
                screen.fill((0,0,0), (inner_x-4, inner_y-4, inner_w+8, inner_h+8))
                # redraw box background/border (draw_box draws the static box)
                self.draw_box(screen, font)
                # draw previous full lines
                for j in range(li):
                    draw_text(screen, font, lines[j], inner_x, inner_y + j * line_h)
                # draw current partial line
                draw_text(screen, font, line[:i], inner_x, inner_y + li * line_h)
                pygame.display.flip()
                time.sleep(0.05)

        # wait for key or timeout
        start = pygame.time.get_ticks()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return
                if ev.type == pygame.KEYDOWN:
                    return
            if not wait_for_key and pygame.time.get_ticks() - start >= timeout:
                return
            pygame.time.wait(20)


# module-level combat message box (positioned slightly lower and taller)
combat_message_box = CombatMessageBox(margin_bottom=80, height=110)

BACKGROUND = [
    "-----------------------------------------------",
    "                                            ",
    "####  ######    ###########  #####  ### #####",
    " ###   ##  #     #####  ##    ###    #   ### ",
    "           #      ##                      # ",
    "                                            ",
    "                                            ",
    "                                            ",
    "                                            ",
    "                                            ",
    "                                            ",
    "----------------------------------------------",
]

def draw_custom_dungeon(screen, font_ascii, offset):
    screen_width, screen_height = screen.get_size()
    line_height = 20
    background_height = len(BACKGROUND) * line_height
    start_y = (screen_height - background_height) // 2
    # Determinar el ancho en píxeles de una repetición del patrón
    sample_line = BACKGROUND[0]
    pattern_px_width = font_ascii.size(sample_line)[0] if sample_line else screen_width

    # Normalizar offset para hacer wrap
    offset_mod = offset % pattern_px_width if pattern_px_width else 0

    # Try using cached surface for performance
    dungeon_surf = get_dungeon_surface(font_ascii)
    if dungeon_surf:
        surf_w = dungeon_surf.get_width()
        # draw repeated surfaces to cover screen, using offset_mod
        x_start = -offset_mod
        for i in range(-1, int(screen_width / surf_w) + 2):
            screen.blit(dungeon_surf, (x_start + i * surf_w, start_y))
        return

    # Fallback: draw lines (slower)
    for i, line in enumerate(BACKGROUND):
        # Dibujar suficientes repeticiones empezando en -offset_mod para cubrir la pantalla
        y_position = start_y + i * line_height
        draw_x = -offset_mod
        # Dibujar repetido hasta cubrir la anchura
        while draw_x < screen_width:
            draw_text(screen, font_ascii, line, int(draw_x), y_position, (200, 200, 200))
            draw_x += pattern_px_width


def fade_out(screen, duration=800):
    """Efecto de fade out (desvanecimiento a negro)"""
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))
    
    start_time = pygame.time.get_ticks()
    
    while pygame.time.get_ticks() - start_time < duration:
        # Calcular el alpha basado en el tiempo transcurrido
        elapsed = pygame.time.get_ticks() - start_time
        alpha = int((elapsed / duration) * 255)
        alpha = min(255, alpha)  # Asegurar que no supere 255
        
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.wait(16)  # ~60 FPS


def fade_in(screen, target_surface, duration=800):
    """Efecto de fade in (aparición gradual desde negro)"""
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))
    
    start_time = pygame.time.get_ticks()
    
    while pygame.time.get_ticks() - start_time < duration:
        # Calcular el alpha basado en el tiempo transcurrido
        elapsed = pygame.time.get_ticks() - start_time
        alpha = int(255 - (elapsed / duration) * 255)
        alpha = max(0, alpha)  # Asegurar que no sea menor que 0
        
        # Dibujar la superficie objetivo primero
        screen.blit(target_surface, (0, 0))
        
        # Aplicar el fade solo si alpha > 0
        if alpha > 0:
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
        
        pygame.display.flip()
        pygame.time.wait(16)  # ~60 FPS
    
    # Asegurar que la imagen final se muestre sin fade
    screen.blit(target_surface, (0, 0))
    pygame.display.flip()


def menu_fade_in(screen, duration=800):
    """Efecto de fade in simple para menús"""
    fade_surface = pygame.Surface(screen.get_size())
    fade_surface.fill((0, 0, 0))
    
    start_time = pygame.time.get_ticks()
    
    while pygame.time.get_ticks() - start_time < duration:
        # Calcular el alpha basado en el tiempo transcurrido
        elapsed = pygame.time.get_ticks() - start_time
        alpha = int(255 - (elapsed / duration) * 255)
        alpha = max(0, alpha)  # Asegurar que no sea menor que 0
        
        # Solo aplicar fade si alpha > 0
        if alpha > 0:
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
        
        pygame.display.flip()
        pygame.time.wait(16)  # ~60 FPS