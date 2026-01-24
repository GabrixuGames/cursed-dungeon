"""
Sistema de Combate por Turnos para Cursed Dungeon.

Este módulo implementa el gestor de combate por turnos que reemplaza
el sistema de combate en tiempo real.

Agente: GameDevSenior
"""

from typing import Literal, Optional, Dict, List, Tuple
from collections import deque
import random


class CombatManager:
    """Gestor del sistema de combate por turnos."""
    
    def __init__(self, player, enemy):
        """
        Inicializa el gestor de combate.
        
        Args:
            player: Instancia de MainCharacter
            enemy: Instancia de Enemy
        """
        self.player = player
        self.enemy = enemy
        self.turn_count = 0
        self.combat_active = True
        self.turn_queue = deque()
        self.player_buffs: List[Dict] = []  # Buffs activos del jugador
        self.enemy_buffs: List[Dict] = []   # Buffs activos del enemigo
        self.player_active_states: List[Dict] = []  # Estados alterados activos
        
        # Calcular orden inicial de turnos
        self._calculate_turn_order()
    
    def _calculate_turn_order(self):
        """
        Calcula el orden de turnos basado en velocidad.
        
        Reglas:
        - El personaje más rápido va primero
        - Si la diferencia de velocidad > 0.3, el rápido ataca 2 veces
        """
        player_speed = self.player.getWeapon()["attack_ratio"]
        enemy_speed = self.enemy.getAttackRate()
        
        # Limpiar cola de turnos
        self.turn_queue.clear()
        
        # Sistema simple: el más rápido va primero
        speed_diff = abs(player_speed - enemy_speed)
        
        if player_speed > enemy_speed:
            self.turn_queue.append("player")
            # Si la diferencia es significativa, el jugador ataca 2 veces
            if speed_diff > 0.3:
                self.turn_queue.append("player")
            self.turn_queue.append("enemy")
        else:
            self.turn_queue.append("enemy")
            # Si la diferencia es significativa, el enemigo ataca 2 veces
            if speed_diff > 0.3:
                self.turn_queue.append("enemy")
            self.turn_queue.append("player")
    
    def get_current_turn(self) -> Literal["player", "enemy"]:
        """
        Retorna de quién es el turno actual.
        
        Returns:
            "player" o "enemy"
        """
        if not self.turn_queue:
            self._calculate_turn_order()
        return self.turn_queue[0]
    
    def end_turn(self):
        """Finaliza el turno actual y pasa al siguiente."""
        if self.turn_queue:
            self.turn_queue.popleft()
        
        # Si no quedan turnos, iniciar nuevo ciclo
        if not self.turn_queue:
            self.turn_count += 1
            self._calculate_turn_order()
            self._process_turn_effects()
    
    def _process_turn_effects(self):
        """
        Procesa efectos al final de cada ciclo completo de turnos.
        
        - Regenera maná del jugador
        - Actualiza cooldowns de habilidades
        - Procesa buffs activos
        - Procesa estados alterados
        """
        # Regenerar maná del jugador
        if hasattr(self.player, 'skill_manager') and self.player.skill_manager:
            self.player.skill_manager.regenerate_mana()
            self.player.skill_manager.update_cooldowns()
        
        # Procesar buffs activos
        self._update_buffs(self.player_buffs)
        self._update_buffs(self.enemy_buffs)
        
        # Procesar estados alterados
        # Los estados se procesarán en el turno del enemigo
        # para mantener compatibilidad con el código existente
    
    def _update_buffs(self, buff_list: List[Dict]):
        """
        Actualiza la duración de los buffs activos.
        
        Args:
            buff_list: Lista de buffs a actualizar
        """
        for buff in buff_list[:]:  # Iterar sobre copia para poder eliminar
            if "duration" in buff:
                buff["duration"] -= 1
                if buff["duration"] <= 0:
                    buff_list.remove(buff)
    
    def process_player_state_effects(self) -> Optional[str]:
        """
        Procesa efectos de estados alterados del jugador.
        
        Returns:
            Mensaje de efecto aplicado o None
        """
        if not self.player.getState():
            return None
        
        state = self.player.getState()
        
        # Aplicar daño de estado
        if "effect" in state and "health" in state["effect"]:
            damage = abs(state["effect"]["health"])
            self.player.setHealth(self.player.getHealth() - damage)
            
            state_name = state.get("state", state.get("name", "un estado"))
            return f"Pierdes {damage} HP debido a {state_name}."
        
        return None
    
    def add_buff(self, target: Literal["player", "enemy"], buff: Dict):
        """
        Añade un buff a un objetivo.
        
        Args:
            target: "player" o "enemy"
            buff: Diccionario con información del buff
        """
        if target == "player":
            self.player_buffs.append(buff)
        else:
            self.enemy_buffs.append(buff)
    
    def get_active_buffs(self, target: Literal["player", "enemy"]) -> List[Dict]:
        """
        Obtiene los buffs activos de un objetivo.
        
        Args:
            target: "player" o "enemy"
        
        Returns:
            Lista de buffs activos
        """
        if target == "player":
            return self.player_buffs
        else:
            return self.enemy_buffs
    
    def calculate_flee_chance(self) -> float:
        """
        Calcula la probabilidad de huida del jugador.
        
        Returns:
            Probabilidad de huida (0-100)
        """
        # Si tiene el efecto de Cuerda de Escape, huida garantizada
        if hasattr(self.player, '_guaranteed_flee') and self.player._guaranteed_flee:
            return 100.0
        
        level_diff = self.player.getLevel() - self.enemy.level_max
        base_chance = 50  # 50% base
        
        # +5% por cada nivel de diferencia
        chance = base_chance + (level_diff * 5)
        
        # Limitar entre 10% y 90%
        return max(10.0, min(90.0, chance))
    
    def attempt_flee(self) -> Tuple[bool, str]:
        """
        Intenta huir del combate.
        
        Returns:
            Tuple[bool, str]: (success, message)
        """
        flee_chance = self.calculate_flee_chance()
        roll = random.uniform(0, 100)
        
        if roll < flee_chance:
            self.combat_active = False
            
            # Consumir efecto de Cuerda de Escape si se usó
            if hasattr(self.player, '_guaranteed_flee') and self.player._guaranteed_flee:
                self.player._guaranteed_flee = False
                return True, "¡Usaste Cuerda de Escape! Huida garantizada."
            
            return True, f"¡Lograste huir! (Probabilidad: {flee_chance:.0f}%)"
        else:
            return False, f"¡No pudiste escapar! (Probabilidad: {flee_chance:.0f}%)"
    
    def is_combat_over(self) -> Tuple[bool, Optional[Literal["victory", "defeat", "flee"]]]:
        """
        Verifica si el combate ha terminado.
        
        Returns:
            Tuple[bool, str]: (is_over, result)
        """
        if self.player.getHealth() <= 0:
            return True, "defeat"
        if self.enemy.getHealth() <= 0:
            return True, "victory"
        if not self.combat_active:
            return True, "flee"
        return False, None
    
    def get_turn_info(self) -> Dict:
        """
        Obtiene información sobre el estado actual del combate.
        
        Returns:
            Diccionario con información del turno
        """
        return {
            "current_turn": self.get_current_turn(),
            "turn_count": self.turn_count,
            "turn_queue": list(self.turn_queue),
            "player_hp": self.player.getHealth(),
            "enemy_hp": self.enemy.getHealth(),
            "player_mana": self.player.skill_manager.current_mana if self.player.skill_manager else 0,
            "player_buffs": len(self.player_buffs),
            "enemy_buffs": len(self.enemy_buffs),
        }


def create_combat_manager(player, enemy) -> CombatManager:
    """
    Factory function para crear un CombatManager.
    
    Args:
        player: Instancia de MainCharacter
        enemy: Instancia de Enemy
    
    Returns:
        CombatManager inicializado
    """
    return CombatManager(player, enemy)
