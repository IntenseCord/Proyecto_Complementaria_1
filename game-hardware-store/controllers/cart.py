"""
Controlador del carrito de compras
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import login_required, current_user
from database import db
from models.database_models import CartItem, Game, Hardware, Order, OrderItem
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from datetime import datetime

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/carrito')
@login_required
def ver_carrito():
    """Ver el carrito de compras"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    # Calcular total
    total = sum(item.get_subtotal() for item in cart_items)
    
    return render_template('cart/carrito.html', cart_items=cart_items, total=total)

@cart_bp.route('/carrito/agregar', methods=['POST'])
@login_required
def agregar_al_carrito():
    """Agregar producto al carrito"""
    data = request.get_json() if request.is_json else request.form
    
    product_type = data.get('product_type')
    product_id = int(data.get('product_id'))
    quantity = int(data.get('quantity', 1))
    
    if product_type not in ['game', 'hardware']:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Tipo de producto inválido'}), 400
        flash('Tipo de producto inválido', 'danger')
        return redirect(request.referrer or url_for('index'))
    
    # Verificar que el producto existe
    if product_type == 'game':
        product = Game.query.get(product_id)
    else:
        product = Hardware.query.get(product_id)
    
    if not product:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Producto no encontrado'}), 404
        flash('Producto no encontrado', 'danger')
        return redirect(request.referrer or url_for('index'))
    
    # Verificar stock
    if product.stock < quantity:
        if request.is_json:
            return jsonify({'success': False, 'message': 'Stock insuficiente'}), 400
        flash('Stock insuficiente', 'danger')
        return redirect(request.referrer or url_for('index'))
    
    # Verificar si ya existe en el carrito
    existing_item = CartItem.query.filter_by(
        user_id=current_user.id,
        product_type=product_type,
        product_id=product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += quantity
        message = 'Cantidad actualizada en el carrito'
    else:
        cart_item = CartItem(
            user_id=current_user.id,
            product_type=product_type,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
        message = 'Producto agregado al carrito'
    
    db.session.commit()
    
    if request.is_json:
        return jsonify({
            'success': True,
            'message': message,
            'cart_count': CartItem.query.filter_by(user_id=current_user.id).count()
        })
    
    flash(message, 'success')
    return redirect(request.referrer or url_for('index'))

@cart_bp.route('/carrito/actualizar/<int:item_id>', methods=['POST'])
@login_required
def actualizar_cantidad(item_id):
    """Actualizar cantidad de un item en el carrito"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Verificar que el item pertenece al usuario
    if cart_item.user_id != current_user.id:
        flash('No tienes permiso para modificar este item', 'danger')
        return redirect(url_for('cart.ver_carrito'))
    
    quantity = int(request.form.get('quantity', 1))
    
    if quantity <= 0:
        db.session.delete(cart_item)
        flash('Producto eliminado del carrito', 'info')
    else:
        # Verificar stock
        product = cart_item.get_product()
        if product and product.stock >= quantity:
            cart_item.quantity = quantity
            flash('Cantidad actualizada', 'success')
        else:
            flash('Stock insuficiente', 'danger')
    
    db.session.commit()
    return redirect(url_for('cart.ver_carrito'))

@cart_bp.route('/carrito/eliminar/<int:item_id>', methods=['POST'])
@login_required
def eliminar_del_carrito(item_id):
    """Eliminar un item del carrito"""
    cart_item = CartItem.query.get_or_404(item_id)
    
    # Verificar que el item pertenece al usuario
    if cart_item.user_id != current_user.id:
        if request.is_json:
            return jsonify({'success': False, 'message': 'No autorizado'}), 403
        flash('No tienes permiso para eliminar este item', 'danger')
        return redirect(url_for('cart.ver_carrito'))
    
    db.session.delete(cart_item)
    db.session.commit()
    
    if request.is_json:
        return jsonify({
            'success': True,
            'message': 'Producto eliminado del carrito',
            'cart_count': CartItem.query.filter_by(user_id=current_user.id).count()
        })
    
    flash('Producto eliminado del carrito', 'success')
    return redirect(url_for('cart.ver_carrito'))

@cart_bp.route('/carrito/vaciar', methods=['POST'])
@login_required
def vaciar_carrito():
    """Vaciar todo el carrito"""
    CartItem.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    
    flash('Carrito vaciado', 'info')
    return redirect(url_for('cart.ver_carrito'))

@cart_bp.route('/carrito/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Proceso de checkout"""
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    
    if not cart_items:
        flash('Tu carrito está vacío', 'warning')
        return redirect(url_for('cart.ver_carrito'))
    
    if request.method == 'POST':
        # Calcular total
        total = sum(item.get_subtotal() for item in cart_items)
        
        # Crear orden
        order = Order(
            user_id=current_user.id,
            total=total,
            status='completed'
        )
        db.session.add(order)
        db.session.flush()  # Para obtener el ID de la orden
        
        # Crear items de la orden y actualizar stock
        for cart_item in cart_items:
            product = cart_item.get_product()
            
            if not product or product.stock < cart_item.quantity:
                db.session.rollback()
                flash(f'Stock insuficiente para {product.nombre if hasattr(product, "nombre") else product.modelo}', 'danger')
                return redirect(url_for('cart.ver_carrito'))
            
            # Crear item de orden
            order_item = OrderItem(
                order_id=order.id,
                product_type=cart_item.product_type,
                product_id=cart_item.product_id,
                product_name=product.nombre if hasattr(product, 'nombre') else f"{product.marca} {product.modelo}",
                quantity=cart_item.quantity,
                price=product.precio
            )
            db.session.add(order_item)
            
            # Actualizar stock
            product.stock -= cart_item.quantity
        
        # Vaciar carrito
        CartItem.query.filter_by(user_id=current_user.id).delete()
        
        db.session.commit()
        
        flash(f'¡Compra realizada con éxito! Orden #{order.id}', 'success')
        return redirect(url_for('cart.orden_confirmada', order_id=order.id))
    
    # Calcular total para mostrar
    total = sum(item.get_subtotal() for item in cart_items)
    
    return render_template('cart/checkout.html', cart_items=cart_items, total=total)

@cart_bp.route('/orden/<int:order_id>')
@login_required
def orden_confirmada(order_id):
    """Página de confirmación de orden"""
    order = Order.query.get_or_404(order_id)
    
    # Verificar que la orden pertenece al usuario
    if order.user_id != current_user.id:
        flash('No tienes permiso para ver esta orden', 'danger')
        return redirect(url_for('index'))
    
    return render_template('cart/orden_confirmada.html', order=order)

@cart_bp.route('/mis-ordenes')
@login_required
def mis_ordenes():
    """Ver historial de órdenes del usuario"""
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('cart/mis_ordenes.html', orders=orders)

@cart_bp.route('/api/carrito/count')
@login_required
def cart_count():
    """API para obtener la cantidad de items en el carrito"""
    count = CartItem.query.filter_by(user_id=current_user.id).count()
    return jsonify({'count': count})

@cart_bp.route('/orden/<int:order_id>/pdf')
@login_required
def descargar_pdf(order_id):
    """Generar y descargar PDF de la orden"""
    order = Order.query.get_or_404(order_id)
    
    # Verificar que la orden pertenece al usuario
    if order.user_id != current_user.id:
        flash('No tienes permiso para descargar esta orden', 'danger')
        return redirect(url_for('index'))
    
    # Crear buffer para el PDF
    buffer = BytesIO()
    
    # Crear documento PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    # Estilos
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12
    )
    
    # Título
    elements.append(Paragraph("GameTech Store", title_style))
    elements.append(Paragraph("Factura de Compra", styles['Heading2']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Información de la orden
    order_info = [
        ['Número de Orden:', f'#{order.id}'],
        ['Fecha:', order.created_at.strftime('%d/%m/%Y %H:%M')],
        ['Cliente:', current_user.username],
        ['Email:', current_user.email],
        ['Estado:', order.status.upper()]
    ]
    
    order_table = Table(order_info, colWidths=[2*inch, 4*inch])
    order_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    elements.append(order_table)
    elements.append(Spacer(1, 0.4*inch))
    
    # Productos
    elements.append(Paragraph("Productos", heading_style))
    
    # Tabla de productos
    product_data = [['Producto', 'Cantidad', 'Precio Unit.', 'Subtotal']]
    
    for item in order.items:
        product_data.append([
            item.product_name,
            str(item.quantity),
            f'${item.price:.2f}',
            f'${item.get_subtotal():.2f}'
        ])
    
    # Calcular totales
    subtotal = order.total
    iva = subtotal * 0.19
    total = subtotal * 1.19
    
    # Agregar filas de totales
    product_data.append(['', '', 'Subtotal:', f'${subtotal:.2f}'])
    product_data.append(['', '', 'Envío:', 'GRATIS'])
    product_data.append(['', '', 'IVA (19%):', f'${iva:.2f}'])
    product_data.append(['', '', 'TOTAL:', f'${total:.2f}'])
    
    product_table = Table(product_data, colWidths=[3*inch, 1*inch, 1.5*inch, 1.5*inch])
    product_table.setStyle(TableStyle([
        # Header
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # Body
        ('TEXTCOLOR', (0, 1), (-1, -5), colors.black),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -5), 1, colors.grey),
        
        # Totales
        ('FONTNAME', (2, -4), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (2, -1), (-1, -1), colors.HexColor('#28a745')),
        ('TEXTCOLOR', (2, -1), (-1, -1), colors.whitesmoke),
        ('FONTSIZE', (2, -1), (-1, -1), 12),
    ]))
    
    elements.append(product_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Nota final
    note_style = ParagraphStyle(
        'Note',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    elements.append(Paragraph("Gracias por tu compra en GameTech Store", note_style))
    elements.append(Paragraph("Este documento es una factura válida", note_style))
    
    # Construir PDF
    doc.build(elements)
    
    # Preparar respuesta
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=orden_{order.id}.pdf'
    
    return response
