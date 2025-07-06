# app/routes/admin_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models.models import CategoriaInventario, Habitacion, Categoria, Cama, Inventario, RelacionCama, Foto, TipoHabitacion
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from app.models.models import Persona, Rol
from collections import Counter


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/panel')
@login_required
def panel_admin():
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('admin/panel_admin.html')


@admin_bp.route('/admin/habitaciones/nueva', methods=['GET', 'POST'])
@login_required
def nueva_habitacion():
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso restringido', 'danger')
        return redirect(url_for('auth.login'))

    categorias = Categoria.query.all()
    camas = Cama.query.all()
    tipos = TipoHabitacion.query.all()  # ✅ AÑADIDO

    if request.method == 'POST':
        tipo_id = request.form['tipo_id']
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
            tipos_idtipo=tipo_id,
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

        camas_dict = {}
        for key, value in request.form.items():
            if key.startswith('camas[') and key.endswith(']'):
                id_cama = int(key[6:-1])
                cantidad = int(value)
                if cantidad > 0:
                    camas_dict[id_cama] = cantidad

        for idcama, cantidad in camas_dict.items():
            for _ in range(cantidad):
                relacion = RelacionCama(
                    camas_idcamas=idcama,
                    habitaciones_idhabitaciones=habitacion.idhabitaciones
                )
                db.session.add(relacion)

        for archivo in request.files.getlist('fotos'):
            if archivo:
                foto = Foto(fotos=archivo.read(),
                            habitaciones_idhabitaciones=habitacion.idhabitaciones)
                db.session.add(foto)

        db.session.commit()
        flash('Habitación registrada correctamente')
        return redirect(url_for('admin.nueva_habitacion'))

    return render_template('admin/nueva_habitacion.html', categorias=categorias, camas=camas, tipos=tipos)


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

        # Eliminar camas actuales
    RelacionCama.query.filter_by(habitaciones_idhabitaciones=id).delete()

# Leer cantidades nuevas desde el formulario
    camas_dict = {}
    for key, value in request.form.items():
        if key.startswith('camas[') and key.endswith(']'):
            id_cama = int(key[6:-1])
        cantidad = int(value)
        if cantidad > 0:
            camas_dict[id_cama] = cantidad

# Insertar nuevas relaciones
    for idcama, cantidad in camas_dict.items():
        for _ in range(cantidad):
            nueva_rel = RelacionCama(
                camas_idcamas=idcama,
                habitaciones_idhabitaciones=id
            )
        db.session.add(nueva_rel)

        db.session.commit()
        flash('Habitación actualizada correctamente.', 'success')
        return redirect(url_for('admin.listar_habitaciones'))

    # Cuenta cuántas veces aparece cada tipo de cama en la habitación
    camas_relacionadas = Counter([r.camas_idcamas for r in habitacion.camas])
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
    categorias = CategoriaInventario.query.all()

    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']
        descripcion = request.form['descripcion']

        categoria_id = request.form['categoria']

        if categoria_id == 'otra':
            nueva_cat_nombre = request.form['nueva_categoria'].strip()
            if nueva_cat_nombre:
                nueva_categoria = CategoriaInventario(nombre=nueva_cat_nombre)
                db.session.add(nueva_categoria)
                db.session.flush()
                categoria_id = nueva_categoria.id
            else:
                flash("Debes ingresar el nombre de la nueva categoría", "danger")
                return redirect(url_for('admin.inventario_nuevo'))

        nuevo = Inventario(
            nombre=nombre,
            categoria=int(categoria_id),
            cantidad=cantidad,
            precio=precio,
            descripcion=descripcion
        )
        db.session.add(nuevo)
        db.session.commit()
        flash("Producto agregado correctamente", "success")
        return redirect(url_for('admin.ver_inventario'))

    return render_template("admin/inventario_nuevo.html", categorias=categorias)


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


# RUTA PARA EL APARTADO DEL PERSONAL:
@admin_bp.route('/admin/personal')
@login_required
def ver_personal():
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    from app.models.models import Persona
    empleados = Persona.query.all()
    return render_template('admin/personal_listar.html', empleados=empleados)


# RUTA PARA AGREGAR NUEVOS EMPLEADOS:
@admin_bp.route('/admin/personal/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_empleado():
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    roles = Rol.query.all()

    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        contrasena = generate_password_hash(request.form['contrasena'])
        rol_id = request.form['rol']

        persona = Persona(
            cedula=cedula,
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
            contrasena=contrasena,
            roles_idroles=rol_id
        )
        db.session.add(persona)
        db.session.commit()
        flash('Empleado registrado exitosamente', 'success')
        return redirect(url_for('admin.ver_personal'))

    return render_template('admin/personal_nuevo.html', roles=roles)


@admin_bp.route('/admin/personal/editar/<int:cedula>', methods=['GET', 'POST'])
@login_required
def editar_empleado(cedula):
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    persona = Persona.query.get_or_404(cedula)
    roles = Rol.query.all()

    if request.method == 'POST':
        persona.nombre = request.form['nombre']
        persona.correo = request.form['correo']
        persona.telefono = request.form['telefono']
        persona.direccion = request.form['direccion']
        persona.roles_idroles = int(request.form['rol'])

        db.session.commit()
        flash('Empleado actualizado correctamente', 'success')
        return redirect(url_for('admin.ver_personal'))

    return render_template('admin/personal_editar.html', persona=persona, roles=roles)


@admin_bp.route('/admin/personal/cambiar_clave/<int:cedula>', methods=['GET', 'POST'])
@login_required
def cambiar_contrasena_empleado(cedula):
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    persona = Persona.query.get_or_404(cedula)

    if request.method == 'POST':
        nueva_clave = request.form['nueva_contrasena']
        confirmar = request.form['confirmar_contrasena']

        if nueva_clave != confirmar:
            flash('Las contraseñas no coinciden', 'danger')
            return redirect(request.url)

        persona.contrasena = generate_password_hash(nueva_clave)
        db.session.commit()
        flash('Contraseña actualizada exitosamente.', 'success')
        return redirect(url_for('admin.ver_personal'))

    return render_template('admin/cambiar_contrasena.html', persona=persona)


@admin_bp.route('/admin/personal/eliminar/<int:cedula>')
@login_required
def eliminar_empleado(cedula):
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso denegado', 'danger')
        return redirect(url_for('auth.login'))

    persona = Persona.query.get_or_404(cedula)

    if persona.cedula == current_user.cedula:
        flash('No puedes eliminar tu propio usuario', 'warning')
        return redirect(url_for('admin.ver_personal'))

    db.session.delete(persona)
    db.session.commit()
    flash('Empleado eliminado correctamente.', 'info')
    return redirect(url_for('admin.ver_personal'))
