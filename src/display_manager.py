"""
Display Manager - Optimized screen updates and rendering
Reduces pygame.display.flip() calls and improves performance
"""
import pygame
import time
from config import DisplayConfig, TransitionConfig

class DisplayManager:
    """Manages screen updates and reduces unnecessary redraws."""
    
    def __init__(self, screen):
        self.screen = screen
        self.last_update = 0
        self.min_update_interval = 1000 / DisplayConfig.FPS  # Minimum ms between updates
        self.dirty_areas = []
        self.force_update = False
        
    def mark_dirty(self, rect=None):
        """Mark an area as needing update. If rect is None, mark entire screen."""
        if rect is None:
            self.force_update = True
            self.dirty_areas.clear()
        else:
            self.dirty_areas.append(rect)
    
    def should_update(self):
        """Check if enough time has passed for an update."""
        current_time = pygame.time.get_ticks()
        return (current_time - self.last_update) >= self.min_update_interval
    
    def update(self, force=False):
        """Update the display if needed."""
        current_time = pygame.time.get_ticks()
        
        if force or self.force_update or self.should_update():
            if self.dirty_areas and not self.force_update:
                # Update only dirty areas for better performance
                pygame.display.update(self.dirty_areas)
            else:
                # Full screen update
                pygame.display.flip()
            
            self.last_update = current_time
            self.dirty_areas.clear()
            self.force_update = False
            return True
        return False
    
    def fast_text(self, font, text, pos, color=(255, 255, 255)):
        """Render text directly without slow_print for better performance."""
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, pos)
        self.mark_dirty(pygame.Rect(pos, text_surface.get_size()))
        return text_surface.get_rect(topleft=pos)

class ResourceCache:
    """Cache frequently used resources to avoid repeated loading."""
    
    def __init__(self):
        self.fonts = {}
        self.sounds = {}
        self.surfaces = {}
        
    def get_font(self, path, size):
        """Get cached font or create new one."""
        key = f"{path}_{size}"
        if key not in self.fonts:
            try:
                self.fonts[key] = pygame.font.Font(path, size)
            except (pygame.error, FileNotFoundError):
                self.fonts[key] = pygame.font.Font(None, size)
        return self.fonts[key]
    
    def get_sound(self, path):
        """Get cached sound or load new one."""
        if path not in self.sounds:
            try:
                sound = pygame.mixer.Sound(path)
                self.sounds[path] = sound
            except (pygame.error, FileNotFoundError):
                # Return a dummy sound object that does nothing
                self.sounds[path] = None
        return self.sounds[path]
    
    def get_surface(self, key, create_func):
        """Get cached surface or create using provided function."""
        if key not in self.surfaces:
            self.surfaces[key] = create_func()
        return self.surfaces[key]
    
    def clear_cache(self):
        """Clear all cached resources."""
        self.fonts.clear()
        self.sounds.clear()
        self.surfaces.clear()

# Global instances
_display_manager = None
_resource_cache = ResourceCache()

def init_display_manager(screen):
    """Initialize the global display manager."""
    global _display_manager
    _display_manager = DisplayManager(screen)
    return _display_manager

def get_display_manager():
    """Get the global display manager."""
    return _display_manager

def get_resource_cache():
    """Get the global resource cache."""
    return _resource_cache

class OptimizedText:
    """Optimized text rendering utilities."""
    
    @staticmethod
    def render_multiline(display_manager, font, lines, start_pos, line_spacing=30, color=(255, 255, 255)):
        """Render multiple lines efficiently."""
        x, y = start_pos
        rects = []
        
        for line in lines:
            if line.strip():  # Skip empty lines
                rect = display_manager.fast_text(font, line, (x, y), color)
                rects.append(rect)
            y += line_spacing
        
        return rects
    
    @staticmethod
    def render_centered(display_manager, font, text, center_x, y, color=(255, 255, 255)):
        """Render text centered horizontally."""
        text_surface = font.render(text, True, color)
        x = center_x - text_surface.get_width() // 2
        display_manager.screen.blit(text_surface, (x, y))
        rect = pygame.Rect(x, y, text_surface.get_width(), text_surface.get_height())
        display_manager.mark_dirty(rect)
        return rect

def optimized_slow_print(display_manager, font, text, pos, color=(255, 255, 255), delay=0.03):
    """Optimized version of slow_print with better performance."""
    x, y = pos
    current_x = x
    
    # Pre-calculate character positions for better performance
    char_positions = []
    for char in text:
        char_width = font.size(char)[0]
        char_positions.append((current_x, char_width))
        current_x += char_width
    
    # Clear the area once
    text_width = current_x - x
    text_height = font.get_height()
    clear_rect = pygame.Rect(x, y, text_width + 8, text_height + 4)
    display_manager.screen.fill((0, 0, 0), clear_rect)
    display_manager.mark_dirty(clear_rect)
    
    # Render characters with timing
    current_x = x
    for i, char in enumerate(text):
        char_surface = font.render(char, True, color)
        display_manager.screen.blit(char_surface, (current_x, y))
        
        # Update only the character area
        char_rect = pygame.Rect(current_x, y, char_surface.get_width(), char_surface.get_height())
        display_manager.mark_dirty(char_rect)
        display_manager.update()
        
        current_x += char_positions[i][1]
        time.sleep(delay)