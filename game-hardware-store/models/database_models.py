"""
Modelos de base de datos usando SQLAlchemy
"""
from database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_, and_
import json

class User(db.Model):
    """Modelo de usuario"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relaciones
    cart_items = db.relationship('CartItem', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Establecer contraseña hasheada"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verificar contraseña"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Game(db.Model):
    """Modelo de juego con base de datos"""
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False, index=True)
    descripcion = db.Column(db.Text, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen = db.Column(db.String(300))
    genero = db.Column(db.String(50), index=True)
    desarrollador = db.Column(db.String(100))
    fecha_lanzamiento = db.Column(db.DateTime)
    requisitos_minimos = db.Column(db.Text)  # JSON string
    requisitos_recomendados = db.Column(db.Text)  # JSON string
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_requisitos_minimos(self):
        """Obtener requisitos mínimos como dict"""
        return json.loads(self.requisitos_minimos) if self.requisitos_minimos else {}
    
    def get_requisitos_recomendados(self):
        """Obtener requisitos recomendados como dict"""
        return json.loads(self.requisitos_recomendados) if self.requisitos_recomendados else {}
    
    @property
    def requisitos_minimos_dict(self):
        """Property para acceder a requisitos mínimos como dict en templates"""
        return self.get_requisitos_minimos()
    
    @property
    def requisitos_recomendados_dict(self):
        """Property para acceder a requisitos recomendados como dict en templates"""
        return self.get_requisitos_recomendados()
    
    @classmethod
    def get_all_games(cls):
        """Obtener todos los juegos"""
        return cls.query.filter_by().all()
    
    @classmethod
    def get_game_by_id(cls, game_id):
        """Obtener un juego por ID"""
        return cls.query.get(game_id)
    
    @classmethod
    def search_games(cls, query):
        """Buscar juegos por nombre, descripción o género"""
        if not query:
            return []
        
        search_term = f"%{query}%"
        return cls.query.filter(
            db.or_(
                cls.nombre.ilike(search_term),
                cls.descripcion.ilike(search_term),
                cls.genero.ilike(search_term)
            )
        ).all()
    
    @classmethod
    def get_games_by_hardware(cls, hardware_specs):
        """Obtener juegos compatibles con el hardware especificado usando el sistema de compatibilidad"""
        from models.compatibility import Compatibility

        juegos = cls.get_all_games()
        juegos_compatibles = []

        for juego in juegos:
            # Convertir hardware_specs a objetos Hardware para compatibilidad
            componentes = []
            for tipo, specs in hardware_specs.items():
                # Crear un objeto Hardware temporal para la comparación
                componente = Hardware(
                    tipo=tipo.upper(),
                    marca=specs.get('marca', ''),
                    modelo=specs.get('modelo', ''),
                    especificaciones=json.dumps(specs)
                )
                componentes.append(componente)

            # Verificar compatibilidad usando el sistema existente
            resultado = Compatibility.verificar_compatibility_completa([juego], componentes)
            if resultado['compatible']:
                juegos_compatibles.append(juego)

        return juegos_compatibles
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'precio': self.precio,
            'imagen': self.imagen,
            'genero': self.genero,
            'desarrollador': self.desarrollador,
            'fecha_lanzamiento': self.fecha_lanzamiento.isoformat() if self.fecha_lanzamiento else None,
            'requisitos_minimos': self.get_requisitos_minimos(),
            'requisitos_recomendados': self.get_requisitos_recomendados(),
            'stock': self.stock
        }
    
    def __repr__(self):
        return f'<Game {self.nombre}>'


class Hardware(db.Model):
    """Modelo de hardware con base de datos"""
    __tablename__ = 'hardware'
    
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False, index=True)
    marca = db.Column(db.String(100), nullable=False, index=True)
    modelo = db.Column(db.String(200), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(300))
    especificaciones = db.Column(db.Text)  # JSON string
    stock = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_especificaciones(self):
        """Obtener especificaciones como dict"""
        return json.loads(self.especificaciones) if self.especificaciones else {}
    
    @property
    def especificaciones_dict(self):
        """Property para acceder a especificaciones como dict en templates"""
        return self.get_especificaciones()
    
    @classmethod
    def get_all_hardware(cls):
        """Obtener todo el hardware"""
        return cls.query.all()
    
    @classmethod
    def get_hardware_by_tipo(cls, tipo):
        """Obtener hardware por tipo"""
        return cls.query.filter_by(tipo=tipo).all()
    
    @classmethod
    def get_hardware_by_id(cls, hardware_id):
        """Obtener hardware por ID"""
        return cls.query.get(hardware_id)
    
    @classmethod
    def buscar_hardware(cls, query):
        """Buscar hardware"""
        search = f"%{query}%"
        return cls.query.filter(
            or_(
                cls.marca.ilike(search),
                cls.modelo.ilike(search),
                cls.descripcion.ilike(search),
                cls.tipo.ilike(search)
            )
        ).all()
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            'id': self.id,
            'tipo': self.tipo,
            'marca': self.marca,
            'modelo': self.modelo,
            'precio': self.precio,
            'descripcion': self.descripcion,
            'imagen': self.imagen,
            'especificaciones': self.get_especificaciones(),
            'stock': self.stock
        }
    
    def __repr__(self):
        return f'<Hardware {self.marca} {self.modelo}>'


class CartItem(db.Model):
    """Modelo de item en el carrito"""
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_type = db.Column(db.String(20), nullable=False)  # 'game' o 'hardware'
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_product(self):
        """Obtener el producto asociado"""
        if self.product_type == 'game':
            return Game.query.get(self.product_id)
        elif self.product_type == 'hardware':
            return Hardware.query.get(self.product_id)
        return None
    
    def get_subtotal(self):
        """Calcular subtotal"""
        product = self.get_product()
        if product:
            return product.precio * self.quantity
        return 0.0
    
    def __repr__(self):
        return f'<CartItem {self.product_type}:{self.product_id}>'


class Order(db.Model):
    """Modelo de orden de compra"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.id} - ${self.total}>'


class OrderItem(db.Model):
    """Modelo de item en una orden"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_type = db.Column(db.String(20), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    
    def get_subtotal(self):
        """Calcular subtotal"""
        return self.price * self.quantity
    
    def __repr__(self):
        return f'<OrderItem {self.product_name}>'
