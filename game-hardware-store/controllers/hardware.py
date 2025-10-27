from flask import Blueprint, render_template, request, jsonify
from models.database_models import Hardware, Game

hardware_bp = Blueprint('hardware', __name__)

@hardware_bp.route('/hardware')
def lista_hardware():
    """Página que muestra todo el hardware disponible"""
    hardware = Hardware.get_all_hardware()

    # Organizar por categorías
    categorias = {}
    for componente in hardware:
        if componente.tipo not in categorias:
            categorias[componente.tipo] = []
        categorias[componente.tipo].append(componente)

    return render_template('hardware.html', categorias=categorias, hardware=hardware)

@hardware_bp.route('/hardware/categoria/<categoria>')
def hardware_por_categoria(categoria):
    """Página que muestra hardware por categoría específica"""
    componentes = Hardware.get_hardware_by_tipo(categoria)

    if not componentes:
        return render_template('404.html'), 404

    return render_template('hardware_category.html', componentes=componentes, categoria=categoria)

@hardware_bp.route('/configurador-pc')
def configurador_pc():
    """Página del configurador de PC interactivo"""
    hardware = Hardware.get_all_hardware()

    # Organizar por categorías para el configurador
    categorias = {
        'CPU': [h for h in hardware if h.tipo == 'CPU'],
        'GPU': [h for h in hardware if h.tipo == 'GPU'],
        'RAM': [h for h in hardware if h.tipo == 'RAM'],
        'Placa Madre': [h for h in hardware if h.tipo == 'Placa Madre']
    }

    return render_template('pc_builder.html', categorias=categorias)

@hardware_bp.route('/api/hardware/tipos')
def api_tipos_hardware():
    """API para obtener tipos de hardware disponibles"""
    hardware = Hardware.get_all_hardware()
    tipos = list(set(componente.tipo for componente in hardware))

    return jsonify({'tipos': sorted(tipos)})

@hardware_bp.route('/api/hardware/buscar')
def api_buscar_hardware():
    """API para buscar hardware"""
    query = request.args.get('q', '')
    tipo = request.args.get('tipo', '')
    
    # Si se especifica un tipo, buscar por tipo
    if tipo:
        resultados = Hardware.get_hardware_by_tipo(tipo)
    else:
        resultados = Hardware.buscar_hardware(query)

    hardware_data = []
    for componente in resultados:
        hardware_data.append({
            'id': componente.id,
            'tipo': componente.tipo,
            'marca': componente.marca,
            'modelo': componente.modelo,
            'precio': componente.precio,
            'descripcion': componente.descripcion,
            'imagen': componente.imagen,
            'socket': componente.socket if hasattr(componente, 'socket') else None,
            'especificaciones': componente.especificaciones if hasattr(componente, 'especificaciones') else {}
        })

    return jsonify({'resultados': hardware_data})

@hardware_bp.route('/comparar-hardware', methods=['POST'])
def comparar_hardware():
    """Comparar componentes de hardware seleccionados"""
    data = request.get_json()
    componentes_ids = data.get('componentes', [])

    componentes = []
    for cid in componentes_ids:
        componente = Hardware.get_hardware_by_id(cid)
        if componente:
            componentes.append(componente)

    if not componentes:
        return jsonify({'error': 'No se encontraron componentes para comparar'}), 400

    # Crear tabla de comparación
    comparacion = {
        'componentes': [],
        'caracteristicas': {}
    }

    caracteristicas_comunes = set()
    for componente in componentes:
        comp_data = {
            'id': componente.id,
            'tipo': componente.tipo,
            'marca': componente.marca,
            'modelo': componente.modelo,
            'precio': componente.precio,
            'imagen': componente.imagen
        }
        comparacion['componentes'].append(comp_data)

        # Agregar especificaciones
        caracteristicas_comunes.update(componente.get_especificaciones().keys())

    caracteristicas_comunes = sorted(list(caracteristicas_comunes))

    # Crear matriz de comparación
    for caracteristica in caracteristicas_comunes:
        comparacion['caracteristicas'][caracteristica] = {}
        for componente in componentes:
            valor = componente.get_especificaciones().get(caracteristica, 'N/A')
            comparacion['caracteristicas'][caracteristica][componente.id] = valor

    return jsonify(comparacion)
