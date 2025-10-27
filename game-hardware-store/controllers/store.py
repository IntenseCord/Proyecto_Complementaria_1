from flask import Blueprint, render_template, request, jsonify
from models.database_models import Game, Hardware
from models.compatibility import Compatibility

store_bp = Blueprint('store', __name__)

@store_bp.route('/tienda')
def tienda():
    """Página principal de la tienda"""
    juegos = Game.get_all_games()
    hardware = Hardware.get_all_hardware()
    return render_template('store.html', juegos=juegos, hardware=hardware)

@store_bp.route('/juego/<int:juego_id>')
def juego_detalle(juego_id):
    """Página de detalle de un juego específico"""
    juego = Game.get_game_by_id(juego_id)
    if not juego:
        return render_template('404.html'), 404

    # Obtener juegos relacionados (mismo género)
    juegos_relacionados = [j for j in Game.get_all_games() if j.genero == juego.genero and j.id != juego.id][:3]

    return render_template('game_detail.html', juego=juego, juegos_relacionados=juegos_relacionados)

@store_bp.route('/hardware/<int:hardware_id>')
def hardware_detalle(hardware_id):
    """Página de detalle de un componente de hardware"""
    componente = Hardware.get_hardware_by_id(hardware_id)
    if not componente:
        return render_template('404.html'), 404

    # Obtener hardware relacionado (mismo tipo)
    hardware_relacionado = [h for h in Hardware.get_all_hardware() if h.tipo == componente.tipo and h.id != componente.id][:3]

    return render_template('hardware_detail.html', componente=componente, hardware_relacionado=hardware_relacionado)

@store_bp.route('/consultar-compatibilidad', methods=['POST'])
def consultar_compatibilidad():
    """Consultar compatibilidad de juegos con hardware específico"""
    data = request.get_json()

    # Obtener especificaciones del hardware del usuario
    hardware_usuario = {
        'cpu': data.get('cpu', ''),
        'ram': data.get('ram', ''),
        'gpu': data.get('gpu', ''),
        'storage': data.get('storage', '')
    }

    # Obtener juegos compatibles
    juegos_compatibles = Game.get_games_by_hardware(hardware_usuario)

    # Crear lista de juegos para enviar al frontend
    juegos_data = [juego.to_dict() for juego in juegos_compatibles]

    return jsonify({
        'success': True,
        'juegos': juegos_data,
        'total': len(juegos_data)
    })

@store_bp.route('/verificar-setup-completo', methods=['POST'])
def verificar_setup_completo():
    """Verificar compatibilidad de un setup completo con juegos seleccionados"""
    data = request.get_json()

    juegos_seleccionados_ids = data.get('juegos', [])
    componentes_seleccionados_ids = data.get('componentes', [])

    # Obtener objetos de juegos y componentes
    juegos = [Game.get_game_by_id(jid) for jid in juegos_seleccionados_ids if Game.get_game_by_id(jid)]
    componentes = [Hardware.get_hardware_by_id(cid) for cid in componentes_seleccionados_ids if Hardware.get_hardware_by_id(cid)]

    # Verificar compatibilidad
    resultado = Compatibility.verificar_compatibility_completa(juegos, componentes)

    # Calcular precio total
    precio_total = sum(componente.precio for componente in componentes) + sum(juego.precio for juego in juegos)

    return jsonify({
        'success': True,
        'compatible': resultado['compatible'],
        'detalles': resultado['detalles'],
        'precio_total': precio_total,
        'componentes_count': len(componentes),
        'juegos_count': len(juegos)
    })

@store_bp.route('/buscar')
def buscar():
    """Página de búsqueda de productos"""
    query = request.args.get('q', '')

    if not query:
        return render_template('search.html', resultados=[], query='')

    # Buscar en juegos usando el método de la base de datos
    juegos_resultados = Game.search_games(query)

    # Buscar en hardware
    hardware_resultados = Hardware.buscar_hardware(query)

    resultados = {
        'juegos': juegos_resultados,
        'hardware': hardware_resultados
    }

    return render_template('search.html', resultados=resultados, query=query)
