"""
Input Manager - Enhanced keyboard and input handling
Provides shortcuts, tooltips, and better UX
"""
import pygame
import time
from config import Colors, MenuConfig

class InputManager:
    """Enhanced input handling with shortcuts and confirmations."""
    
    def __init__(self):
        self.key_repeat_delay = 300  # ms before repeat starts
        self.key_repeat_rate = 50    # ms between repeats
        self.last_key_time = {}
        self.held_keys = set()
        
    def is_key_pressed(self, key, allow_repeat=True):
        """Check if key is pressed with optional repeat handling."""
        current_time = pygame.time.get_ticks()
        
        if key in self.held_keys:
            if allow_repeat:
                last_time = self.last_key_time.get(key, 0)
                if current_time - last_time > self.key_repeat_rate:
                    self.last_key_time[key] = current_time
                    return True
            return False
        else:
            self.last_key_time[key] = current_time
            return True
    
    def handle_key_down(self, key):
        """Handle key down event."""
        self.held_keys.add(key)
        return self.is_key_pressed(key, False)
    
    def handle_key_up(self, key):
        """Handle key up event."""
        self.held_keys.discard(key)
        if key in self.last_key_time:
            del self.last_key_time[key]
    
    def clear_all(self):
        """Clear all key states."""
        self.held_keys.clear()
        self.last_key_time.clear()

class Tooltip:
    """Tooltip system for better UX."""
    
    def __init__(self):
        self.active_tooltip = None
        self.tooltip_timer = 0
        self.show_delay = 1000  # ms to wait before showing tooltip
        
    def set_tooltip(self, text, position=None):
        """Set tooltip to show after delay."""
        self.active_tooltip = {
            'text': text,
            'position': position,
            'created': pygame.time.get_ticks()
        }
    
    def clear_tooltip(self):
        """Clear active tooltip."""
        self.active_tooltip = None
    
    def draw(self, screen, font):
        """Draw tooltip if active and delay has passed."""
        if not self.active_tooltip:
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.active_tooltip['created'] < self.show_delay:
            return
        
        text = self.active_tooltip['text']
        position = self.active_tooltip['position'] or pygame.mouse.get_pos()
        
        # Create tooltip surface
        padding = 8
        text_surface = font.render(text, True, Colors.WHITE)
        tooltip_width = text_surface.get_width() + padding * 2
        tooltip_height = text_surface.get_height() + padding * 2
        
        # Adjust position to stay on screen
        x, y = position
        screen_width, screen_height = screen.get_size()
        
        if x + tooltip_width > screen_width:
            x = screen_width - tooltip_width - 10
        if y + tooltip_height > screen_height:
            y = y - tooltip_height - 10
        
        # Draw tooltip background
        tooltip_rect = pygame.Rect(x, y, tooltip_width, tooltip_height)
        pygame.draw.rect(screen, Colors.POPUP_BG, tooltip_rect)
        pygame.draw.rect(screen, Colors.WHITE, tooltip_rect, 1)
        
        # Draw text
        text_x = x + padding
        text_y = y + padding
        screen.blit(text_surface, (text_x, text_y))

