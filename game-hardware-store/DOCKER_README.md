# 🐳 Guía de Docker para GameTech Store

Esta guía te ayudará a ejecutar la aplicación GameTech Store usando Docker.

## 📋 Requisitos Previos

- Docker instalado en tu sistema ([Descargar Docker](https://www.docker.com/get-started))
- Docker Compose (viene incluido con Docker Desktop)

## 🚀 Opción 1: Ejecutar con Docker Compose (Recomendado)

### Paso 1: Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```bash
SECRET_KEY=tu-clave-secreta-super-segura-aqui
DATABASE_URL=sqlite:///instance/gametech_store.db
FLASK_ENV=production
```

### Paso 2: Construir y ejecutar

```bash
# Construir y ejecutar en segundo plano
docker-compose up -d --build

# Ver los logs
docker-compose logs -f

# Detener los contenedores
docker-compose down
```

### Paso 3: Acceder a la aplicación

Abre tu navegador en: `http://localhost:5000`

## 🔧 Opción 2: Ejecutar solo con Docker

### Construir la imagen

```bash
docker build -t gametech-store .
```

### Ejecutar el contenedor

```bash
docker run -d \
  --name gametech-store \
  -p 5000:5000 \
  -e SECRET_KEY=tu-clave-secreta \
  -v $(pwd)/instance:/app/instance \
  gametech-store
```

## 🗄️ Usar PostgreSQL (Opcional)

Si prefieres usar PostgreSQL en lugar de SQLite:

1. Descomenta la sección `db` en `docker-compose.yml`
2. Actualiza la variable `DATABASE_URL` en tu archivo `.env`:

```bash
DATABASE_URL=postgresql://gametech:gametech_password@db:5432/gametech_store
```

3. Ejecuta:

```bash
docker-compose up -d --build
```

## 📊 Inicializar la Base de Datos

### Crear las tablas

```bash
# Acceder al contenedor
docker exec -it gametech-store bash

# Dentro del contenedor, ejecutar Python
python

# En el intérprete de Python
from app import app
from database import db
with app.app_context():
    db.create_all()
exit()
```

### Actualizar el stock

```bash
# Desde dentro del contenedor
python update_stock.py
```

O desde fuera:

```bash
docker exec -it gametech-store python update_stock.py
```

## 🔍 Comandos Útiles

### Ver logs en tiempo real
```bash
docker-compose logs -f web
```

### Reiniciar la aplicación
```bash
docker-compose restart web
```

### Acceder al contenedor
```bash
docker exec -it gametech-store bash
```

### Limpiar todo (contenedores, imágenes, volúmenes)
```bash
docker-compose down -v
docker system prune -a
```

## 📦 Desplegar en Producción

### Docker Hub

1. **Construir la imagen:**
```bash
docker build -t tu-usuario/gametech-store:latest .
```

2. **Subir a Docker Hub:**
```bash
docker login
docker push tu-usuario/gametech-store:latest
```

3. **En el servidor de producción:**
```bash
docker pull tu-usuario/gametech-store:latest
docker run -d -p 80:5000 --name gametech-store tu-usuario/gametech-store:latest
```

### Render, Railway, o servicios similares

Estos servicios detectan automáticamente el `Dockerfile` y construyen la imagen.

Solo necesitas:
1. Conectar tu repositorio de GitHub
2. Configurar las variables de entorno
3. Desplegar

## 🔐 Seguridad

**IMPORTANTE:** Antes de desplegar en producción:

1. Cambia el `SECRET_KEY` por uno generado aleatoriamente
2. Usa PostgreSQL en lugar de SQLite
3. Configura HTTPS
4. Revisa las configuraciones de seguridad en `app.py`

## 🐛 Solución de Problemas

### El contenedor no inicia
```bash
docker-compose logs web
```

### Error de permisos con SQLite
```bash
docker-compose down
sudo chown -R $USER:$USER instance/
docker-compose up -d
```

### Limpiar y empezar de nuevo
```bash
docker-compose down -v
docker-compose up -d --build
```

## 📝 Notas

- Los datos de SQLite se guardan en `./instance` (persistente)
- Los archivos estáticos están en `./static` (persistente)
- La aplicación se ejecuta con Gunicorn (4 workers) en producción
- El puerto por defecto es 5000 (puedes cambiarlo en `docker-compose.yml`)
