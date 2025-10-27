"""
Controlador para el panel de administración
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from database import db
from models.database_models import Game, Hardware, User
from werkzeug.utils import secure_filename
import os
from datetime import datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Decorador para verificar que el usuario sea administrador
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash('No tienes permisos para acceder a esta página', 'danger')
            return redirect(url_for('store.index'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== DASHBOARD ====================
@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """Panel principal de administración"""
    total_games = Game.query.count()
    total_hardware = Hardware.query.count()
    total_users = User.query.count()
    
    # Productos con bajo stock
    low_stock_games = Game.query.filter(Game.stock < 10).all()
    low_stock_hardware = Hardware.query.filter(Hardware.stock < 10).all()
    
    return render_template('admin/dashboard.html',
                         total_games=total_games,
                         total_hardware=total_hardware,
                         total_users=total_users,
                         low_stock_games=low_stock_games,
                         low_stock_hardware=low_stock_hardware)

# ==================== GESTIÓN DE JUEGOS ====================
@admin_bp.route('/games')
@login_required
@admin_required
def games():
    """Lista de todos los juegos"""
    games = Game.query.order_by(Game.created_at.desc()).all()
    return render_template('admin/games.html', games=games)

@admin_bp.route('/games/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_game():
    """Crear nuevo juego"""
    if request.method == 'POST':
        try:
            import json
            # Construir requisitos mínimos
            req_min = {
                'CPU': request.form.get('min_cpu', ''),
                'GPU': request.form.get('min_gpu', ''),
                'RAM': request.form.get('min_ram', ''),
                'Almacenamiento': request.form.get('min_storage', '')
            }
            # Construir requisitos recomendados
            req_rec = {
                'CPU': request.form.get('rec_cpu', ''),
                'GPU': request.form.get('rec_gpu', ''),
                'RAM': request.form.get('rec_ram', ''),
                'Almacenamiento': request.form.get('rec_storage', '')
            }
            
            game = Game(
                nombre=request.form['title'],
                descripcion=request.form['description'],
                precio=float(request.form['price']),
                stock=int(request.form['stock']),
                genero=request.form['genre'],
                fecha_lanzamiento=datetime.strptime(request.form['release_date'], '%Y-%m-%d'),
                desarrollador=request.form['developer'],
                imagen=request.form.get('image_url', ''),
                requisitos_minimos=json.dumps(req_min),
                requisitos_recomendados=json.dumps(req_rec)
            )
            
            db.session.add(game)
            db.session.commit()
            
            flash(f'Juego "{game.nombre}" creado exitosamente', 'success')
            return redirect(url_for('admin.games'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el juego: {str(e)}', 'danger')
    
    return render_template('admin/game_form.html', game=None)

@admin_bp.route('/games/<int:game_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_game(game_id):
    """Editar juego existente"""
    game = Game.query.get_or_404(game_id)
    
    if request.method == 'POST':
        try:
            import json
            # Construir requisitos mínimos
            req_min = {
                'CPU': request.form.get('min_cpu', ''),
                'GPU': request.form.get('min_gpu', ''),
                'RAM': request.form.get('min_ram', ''),
                'Almacenamiento': request.form.get('min_storage', '')
            }
            # Construir requisitos recomendados
            req_rec = {
                'CPU': request.form.get('rec_cpu', ''),
                'GPU': request.form.get('rec_gpu', ''),
                'RAM': request.form.get('rec_ram', ''),
                'Almacenamiento': request.form.get('rec_storage', '')
            }
            
            game.nombre = request.form['title']
            game.descripcion = request.form['description']
            game.precio = float(request.form['price'])
            game.stock = int(request.form['stock'])
            game.genero = request.form['genre']
            game.fecha_lanzamiento = datetime.strptime(request.form['release_date'], '%Y-%m-%d')
            game.desarrollador = request.form['developer']
            game.imagen = request.form.get('image_url', '')
            game.requisitos_minimos = json.dumps(req_min)
            game.requisitos_recomendados = json.dumps(req_rec)
            
            db.session.commit()
            
            flash(f'Juego "{game.nombre}" actualizado exitosamente', 'success')
            return redirect(url_for('admin.games'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el juego: {str(e)}', 'danger')
    
    return render_template('admin/game_form.html', game=game)

@admin_bp.route('/games/<int:game_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_game(game_id):
    """Eliminar juego"""
    game = Game.query.get_or_404(game_id)
    
    try:
        title = game.nombre
        db.session.delete(game)
        db.session.commit()
        flash(f'Juego "{title}" eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el juego: {str(e)}', 'danger')
    
    return redirect(url_for('admin.games'))

# ==================== GESTIÓN DE HARDWARE ====================
@admin_bp.route('/hardware')
@login_required
@admin_required
def hardware():
    """Lista de todo el hardware"""
    hardware_items = Hardware.query.order_by(Hardware.created_at.desc()).all()
    return render_template('admin/hardware.html', hardware_items=hardware_items)

@admin_bp.route('/hardware/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_hardware():
    """Crear nuevo hardware"""
    if request.method == 'POST':
        try:
            hardware = Hardware(
                tipo=request.form['category'],
                marca=request.form['brand'],
                modelo=request.form['model'],
                precio=float(request.form['price']),
                descripcion=request.form['description'],
                imagen=request.form.get('image_url', ''),
                especificaciones=request.form.get('specifications', ''),
                stock=int(request.form['stock'])
            )
            
            db.session.add(hardware)
            db.session.commit()
            
            flash(f'Hardware "{hardware.marca} {hardware.modelo}" creado exitosamente', 'success')
            return redirect(url_for('admin.hardware'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el hardware: {str(e)}', 'danger')
    
    return render_template('admin/hardware_form.html', hardware=None)

@admin_bp.route('/hardware/<int:hardware_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_hardware(hardware_id):
    """Editar hardware existente"""
    hardware = Hardware.query.get_or_404(hardware_id)
    
    if request.method == 'POST':
        try:
            hardware.tipo = request.form['category']
            hardware.marca = request.form['brand']
            hardware.modelo = request.form['model']
            hardware.precio = float(request.form['price'])
            hardware.descripcion = request.form['description']
            hardware.imagen = request.form.get('image_url', '')
            hardware.especificaciones = request.form.get('specifications', '')
            hardware.stock = int(request.form['stock'])
            
            db.session.commit()
            
            flash(f'Hardware "{hardware.marca} {hardware.modelo}" actualizado exitosamente', 'success')
            return redirect(url_for('admin.hardware'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el hardware: {str(e)}', 'danger')
    
    return render_template('admin/hardware_form.html', hardware=hardware)

@admin_bp.route('/hardware/<int:hardware_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_hardware(hardware_id):
    """Eliminar hardware"""
    hardware = Hardware.query.get_or_404(hardware_id)
    
    try:
        name = f"{hardware.marca} {hardware.modelo}"
        db.session.delete(hardware)
        db.session.commit()
        flash(f'Hardware "{name}" eliminado exitosamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el hardware: {str(e)}', 'danger')
    
    return redirect(url_for('admin.hardware'))

# ==================== GESTIÓN DE USUARIOS ====================
@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Lista de todos los usuarios"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    """Cambiar estado de administrador de un usuario"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('No puedes cambiar tu propio estado de administrador', 'warning')
        return redirect(url_for('admin.users'))
    
    try:
        user.is_admin = not user.is_admin
        db.session.commit()
        status = "administrador" if user.is_admin else "usuario normal"
        flash(f'Usuario "{user.username}" ahora es {status}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar el estado: {str(e)}', 'danger')
    
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/<int:user_id>/toggle-active', methods=['POST'])
@login_required
@admin_required
def toggle_active(user_id):
    """Activar/desactivar usuario"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('No puedes desactivar tu propia cuenta', 'warning')
        return redirect(url_for('admin.users'))
    
    try:
        user.is_active = not user.is_active
        db.session.commit()
        status = "activado" if user.is_active else "desactivado"
        flash(f'Usuario "{user.username}" ha sido {status}', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al cambiar el estado: {str(e)}', 'danger')
    
    return redirect(url_for('admin.users'))