class ConfirmationDialog:
    """Confirmation dialog for important actions."""
    
    def __init__(self, message, on_confirm=None, on_cancel=None):
        self.message = message
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.selection = 0  # 0 = Yes, 1 = No
        self.active = True
    
    def draw(self, screen, font):
        """Draw the confirmation dialog."""
        if not self.active:
            return
        
        # Overlay
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(128)
        overlay.fill(Colors.BLACK)
        screen.blit(overlay, (0, 0))
        
        # Dialog box
        dialog_width = 400
        dialog_height = 200
        x = (screen.get_width() - dialog_width) // 2
        y = (screen.get_height() - dialog_height) // 2
        
        dialog_rect = pygame.Rect(x, y, dialog_width, dialog_height)
        pygame.draw.rect(screen, Colors.POPUP_BG, dialog_rect)
        pygame.draw.rect(screen, Colors.WHITE, dialog_rect, 2)
        
        # Message
        message_surface = font.render(self.message, True, Colors.WHITE)
        message_x = x + (dialog_width - message_surface.get_width()) // 2
        message_y = y + 40
        screen.blit(message_surface, (message_x, message_y))
        
        # Options
        options = ["Sí", "No"]
        option_y = y + 120
        
        for i, option in enumerate(options):
            color = Colors.YELLOW if i == self.selection else Colors.WHITE
            option_surface = font.render(option, True, color)
            option_x = x + 100 + i * 150
            screen.blit(option_surface, (option_x, option_y))
        
        # Instructions
        instruction = "← → para seleccionar, ENTER para confirmar, ESC para cancelar"
        instruction_surface = font.render(instruction, True, Colors.LIGHT_GRAY)
        instruction_x = x + (dialog_width - instruction_surface.get_width()) // 2
        instruction_y = y + dialog_height - 30
        screen.blit(instruction_surface, (instruction_x, instruction_y))
    
    def handle_input(self, event):
        """Handle input for confirmation dialog."""
        if not self.active:
            return None
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selection = 0
            elif event.key == pygame.K_RIGHT:
                self.selection = 1
            elif event.key == pygame.K_RETURN:
                self.active = False
                if self.selection == 0 and self.on_confirm:
                    self.on_confirm()
                    return "confirmed"
                elif self.selection == 1 and self.on_cancel:
                    self.on_cancel()
                    return "cancelled"
                return "confirmed" if self.selection == 0 else "cancelled"
            elif event.key == pygame.K_ESCAPE:
                self.active = False
                if self.on_cancel:
                    self.on_cancel()
                return "cancelled"
        
        return None

class KeyboardShortcuts:
    """Keyboard shortcuts manager."""
    
    def __init__(self):
        self.shortcuts = {
            # Global shortcuts
            pygame.K_F1: "help",
            pygame.K_F4: "quit_confirm",  # Alt+F4 equivalent
            pygame.K_F11: "toggle_fullscreen",
            pygame.K_ESCAPE: "back_or_menu",
            
            # Audio shortcuts
            pygame.K_m: "toggle_mute",
            pygame.K_PLUS: "volume_up",
            pygame.K_MINUS: "volume_down",
            
            # Game shortcuts
            pygame.K_F5: "quick_save",
            pygame.K_F9: "quick_load",
            pygame.K_SPACE: "skip_text",
            pygame.K_TAB: "show_stats",
            
            # Debug shortcuts (only in development)
            pygame.K_F12: "debug_menu",
        }
        
        # Modifier key combinations
        self.modifier_shortcuts = {
            (pygame.K_LCTRL, pygame.K_s): "save_game",
            (pygame.K_LCTRL, pygame.K_o): "load_game",
            (pygame.K_LCTRL, pygame.K_q): "quit_confirm",
            (pygame.K_LALT, pygame.K_F4): "quit_confirm",
        }
        
        self.held_modifiers = set()
    
    def update_modifiers(self, event):
        """Update held modifier keys."""
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_LALT, pygame.K_RALT, pygame.K_LSHIFT, pygame.K_RSHIFT]:
                self.held_modifiers.add(event.key)
        elif event.type == pygame.KEYUP:
            self.held_modifiers.discard(event.key)
    
    def get_shortcut(self, event):
        """Get shortcut action for the given event."""
        if event.type != pygame.KEYDOWN:
            return None
        
        # Check modifier combinations first
        for (modifier, key), action in self.modifier_shortcuts.items():
            if modifier in self.held_modifiers and event.key == key:
                return action
        
        # Check single key shortcuts
        return self.shortcuts.get(event.key)

