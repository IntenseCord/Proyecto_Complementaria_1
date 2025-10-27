// JavaScript principal para GameTech Store

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades comunes
    initializeCommonFeatures();

    // Inicializar funcionalidades específicas según la página
    const currentPath = window.location.pathname;
    if (currentPath === '/' || currentPath === '/index') {
        initializeHomePage();
    } else if (currentPath.startsWith('/tienda')) {
        initializeStorePage();
    } else if (currentPath.startsWith('/juego/')) {
        initializeGameDetailPage();
    }
});

/**
 * Inicializar funcionalidades comunes a todas las páginas
 */
function initializeCommonFeatures() {
    // Navbar activa
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');

    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPath || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });

    // Tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Smooth scroll para enlaces internos
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Inicializar funcionalidades de la página principal
 */
function initializeHomePage() {
    // Animación de fade-in para las tarjetas de características
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
            }
        });
    }, observerOptions);

    document.querySelectorAll('.feature-card').forEach(card => {
        observer.observe(card);
    });

    // Auto-rotación de productos destacados (opcional)
    rotateFeaturedProducts();
}

/**
 * Inicializar funcionalidades de la página de tienda
 */
function initializeStorePage() {
    // Los filtros ya están manejados en el template store.html

    // Inicializar carrito de compras (simulado)
    initializeShoppingCart();

    // Inicializar comparación de productos
    initializeProductComparison();
}

/**
 * Inicializar funcionalidades de la página de detalle de juego
 */
function initializeGameDetailPage() {
    // Verificador de compatibilidad ya manejado en game_detail.html

    // Inicializar galería de imágenes (si aplica)
    initializeImageGallery();

    // Inicializar reseñas (simulado)
    initializeReviews();
}

/**
 * Funcionalidad del carrito de compras (simulada)
 */
function initializeShoppingCart() {
    let cart = JSON.parse(localStorage.getItem('gametech_cart')) || [];

    // Actualizar contador del carrito
    updateCartCounter();

    // Manejar clics en botones "Agregar al carrito"
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('add-to-cart-btn') || e.target.closest('.add-to-cart-btn')) {
            const button = e.target.classList.contains('add-to-cart-btn') ? e.target : e.target.closest('.add-to-cart-btn');
            const productId = button.getAttribute('data-juego-id') || button.getAttribute('data-hardware-id');
            const productType = button.getAttribute('data-juego-id') ? 'game' : 'hardware';

            addToCart(productId, productType);
        }
    });

    function addToCart(productId, productType) {
        // Buscar el producto
        let product = null;
        if (productType === 'game') {
            // Buscar en juegos (simulado)
            product = getGameById(productId);
        } else {
            // Buscar en hardware (simulado)
            product = getHardwareById(productId);
        }

        if (product) {
            cart.push({
                id: productId,
                type: productType,
                name: product.nombre || product.modelo,
                price: product.precio,
                image: product.imagen
            });

            localStorage.setItem('gametech_cart', JSON.stringify(cart));
            updateCartCounter();
            showToast(`${product.nombre || product.modelo} agregado al carrito`, 'success');
        }
    }

    function updateCartCounter() {
        const cartCounter = document.querySelector('.cart-counter');
        if (cartCounter) {
            cartCounter.textContent = cart.length;
            cartCounter.style.display = cart.length > 0 ? 'inline' : 'none';
        }
    }

    function showToast(message, type) {
        const toast = document.createElement('div');
        toast.className = `toast align-items-center text-white bg-${type} border-0`;
        toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;

        document.body.appendChild(toast);
        const bsToast = new bootstrap.Toast(toast);
        bsToast.show();

        setTimeout(() => {
            if (document.body.contains(toast)) {
                document.body.removeChild(toast);
            }
        }, 3000);
    }
}

/**
 * Funcionalidad de comparación de productos
 */
function initializeProductComparison() {
    const compareButtons = document.querySelectorAll('.compare-btn');

    compareButtons.forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            const productType = this.getAttribute('data-product-type');

            // Lógica de comparación (simulada)
            showToast('Producto agregado para comparación', 'info');
        });
    });
}

/**
 * Galería de imágenes (simulada)
 */
function initializeImageGallery() {
    const galleryImages = document.querySelectorAll('.gallery-image');
    const mainImage = document.querySelector('.main-image');

    if (galleryImages.length > 0 && mainImage) {
        galleryImages.forEach(img => {
            img.addEventListener('click', function() {
                mainImage.src = this.src;
                galleryImages.forEach(i => i.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }
}

/**
 * Sistema de reseñas (simulado)
 */
function initializeReviews() {
    const reviewForm = document.querySelector('.review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', function(e) {
            e.preventDefault();
            showToast('Reseña enviada correctamente', 'success');
            this.reset();
        });
    }
}

/**
 * Funciones auxiliares (simuladas)
 */
function getGameById(id) {
    // Simulación - en producción vendría de una API
    const games = [
        { id: 1, nombre: 'Cyberpunk 2077', precio: 59.99, imagen: '/static/images/cyberpunk.jpg' },
        { id: 2, nombre: 'The Witcher 3', precio: 39.99, imagen: '/static/images/witcher3.jpg' }
    ];
    return games.find(game => game.id == id);
}

function getHardwareById(id) {
    // Simulación - en producción vendría de una API
    const hardware = [
        { id: 1, modelo: 'RTX 4060', precio: 399.99, imagen: '/static/images/rtx4060.jpg' },
        { id: 2, modelo: 'Intel Core i5-12400F', precio: 199.99, imagen: '/static/images/i5-12400f.jpg' }
    ];
    return hardware.find(item => item.id == id);
}

/**
 * Rotación automática de productos destacados
 */
function rotateFeaturedProducts() {
    const featuredProducts = document.querySelectorAll('.featured-product');
    let currentIndex = 0;

    if (featuredProducts.length <= 1) return;

    setInterval(() => {
        featuredProducts.forEach((product, index) => {
            product.style.display = index === currentIndex ? 'block' : 'none';
        });

        currentIndex = (currentIndex + 1) % featuredProducts.length;
    }, 5000);
}

/**
 * Utilidades generales
 */
const GameTechUtils = {
    // Formatear precio
    formatPrice: function(price) {
        return new Intl.NumberFormat('es-ES', {
            style: 'currency',
            currency: 'USD'
        }).format(price);
    },

    // Validar email
    isValidEmail: function(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    },

    // Debounce para búsquedas
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// Hacer las utilidades disponibles globalmente
window.GameTechUtils = GameTechUtils;
