"""
Script para verificar el contenido de la base de datos
"""
from app import app
from models.database_models import Hardware, Game
from database import db

with app.app_context():
    # Verificar hardware
    all_hardware = Hardware.get_all_hardware()
    print(f"\n=== HARDWARE EN LA BASE DE DATOS ===")
    print(f"Total de productos: {len(all_hardware)}")
    
    # Contar por tipo
    tipos = {}
    for hw in all_hardware:
        if hw.tipo not in tipos:
            tipos[hw.tipo] = 0
        tipos[hw.tipo] += 1
    
    print("\nProductos por tipo:")
    for tipo, count in tipos.items():
        print(f"  - {tipo}: {count}")
    
    # Mostrar detalles de Motherboards
    motherboards = [hw for hw in all_hardware if hw.tipo == 'Motherboard']
    print(f"\n=== MOTHERBOARDS ===")
    print(f"Total: {len(motherboards)}")
    for mb in motherboards:
        print(f"  - {mb.marca} {mb.modelo} (ID: {mb.id})")
    
    # Verificar juegos
    all_games = Game.get_all_games()
    print(f"\n=== JUEGOS EN LA BASE DE DATOS ===")
    print(f"Total de juegos: {len(all_games)}")
