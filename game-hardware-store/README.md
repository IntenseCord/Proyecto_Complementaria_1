# GameTech Store 🕹️

Una tienda web completa de juegos y hardware gaming desarrollada con Flask usando el patrón Modelo-Vista-Controlador (MVC).

## ✨ Características Principales

- **🕹️ Catálogo de Juegos**: Explora una amplia selección de juegos con detalles completos y requisitos del sistema
- **💻 Tienda de Hardware**: Componentes gaming de alta calidad (CPU, GPU, RAM, Motherboards)
- **🔍 Verificador de Compatibilidad**: Sistema inteligente que verifica si los juegos funcionan con tu hardware
- **🛠️ Configurador de PC**: Herramienta interactiva para construir tu PC gaming ideal
- **📱 Diseño Responsivo**: Interfaz moderna y atractiva que funciona en todos los dispositivos
- **🛒 Carrito de Compras**: Sistema completo de compras (simulado)
- **🔎 Búsqueda Avanzada**: Encuentra productos rápidamente con nuestro motor de búsqueda

## 🚀 Instalación y Configuración

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clona o descarga el proyecto**:
   ```bash
   git clone <url-del-repositorio>
   cd game-hardware-store
   ```

2. **Crea un entorno virtual** (recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta la aplicación**:
   ```bash
   python app.py
   ```

5. **Abre tu navegador** y ve a `http://localhost:5000`

## 📁 Estructura del Proyecto

```
game-hardware-store/
│
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias de Python
├── README.md             # Este archivo
│
├── models/               # Capa de Modelo (MVC)
│   ├── __init__.py
│   ├── game.py          # Modelo de juegos
│   ├── hardware.py      # Modelo de componentes de hardware
│   └── compatibility.py # Modelo de compatibilidad
│
├── controllers/          # Capa de Controlador (MVC)
│   ├── __init__.py
│   ├── store.py         # Controlador de la tienda
│   └── hardware.py      # Controlador de hardware
│
├── templates/           # Plantillas HTML (Vista MVC)
│   ├── base.html       # Template base
│   ├── index.html      # Página principal
│   ├── store.html      # Página de tienda
│   ├── game_detail.html # Detalle de juego
│   ├── hardware.html   # Lista de hardware
│   ├── hardware_detail.html # Detalle de hardware
│   ├── pc_builder.html # Configurador de PC
│   ├── search.html     # Página de búsqueda
│   ├── about.html      # Página "Acerca de"
│   └── 404.html        # Página de error 404
│
└── static/             # Archivos estáticos
    ├── css/
    │   └── style.css   # Estilos personalizados
    ├── js/
    │   └── main.js     # JavaScript principal
    └── images/         # Imágenes de productos
```

## 🎮 Uso de la Aplicación

### Explorar la Tienda

1. **Página Principal** (`/`): Vista general con productos destacados
2. **Tienda** (`/tienda`): Catálogo completo de juegos y hardware
3. **Hardware** (`/hardware`): Sección dedicada a componentes gaming

### Verificador de Compatibilidad

1. Ve a la página de **Tienda** (`/tienda`)
2. Selecciona las especificaciones de tu hardware en el verificador
3. Haz clic en **"Buscar Juegos"** para ver juegos compatibles

### Configurador de PC

1. Ve al **Configurador de PC** (`/configurador-pc`)
2. Selecciona tu presupuesto y uso principal
3. Elige componentes manualmente o usa **"Auto-recomendar"**
4. Revisa las recomendaciones automáticas
5. Finaliza tu configuración

### Búsqueda

- Usa la barra de búsqueda en el navbar
- Prueba términos como "Cyberpunk 2077", "RTX 4060", "Intel Core i5"
- Los resultados incluyen tanto juegos como hardware

## 🔧 Características Técnicas

### Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Framework CSS**: Bootstrap 5.1.3
- **Iconos**: Font Awesome 6.0.0
- **Patrón Arquitectural**: MVC (Modelo-Vista-Controlador)

### Modelo de Datos

- **Game**: Información completa de juegos (nombre, descripción, precio, requisitos, etc.)
- **Hardware**: Componentes de PC (CPU, GPU, RAM, Motherboards)
- **Compatibility**: Sistema de verificación de compatibilidad

### Sistema de Compatibilidad

El algoritmo de compatibilidad considera:
- Especificaciones técnicas mínimas y recomendadas
- Comparación de componentes (CPU, GPU, RAM)
- Recomendaciones basadas en presupuesto y uso

## 🚀 Despliegue en Producción

### Opción 1: Heroku

1. Crea una cuenta en [Heroku](https://heroku.com)
2. Instala la CLI de Heroku
3. Despliega la aplicación:
   ```bash
   heroku create nombre-de-tu-app
   git push heroku main
   ```

### Opción 2: Railway

1. Crea una cuenta en [Railway](https://railway.app)
2. Conecta tu repositorio de GitHub
3. Railway detectará automáticamente que es una aplicación Python

### Variables de Entorno (Producción)

```bash
FLASK_ENV=production
SECRET_KEY=tu_clave_secreta_muy_segura
```

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Funcionalidades Planificadas

- [ ] Sistema de autenticación de usuarios
- [ ] Base de datos real (PostgreSQL/MongoDB)
- [ ] Procesamiento de pagos integrado
- [ ] Sistema de reseñas y calificaciones
- [ ] API REST completa
- [ ] Aplicación móvil (React Native)
- [ ] Integración con plataformas de gaming (Steam, Epic Games)

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 🙏 Agradecimientos

- **Flask**: Framework web increíblemente flexible
- **Bootstrap**: Framework CSS que hace que todo se vea genial
- **Font Awesome**: Iconos hermosos y consistentes
- **Comunidad de desarrolladores**: Por el apoyo y las mejores prácticas

## 📞 Contacto

¿Tienes preguntas o sugerencias? ¡Nos encantaría saber de ti!

- **Email**: info@gametechstore.com
- **GitHub Issues**: [Reportar un problema](https://github.com/tuusuario/game-hardware-store/issues)
- **Twitter**: [@GameTechStore](https://twitter.com/GameTechStore)

---

**¡Gracias por usar GameTech Store! 🎮✨**

*Construido con ❤️ por desarrolladores apasionados por el gaming*
