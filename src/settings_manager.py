"""
Settings Manager - User preferences and configuration
Handles game settings like volume, controls, display options
"""
import json
import os
import pygame
from config import AudioConfig, DisplayConfig, TransitionConfig

class GameSettings:
    """Manages user settings and preferences."""
    
    def __init__(self):
        self.settings_file = "settings.json"
        self.default_settings = {
            "audio": {
                "master_volume": 1.0,
                "sfx_volume": AudioConfig.SFX_VOLUME,
                "music_volume": AudioConfig.MAIN_MENU_VOLUME,
                "mute": False
            },
            "display": {
                "fullscreen": False,
                "resolution": [DisplayConfig.WINDOW_WIDTH, DisplayConfig.WINDOW_HEIGHT],
                "fps_limit": DisplayConfig.FPS,
                "vsync": True
            },
            "gameplay": {
                "text_speed": TransitionConfig.SLOW_PRINT_DELAY,
                "auto_save": True,
                "skip_animations": False,
                "show_fps": False
            },
            "controls": {
                "confirm_key": "return",
                "cancel_key": "escape",
                "up_key": "up",
                "down_key": "down",
                "left_key": "left",
                "right_key": "right"
            }
        }
        self.current_settings = self.default_settings.copy()
        self.load_settings()
    
    def load_settings(self):
        """Load settings from file or create defaults."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Merge with defaults to ensure all settings exist
                    self._merge_settings(loaded_settings)
                    print("Settings loaded successfully")
            else:
                print("No settings file found, using defaults")
                self.save_settings()
        except Exception as e:
            print(f"Error loading settings: {e}")
            self.current_settings = self.default_settings.copy()
    
    def _merge_settings(self, loaded_settings):
        """Merge loaded settings with defaults to ensure completeness."""
        for category, settings in self.default_settings.items():
            if category in loaded_settings:
                for key, default_value in settings.items():
                    if key in loaded_settings[category]:
                        self.current_settings[category][key] = loaded_settings[category][key]
                    else:
                        self.current_settings[category][key] = default_value
            else:
                self.current_settings[category] = settings.copy()
    
    def save_settings(self):
        """Save current settings to file."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.current_settings, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving settings: {e}")
            return False
    
    def get(self, category, key):
        """Get a specific setting value."""
        return self.current_settings.get(category, {}).get(key, None)
    
    def set(self, category, key, value):
        """Set a specific setting value."""
        if category not in self.current_settings:
            self.current_settings[category] = {}
        self.current_settings[category][key] = value
    
    def get_volume(self, volume_type="master"):
        """Get volume setting (0.0 to 1.0)."""
        base_volume = self.get("audio", f"{volume_type}_volume")
        master_volume = self.get("audio", "master_volume")
        mute = self.get("audio", "mute")
        
        if mute:
            return 0.0
        return base_volume * master_volume
    
    def toggle_mute(self):
        """Toggle mute setting."""
        current_mute = self.get("audio", "mute")
        self.set("audio", "mute", not current_mute)
        return not current_mute
    
    def reset_to_defaults(self):
        """Reset all settings to defaults."""
        self.current_settings = self.default_settings.copy()
        self.save_settings()

