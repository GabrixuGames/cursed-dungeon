import json
from src.animations.animations import animation_enemy_atack, animation_enemy_evade
from src.others import slow_print



class enemy:
    def __init__(self, name, health, damage, attack_rate, evade_chance, level_min, level_max, state):
        self.name = name
        self.health = health
        self.damage = damage
        self.attack_rate = attack_rate
        self.evade_chance = evade_chance
        self.level_min = level_min
        self.level_max = level_max
        self.exp = round(20 * (1.2 ** (self.level_max - 1)), 2)
        self.gold = int(30 * (1.2 ** (self.level_max - 1)))
        self.state = state

    def getName(self):
        return self.name
    
    def getHealth(self):
        return self.health
    
    def getDamage(self):
        return self.damage
    
    def getAttackRate(self):    
        return self.attack_rate
    
    def getEvadeChance(self):
        return self.evade_chance
    
    def getLevelMin(self):
        return self.level_min
    
    def getLevelMax(self):
        return self.level_max
    
    def getExp(self):
        return self.exp
    
    def getGold(self):
        return self.gold

    def getState(self):
        return self.state
    
    def setHealth(self, health):
        self.health = max(0, health)

    def setName(self, name):
        self.name = name

    def setDamage(self, damage):
        self.damage = damage

    def setAttackRate(self, attack_rate):
        self.attack_rate = attack_rate

    def setEvadeChance(self, evade_chance):
        self.evade_chance = evade_chance

    def setLevelMin(self, level_min):
        self.level_min = level_min

    def setLevelMax(self, level_max):
        self.level_max = level_max

    def setExp(self, exp):
        self.exp = exp

    def setGold(self, gold):
        self.gold = gold
    
    def setState(self, state):
        self.state = state

    def attack(self, screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance, y_offset):
        mainChar.setHealth(mainChar.getHealth() - self.damage)
        animation_enemy_atack(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance)
        slow_print(screen, font_text, f"{self.name} te ha hecho {self.damage} de daño", 50, y_offset)    
    
    def evade(self, screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance, y_offset):
        animation_enemy_evade(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, mainChar, enemy_instance)
        slow_print(screen, font_text, f"{self.name} ha esquivado el ataque", 50, y_offset)
    
    def apply_state(self, mainChar, screen, font_text, y_offset):
        if self.state:
            mainChar.setState(self.state)
            slow_print(screen, font_text, f"{self.name} te ha afectado con {self.state[0]['name']}.", 50, y_offset)

def load_enemies(enemyDb, mainChar):
    lvlmin = mainChar.getLevel() - 4
    lvlmax = mainChar.getLevel() + 4
    valid_enemies = []

    with open(enemyDb, 'r', encoding='utf-8') as archivo:
        normalEnemy = json.load(archivo)

        # Filtrar y crear instancias de Enemy
        for enemy_data in normalEnemy.get("normal", []):
            if int(enemy_data["level_min"]) >= lvlmin and int(enemy_data["level_max"]) <= lvlmax:
                enemy_instance = enemy(
                    name=enemy_data["name"],
                    health=enemy_data["health"],
                    damage=enemy_data["damage"],
                    evade_chance=enemy_data["evadeChance"],
                    attack_rate=enemy_data["attackRate"],
                    state=enemy_data.get("states", []),
                    level_min=enemy_data["level_min"],
                    level_max=enemy_data["level_max"]
                )
                valid_enemies.append(enemy_instance)

    return valid_enemies
