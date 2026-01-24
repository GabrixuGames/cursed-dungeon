"""
Test visual de la tienda mejorada con pestañas.
Ejecutar: python tests/test_shop_visual.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
from src.object.main_character import MainCharacter
from src.inventory_system import get_inventory_manager, reset_inventory_manager
from src.others import resource_path

# Inicializar pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Test - Tienda Mejorada")

try:
    font = pygame.font.Font(resource_path("src/assets/fonts/texgyrebonum-regular.otf"), 25)
except:
    font = pygame.font.Font(None, 25)

# Crear personaje de prueba
print("\n=== TEST VISUAL DE LA TIENDA ===\n")
print("Inicializando personaje...")

character = MainCharacter("TestHero")
character.setMoney(500)
character.setLevel(5)

# Inicializar inventario
reset_inventory_manager()
character.inventory_manager = get_inventory_manager()
character.inventory_manager.load_item_database()

# Añadir algunos items al inventario para probar la visualización
character.inventory_manager.add_item("hp_potion_small", 3)
character.inventory_manager.add_item("mp_potion_medium", 2)
character.inventory_manager.add_item("antidote", 1)

print(f"✅ Personaje creado:")
print(f"   - Nombre: {character.getName()}")
print(f"   - Nivel: {character.getLevel()}")
print(f"   - Dinero: {character.getMoney()} oro")
print(f"   - Items en inventario: {character.inventory_manager.get_total_slots_used()}/{character.inventory_manager.max_slots}")
print(f"\n📦 Contenido del inventario:")
for item, qty in character.inventory_manager.get_all_items():
    print(f"   - {item.name} x{qty}")

print("\n" + "="*50)
print("INSTRUCCIONES:")
print("  ← / → : Cambiar entre pestañas (Armas / Items)")
print("  ↑ / ↓ : Navegar por las opciones")
print("  Enter : Comprar item/arma seleccionado")
print("  Esc   : Salir de la tienda")
print("="*50 + "\n")

# Importar y ejecutar la tienda
from levels.shop import shop

print("Abriendo tienda...\n")

try:
    shop(character, screen, font, 800, 600)
    print("\n✅ Tienda cerrada correctamente")
    
    # Mostrar estado final
    print(f"\n📊 Estado final del personaje:")
    print(f"   - Dinero restante: {character.getMoney()} oro")
    print(f"   - Items en inventario: {character.inventory_manager.get_total_slots_used()}/{character.inventory_manager.max_slots}")
    
    if character.inventory_manager.get_all_items():
        print(f"\n📦 Inventario actualizado:")
        for item, qty in character.inventory_manager.get_all_items():
            print(f"   - {item.name} x{qty}")
    else:
        print(f"\n📦 Inventario vacío")
    
except Exception as e:
    print(f"\n❌ Error ejecutando tienda: {e}")
    import traceback
    traceback.print_exc()

pygame.quit()
print("\n=== TEST COMPLETADO ===")
