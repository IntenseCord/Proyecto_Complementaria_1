"""
Controlador de autenticación
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from database import db
from models.database_models import User
import re

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Página de registro de usuarios"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validaciones básicas
        if not username or not email or not password:
            flash('Todos los campos son obligatorios', 'danger')
            return render_template('auth/registro.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('auth/registro.html')
        
        # Validaciones de seguridad para la contraseña
        if len(password) < 8:
            flash('La contraseña debe tener al menos 8 caracteres', 'danger')
            return render_template('auth/registro.html')
        
        if not re.search(r'[A-Z]', password):
            flash('La contraseña debe contener al menos una letra mayúscula', 'danger')
            return render_template('auth/registro.html')
        
        if not re.search(r'[a-z]', password):
            flash('La contraseña debe contener al menos una letra minúscula', 'danger')
            return render_template('auth/registro.html')
        
        if not re.search(r'\d', password):
            flash('La contraseña debe contener al menos un número', 'danger')
            return render_template('auth/registro.html')
        
        # Verificar si el usuario ya existe
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso', 'danger')
            return render_template('auth/registro.html')
        
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'danger')
            return render_template('auth/registro.html')
        
        # Crear nuevo usuario con contraseña cifrada
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('¡Registro exitoso! Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/registro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        if not username or not password:
            flash('Por favor ingresa usuario y contraseña', 'danger')
            return render_template('auth/login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            # Login exitoso
            login_user(user, remember=remember)
            flash(f'¡Bienvenido {user.username}!', 'success')
            
            # Redirigir a la página solicitada o al inicio
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            # Login fallido
            flash('Usuario o contraseña incorrectos', 'danger')
            # Aquí podrías implementar un contador de intentos fallidos
            # Para simplicidad, solo mostramos el mensaje
    
    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Cerrar sesión"""
    logout_user()
    # Limpiar toda la sesión
    session.clear()
    flash('Has cerrado sesión correctamente', 'info')
    response = redirect(url_for('index'))
    # Eliminar la cookie de remember me si existe
    response.set_cookie('remember_token', '', expires=0)
    # Prevenir caché del navegador
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@auth_bp.route('/perfil')
@login_required
def perfil():
    """Página de perfil del usuario"""
    return render_template('auth/perfil.html', user=current_user)

@auth_bp.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    """Editar perfil del usuario"""
    if request.method == 'POST':
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        
        # Actualizar email
        if email and email != current_user.email:
            if User.query.filter_by(email=email).first():
                flash('El email ya está en uso', 'danger')
            else:
                current_user.email = email
                flash('Email actualizado correctamente', 'success')
        
        # Cambiar contraseña
        if current_password and new_password:
            if current_user.check_password(current_password):
                if len(new_password) >= 8 and re.search(r'[A-Z]', new_password) and re.search(r'[a-z]', new_password) and re.search(r'\d', new_password):
                    current_user.set_password(new_password)
                    flash('Contraseña actualizada correctamente', 'success')
                else:
                    flash('La nueva contraseña debe tener al menos 8 caracteres, con mayúscula, minúscula y número', 'danger')
            else:
                flash('Contraseña actual incorrecta', 'danger')
        
        db.session.commit()
        return redirect(url_for('auth.perfil'))
    
    return render_template('auth/editar_perfil.html', user=current_user)