class HelpSystem:
    """In-game help and tutorial system."""
    
    def __init__(self):
        self.help_pages = [
            {
                "title": "Controles Básicos",
                "content": [
                    "↑/↓ - Navegar menús",
                    "ENTER - Confirmar selección", 
                    "ESC - Volver/Cancelar",
                    "F1 - Mostrar esta ayuda",
                    "M - Silenciar/Activar audio",
                    "TAB - Mostrar estadísticas"
                ]
            },
            {
                "title": "Combat",
                "content": [
                    "El combate es automático",
                    "Tu personaje y enemigo atacan por turnos",
                    "La velocidad de ataque depende del arma",
                    "Puedes esquivar ataques enemigos",
                    "Ganas experiencia al derrotar enemigos"
                ]
            },
            {
                "title": "Progresión",
                "content": [
                    "Sube de nivel para ganar puntos de atributo",
                    "Mejora Vida, Daño o Evasión",
                    "Compra armas mejores en la tienda",
                    "Guarda tu progreso regularmente",
                    "Explora mazmorras para ganar experiencia"
                ]
            }
        ]
        self.current_page = 0
        self.active = False
    
    def show_help(self):
        """Show help system."""
        self.active = True
        self.current_page = 0
    
    def hide_help(self):
        """Hide help system."""
        self.active = False
    
    def next_page(self):
        """Go to next help page."""
        self.current_page = (self.current_page + 1) % len(self.help_pages)
    
    def prev_page(self):
        """Go to previous help page."""
        self.current_page = (self.current_page - 1) % len(self.help_pages)
    
    def draw(self, screen, font):
        """Draw the help system."""
        if not self.active:
            return
        
        # Overlay
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(180)
        overlay.fill(Colors.BLACK)
        screen.blit(overlay, (0, 0))
        
        # Help box
        box_width = 600
        box_height = 500
        x = (screen.get_width() - box_width) // 2
        y = (screen.get_height() - box_height) // 2
        
        box_rect = pygame.Rect(x, y, box_width, box_height)
        pygame.draw.rect(screen, Colors.POPUP_BG, box_rect)
        pygame.draw.rect(screen, Colors.WHITE, box_rect, 2)
        
        # Title
        page = self.help_pages[self.current_page]
        title_surface = font.render(f"AYUDA - {page['title']}", True, Colors.YELLOW)
        title_x = x + (box_width - title_surface.get_width()) // 2
        screen.blit(title_surface, (title_x, y + 20))
        
        # Content
        content_y = y + 80
        for i, line in enumerate(page['content']):
            line_surface = font.render(line, True, Colors.WHITE)
            screen.blit(line_surface, (x + 40, content_y + i * 30))
        
        # Navigation
        nav_text = f"Página {self.current_page + 1} de {len(self.help_pages)}"
        nav_surface = font.render(nav_text, True, Colors.LIGHT_GRAY)
        nav_x = x + (box_width - nav_surface.get_width()) // 2
        screen.blit(nav_surface, (nav_x, y + box_height - 80))
        
        # Instructions
        instructions = "← → para cambiar página, ESC para cerrar"
        inst_surface = font.render(instructions, True, Colors.LIGHT_GRAY)
        inst_x = x + (box_width - inst_surface.get_width()) // 2
        screen.blit(inst_surface, (inst_x, y + box_height - 50))
    
    def handle_input(self, event):
        """Handle input for help system."""
        if not self.active:
            return None
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_F1:
                self.hide_help()
                return "close"
            elif event.key == pygame.K_LEFT:
                self.prev_page()
            elif event.key == pygame.K_RIGHT:
                self.next_page()
        
        return None

# Global instances
_input_manager = InputManager()
_tooltip_system = Tooltip()
_keyboard_shortcuts = KeyboardShortcuts()
_help_system = HelpSystem()

def get_input_manager():
    return _input_manager

def get_tooltip_system():
    return _tooltip_system

def get_keyboard_shortcuts():
    return _keyboard_shortcuts

def get_help_system():
    return _help_system