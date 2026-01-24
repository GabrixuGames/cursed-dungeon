import json
from src.animations.animations import animation_enemy_atack, animation_enemy_evade
from src.others import slow_print, toast_manager


class Enemy:
    """Clase que representa un enemigo en Cursed Dungeon."""
    
    def __init__(self, name, health, damage, attack_rate, evade_chance, level_min, level_max, state):
        self._name = name
        self._health = health
        self._damage = damage
        self._attack_rate = attack_rate
        self._evade_chance = evade_chance
        self._level_min = level_min
        self._level_max = level_max
        self._exp = round(20 * (1.2 ** (self._level_max - 1)), 2)
        self._gold = int(30 * (1.2 ** (self._level_max - 1)))
        self._state = state

    # Properties with getters and setters
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
    
    @property
    def health(self):
        return self._health
    
    @health.setter
    def health(self, value):
        self._health = max(0, value)
    
    @property
    def damage(self):
        return self._damage
    
    @damage.setter
    def damage(self, value):
        self._damage = value
    
    @property
    def attack_rate(self):
        return self._attack_rate
    
    @attack_rate.setter
    def attack_rate(self, value):
        self._attack_rate = value
    
    @property
    def evade_chance(self):
        return self._evade_chance
    
    @evade_chance.setter
    def evade_chance(self, value):
        self._evade_chance = value
    
    @property
    def level_min(self):
        return self._level_min
    
    @level_min.setter
    def level_min(self, value):
        self._level_min = value
    
    @property
    def level_max(self):
        return self._level_max
    
    @level_max.setter
    def level_max(self, value):
        self._level_max = value
    
    @property
    def exp(self):
        return self._exp
    
    @exp.setter
    def exp(self, value):
        self._exp = value
    
    @property
    def gold(self):
        return self._gold
    
    @gold.setter
    def gold(self, value):
        self._gold = value
    
    @property
    def state(self):
        return self._state
    
    @state.setter
    def state(self, value):
        self._state = value
    
    # Legacy methods for backward compatibility (to be removed in future versions)
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
        self.health = health
    
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

    def attack(self, screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance, y_offset):
        main_character.setHealth(main_character.getHealth() - self.damage)
        animation_enemy_atack(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)
        return f"{self.name} te ha hecho {self.damage} de daño"
    
    def evade(self, screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance, y_offset):
        animation_enemy_evade(screen, font_text, font_ascii, player_x, player_y, inicial_player_health, hud_enemy_hp, main_character, enemy_instance)
        return f"{self.name} ha esquivado el ataque"
    
    def apply_state(self, main_character, screen, font_text, y_offset):
        if self.state:
            # Determine the actual state object (use first if it's a list)
            state_obj = self.state[0] if isinstance(self.state, list) and len(self.state) > 0 else (self.state if isinstance(self.state, dict) else {})
            # Apply the single state object to the main character
            main_character.setState(state_obj)
            # State objects in JSON use the key 'state' for the state name (not 'name').
            # Be defensive: accept either 'state' or 'name' and avoid KeyError.
            state_name = state_obj.get('state') or state_obj.get('name') or 'un estado'
            return f"{self.name} te ha afectado con {state_name}."
        return None

def load_enemies(enemyDb, main_character):
    lvlmin = main_character.getLevel() - 4
    lvlmax = main_character.getLevel() + 4
    valid_enemies = []

    with open(enemyDb, 'r', encoding='utf-8') as archivo:
        normalEnemy = json.load(archivo)

        # Filtrar y crear instancias de Enemy
        for enemy_data in normalEnemy.get("normal", []):
            if int(enemy_data["level_min"]) >= lvlmin and int(enemy_data["level_max"]) <= lvlmax:
                # Normalizar estados: asegurar que cada estado tenga 'name', 'chance', 'duration' y 'effect'
                raw_states = enemy_data.get("states", []) or []
                normalized_states = []
                for s in raw_states:
                    # Copiar para no mutar el origen
                    state_obj = dict(s)
                    # 'state' en JSON original representa el nombre; normalizamos a 'name'
                    if 'state' in state_obj and 'name' not in state_obj:
                        state_obj['name'] = state_obj['state']
                    # Garantizar claves mínimas
                    state_obj.setdefault('chance', 0)
                    state_obj.setdefault('duration', 0)
                    state_obj.setdefault('effect', {})
                    # Aceptar también 'name' si ya existe
                    normalized_states.append(state_obj)

                enemy_instance = Enemy(
                    name=enemy_data["name"],
                    health=enemy_data["health"],
                    damage=enemy_data["damage"],
                    evade_chance=enemy_data["evadeChance"],
                    attack_rate=enemy_data["attackRate"],
                    state=normalized_states,
                    level_min=enemy_data["level_min"],
                    level_max=enemy_data["level_max"]
                )
                valid_enemies.append(enemy_instance)

    return valid_enemies
