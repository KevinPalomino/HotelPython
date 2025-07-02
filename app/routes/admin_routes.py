# app/routes/admin_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.models import Habitacion, Categoria, Cama, Inventario, RelacionCama, Foto
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/panel')
@login_required
def panel_admin():
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('admin/panel_admin.html')


@admin_bp.route('/recepcion')
@login_required
def panel_recepcionista():
    return render_template('admin/panel_recepcionista.html')


@admin_bp.route('/admin/habitaciones/nueva', methods=['GET', 'POST'])
@login_required
def nueva_habitacion():
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso restringido', 'danger')
        return redirect(url_for('auth.login'))

    categorias = Categoria.query.all()
    camas = Cama.query.all()

    if request.method == 'POST':
        tipo = request.form['tipo']
        capacidad = request.form['capacidad']
        precio = request.form['precio']

        if request.form['categoria'] == 'nueva':
            nuevo_nombre = request.form['nueva_categoria_nombre']
            nueva_descripcion = request.form['nueva_categoria_descripcion']
            nueva_cat = Categoria(nombre=nuevo_nombre,
                                  descripcion=nueva_descripcion)
            db.session.add(nueva_cat)
            db.session.flush()
            categoria_id = nueva_cat.idcategorias
        else:
            categoria_id = int(request.form['categoria'])

        ventilador = 'ventilador' in request.form
        aire = 'aire_acondicionado' in request.form
        tv = 'tv' in request.form
        tina = 'tina' in request.form
        wifi = 'wifi' in request.form
        bar = 'bar' in request.form
        aseo = 'aseo' in request.form
        caja_fuerte = 'caja_fuerte' in request.form

        habitacion = Habitacion(
            tipo=tipo,
            capacidad=capacidad,
            precio=precio,
            estado=True,
            categorias_idcategorias=categoria_id,
            ventilador=ventilador,
            aire_acondicionado=aire,
            TV=tv,
            tina=tina,
            wifi=wifi,
            bar=bar,
            aseo=aseo,
            caja_fuerte=caja_fuerte
        )
        db.session.add(habitacion)
        db.session.flush()

        camas_seleccionadas = request.form.getlist('camas')
        for cama_id in camas_seleccionadas:
            relacion = RelacionCama(camas_idcamas=int(
                cama_id), habitaciones_idhabitaciones=habitacion.idhabitaciones)
            db.session.add(relacion)

        for archivo in request.files.getlist('fotos'):
            if archivo:
                foto = Foto(fotos=archivo.read(),
                            habitaciones_idhabitaciones=habitacion.idhabitaciones)
                db.session.add(foto)

        db.session.commit()
        flash('Habitación registrada correctamente')
        return redirect(url_for('admin.nueva_habitacion'))

    return render_template('admin/nueva_habitacion.html', categorias=categorias, camas=camas)


@admin_bp.route('/admin/habitaciones')
@login_required
def listar_habitaciones():
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso restringido', 'danger')
        return redirect(url_for('auth.login'))

    habitaciones = Habitacion.query.all()
    return render_template('admin/listar_habitaciones.html', habitaciones=habitaciones)


@admin_bp.route('/admin/habitaciones/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_habitacion(id):
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    habitacion = Habitacion.query.get_or_404(id)
    categorias = Categoria.query.all()
    camas = Cama.query.all()

    if request.method == 'POST':
        habitacion.tipo = request.form['tipo']
        habitacion.capacidad = request.form['capacidad']
        habitacion.precio = request.form['precio']
        habitacion.estado = 'estado' in request.form
        habitacion.categorias_idcategorias = int(request.form['categoria'])

        habitacion.ventilador = 'ventilador' in request.form
        habitacion.aire_acondicionado = 'aire_acondicionado' in request.form
        habitacion.TV = 'tv' in request.form
        habitacion.tina = 'tina' in request.form
        habitacion.wifi = 'wifi' in request.form
        habitacion.bar = 'bar' in request.form
        habitacion.aseo = 'aseo' in request.form
        habitacion.caja_fuerte = 'caja_fuerte' in request.form

        RelacionCama.query.filter_by(habitaciones_idhabitaciones=id).delete()
        camas_seleccionadas = request.form.getlist('camas')
        for cama_id in camas_seleccionadas:
            nueva_rel = RelacionCama(camas_idcamas=int(
                cama_id), habitaciones_idhabitaciones=id)
            db.session.add(nueva_rel)

        db.session.commit()
        flash('Habitación actualizada correctamente.', 'success')
        return redirect(url_for('admin.listar_habitaciones'))

    camas_relacionadas = [r.camas_idcamas for r in habitacion.camas]
    return render_template('admin/editar_habitacion.html',
                           habitacion=habitacion,
                           categorias=categorias,
                           camas=camas,
                           camas_relacionadas=camas_relacionadas)


@admin_bp.route('/admin/habitaciones/eliminar/<int:id>')
@login_required
def eliminar_habitacion(id):
    habitacion = Habitacion.query.get_or_404(id)
    habitacion.estado = False  # Marcarla como no disponible en lugar de borrarla
    db.session.commit()
    flash('Habitación marcada como inactiva.', 'info')
    return redirect(url_for('admin.listar_habitaciones'))


@admin_bp.route('/admin/reservas')
@login_required
def ver_reservas():
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    from app.models.models import Reserva, Cliente, Persona, Habitacion

    reservas = Reserva.query.all()
    return render_template('admin/reservas.html', reservas=reservas)


@admin_bp.route('/admin/inventario')
@login_required
def ver_inventario():
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    productos = Inventario.query.all()
    return render_template('admin/inventario_listar.html', productos=productos)


@admin_bp.route('/admin/inventario/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_producto():
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        categoria = request.form['categoria']
        cantidad = request.form['cantidad']
        descripcion = request.form['descripcion']
        precio = request.form['precio']

        producto = Inventario(
            nombre=nombre,
            categoria=bool(int(categoria)),  # 0 = bebida, 1 = alimento
            cantidad=int(cantidad),
            descripcion=descripcion,
            precio=int(precio)
        )
        db.session.add(producto)
        db.session.commit()
        flash("Producto agregado correctamente", "success")
        return redirect(url_for('admin.ver_inventario'))

    return render_template('admin/inventario_nuevo.html')


@admin_bp.route('/admin/inventario/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    producto = Inventario.query.get_or_404(id)

    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.categoria = bool(int(request.form['categoria']))
        producto.cantidad = int(request.form['cantidad'])
        producto.descripcion = request.form['descripcion']
        producto.precio = int(request.form['precio'])

        db.session.commit()
        flash("Producto actualizado correctamente", "success")
        return redirect(url_for('admin.ver_inventario'))

    return render_template('admin/inventario_editar.html', producto=producto)


@admin_bp.route('/admin/inventario/eliminar/<int:id>')
@login_required
def eliminar_producto(id):
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    producto = Inventario.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash("Producto eliminado correctamente", "info")
    return redirect(url_for('admin.ver_inventario'))
