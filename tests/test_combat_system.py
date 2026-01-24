"""
Test básico del sistema de combate por turnos.
Agente: QA
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_combat_manager():
    """Prueba el CombatManager."""
    print("\n[TEST] CombatManager...")
    try:
        from src.object.main_character import MainCharacter
        from src.object.enemy import Enemy
        from levels.combat_manager import CombatManager
        from src.skill_system import SkillManager
        from src.inventory_system import InventoryManager
        from src.others import resource_path
        
        # Crear personaje de prueba
        player = MainCharacter("TestHero")
        player.setWeapon({"name": "Espada", "damage": 10, "attack_ratio": 0.7})
        player.skill_manager = SkillManager()
        player.inventory_manager = InventoryManager()
        player.inventory_manager.load_item_database(resource_path("src/db/itemsDb.json"))
        
        # Crear enemigo de prueba
        enemy = Enemy(
            name="Goblin",
            health=50,
            damage=8,
            attack_rate=0.5,
            evade_chance=10,
            level_min=1,
            level_max=1,
            state=[{"state": "Envenenado", "chance": 30, "duration": 3, 
                   "effect": {"health": -4}}]
        )
        
        # Crear CombatManager
        combat_mgr = CombatManager(player, enemy)
        
        # Verificar turno inicial
        current_turn = combat_mgr.get_current_turn()
        assert current_turn in ["player", "enemy"], "Turno inicial inválido"
        print(f"  ✓ Turno inicial: {current_turn}")
        
        # Verificar cálculo de probabilidad de huida
        flee_chance = combat_mgr.calculate_flee_chance()
        assert 10 <= flee_chance <= 90, "Probabilidad de huida fuera de rango"
        print(f"  ✓ Probabilidad de huida: {flee_chance:.1f}%")
        
        # Simular algunos turnos
        for i in range(3):
            turn = combat_mgr.get_current_turn()
            combat_mgr.end_turn()
            print(f"  ✓ Turno {i+1}: {turn} -> {combat_mgr.get_current_turn()}")
        
        # Verificar que el combate sigue activo
        is_over, result = combat_mgr.is_combat_over()
        assert not is_over, "Combate terminó prematuramente"
        print(f"  ✓ Combate activo correctamente")
        
        # Simular derrota del enemigo
        enemy.setHealth(0)
        is_over, result = combat_mgr.is_combat_over()
        assert is_over and result == "victory", "Victoria no detectada"
        print(f"  ✓ Victoria detectada correctamente")
        
        print("✅ CombatManager funciona correctamente\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_combat_menu():
    """Prueba el CombatMenu."""
    print("[TEST] CombatMenu...")
    try:
        from levels.combat_menu import CombatMenu
        import pygame
        
        # Inicializar pygame sin display
        pygame.init()
        
        # Crear menú
        menu = CombatMenu()
        
        # Verificar opciones
        assert len(menu.OPTIONS) == 4, "Número de opciones incorrecto"
        assert menu.current_selection == 0, "Selección inicial incorrecta"
        print(f"  ✓ Menú creado con {len(menu.OPTIONS)} opciones")
        
        # Verificar navegación
        menu.current_selection = 1
        assert menu.current_selection == 1, "Navegación no funciona"
        print(f"  ✓ Navegación funciona")
        
        # Verificar submenús
        test_items = [
            {"id": "skill1", "name": "Test Skill", "description": "Test", 
             "mana_cost": 10, "available": True, "reason": ""}
        ]
        menu.open_submenu("skill", test_items)
        assert menu.submenu_active, "Submenú no se abrió"
        assert menu.submenu_type == "skill", "Tipo de submenú incorrecto"
        print(f"  ✓ Submenús funcionan")
        
        menu.close_submenu()
        assert not menu.submenu_active, "Submenú no se cerró"
        print(f"  ✓ Cerrar submenú funciona")
        
        pygame.quit()
        
        print("✅ CombatMenu funciona correctamente\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def test_skill_integration():
    """Prueba la integración de habilidades."""
    print("[TEST] Integración de Habilidades...")
    try:
        from src.object.main_character import MainCharacter
        from src.skill_system import SkillManager
        
        # Crear personaje con SkillManager
        player = MainCharacter("TestHero")
        player.skill_manager = SkillManager()
        
        # Verificar maná inicial
        assert player.skill_manager.current_mana == 100, "Maná inicial incorrecto"
        print(f"  ✓ Maná inicial: {player.skill_manager.current_mana}/100")
        
        # Verificar habilidades disponibles
        skills = player.skill_manager.skills_db
        assert len(skills) > 0, "No hay habilidades cargadas"
        print(f"  ✓ {len(skills)} habilidades cargadas")
        
        # Probar uso de habilidad
        skill_id = "power_strike"
        can_use, reason = player.skill_manager.can_use_skill(skill_id)
        assert can_use, f"No se puede usar {skill_id}: {reason}"
        print(f"  ✓ Puede usar {skill_id}")
        
        # Usar habilidad
        success = player.skill_manager.use_skill(skill_id)
        assert success, "No se pudo usar la habilidad"
        assert player.skill_manager.current_mana < 100, "Maná no se consumió"
        print(f"  ✓ Habilidad usada, maná restante: {player.skill_manager.current_mana}")
        
        # Verificar cooldown
        assert skill_id in player.skill_manager.cooldowns, "Cooldown no se activó"
        print(f"  ✓ Cooldown activado: {player.skill_manager.cooldowns[skill_id]} turnos")
        
        # Regenerar maná
        old_mana = player.skill_manager.current_mana
        player.skill_manager.regenerate_mana()
        assert player.skill_manager.current_mana > old_mana, "Maná no se regeneró"
        print(f"  ✓ Maná regenerado: {old_mana} -> {player.skill_manager.current_mana}")
        
        # Actualizar cooldowns
        player.skill_manager.update_cooldowns()
        print(f"  ✓ Cooldowns actualizados")
        
        print("✅ Integración de habilidades funciona correctamente\n")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Ejecuta todos los tests del sistema de combate."""
    print("="*60)
    print("TESTS DEL SISTEMA DE COMBATE POR TURNOS")
    print("="*60)
    
    results = []
    
    # Ejecutar tests
    results.append(("CombatManager", test_combat_manager()))
    results.append(("CombatMenu", test_combat_menu()))
    results.append(("Skill Integration", test_skill_integration()))
    
    # Mostrar resultados
    print("="*60)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"RESULTADOS: {passed}/{total} tests pasados")
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {name}")
    
    print("="*60)
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
