from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, current_user
import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
import secrets
from flask_wtf.csrf import CSRFProtect

# Cargar variables de entorno
load_dotenv()

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de la aplicación
secret_key = os.environ.get('SECRET_KEY')
if not secret_key or secret_key == 'dev-secret-key-change-in-production':
    # Generar una clave secreta segura si no está configurada
    secret_key = secrets.token_hex(32)
    print("⚠️  SECRET_KEY no configurada. Usando clave generada (cámbiala en producción)")

app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///instance/gametech_store.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configuración de seguridad para sesiones y cookies
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'  # Solo HTTPS en producción
app.config['SESSION_COOKIE_HTTPONLY'] = True  # No accesible vía JavaScript
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protección CSRF básica
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hora de sesión permanente
app.config['REMEMBER_COOKIE_DURATION'] = 3600  # 1 hora para remember me
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'

# Inicializar CSRF protection
csrf = CSRFProtect(app)

# Crear directorio de uploads si no existe
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializar base de datos
from database import db
db.init_app(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models.database_models import User
    return User.query.get(int(user_id))

# Importar modelos
from models.database_models import Game, Hardware, User
from models.compatibility import Compatibility

# Importar controladores
from controllers.store import store_bp
from controllers.hardware import hardware_bp
from controllers.auth import auth_bp
from controllers.cart import cart_bp
from controllers.admin import admin_bp

# Registrar blueprints
app.register_blueprint(store_bp)
app.register_blueprint(hardware_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(admin_bp)

# Configurar logging
if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/gametech_store.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('GameTech Store startup')

@app.route('/')
def index():
    """Página principal de la tienda"""
    juegos = Game.get_all_games()
    hardware = Hardware.get_all_hardware()

    # Obtener algunos productos destacados
    juegos_destacados = juegos[:3]
    hardware_destacado = hardware[:3]

    return render_template('index.html', 
                         juegos_destacados=juegos_destacados, 
                         hardware_destacado=hardware_destacado)

@app.route('/about')
def about():
    """Página acerca de"""
    return render_template('about.html')

@app.errorhandler(404)
def page_not_found(error):
    """Manejador de error 404"""
    app.logger.warning(f'404 error: {request.url}')
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Manejador de error 500"""
    db.session.rollback()
    app.logger.error(f'500 error: {error}')
    return render_template('500.html'), 500

@app.errorhandler(403)
def forbidden(error):
    """Manejador de error 403"""
    return render_template('403.html'), 403

# Prevenir caché en páginas que requieren autenticación
@app.after_request
def add_header(response):
    """Agregar headers para prevenir caché en páginas protegidas"""
    if current_user.is_authenticated or request.endpoint in ['auth.login', 'auth.registro']:
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

# Context processor para hacer variables disponibles en todos los templates
@app.context_processor
def inject_user():
    """Inyectar información del usuario en todos los templates"""
    cart_count = 0
    if current_user.is_authenticated:
        from models.database_models import CartItem
        cart_count = CartItem.query.filter_by(user_id=current_user.id).count()
    return dict(cart_count=cart_count)

if __name__ == '__main__':
    # Inicializar la base de datos
    with app.app_context():
        from database import seed_database
        db.create_all()
        # Poblar con datos iniciales si está vacía
        if Game.query.count() == 0:
            seed_database()
    
    # Ejecutar la aplicación
    app.run(debug=True, host='0.0.0.0', port=5000)
