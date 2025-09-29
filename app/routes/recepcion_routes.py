from flask import Blueprint, render_template, redirect, request, url_for, flash, jsonify
from flask_login import login_required, current_user
from datetime import date, datetime, timedelta
from app import db
from sqlalchemy import or_
from app.models.models import Habitacion, Persona, Reserva, Rol, DetalleReserva, Cliente, Consumo, Inventario, Ventas
from sqlalchemy import text


recepcion_bp = Blueprint('recepcion', __name__)

# *** FUNCIÓN HELPER PARA CONVERTIR ESTADOS DE HABITACIÓN ***


def get_estado_habitacion_texto(estado):
    """
    Convierte el estado de habitación a texto legible
    """
    estados_map = {
        'disponible': 'Disponible',
        'ocupada': 'Ocupada',
        'mantenimiento': 'En Mantenimiento',
        'inactiva': 'Inactiva'
    }
    return estados_map.get(estado, f'Estado: {estado}')


def es_habitacion_disponible(habitacion):
    """
    Verifica si una habitación está disponible
    """
    return habitacion.estado == 'disponible'


def es_habitacion_ocupada(habitacion):
    """
    Verifica si una habitación está ocupada
    """
    return habitacion.estado == 'ocupada'


@recepcion_bp.route('/recepcion')
@login_required
def panel_recepcionista():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('recepcion/panel.html')


@recepcion_bp.route('/recepcion/checkin')
@login_required
def ver_reservas_checkin():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    fecha_filtro_str = request.args.get('fecha')
    hoy = date.today()

    # Marcar como canceladas las reservas vencidas (check-in < hoy y estado = 0)
    reservas_vencidas = db.session.query(Reserva).filter(
        Reserva.estado == 0,  # Pendiente
        Reserva.checkin < hoy
    ).all()

    for reserva in reservas_vencidas:
        reserva.estado = 3  # 3 = Cancelada automáticamente

    if reservas_vencidas:
        db.session.commit()

    # Query base que une las tablas necesarias (solo reservas pendientes no vencidas)
    query = db.session.query(Reserva, Habitacion, Persona).join(
        DetalleReserva, Reserva.idreservas == DetalleReserva.reservas_idreservas
    ).join(
        Habitacion, DetalleReserva.habitaciones_idhabitaciones == Habitacion.idhabitaciones
    ).join(
        Cliente, Reserva.clientes_idclientes == Cliente.idclientes
    ).join(
        Persona, Cliente.personas_cedula == Persona.cedula
    ).filter(
        Reserva.estado == 0,  # Estado 0 = Pendiente
        Reserva.checkin >= hoy  # Solo mostrar reservas válidas
    )

    # Solo aplicar filtro de fecha si se proporciona una fecha específica
    fecha_filtro = None
    if fecha_filtro_str:
        try:
            fecha_filtro = datetime.strptime(
                fecha_filtro_str, '%Y-%m-%d').date()
            query = query.filter(Reserva.checkin == fecha_filtro)
        except ValueError:
            flash('Formato de fecha inválido.', 'warning')
    # Si no hay filtro de fecha, mostrar todas las reservas pendientes válidas

    reservas_info = query.order_by(Reserva.checkin.asc()).all()

    fecha_filtro_display = "todas" if not fecha_filtro_str else (
        fecha_filtro.strftime('%Y-%m-%d') if fecha_filtro else hoy.strftime('%Y-%m-%d'))

    return render_template('recepcion/checkin.html',
                           reservas=reservas_info,
                           fecha_filtro=fecha_filtro_display,
                           hoy=hoy.strftime('%Y-%m-%d'))


