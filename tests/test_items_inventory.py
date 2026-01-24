"""
Tests para el sistema de Items e Inventario.

Ejecutar: python -m pytest tests/test_items_inventory.py -v
O añadir a test_suite.py existente
"""

import sys
import os

# Añadir el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.object.item import Item, load_items
from src.inventory_system import InventoryManager, get_inventory_manager, reset_inventory_manager
from src.object.main_character import MainCharacter


def test_load_items():
    """Test: Cargar items desde JSON."""
    print("\n[TEST 1] Cargando items desde JSON...")
    
    items = load_items("src/db/itemsDb.json")
    
    assert len(items) > 0, "No se cargaron items"
    assert "hp_potion_small" in items, "No se encontró hp_potion_small"
    assert items["hp_potion_small"].name == "Poción de Vida Pequeña"
    
    print(f"✅ Cargados {len(items)} items correctamente")


def test_item_properties():
    """Test: Propiedades de los items."""
    print("\n[TEST 2] Verificando propiedades de items...")
    
    items = load_items("src/db/itemsDb.json")
    potion = items["hp_potion_small"]
    
    assert potion.id == "hp_potion_small"
    assert potion.category == "healing"
    assert potion.price == 25
    assert potion.stackable == True
    assert potion.max_stack == 10
    assert potion.can_use("combat") == True
    assert potion.can_use("shop") == False
    
    print("✅ Propiedades de items correctas")


def test_inventory_add_remove():
    """Test: Añadir y remover items del inventario."""
    print("\n[TEST 3] Probando añadir/remover items...")
    
    reset_inventory_manager()
    inventory = get_inventory_manager()
    inventory.load_item_database("src/db/itemsDb.json")
    
    # Añadir item
    success, msg = inventory.add_item("hp_potion_small", 3)
    assert success == True, f"No se pudo añadir item: {msg}"
    assert inventory.has_item("hp_potion_small", 3) == True
    
    # Remover item
    success, msg = inventory.remove_item("hp_potion_small", 2)
    assert success == True, f"No se pudo remover item: {msg}"
    assert inventory.has_item("hp_potion_small", 1) == True
    assert inventory.has_item("hp_potion_small", 2) == False
    
    print("✅ Añadir/remover items funciona correctamente")


def test_inventory_limits():
    """Test: Límites del inventario."""
    print("\n[TEST 4] Probando límites de inventario...")
    
    reset_inventory_manager()
    inventory = InventoryManager(max_slots=2)
    inventory.load_item_database("src/db/itemsDb.json")
    
    # Añadir hasta llenar slots
    inventory.add_item("hp_potion_small", 1)
    inventory.add_item("mp_potion_small", 1)
    
    # Intentar añadir un tercero (debería fallar)
    success, msg = inventory.add_item("antidote", 1)
    assert success == False, "Debería fallar al añadir a inventario lleno"
    assert "lleno" in msg.lower()
    
    # Verificar límite de stack
    inventory.clear()
    inventory.add_item("hp_potion_small", 10)
    success, msg = inventory.add_item("hp_potion_small", 1)
    assert success == False, "Debería fallar al exceder max_stack"
    
    print("✅ Límites de inventario funcionan correctamente")


def test_use_healing_item():
    """Test: Usar poción de vida."""
    print("\n[TEST 5] Probando uso de poción de vida...")
    
    reset_inventory_manager()
    inventory = get_inventory_manager()
    inventory.load_item_database("src/db/itemsDb.json")
    
    # Crear personaje con poca vida
    character = MainCharacter("TestHero")
    character._max_health = 150
    character.setHealth(50)
    
    # Añadir poción
    inventory.add_item("hp_potion_small", 1)
    
    # Usar poción
    success, msg = inventory.use_item("hp_potion_small", character, "combat")
    assert success == True, f"No se pudo usar poción: {msg}"
    assert character.getHealth() == 80, f"HP incorrecto: {character.getHealth()}"
    assert inventory.has_item("hp_potion_small") == False, "Poción no se removió"
    
    print("✅ Uso de poción de vida funciona correctamente")


def test_use_mana_item():
    """Test: Usar poción de maná."""
    print("\n[TEST 6] Probando uso de poción de maná...")
    
    reset_inventory_manager()
    inventory = get_inventory_manager()
    inventory.load_item_database("src/db/itemsDb.json")
    
    # Crear personaje con skill_manager
    character = MainCharacter("TestMage")
    
    # Mock del skill_manager
    class MockSkillManager:
        def __init__(self):
            self.current_mana = 30
            self.max_mana = 100
    
    character.skill_manager = MockSkillManager()
    
    # Añadir poción de maná
    inventory.add_item("mp_potion_small", 1)
    
    # Usar poción
    success, msg = inventory.use_item("mp_potion_small", character, "combat")
    assert success == True, f"No se pudo usar poción: {msg}"
    assert character.skill_manager.current_mana == 50, f"Maná incorrecto: {character.skill_manager.current_mana}"
    
    print("✅ Uso de poción de maná funciona correctamente")