class SettingsMenu:
    """Interactive settings menu."""
    
    def __init__(self, settings_manager, display_manager):
        self.settings = settings_manager
        self.display = display_manager
        self.categories = ["Audio", "Display", "Gameplay", "Controls"]
        self.current_category = 0
        self.current_setting = 0
        self.in_category = False
    
    def draw_settings_menu(self, screen, font):
        """Draw the settings menu interface."""
        screen.fill((0, 0, 0))
        
        # Title
        title_rect = self.display.fast_text(
            font, "CONFIGURACIÓN", 
            (screen.get_width() // 2 - 100, 50), 
            (255, 255, 255)
        )
        
        # Categories
        y_offset = 150
        for i, category in enumerate(self.categories):
            color = (255, 255, 0) if i == self.current_category else (255, 255, 255)
            prefix = "► " if i == self.current_category and not self.in_category else "  "
            
            self.display.fast_text(
                font, f"{prefix}{category}", 
                (100, y_offset + i * 40), 
                color
            )
        
        # Settings for current category
        if self.in_category:
            self._draw_category_settings(screen, font)
        
        # Instructions
        instructions = [
            "↑/↓: Navegar  ENTER: Seleccionar  ESC: Volver",
            "R: Restaurar valores por defecto"
        ]
        
        for i, instruction in enumerate(instructions):
            self.display.fast_text(
                font, instruction,
                (50, screen.get_height() - 100 + i * 30),
                (150, 150, 150)
            )
        
        self.display.update()
    
    def _draw_category_settings(self, screen, font):
        """Draw settings for the current category."""
        category_name = self.categories[self.current_category].lower()
        settings_dict = self.settings.current_settings.get(category_name, {})
        
        x_offset = 400
        y_offset = 150
        
        setting_keys = list(settings_dict.keys())
        
        for i, (key, value) in enumerate(settings_dict.items()):
            color = (255, 255, 0) if i == self.current_setting else (255, 255, 255)
            prefix = "► " if i == self.current_setting else "  "
            
            # Format value for display
            if isinstance(value, float):
                display_value = f"{value:.2f}"
            elif isinstance(value, bool):
                display_value = "Activado" if value else "Desactivado"
            elif isinstance(value, list):
                display_value = f"{value[0]}x{value[1]}"
            else:
                display_value = str(value)
            
            setting_text = f"{prefix}{key.replace('_', ' ').title()}: {display_value}"
            self.display.fast_text(font, setting_text, (x_offset, y_offset + i * 40), color)
    
    def handle_input(self, event):
        """Handle input for settings menu."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if self.in_category:
                    self.in_category = False
                else:
                    return "back"
            
            elif event.key == pygame.K_UP:
                if self.in_category:
                    category_name = self.categories[self.current_category].lower()
                    max_settings = len(self.settings.current_settings.get(category_name, {}))
                    self.current_setting = (self.current_setting - 1) % max_settings
                else:
                    self.current_category = (self.current_category - 1) % len(self.categories)
            
            elif event.key == pygame.K_DOWN:
                if self.in_category:
                    category_name = self.categories[self.current_category].lower()
                    max_settings = len(self.settings.current_settings.get(category_name, {}))
                    self.current_setting = (self.current_setting + 1) % max_settings
                else:
                    self.current_category = (self.current_category + 1) % len(self.categories)
            
            elif event.key == pygame.K_RETURN:
                if not self.in_category:
                    self.in_category = True
                    self.current_setting = 0
                else:
                    self._toggle_setting()
            
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                if self.in_category:
                    self._adjust_setting(event.key == pygame.K_RIGHT)
            
            elif event.key == pygame.K_r:
                self.settings.reset_to_defaults()
                return "reset"
        
        return None
    
    def _toggle_setting(self):
        """Toggle boolean settings."""
        category_name = self.categories[self.current_category].lower()
        setting_keys = list(self.settings.current_settings.get(category_name, {}).keys())
        
        if self.current_setting < len(setting_keys):
            key = setting_keys[self.current_setting]
            current_value = self.settings.get(category_name, key)
            
            if isinstance(current_value, bool):
                self.settings.set(category_name, key, not current_value)
    
    def _adjust_setting(self, increase):
        """Adjust numeric settings."""
        category_name = self.categories[self.current_category].lower()
        setting_keys = list(self.settings.current_settings.get(category_name, {}).keys())
        
        if self.current_setting < len(setting_keys):
            key = setting_keys[self.current_setting]
            current_value = self.settings.get(category_name, key)
            
            if isinstance(current_value, float):
                adjustment = 0.1 if increase else -0.1
                new_value = max(0.0, min(1.0, current_value + adjustment))
                self.settings.set(category_name, key, new_value)

# Global settings instance
_game_settings = None

def init_settings():
    """Initialize global settings manager."""
    global _game_settings
    _game_settings = GameSettings()
    return _game_settings

def get_settings():
    """Get global settings manager."""
    return _game_settings