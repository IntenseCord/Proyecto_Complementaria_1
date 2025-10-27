# 🚀 Guía de Instalación - GameTech Store (Versión Mejorada)

## 📋 Requisitos Previos

- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)
- **Git** (opcional, para clonar el repositorio)

---

## 🔧 Instalación Paso a Paso

### 1. Descargar o Clonar el Proyecto

```bash
# Si tienes Git instalado:
git clone <url-del-repositorio>
cd game-hardware-store

# O simplemente descomprime el archivo ZIP en una carpeta
```

### 2. Crear un Entorno Virtual (Recomendado)

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**En macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará todas las dependencias necesarias:
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.5
- Flask-Login 0.6.3
- Flask-WTF 1.2.1
- Y más...

### 4. Configurar Variables de Entorno (Opcional)

Copia el archivo de ejemplo y edítalo:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edita el archivo `.env` con tus valores:
```bash
SECRET_KEY=tu_clave_secreta_muy_segura
DATABASE_URL=sqlite:///gametech_store.db
FLASK_ENV=development
```

**Nota:** Si no creas el archivo `.env`, la aplicación usará valores por defecto.

### 5. Ejecutar la Aplicación

```bash
python app.py
```

La primera vez que ejecutes la aplicación:
- ✅ Se creará automáticamente la base de datos SQLite
- ✅ Se poblarán los datos iniciales (juegos, hardware, usuario admin)
- ✅ Se creará el directorio de logs

Verás un mensaje similar a:
```
Base de datos poblada con éxito!
 * Running on http://0.0.0.0:5000
```

### 6. Acceder a la Aplicación

Abre tu navegador y ve a:
```
http://localhost:5000
```

---

## 👤 Usuario Administrador por Defecto

Para probar todas las funcionalidades, usa estas credenciales:

- **Usuario:** `admin`
- **Contraseña:** `admin123`
- **Email:** `admin@gametechstore.com`

**⚠️ IMPORTANTE:** Cambia estas credenciales en producción.

---

## 🗂️ Estructura de la Base de Datos

La base de datos se crea automáticamente en:
```
game-hardware-store/gametech_store.db
```

Contiene:
- **5 juegos** con requisitos y stock
- **8 componentes de hardware** con especificaciones
- **1 usuario admin** por defecto

---

## 🧪 Verificar la Instalación

### Prueba 1: Página Principal
1. Ve a `http://localhost:5000`
2. Deberías ver la página principal con productos destacados

### Prueba 2: Registro de Usuario
1. Click en "Registrarse"
2. Crea una cuenta nueva
3. Inicia sesión

### Prueba 3: Carrito de Compras
1. Inicia sesión
2. Ve a la tienda
3. Agrega productos al carrito
4. Ve al carrito y completa una compra

### Prueba 4: Verificador de Compatibilidad
1. Ve a la tienda
2. Usa el verificador de compatibilidad
3. Verifica que muestre juegos compatibles con tu hardware

---

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
```bash
# Asegúrate de tener el entorno virtual activado
pip install -r requirements.txt
```

### Error: "Address already in use"
```bash
# El puerto 5000 está ocupado. Cambia el puerto en app.py:
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Error: "Database is locked"
```bash
# Cierra todas las instancias de la aplicación y vuelve a ejecutar
```

### Error: "Template not found"
```bash
# Asegúrate de estar en el directorio correcto
cd game-hardware-store
python app.py
```

### La base de datos no se crea
```bash
# Elimina la base de datos existente y vuelve a ejecutar
# Windows:
del gametech_store.db

# macOS/Linux:
rm gametech_store.db

# Luego ejecuta de nuevo:
python app.py
```

---

## 📦 Dependencias Principales

| Paquete | Versión | Propósito |
|---------|---------|-----------|
| Flask | 2.3.3 | Framework web |
| Flask-SQLAlchemy | 3.0.5 | ORM para base de datos |
| Flask-Login | 0.6.3 | Sistema de autenticación |
| Flask-WTF | 1.2.1 | Validación de formularios |
| SQLAlchemy | 2.0.21 | Motor de base de datos |
| Werkzeug | 2.3.7 | Utilidades WSGI |

---

## 🚀 Despliegue en Producción

### Preparación para Producción

1. **Cambiar SECRET_KEY:**
```bash
# Genera una clave segura
python -c "import secrets; print(secrets.token_hex(32))"
```

2. **Configurar base de datos de producción:**
```bash
# En .env
DATABASE_URL=postgresql://usuario:password@localhost/gametech_store
```

3. **Desactivar modo debug:**
```bash
# En .env
FLASK_ENV=production
FLASK_DEBUG=0
```

4. **Usar servidor WSGI:**
```bash
# Gunicorn (incluido en requirements.txt)
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Despliegue en Heroku

```bash
# 1. Instalar Heroku CLI
# 2. Login
heroku login

# 3. Crear app
heroku create nombre-de-tu-app

# 4. Agregar PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# 5. Configurar variables
heroku config:set SECRET_KEY=tu_clave_secreta

# 6. Desplegar
git push heroku main
```

### Despliegue en Railway

1. Conecta tu repositorio de GitHub
2. Railway detectará automáticamente que es una app Flask
3. Configura las variables de entorno
4. Despliega

---

## 📚 Recursos Adicionales

- **Documentación de Flask:** https://flask.palletsprojects.com/
- **SQLAlchemy:** https://www.sqlalchemy.org/
- **Flask-Login:** https://flask-login.readthedocs.io/
- **Bootstrap 5:** https://getbootstrap.com/

---

## 🆘 Soporte

Si encuentras problemas:

1. Revisa la sección de **Solución de Problemas**
2. Verifica los logs en `logs/gametech_store.log`
3. Asegúrate de tener todas las dependencias instaladas
4. Verifica que Python 3.8+ esté instalado

---

## ✅ Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` configurado (opcional)
- [ ] Aplicación ejecutándose (`python app.py`)
- [ ] Base de datos creada automáticamente
- [ ] Acceso a `http://localhost:5000` exitoso
- [ ] Login con usuario admin funciona
- [ ] Carrito de compras funciona

---

## 🎉 ¡Listo!

Tu instalación de GameTech Store está completa. Ahora puedes:

- ✅ Explorar la tienda
- ✅ Crear usuarios
- ✅ Agregar productos al carrito
- ✅ Realizar compras
- ✅ Verificar compatibilidad de hardware
- ✅ Configurar PCs personalizadas

**¡Disfruta de GameTech Store!** 🎮✨
