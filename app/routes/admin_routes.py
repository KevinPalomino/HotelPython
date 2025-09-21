import io
from flask import Blueprint, render_template, request, redirect, send_file, url_for, flash
from app import db
from app.models.models import CategoriaInventario, Habitacion, Categoria, Cama, Inventario, RelacionCama, Foto, TipoHabitacion, Persona, Rol, Reserva, Cliente
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from collections import Counter

admin_bp = Blueprint('admin', __name__)

# CONSTANTES PARA ESTADOS DE HABITACIÓN
class EstadosHabitacion:
    DISPONIBLE = 'disponible'
    OCUPADA = 'ocupada'
    MANTENIMIENTO = 'mantenimiento'
    INACTIVA = 'inactiva'
    
    @classmethod
    def todas_activas(cls):
        """Retorna todos los estados que representan habitaciones activas"""
        return [cls.DISPONIBLE, cls.OCUPADA, cls.MANTENIMIENTO]
    
    @classmethod
    def disponibles_para_admin(cls):
        """Estados que el admin considera como habitaciones disponibles para gestión"""
        return [cls.DISPONIBLE, cls.OCUPADA, cls.MANTENIMIENTO]

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
    tipos = TipoHabitacion.query.all()

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
            estado=EstadosHabitacion.DISPONIBLE,
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

    habitaciones = Habitacion.query.filter(
        Habitacion.estado.in_(EstadosHabitacion.disponibles_para_admin())
    ).all()
    
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
    tipos = TipoHabitacion.query.all()

    if request.method == 'POST':
        habitacion.tipos_idtipo = int(request.form['tipo_id'])
        habitacion.capacidad = int(request.form['capacidad'])
        habitacion.precio = int(request.form['precio'])
        
        if 'estado' in request.form:
            if habitacion.estado == EstadosHabitacion.INACTIVA:
                habitacion.estado = EstadosHabitacion.DISPONIBLE
        else:
            habitacion.estado = EstadosHabitacion.INACTIVA
            
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

        camas_dict = {}
        for key, value in request.form.items():
            if key.startswith('camas[') and key.endswith(']'):
                id_cama = int(key[6:-1])
                cantidad = int(value)
                if cantidad > 0:
                    camas_dict[id_cama] = cantidad

        for idcama, cantidad in camas_dict.items():
            for _ in range(cantidad):
                nueva_rel = RelacionCama(
                    camas_idcamas=idcama,
                    habitaciones_idhabitaciones=id
                )
                db.session.add(nueva_rel)

        for archivo in request.files.getlist('fotos'):
            if archivo and archivo.filename != '':
                nueva_foto = Foto(fotos=archivo.read(),
                                  habitaciones_idhabitaciones=id)
                db.session.add(nueva_foto)

        db.session.commit()
        flash('Habitación actualizada correctamente.', 'success')
        return redirect(url_for('admin.listar_habitaciones'))

    camas_relacionadas = Counter([r.camas_idcamas for r in habitacion.camas])

    return render_template('admin/editar_habitacion.html',
                           habitacion=habitacion,
                           categorias=categorias,
                           camas=camas,
                           tipos=tipos,
                           camas_relacionadas=camas_relacionadas)

@admin_bp.route('/admin/foto/<int:id>')
@login_required
def ver_foto_admin(id):
    foto = Foto.query.get_or_404(id)
    return send_file(
        io.BytesIO(foto.fotos),
        mimetype='image/jpeg'
    )

@admin_bp.route('/admin/foto/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_foto_admin(id):
    foto = Foto.query.get_or_404(id)
    habitacion_id = foto.habitaciones_idhabitaciones

    db.session.delete(foto)
    db.session.commit()

    flash('Foto eliminada correctamente.', 'info')
    return redirect(url_for('admin.editar_habitacion', id=habitacion_id))

@admin_bp.route('/admin/habitaciones/eliminar/<int:id>')
@login_required
def eliminar_habitacion(id):
    habitacion = Habitacion.query.get_or_404(id)
    habitacion.estado = EstadosHabitacion.INACTIVA
    db.session.commit()
    flash('Habitación marcada como inactiva.', 'info')
    return redirect(url_for('admin.listar_habitaciones'))

@admin_bp.route('/admin/habitaciones/inactivas')
@login_required
def habitaciones_inactivas():
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    habitaciones = Habitacion.query.filter_by(estado=EstadosHabitacion.INACTIVA).all()
    return render_template('admin/habitaciones_inactivas.html', habitaciones=habitaciones)

@admin_bp.route('/admin/habitaciones/activar/<int:id>')
@login_required
def activar_habitacion(id):
    habitacion = Habitacion.query.get_or_404(id)
    habitacion.estado = EstadosHabitacion.DISPONIBLE
    db.session.commit()
    flash('Habitación habilitada nuevamente.', 'success')
    return redirect(url_for('admin.habitaciones_inactivas'))

@admin_bp.route('/admin/reservas')
@login_required
def ver_reservas():
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

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
                return redirect(url_for('admin.nuevo_producto'))

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
        producto.categoria = int(request.form['categoria'])
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

@admin_bp.route('/admin/personal')
@login_required
def ver_personal():
    if current_user.rol.nombre != 'Administrador':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    empleados = Persona.query.all()
    return render_template('admin/personal_listar.html', empleados=empleados)

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

@admin_bp.app_template_filter('estado_habitacion_admin')
def estado_habitacion_admin_filter(estado):
    """
    Filtro para templates de admin que convierte estados a texto legible
    """
    estado_map = {
        EstadosHabitacion.DISPONIBLE: 'Disponible',
        EstadosHabitacion.OCUPADA: 'Ocupada',
        EstadosHabitacion.MANTENIMIENTO: 'En Mantenimiento',
        EstadosHabitacion.INACTIVA: 'Inactiva'
    }
    return estado_map.get(estado, f'Estado: {estado}')