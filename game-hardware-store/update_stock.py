"""
Script para actualizar el stock de todos los productos en la base de datos
"""
from app import app
from database import db
from models.database_models import Game, Hardware

def update_stock():
    """Actualizar el stock de todos los juegos y hardware"""
    with app.app_context():
        # Actualizar stock de juegos
        games = Game.query.all()
        for game in games:
            if game.stock == 0:
                game.stock = 100  # Asignar stock de 100 unidades
        
        # Actualizar stock de hardware
        hardware_items = Hardware.query.all()
        for hardware in hardware_items:
            if hardware.stock == 0:
                hardware.stock = 50  # Asignar stock de 50 unidades
        
        # Guardar cambios
        db.session.commit()
        
        print(f"✅ Stock actualizado:")
        print(f"   - {len(games)} juegos ahora tienen stock de 100 unidades")
        print(f"   - {len(hardware_items)} componentes de hardware ahora tienen stock de 50 unidades")

if __name__ == '__main__':
    update_stock()
