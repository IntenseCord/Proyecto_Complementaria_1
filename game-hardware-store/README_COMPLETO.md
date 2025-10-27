# GameTech Store 🕹️

Una tienda web completa de juegos y hardware gaming desarrollada con Flask usando el patrón Modelo-Vista-Controlador (MVC).

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📑 Tabla de Contenidos

- [Características](#-características-principales)
- [Instalación](#-instalación-rápida)
- [Uso](#-uso-de-la-aplicación)
- [Docker](#-despliegue-con-docker)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías](#-tecnologías-utilizadas)
- [Solución de Problemas](#-solución-de-problemas)
- [Seguridad](#-seguridad-y-mejores-prácticas)
- [Contribuir](#-contribuir)

---

## ✨ Características Principales

### 🛍️ Funcionalidades de la Tienda
- **Catálogo de Juegos**: Explora juegos con detalles completos y requisitos del sistema
- **Tienda de Hardware**: Componentes gaming (CPU, GPU, RAM, Placas Base)
- **Carrito de Compras**: Sistema completo de compras con checkout
- **Gestión de Órdenes**: Historial de compras y seguimiento

### 🔐 Sistema de Usuarios
- **Autenticación Completa**: Registro, login, logout con protección CSRF
- **Perfiles de Usuario**: Gestión de información personal
- **Panel de Administración**: CRUD completo para juegos y hardware
- **Roles y Permisos**: Sistema de administradores

### 🛠️ Herramientas Avanzadas
- **Verificador de Compatibilidad**: Verifica si los juegos funcionan con tu hardware
- **Configurador de PC**: Construye tu PC gaming ideal con recomendaciones
- **Búsqueda Inteligente**: Motor de búsqueda para productos

### 🎨 Diseño y UX
- **Diseño Responsivo**: Funciona en todos los dispositivos
- **Interfaz Moderna**: UI/UX intuitiva con Bootstrap 5
- **Animaciones Suaves**: Transiciones y efectos visuales

---

## 🚀 Instalación Rápida

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clona el proyecto**:
```bash
git clone <url-del-repositorio>
cd game-hardware-store
```

2. **Crea un entorno virtual**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Instala las dependencias**:
```bash
pip install -r requirements.txt
```

4. **Configura las variables de entorno** (opcional):
```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Genera una SECRET_KEY segura
python -c "import secrets; print(secrets.token_hex(32))"

# Edita .env con tu SECRET_KEY
```

5. **Ejecuta la aplicación**:
```bash
python app.py
```

6. **Accede a la aplicación**:
```
http://localhost:5000
```

### 👤 Usuario Administrador por Defecto

- **Usuario:** `admin`
- **Contraseña:** `Admin123`
- **Email:** `admin@gametechstore.com`

⚠️ **IMPORTANTE:** Cambia estas credenciales en producción.

---

## 🎮 Uso de la Aplicación

### Explorar la Tienda
1. **Página Principal** (`/`): Vista general con productos destacados
2. **Tienda** (`/tienda`): Catálogo completo de juegos
3. **Hardware** (`/hardware`): Componentes gaming con filtros por categoría

### Verificador de Compatibilidad
1. Ve a la página de **Tienda** (`/tienda`)
2. Selecciona las especificaciones de tu hardware
3. Haz clic en **"Buscar Juegos"** para ver juegos compatibles

### Configurador de PC
1. Ve al **Configurador de PC** (`/configurador-pc`)
2. Selecciona tu presupuesto y uso principal
3. Elige componentes manualmente o usa **"Auto-recomendar"**
4. Finaliza tu configuración

### Panel de Administración
1. Inicia sesión como administrador
2. Accede a `/admin`
3. Gestiona juegos, hardware y usuarios

---

## 🐳 Despliegue con Docker

### Opción 1: Docker Compose (Recomendado)

```bash
# Construir y ejecutar
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

### Opción 2: Docker solo

```bash
# Construir imagen
docker build -t gametech-store .

# Ejecutar contenedor
docker run -d \
  --name gametech-store \
  -p 5000:5000 \
  -e SECRET_KEY=tu-clave-secreta \
  gametech-store
```

### Usar PostgreSQL con Docker

1. Descomenta la sección `db` en `docker-compose.yml`
2. Actualiza `DATABASE_URL` en `.env`:
```bash
DATABASE_URL=postgresql://gametech:gametech_password@db:5432/gametech_store
```
3. Ejecuta: `docker-compose up -d --build`

---

## 📁 Estructura del Proyecto

```
game-hardware-store/
│
├── app.py                      # Aplicación principal Flask
├── database.py                 # Configuración de base de datos
├── requirements.txt            # Dependencias de Python
├── Dockerfile                  # Configuración de Docker
├── docker-compose.yml          # Orquestación de contenedores
├── .env.example                # Ejemplo de variables de entorno
│
├── models/                     # Capa de Modelo (MVC)
│   ├── database_models.py      # Modelos SQLAlchemy
│   ├── hardware.py             # Modelo de hardware
│   └── compatibility.py        # Sistema de compatibilidad
│
├── controllers/                # Capa de Controlador (MVC)
│   ├── store.py                # Controlador de tienda
│   ├── hardware.py             # Controlador de hardware
│   ├── auth.py                 # Controlador de autenticación
│   ├── cart.py                 # Controlador de carrito
│   └── admin.py                # Controlador de administración
│
├── templates/                  # Plantillas HTML (Vista MVC)
│   ├── base.html               # Template base
│   ├── index.html              # Página principal
│   ├── store.html              # Tienda de juegos
│   ├── hardware.html           # Tienda de hardware
│   ├── pc_builder.html         # Configurador de PC
│   ├── auth/                   # Templates de autenticación
│   ├── cart/                   # Templates de carrito
│   └── admin/                  # Templates de administración
│
├── static/                     # Archivos estáticos
│   ├── css/
│   │   └── style.css           # Estilos personalizados
│   ├── js/
│   │   └── main.js             # JavaScript principal
│   └── uploads/                # Imágenes subidas
│
├── instance/                   # Base de datos SQLite
│   └── gametech_store.db
│
└── logs/                       # Logs de la aplicación
    └── gametech_store.log
```

---

## 🔧 Tecnologías Utilizadas

### Backend
- **Flask 2.3.3**: Framework web
- **SQLAlchemy 2.0.21**: ORM para base de datos
- **Flask-Login 0.6.3**: Sistema de autenticación
- **Flask-WTF 1.2.1**: Protección CSRF y validación de formularios
- **Werkzeug 2.3.7**: Utilidades WSGI y seguridad

### Frontend
- **Bootstrap 5.1.3**: Framework CSS
- **Font Awesome 6.0.0**: Iconos
- **JavaScript ES6+**: Interactividad

### Base de Datos
- **SQLite**: Desarrollo (por defecto)
- **PostgreSQL**: Producción (recomendado)

### Despliegue
- **Docker**: Containerización
- **Gunicorn**: Servidor WSGI para producción

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
# Cierra todas las instancias de la aplicación
# En Windows:
taskkill /F /IM python.exe

# Luego vuelve a ejecutar
python app.py
```

### Problema: Logout no funciona correctamente
**Solución:** Ya implementada. El logout ahora:
- Usa POST request con protección CSRF
- Limpia completamente la sesión
- Previene caché del navegador
- Ver `SOLUCION_LOGOUT.md` para más detalles

### Problema: Filtros de categoría no funcionan
**Solución:** Verificar que los tipos de productos en la base de datos coincidan con los filtros en el template.

---

## 🔐 Seguridad y Mejores Prácticas

### Implementadas ✅

1. **Protección CSRF**: Todos los formularios incluyen tokens CSRF
2. **Contraseñas Hasheadas**: Uso de Werkzeug para hash seguro
3. **Validación de Formularios**: Flask-WTF valida todos los inputs
4. **Sesiones Seguras**: Cookies HttpOnly y SameSite
5. **Logout Seguro**: POST request con token CSRF
6. **Prevención de Caché**: Headers para páginas protegidas
7. **Sanitización de Inputs**: Validación en backend

### Recomendaciones para Producción

1. **SECRET_KEY**: Genera una clave segura y única
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

2. **Base de Datos**: Usa PostgreSQL en lugar de SQLite
```bash
DATABASE_URL=postgresql://usuario:password@localhost/gametech_store
```

3. **HTTPS**: Siempre usa HTTPS en producción
```python
app.config['SESSION_COOKIE_SECURE'] = True
```

4. **Variables de Entorno**: Nunca subas `.env` al repositorio
```bash
# Agregar a .gitignore
.env
```

5. **Límite de Intentos**: Implementa rate limiting para login

---

## 🚀 Despliegue en Producción

### Heroku

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

### Railway

1. Conecta tu repositorio de GitHub
2. Railway detectará automáticamente Flask
3. Configura las variables de entorno
4. Despliega

### Render

1. Conecta tu repositorio
2. Selecciona "Web Service"
3. Configura:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Agrega variables de entorno
5. Despliega

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

### Guías de Contribución

- Sigue el estilo de código existente
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación
- Asegúrate de que todos los tests pasen

---

## 📝 Funcionalidades Planificadas

- [ ] Sistema de reseñas y calificaciones
- [ ] Integración con pasarelas de pago reales
- [ ] API REST completa
- [ ] Aplicación móvil (React Native)
- [ ] Integración con Steam API
- [ ] Sistema de wishlist
- [ ] Notificaciones por email
- [ ] Chat de soporte en vivo

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

- **Flask**: Framework web increíblemente flexible
- **Bootstrap**: Framework CSS que hace que todo se vea genial
- **Font Awesome**: Iconos hermosos y consistentes
- **Comunidad de desarrolladores**: Por el apoyo y las mejores prácticas

---

## 📞 Contacto

¿Tienes preguntas o sugerencias? ¡Nos encantaría saber de ti!

- **Email**: info@gametechstore.com
- **GitHub Issues**: [Reportar un problema](https://github.com/tuusuario/game-hardware-store/issues)

---

## ✅ Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas
- [ ] Archivo `.env` configurado
- [ ] Aplicación ejecutándose
- [ ] Base de datos creada
- [ ] Acceso a `http://localhost:5000` exitoso
- [ ] Login con usuario admin funciona

---

**¡Gracias por usar GameTech Store! 🎮✨**

*Construido con ❤️ por desarrolladores apasionados por el gaming*