@recepcion_bp.route('/recepcion/checkin/<int:reserva_id>', methods=['GET', 'POST'])
@login_required
def hacer_checkin(reserva_id):
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    reserva_info = db.session.query(Reserva, Habitacion, Persona).join(
        DetalleReserva, Reserva.idreservas == DetalleReserva.reservas_idreservas
    ).join(
        Habitacion, DetalleReserva.habitaciones_idhabitaciones == Habitacion.idhabitaciones
    ).join(
        Cliente, Reserva.clientes_idclientes == Cliente.idclientes
    ).join(
        Persona, Cliente.personas_cedula == Persona.cedula
    ).filter(Reserva.idreservas == reserva_id).first_or_404()

    reserva, habitacion, persona = reserva_info

    if reserva.estado != 0:
        flash('Esta reserva no está pendiente de check-in.', 'warning')
        return redirect(url_for('recepcion.ver_reservas_checkin'))

    if request.method == 'POST':
        try:
            reserva.estado = 1
            habitacion.estado = 'ocupada'

            db.session.commit()
            flash(
                f'Check-in para {persona.nombre} en la habitación {habitacion.idhabitaciones} realizado con éxito.', 'success')
            return redirect(url_for('recepcion.ver_reservas_checkin'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar el check-in: {str(e)}', 'danger')

    return render_template('recepcion/hacer_checkin.html',
                           reserva=reserva,
                           habitacion=habitacion,
                           cliente=persona)


@recepcion_bp.route('/recepcion/reservas-canceladas')
@login_required
def ver_reservas_canceladas():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    hoy = date.today()

    reservas_canceladas = db.session.query(Reserva, Habitacion, Persona).join(
        DetalleReserva, Reserva.idreservas == DetalleReserva.reservas_idreservas
    ).join(
        Habitacion, DetalleReserva.habitaciones_idhabitaciones == Habitacion.idhabitaciones
    ).join(
        Cliente, Reserva.clientes_idclientes == Cliente.idclientes
    ).join(
        Persona, Cliente.personas_cedula == Persona.cedula
    ).filter(
        Reserva.estado == 3  # Estado 3 = Cancelada
    ).order_by(Reserva.checkin.desc()).all()

    return render_template('recepcion/reservas_canceladas.html',
                           reservas=reservas_canceladas,
                           hoy=hoy.strftime('%Y-%m-%d'))


@recepcion_bp.route('/recepcion/cancelar-reserva/<int:reserva_id>', methods=['POST'])
@login_required
def cancelar_reserva(reserva_id):
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    try:
        reserva = Reserva.query.get_or_404(reserva_id)
        razon = request.form.get('razon', '').strip()

        if not razon:
            flash('Debe proporcionar una razón para la cancelación.', 'danger')
            return redirect(url_for('recepcion.ver_reservas_checkin'))

        if reserva.estado != 0:
            flash('Solo se pueden cancelar reservas pendientes.', 'warning')
            return redirect(url_for('recepcion.ver_reservas_checkin'))

        reserva.estado = 3  # 3 = Cancelada manualmente
        db.session.commit()
        flash(f'Reserva cancelada exitosamente. Razón: {razon}', 'info')

    except Exception as e:
        db.session.rollback()
        flash(f'Error al cancelar la reserva: {str(e)}', 'danger')

    return redirect(url_for('recepcion.ver_reservas_checkin'))


@recepcion_bp.route('/recepcion/checkin-directo', methods=['GET', 'POST'])
@login_required
def checkin_directo():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        try:
            cliente_cedula = request.form.get('cliente_cedula')
            habitacion_ids = request.form.getlist('habitacion')
            checkin_date = date.today()
            checkout_str = request.form.get('checkout')
            abono = request.form.get('abono', 0)
            comentario = request.form.get('comentario', '').strip()

            if not cliente_cedula or not habitacion_ids or not checkout_str:
                flash(
                    'Debe seleccionar un cliente, al menos una habitación y una fecha de checkout.', 'danger')
                return redirect(request.url)

            habitacion_ids = [int(id) for id in habitacion_ids]

            try:
                checkout_date = datetime.strptime(
                    checkout_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Formato de fecha de checkout inválido.', 'danger')
                return redirect(request.url)

            if checkout_date <= checkin_date:
                flash('La fecha de salida debe ser posterior al día de hoy.', 'danger')
                return redirect(request.url)

            persona = Persona.query.filter_by(cedula=cliente_cedula).first()
            if not persona:
                flash('Cliente no encontrado.', 'danger')
                return redirect(request.url)

            cliente = Cliente.query.filter_by(
                personas_cedula=cliente_cedula).first()
            if not cliente:
                cliente = Cliente(
                    personas_cedula=cliente_cedula,
                    departamento='',
                    ciudad=''
                )
                db.session.add(cliente)
                db.session.flush()

            habitaciones_validas = []
            for hab_id in habitacion_ids:
                habitacion = Habitacion.query.filter_by(
                    idhabitaciones=hab_id).first()
                if not habitacion:
                    flash(f'La habitación ID {hab_id} no existe.', 'danger')
                    return redirect(request.url)

                if not es_habitacion_disponible(habitacion):
                    flash(
                        f'La habitación ID {hab_id} no está disponible.', 'danger')
                    return redirect(request.url)

                habitaciones_validas.append(habitacion)

            for hab_id in habitacion_ids:
                reservas_conflicto = db.session.query(Reserva).join(DetalleReserva).filter(
                    DetalleReserva.habitaciones_idhabitaciones == hab_id,
                    Reserva.estado.in_([0, 1]),
                    Reserva.checkin < checkout_date,
                    Reserva.checkout > checkin_date
                ).first()

                if reservas_conflicto:
                    flash(
                        f'La habitación ID {hab_id} ya está reservada en esas fechas.', 'danger')
                    return redirect(request.url)

            nueva_reserva = Reserva(
                checkin=checkin_date,
                checkout=checkout_date,
                abono=int(float(abono)) if abono else 0,
                estado=1,
                comentario=request.form.get('comentario'),
                clientes_idclientes=cliente.idclientes
            )

            db.session.add(nueva_reserva)
            db.session.flush()

            for habitacion in habitaciones_validas:
                detalle_reserva = DetalleReserva(
                    reservas_idreservas=nueva_reserva.idreservas,
                    habitaciones_idhabitaciones=habitacion.idhabitaciones
                )
                db.session.add(detalle_reserva)
                habitacion.estado = 'ocupada'

            db.session.commit()

            habitaciones_texto = ', '.join(
                [str(h.idhabitaciones) for h in habitaciones_validas])
            flash(
                f'Check-in directo realizado con éxito para {persona.nombre} en las habitaciones: {habitaciones_texto}.', 'success')

            return redirect(url_for('recepcion.panel_recepcionista'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar el check-in directo: {str(e)}', 'danger')
            return redirect(request.url)

    hoy = date.today()
    manana = hoy + timedelta(days=1)

    todas_habitaciones = Habitacion.query.all()
    habitaciones_disponibles_hoy = []

    for habitacion in todas_habitaciones:
        if es_habitacion_disponible(habitacion):
            reservas_conflicto = db.session.query(Reserva).join(DetalleReserva).filter(
                DetalleReserva.habitaciones_idhabitaciones == habitacion.idhabitaciones,
                Reserva.estado.in_([0, 1]),
                Reserva.checkin <= hoy,
                Reserva.checkout > hoy
            ).first()

            if not reservas_conflicto:
                habitacion.estado_texto = get_estado_habitacion_texto(
                    habitacion.estado)
                habitaciones_disponibles_hoy.append(habitacion)

    return render_template('recepcion/checkin_directo.html',
                           habitaciones=habitaciones_disponibles_hoy,
                           hoy=hoy.strftime('%Y-%m-%d'),
                           manana=manana.strftime('%Y-%m-%d'))


@recepcion_bp.route('/recepcion/checkout')
@login_required
def ver_reservas_checkout():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    hoy = date.today()
    fecha_filtro_str = request.args.get('fecha')
    nombre_filtro = request.args.get('nombre')  # 👈 Nuevo campo

    # Traemos TODAS las reservas en curso
    query = db.session.query(Reserva, Habitacion, Persona).join(
        DetalleReserva, Reserva.idreservas == DetalleReserva.reservas_idreservas
    ).join(
        Habitacion, DetalleReserva.habitaciones_idhabitaciones == Habitacion.idhabitaciones
    ).join(
        Cliente, Reserva.clientes_idclientes == Cliente.idclientes
    ).join(
        Persona, Cliente.personas_cedula == Persona.cedula
    ).filter(
        Reserva.estado == 1
    )

    # Filtro por fecha (opcional)
    fecha_filtro = None
    if fecha_filtro_str:
        try:
            fecha_filtro = datetime.strptime(
                fecha_filtro_str, '%Y-%m-%d').date()
            if fecha_filtro < hoy:
                flash('No se pueden consultar fechas pasadas.', 'warning')
            else:
                query = query.filter(Reserva.checkout == fecha_filtro)
        except ValueError:
            flash(
                'Formato de fecha inválido, mostrando todos los check-outs pendientes.', 'warning')

    # Filtro por nombre (opcional)
    if nombre_filtro:
        query = query.filter(Persona.nombre.ilike(f"%{nombre_filtro}%"))

    reservas_info = query.all()

    return render_template(
        'recepcion/checkout.html',
        reservas=reservas_info,
        fecha_filtro=fecha_filtro_str or "",
        nombre_filtro=nombre_filtro or "",
        hoy=hoy.strftime('%Y-%m-%d')
    )


@recepcion_bp.route('/recepcion/checkout/<int:reserva_id>', methods=['GET', 'POST'])
@login_required
def hacer_checkout(reserva_id):
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    reserva_info = db.session.query(Reserva, Habitacion, Persona).join(
        DetalleReserva, Reserva.idreservas == DetalleReserva.reservas_idreservas
    ).join(
        Habitacion, DetalleReserva.habitaciones_idhabitaciones == Habitacion.idhabitaciones
    ).join(
        Cliente, Reserva.clientes_idclientes == Cliente.idclientes
    ).join(
        Persona, Cliente.personas_cedula == Persona.cedula
    ).filter(Reserva.idreservas == reserva_id).first_or_404()

    reserva, habitacion, persona = reserva_info

    if reserva.estado != 1:
        flash('Esta reserva no está en curso para hacer check-out.', 'warning')
        return redirect(url_for('recepcion.ver_reservas_checkout'))

    if request.method == 'POST':
        try:
            reserva.estado = 2
            habitacion.estado = 'disponible'

            db.session.commit()
            flash(
                f'Check-out para {persona.nombre} de la habitación {habitacion.idhabitaciones} realizado con éxito.', 'success')
            return redirect(url_for('recepcion.ver_reservas_checkout'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar el check-out: {str(e)}', 'danger')

    return render_template('recepcion/hacer_checkout.html',
                           reserva=reserva,
                           habitacion=habitacion,
                           cliente=persona)


@recepcion_bp.route('/recepcion/cliente/nuevo', methods=['GET', 'POST'])
@login_required
def registrar_cliente():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso denegado', 'danger')
        return redirect(url_for('auth.login'))

    next_url = request.args.get('next')

    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        if Persona.query.filter_by(cedula=cedula).first():
            flash('Ya existe una persona registrada con esa cédula.', 'danger')
            return render_template('recepcion/registrar_cliente.html', next_url=next_url)

        nuevo_cliente = Persona(
            cedula=cedula,
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
            roles_idroles=2
        )
        db.session.add(nuevo_cliente)
        db.session.commit()

        flash('Cliente registrado correctamente', 'success')

        if next_url:
            return redirect(f"{next_url}?cliente_cedula={cedula}")

        return redirect(url_for('recepcion.panel_recepcionista'))

    return render_template('recepcion/registrar_cliente.html', next_url=next_url)


@recepcion_bp.route('/recepcion/reserva/nueva', methods=['GET', 'POST'])
@login_required
def nueva_reserva():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        try:
            cliente_cedula = request.form.get('cliente_cedula')
            habitacion_ids = request.form.getlist('habitacion')
            checkin_str = request.form.get('checkin')
            checkout_str = request.form.get('checkout')
            abono = request.form.get('abono', 0)
            comentario = request.form.get(
                'comentario', '').strip()  # <-- AGREGAR ESTA LÍNEA

            if not all([cliente_cedula, habitacion_ids, checkin_str, checkout_str]):
                flash(
                    'Todos los campos son obligatorios: cliente, fechas y al menos una habitación.', 'danger')
                return redirect(request.url)

            habitacion_ids = [int(id) for id in habitacion_ids]

            checkin_date = datetime.strptime(checkin_str, '%Y-%m-%d').date()
            checkout_date = datetime.strptime(checkout_str, '%Y-%m-%d').date()

            if checkout_date <= checkin_date:
                flash('La fecha de salida debe ser posterior a la de entrada.', 'danger')
                return redirect(request.url)

            cliente_obj = Cliente.query.join(Persona).filter(
                Persona.cedula == cliente_cedula).first()
            if not cliente_obj:
                persona = Persona.query.filter_by(
                    cedula=cliente_cedula).first()
                if persona:
                    cliente_obj = Cliente(
                        personas_cedula=persona.cedula, departamento='', ciudad='')
                    db.session.add(cliente_obj)
                    db.session.flush()
                else:
                    flash('Cliente no encontrado. Regístrelo primero.', 'danger')
                    return redirect(request.url)

            for hab_id in habitacion_ids:
                reservas_conflicto = db.session.query(Reserva).join(DetalleReserva).filter(
                    DetalleReserva.habitaciones_idhabitaciones == hab_id,
                    Reserva.estado.in_([0, 1]),
                    Reserva.checkin < checkout_date,
                    Reserva.checkout > checkin_date
                ).first()

                if reservas_conflicto:
                    flash(
                        f'La habitación ID {hab_id} ya está reservada en esas fechas.', 'danger')
                    return redirect(request.url)

            nueva_reserva = Reserva(
                checkin=checkin_date,
                checkout=checkout_date,
                abono=int(float(abono)),
                estado=0,
                comentario=comentario,  # <-- USAR LA VARIABLE AQUÍ
                clientes_idclientes=cliente_obj.idclientes
            )
            db.session.add(nueva_reserva)
            db.session.flush()

            for hab_id in habitacion_ids:
                detalle_reserva = DetalleReserva(
                    reservas_idreservas=nueva_reserva.idreservas,
                    habitaciones_idhabitaciones=hab_id
                )
                db.session.add(detalle_reserva)

            db.session.commit()

            flash('Reserva registrada con éxito.', 'success')
            return redirect(url_for('recepcion.panel_recepcionista'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error al procesar la reserva: {str(e)}', 'danger')
            return redirect(request.url)

    todas_habitaciones = Habitacion.query.all()
    habitaciones_activas = []

    for habitacion in todas_habitaciones:
        if habitacion.estado not in ['mantenimiento', 'inactiva']:
            habitacion.estado_texto = get_estado_habitacion_texto(
                habitacion.estado)
            habitaciones_activas.append(habitacion)

    cliente_registrado = None
    cliente_cedula_param = request.args.get('cliente_cedula')
    if cliente_cedula_param:
        cliente_registrado = Persona.query.filter_by(
            cedula=cliente_cedula_param, roles_idroles=2).first()

    return render_template('recepcion/reserva_nueva.html',
                           habitaciones=habitaciones_activas,
                           cliente_registrado=cliente_registrado)


@recepcion_bp.route('/recepcion/habitacion/reservas')
@login_required
def reservas_por_habitacion():
    if current_user.rol.nombre != 'Recepcionista':
        return jsonify({'error': 'No autorizado'}), 403

    ids_str = request.args.get('ids')
    if not ids_str:
        return jsonify([])

    try:
        habitacion_ids = [int(id) for id in ids_str.split(',')]
    except ValueError:
        return jsonify({'error': 'IDs de habitación inválidos'}), 400

    hoy = date.today()

    reservas = db.session.query(Reserva).join(DetalleReserva).filter(
        DetalleReserva.habitaciones_idhabitaciones.in_(habitacion_ids),
        Reserva.checkout > hoy,
        Reserva.estado.in_([0, 1])
    ).all()

    lista_reservas = [
        {
            'checkin': r.checkin.strftime('%Y-%m-%d'),
            'checkout': r.checkout.strftime('%Y-%m-%d'),
            'estado': r.estado
        } for r in reservas
    ]

    return jsonify(lista_reservas)


@recepcion_bp.route('/recepcion/buscar-cliente')
@login_required
def buscar_cliente():
    if current_user.rol.nombre != 'Recepcionista':
        return jsonify({'error': 'No autorizado'}), 403

    search_term = request.args.get('q', '').strip()
    if not search_term:
        return jsonify([])

    clientes = Persona.query.filter(
        Persona.roles_idroles == 2,
        or_(
            Persona.nombre.ilike(f'%{search_term}%'),
            Persona.cedula.ilike(f'%{search_term}%')
        )
    ).limit(10).all()

    resultados = [{'cedula': c.cedula, 'nombre': c.nombre} for c in clientes]
    return jsonify(resultados)


@recepcion_bp.route('/recepcion/clientes-alojados')
@login_required
def clientes_alojados():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    filtro = request.args.get('filtro', '').strip().lower()

    query = db.session.query(
        Persona.cedula,
        Persona.nombre,
        Habitacion.idhabitaciones,
        Reserva.checkin,
        Reserva.checkout,
        DetalleReserva.iddetalle_reserva.label("detalle_id") 
    ).join(
        Cliente, Persona.cedula == Cliente.personas_cedula
    ).join(
        Reserva, Cliente.idclientes == Reserva.clientes_idclientes
    ).join(
        DetalleReserva, Reserva.idreservas == DetalleReserva.reservas_idreservas
    ).join(
        Habitacion, DetalleReserva.habitaciones_idhabitaciones == Habitacion.idhabitaciones
    ).filter(
        Reserva.estado == 1
    )

    if filtro:
        query = query.filter(
            or_(
                Persona.nombre.ilike(f'%{filtro}%'),
                Persona.cedula.ilike(f'%{filtro}%')
            )
        )

    clientes_info = query.all()
    
    return render_template('recepcion/clientes_alojados.html',
                           clientes=clientes_info,
                           filtro=filtro)


@recepcion_bp.route('/recepcion/clientes_personal')
@login_required
def clientes_personal():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    filtro = request.args.get('filtro', '').strip().lower()

    personas = Persona.query.join(Rol).filter(
        Rol.nombre.in_(['Cliente', 'Recepcionista'])).all()

    if filtro:
        personas = [
            p for p in personas if
            filtro in str(p.cedula).lower() or
            filtro in p.nombre.lower() or
            filtro in p.rol.nombre.lower()
        ]

    return render_template('recepcion/clientes_personal.html', personas=personas, filtro=filtro)

# -----------------------------
# CONSUMOS DE CLIENTES ALOJADOS
# -----------------------------
@recepcion_bp.route('/recepcion/consumo/nuevo', methods=['GET', 'POST'])
@login_required
def nuevo_consumo():
    # import local (ya tienes models arriba, pero lo ponemos por claridad)
    from app.models.models import Consumo, Inventario, Ventas, DetalleReserva, Reserva, Habitacion

    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    # recibir parámetros GET (vienen del enlace en clientes_alojados)
    habitacion_id = request.args.get("habitacion_id", type=int)
    detalle_id = request.args.get("detalle_id", type=int)
    cliente_cedula = request.args.get("cliente_cedula")

    # datos para el formulario GET
    habitaciones = db.session.query(Habitacion).filter(Habitacion.estado == 'ocupada').all()
    productos = db.session.query(Inventario).filter(Inventario.cantidad > 0).all()

    if request.method == 'POST':
        try:
            # leer hidden fields del form
            habitacion_id_form = request.form.get('habitacion_id')
            detalle_id_form = request.form.get('detalle_id')

            if not habitacion_id_form:
                flash("No se recibió el ID de la habitación.", "danger")
                return redirect(request.url)

            habitacion_id_form = int(habitacion_id_form)

            # 1) intentar usar detalle_id enviado (prioridad)
            detalle_obj = None
            if detalle_id_form:
                try:
                    detalle_obj = DetalleReserva.query.get(int(detalle_id_form))
                except Exception:
                    detalle_obj = None

            # 2) si no viene o no existe, buscar detalle activo (reserva en curso)
            if not detalle_obj:
                detalle_obj = db.session.query(DetalleReserva).join(Reserva).filter(
                    DetalleReserva.habitaciones_idhabitaciones == habitacion_id_form,
                    Reserva.estado == 1  # en curso
                ).order_by(Reserva.checkin.desc()).first()

            # 3) fallback: buscar cualquier detalle relacionado (estado 0 o 1)
            if not detalle_obj:
                detalle_obj = db.session.query(DetalleReserva).join(Reserva).filter(
                    DetalleReserva.habitaciones_idhabitaciones == habitacion_id_form,
                    Reserva.estado.in_([0, 1])
                ).order_by(Reserva.checkin.desc()).first()

            # Si aún no hay detalle, NO insertar (evita IntegrityError). Avisar al usuario.
            if not detalle_obj:
                flash("No se encontró una reserva/detalle asociado a esa habitación. No se puede registrar consumo (fk faltante).", "danger")
                return redirect(url_for('recepcion.clientes_alojados'))

            # leer items del form (array)
            productos_ids = request.form.getlist('producto_id[]')
            cantidades = request.form.getlist('cantidad[]')

            if not productos_ids:
                flash("Debe seleccionar al menos un producto.", "warning")
                return redirect(request.url)

            # procesar cada línea
            for pid, qty in zip(productos_ids, cantidades):
                if not pid or not qty:
                    continue
                producto = Inventario.query.get(int(pid))
                cantidad = int(qty)

                if not producto:
                    flash(f"Producto id {pid} no encontrado.", "danger")
                    return redirect(request.url)

                if cantidad <= 0:
                    continue

                if producto.cantidad < cantidad:
                    flash(f"No hay suficiente stock de {producto.nombre}. Stock actual: {producto.cantidad}", "danger")
                    return redirect(request.url)

                # descontar stock
                producto.cantidad -= cantidad

                precio_unitario = float(producto.precio)
                total = precio_unitario * cantidad

                # crear consumo (usa el iddetalle_reserva correcto)
                consumo = Consumo(
                    fecha=datetime.now(),
                    cantidad=cantidad,
                    total=int(round(total)),  # tu modelo total es Integer
                    inventario_idinventario=producto.idinventario,
                    detalle_reserva_iddetalle_reserva=detalle_obj.iddetalle_reserva,
                    estado=True
                )
                db.session.add(consumo)
                db.session.flush()  # para obtener consumo.idconsumos

                # crear venta ligada al consumo
                venta = Ventas(
                    fecha=consumo.fecha,
                    cantidad=cantidad,
                    precio=precio_unitario,
                    id_inventario=producto.idinventario,
                    id_consumo=consumo.idconsumos
                )
                db.session.add(venta)

            db.session.commit()
            flash("Consumos y Ventas registrados correctamente ✅", "success")
            return redirect(url_for('recepcion.clientes_alojados'))

        except Exception as e:
            db.session.rollback()
            # loguear para debug (si usas app.logger)
            try:
                from flask import current_app
                current_app.logger.exception("Error al registrar consumo")
            except Exception:
                pass
            flash(f"Error al registrar el consumo: {str(e)}", "danger")
            return redirect(request.url)

    # GET: renderizar el formulario con los valores pasados (habitacion_id y detalle_id si existen)
    return render_template("recepcion/nuevo_consumo.html",
                           habitaciones=habitaciones,
                           productos=productos,
                           habitacion_id=habitacion_id,
                           detalle_id=detalle_id,
                           cliente_cedula=cliente_cedula)
