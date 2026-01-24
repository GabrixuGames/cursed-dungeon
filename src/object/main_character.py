import pygame
from src.others import slow_print, toast_manager
import time, json, os
from src.animations.animations import animation_player_atack, animation_player_evade, animation_victory


class MainCharacter:
    """Clase que representa el personaje principal del jugador."""

    def __init__(self, name):
        self._name = name
        self._level = 1
        self._damage = 10
        self._health = 150
        self._evade_chance = 5
        self._experience = 0
        self._weapon = None
        self._money = 0
        self._atributes = 0
        self._to_next_level = 100 * (1.2 ** (self._level - 1))
        self._state = None
    
    # Properties
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def level(self):
        return self._level
    
    @level.setter
    def level(self, value):
        self._level = value
    
    @property
    def damage(self):
        return self._damage
    
    @damage.setter
    def damage(self, value):
        self._damage = value
    
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        self._health = max(0, value)
    
    @property
    def evade_chance(self):
        return self._evade_chance
    
    @evade_chance.setter
    def evade_chance(self, value):
        self._evade_chance = value
    
    @property
    def experience(self):
        return self._experience
    
    @experience.setter
    def experience(self, value):
        self._experience = round(value, 2)
    
    @property
    def weapon(self):
        return self._weapon
    
    @weapon.setter
    def weapon(self, value):
        self._weapon = value
    
    @property
    def money(self):
        return self._money
    
    @money.setter
    def money(self, value):
        self._money = value
    
    @property
    def atributes(self):
        return self._atributes
    
    @atributes.setter
    def atributes(self, value):
        self._atributes = value
    
    @property
    def to_next_level(self):
        return self._to_next_level
    
    @to_next_level.setter
    def to_next_level(self, value):
        self._to_next_level = value
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = value
    
    # Legacy methods for backward compatibility
    def getToNextLevel(self):
        return self.to_next_level
    
    def getAtributes(self):
        return self.atributes

    def setAtributes(self, atributes):
        self.atributes = atributes
    
    def getMoney(self):
        return self.money

    def setMoney(self, money):
        self.money = money
    
    def getWeapon(self):
        return self.weapon

    def setWeapon(self, weapon):
        self.weapon = weapon

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getLevel(self):
        return self.level

    def setLevel(self, level):
        self.level = level

    def getDamage(self):
        return self.damage

    def setDamage(self, damage):
        self.damage = damage

    def getHealth(self):
        return self.health

    def setHealth(self, health):
        self.health = health

    def getEvadeChance(self):
        return self.evade_chance

    def setEvadeChance(self, evade):
        self.evade_chance = evade

    def getExperience(self):
        return self.experience

    def setExperience(self, experience):
        self.experience = experience

    def setState(self, state):
        self.state = state
    
    def getState(self):
        return self.state
    
    def next_level(self, screen, font_text, y_offset):
        if self.experience >= self.to_next_level:
            self.level = self.level + 1
            self.atributes = self.atributes + 3
            self.experience = 0
            # Use blocking_message so the level-up messages appear typed and wait for user input
            # Use the combat message box for typed messages with fallback
            from src.others import combat_message_box, blocking_message
            try:
                combat_message_box.show(screen, font_text, "Has subido de nivel!", timeout=1200)
                combat_message_box.show(screen, font_text, f"Nivel: {self.level}, tienes {self.atributes} puntos de atributos.", timeout=1400)
                combat_message_box.show(screen, font_text, "Presiona una tecla para continuar...", wait_for_key=True)
            except Exception:
                blocking_message(screen, font_text, "Has subido de nivel!", 50, y_offset, clear_area=True, timeout=1200)
                y_offset += 30
                blocking_message(screen, font_text, f"Nivel: {self.level}, tienes {self.atributes} puntos de atributos.", 50, y_offset, clear_area=True, timeout=1400)
                y_offset += 35
                # Wait explicitly for a key so the player reads the reward
                blocking_message(screen, font_text, "Presiona una tecla para continuar...", 50, y_offset, clear_area=True, wait_for_key=True)
    
    def player_attack(self, screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance, y_offset):
        from src.object.enemy import Enemy
        # Apply damage first so animations show updated HP if needed
        enemy_instance.setHealth(enemy_instance.getHealth() - (self.damage + self.weapon["damage"]))
        # Play attack animation (this plays the sound too)
        try:
            animation_player_atack(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)
        except Exception:
            # If animation fails, continue and return the message
            pass
        return f"{enemy_instance.getName()} recibe {self.damage + self.weapon['damage']} de daño"
    
    def player_evade(self, screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance, y_offset):
        animation_player_evade(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)
        return "Esquivas el ataque!"
    
    def player_victory(self, screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance, y_offset):
        animation_victory(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)
        self.setExperience(self.experience + enemy_instance.getExp())
        self.setMoney(self.money + enemy_instance.getGold())
        # Return two separate messages: victory line and rewards line
        msg1 = f"Has derrotado a {enemy_instance.getName()}!"
        msg2 = f"Has ganado {enemy_instance.getExp()} exp y {enemy_instance.getGold()} oro!"
        return [msg1, msg2]
    
    def state_damage(self, screen, font_text, y_offset):
        if self.state:
            if "health" in self.state["effect"]:
                self.health = self.health - self.state["effect"]["health"]
                try:
                    toast_manager.add(f"Pierdes {self.state['effect']['health']} puntos de salud debido al {self.state['name']}.", duration=1400)
                except Exception:
                    slow_print(screen, font_text, f"Pierdes {self.state['effect']['health']} puntos de salud debido al {self.state['name']}.", 50, y_offset, clear_area=True)
                y_offset += 30
                if self.health <= 0:
                    try:
                        toast_manager.add(f"Has sido derrotado por el {self.state['name']}.", duration=1800)
                    except Exception:
                        slow_print(screen, font_text, f"Has sido derrotado por el {self.state['name']}.", 50, y_offset, clear_area=True)
                    time.sleep(4)
                    return False
        return True

    def save_game(self, slot: int = 1):
        """
        Save game data using the new SaveManager system.
        
        Args:
            slot: Save slot number (1-3), defaults to 1 for backward compatibility
            
        Returns:
            True if save was successful, False otherwise
        """
        try:
            from src.save_manager import get_save_manager
            
            character_data = {
                "name": self.name,
                "level": self.level,
                "damage": self.damage,
                "health": self.health,
                "evade_chance": self.evade_chance,
                "experience": self.experience,
                "money": self.money,
                "atributes": self.atributes,
                "weapon": self.weapon,
                "to_next_level": self.to_next_level
            }
            
            save_manager = get_save_manager()
            return save_manager.save_game(slot, character_data)
            
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self, slot: int = 1):
        """
        Load game data using the new SaveManager system.
        
        Args:
            slot: Save slot number (1-3), defaults to 1 for backward compatibility
            
        Returns:
            True if load was successful, False otherwise
        """
        try:
            from src.save_manager import get_save_manager
            
            save_manager = get_save_manager()
            character_data = save_manager.load_game(slot)
            
            if character_data is None:
                return False
            
            # Load validated data
            self.name = character_data["name"]
            self.level = character_data["level"]
            self.damage = character_data["damage"]
            self.health = character_data["health"]
            self.evade_chance = character_data["evade_chance"]
            self.experience = character_data["experience"]
            self.money = character_data["money"]
            self.atributes = character_data["atributes"]
            self.weapon = character_data["weapon"]
            self.to_next_level = character_data.get("to_next_level", 100 * (1.2 ** (self.level - 1)))
            
            return True
            
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
    
    # Legacy save/load methods for old save.json format (deprecated)
    def save_game_legacy(self):
        """Save game data to JSON file with error handling."""
        try:
            save_data = {
                "name": self.name,
                "level": self.level,
                "damage": self.damage,
                "health": self.health,
                "evade_chance": self.evade_chance,
                "experience": self.experience,
                "money": self.money,
                "atributes": self.atributes,
                "weapon": self.weapon,
                "to_next_level": self.to_next_level
            }
            save_path = os.path.join(os.getcwd(), "save.json")
            
            # Create backup of existing save file if it exists
            if os.path.exists(save_path):
                backup_path = save_path + ".backup"
                try:
                    os.rename(save_path, backup_path)
                except OSError as e:
                    print(f"Warning: Could not create backup: {e}")
            
            with open(save_path, "w", encoding='utf-8') as save_file:
                json.dump(save_data, save_file, indent=2, ensure_ascii=False)
            
            # Remove backup if save was successful
            backup_path = save_path + ".backup"
            if os.path.exists(backup_path):
                try:
                    os.remove(backup_path)
                except OSError:
                    pass  # Backup can stay if removal fails
                    
            return True
            
        except (IOError, OSError) as e:
            print(f"Error saving game (File I/O): {e}")
            # Restore backup if save failed
            backup_path = save_path + ".backup"
            if os.path.exists(backup_path):
                try:
                    os.rename(backup_path, save_path)
                    print("Backup restored due to save failure")
                except OSError:
                    pass
            return False
            
        except json.JSONEncodeError as e:
            print(f"Error saving game (JSON encoding): {e}")
            return False
            
        except Exception as e:
            print(f"Unexpected error saving game: {e}")
            return False
    
    def load_game_legacy(self):
        """Load game data from JSON file with error handling."""
        save_path = os.path.join(os.getcwd(), "save.json")
        
        try:
            # Check if save file exists
            if not os.path.exists(save_path):
                raise FileNotFoundError(f"Save file not found: {save_path}")
            
            # Check if file is readable
            if not os.access(save_path, os.R_OK):
                raise PermissionError(f"Cannot read save file: {save_path}")
            
            with open(save_path, "r", encoding='utf-8') as save_file:
                save_data = json.load(save_file)
                
            # Validate required fields exist
            required_fields = ["name", "level", "damage", "health", "evade_chance", 
                             "experience", "money", "atributes", "weapon", "to_next_level"]
            
            for field in required_fields:
                if field not in save_data:
                    raise KeyError(f"Missing required field in save data: {field}")
            
            # Validate data types and ranges
            if not isinstance(save_data["level"], int) or save_data["level"] < 1:
                raise ValueError("Invalid level value")
            if not isinstance(save_data["health"], int) or save_data["health"] < 0:
                raise ValueError("Invalid health value")
            if not isinstance(save_data["name"], str) or not save_data["name"].strip():
                raise ValueError("Invalid name value")
                
            # Load validated data
            self.name = save_data["name"]
            self.level = save_data["level"]
            self.damage = save_data["damage"]
            self.health = save_data["health"]
            self.evade_chance = save_data["evade_chance"]
            self.experience = save_data["experience"]
            self.money = save_data["money"]
            self.atributes = save_data["atributes"]
            self.weapon = save_data["weapon"]
            self.to_next_level = save_data["to_next_level"]
            
            return True
            
        except FileNotFoundError as e:
            print(f"Save file not found: {e}")
            return False
            
        except PermissionError as e:
            print(f"Permission error loading save: {e}")
            return False
            
        except json.JSONDecodeError as e:
            print(f"Error parsing save file (corrupted JSON): {e}")
            # Try to load backup
            backup_path = save_path + ".backup"
            if os.path.exists(backup_path):
                print("Attempting to load from backup...")
                try:
                    with open(backup_path, "r", encoding='utf-8') as backup_file:
                        save_data = json.load(backup_file)
                        # Re-validate and load backup data (simplified for brevity)
                        self.name = save_data.get("name", "Unknown")
                        self.level = save_data.get("level", 1)
                        self.damage = save_data.get("damage", 10)
                        self.health = save_data.get("health", 150)
                        self.evade_chance = save_data.get("evade_chance", 5)
                        self.experience = save_data.get("experience", 0)
                        self.money = save_data.get("money", 0)
                        self.atributes = save_data.get("atributes", 0)
                        self.weapon = save_data.get("weapon", {"name": "Bare Hands", "damage": 5, "attack_ratio": 1000})
                        self.to_next_level = save_data.get("to_next_level", 100)
                        print("Backup loaded successfully")
                        return True
                except Exception as backup_error:
                    print(f"Backup also corrupted: {backup_error}")
            return False
            
        except (KeyError, ValueError) as e:
            print(f"Invalid save data: {e}")
            return False
            
        except Exception as e:
            print(f"Unexpected error loading save: {e}")
            return False
