from src.others import slow_print
import time, json, os
from src.animations.animations import animation_player_atack, animation_player_evade, animation_victory


class MainChar:

    def __init__(self, name):
        self.name = name
        self.level = 1
        self.damage = 10
        self.health = 150
        self.evade_chance = 5
        self.experience = 0
        self.weapon = None
        self.money = 0
        self.atributes = 0
        self.to_next_level = 100 * (1.2 ** (self.level - 1))
        self.state = None
    
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
        self.health = max(0, health)

    def getEvadeChance(self):
        return self.evade_chance

    def setEvadeChance(self, evade):
        self.evade_chance = evade

    def getExperience(self):
        return self.experience

    def setExperience(self, experience):
        self.experience = round(experience, 2)

    def setState(self, state):
        self.state = state
    
    def getState(self):
        return self.state
    
    def next_level(self, screen, font_text, y_offset):
        if self.experience >= self.to_next_level:
            self.level = self.level + 1
            self.atributes = self.atributes + 3
            self.experience = 0
            slow_print(screen, font_text, f"Has subido de nivel!",  50, y_offset)
            y_offset += 30
            slow_print(screen, font_text, f"Nivel: {self.level}, tienes {self.atributes} putnos de atributos.",  50, y_offset)
            time.sleep(4)
    
    def player_attack(self, screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance, y_offset):
        from src.object.enemy import enemy
        enemy_instance.setHealth(enemy_instance.getHealth() - (self.damage + self.weapon["damage"]))
        animation_player_atack(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance)
        slow_print(screen, font_text, f"Has hecho {self.damage + self.weapon["damage"]} de daño a {enemy_instance.getName()}.",  50, y_offset)
    
    def player_evade(self, screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance, y_offset):
        animation_player_evade(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance)
        slow_print(screen, font_text, f"Has esquivado el ataque.",  50, y_offset)
    
    def player_victory(self, screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance, y_offset):
        animation_victory(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance)
        self.setExperience(self.experience + enemy_instance.getExp())
        self.setMoney(self.money + enemy_instance.getGold())
        slow_print(screen, font_text, f"¡Has derrotado a {enemy_instance.getName()}!", 50, y_offset)
        y_offset += 30
        slow_print(screen, font_text, f"Has ganado {enemy_instance.getExp()} de experiencia y {enemy_instance.getGold()} de oro.",  50, y_offset)
        time.sleep(4)
    
    def state_damage(self, screen, font_text, y_offset):
        if self.state:
            if "health" in self.state["effect"]:
                self.health = self.health - self.state["effect"]["health"]
                slow_print(screen, font_text, f"Pierdes {self.state['effect']['health']} puntos de salud debido al {self.state['name']}.", 50, y_offset)
                y_offset += 30
                if self.health <= 0:
                    slow_print(screen, font_text, f"Has sido derrotado por el {self.state['name']}.", 50, y_offset)
                    time.sleep(4)
                    return False
        return True

    def save_game(self):
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
        with open(save_path, "w") as save_file:
            json.dump(save_data, save_file)
    
    def load_game(self):
        save_path = os.path.join(os.getcwd(), "save.json")
        with open(save_path, "r") as save_file:
            save_data = json.load(save_file)
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