def test_cure_state_item():
    """Test: Curar estado alterado."""
    print("\n[TEST 7] Probando antídoto...")
    
    reset_inventory_manager()
    inventory = get_inventory_manager()
    inventory.load_item_database("src/db/itemsDb.json")
    
    # Crear personaje envenenado
    character = MainCharacter("TestWarrior")
    character.setState({"state": "Envenenado", "duration": 3})
    
    # Añadir antídoto
    inventory.add_item("antidote", 1)
    
    # Usar antídoto
    success, msg = inventory.use_item("antidote", character, "combat")
    assert success == True, f"No se pudo usar antídoto: {msg}"
    assert character.getState() is None, "Estado no se curó"
    
    print("✅ Antídoto funciona correctamente")


def test_inventory_persistence():
    """Test: Guardar y cargar inventario."""
    print("\n[TEST 8] Probando persistencia de inventario...")
    
    reset_inventory_manager()
    inventory = get_inventory_manager()
    inventory.load_item_database("src/db/itemsDb.json")
    
    # Añadir varios items
    inventory.add_item("hp_potion_small", 5)
    inventory.add_item("mp_potion_medium", 3)
    inventory.add_item("bomb", 2)
    
    # Serializar
    data = inventory.to_dict()
    assert data["max_slots"] == 30
    assert data["items"]["hp_potion_small"] == 5
    
    # Crear nuevo inventario y cargar
    reset_inventory_manager()
    inventory2 = get_inventory_manager()
    inventory2.load_item_database("src/db/itemsDb.json")
    inventory2.from_dict(data)
    
    assert inventory2.has_item("hp_potion_small", 5) == True
    assert inventory2.has_item("mp_potion_medium", 3) == True
    assert inventory2.get_total_slots_used() == 3
    
    print("✅ Persistencia de inventario funciona correctamente")


def test_inventory_integration_maincharacter():
    """Test: Integración con MainCharacter."""
    print("\n[TEST 9] Probando integración con MainCharacter...")
    
    character = MainCharacter("TestHero")
    
    # Inicializar inventario
    from src.inventory_system import get_inventory_manager
    character.inventory_manager = get_inventory_manager()
    character.inventory_manager.load_item_database("src/db/itemsDb.json")
    
    # Añadir items
    character.inventory_manager.add_item("hp_potion_large", 2)
    
    # Guardar
    success = character.save_game(slot=1)
    assert success == True, "No se pudo guardar"
    
    # Crear nuevo personaje y cargar
    character2 = MainCharacter("Dummy")
    success = character2.load_game(slot=1)
    assert success == True, "No se pudo cargar"
    assert character2.getName() == "TestHero"
    assert character2.inventory_manager is not None
    assert character2.inventory_manager.has_item("hp_potion_large", 2) == True
    
    print("✅ Integración con MainCharacter funciona correctamente")


def test_get_usable_items():
    """Test: Filtrar items usables por contexto."""
    print("\n[TEST 10] Probando filtrado de items usables...")
    
    reset_inventory_manager()
    inventory = get_inventory_manager()
    inventory.load_item_database("src/db/itemsDb.json")
    
    # Añadir varios items
    inventory.add_item("hp_potion_small", 3)
    inventory.add_item("bomb", 1)  # Solo usable en combate
    inventory.add_item("antidote", 2)
    
    # Obtener items usables en combate
    combat_items = inventory.get_usable_items("combat")
    assert len(combat_items) == 3, f"Debería haber 3 items usables en combate, hay {len(combat_items)}"
    
    # Obtener items usables en mazmorra (bomb no debería aparecer)
    dungeon_items = inventory.get_usable_items("dungeon")
    assert len(dungeon_items) == 2, f"Debería haber 2 items usables en mazmorra, hay {len(dungeon_items)}"
    
    print("✅ Filtrado de items usables funciona correctamente")


def run_all_tests():
    """Ejecuta todos los tests."""
    tests = [
        test_load_items,
        test_item_properties,
        test_inventory_add_remove,
        test_inventory_limits,
        test_use_healing_item,
        test_use_mana_item,
        test_cure_state_item,
        test_inventory_persistence,
        test_inventory_integration_maincharacter,
        test_get_usable_items
    ]
    
    print("="*60)
    print("TESTS DEL SISTEMA DE ITEMS E INVENTARIO")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ FALLO: {test.__name__}")
            print(f"   Error: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR INESPERADO en {test.__name__}: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"RESULTADOS: {passed} pasados, {failed} fallidos")
    print("="*60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
