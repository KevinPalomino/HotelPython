# app/routes/cliente_routes.py
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, Response
from app import db
from app.models.models import Habitacion, Cliente, Persona, Reserva, DetalleReserva, Foto
from datetime import datetime, date

cliente_bp = Blueprint('cliente', __name__)


@cliente_bp.route('/')
def inicio():
    return redirect(url_for('cliente.ver_habitaciones'))


# Ruta para mostrar las habitaciones disponibles al cliente.
# Se consultan únicamente las habitaciones cuyo estado sea "disponible"
# y se envían al template 'cliente/habitaciones.html' para ser renderizadas.
@cliente_bp.route('/habitaciones')
def ver_habitaciones():
    from app.models.models import Categoria
    # Filtros
    fecha_entrada = request.args.get('fecha_entrada')
    fecha_salida = request.args.get('fecha_salida')
    categoria_id = request.args.get('categoria', type=int)
    precio_min = request.args.get('precio_min', type=int)
    precio_max = request.args.get('precio_max', type=int)

    # Base query: solo habitaciones activas
    habitaciones_query = Habitacion.query.filter_by(estado="disponible")
    if categoria_id:
        habitaciones_query = habitaciones_query.filter(
            Habitacion.categorias_idcategorias == categoria_id)
    if precio_min is not None:
        habitaciones_query = habitaciones_query.filter(
            Habitacion.precio >= precio_min)
    if precio_max is not None:
        habitaciones_query = habitaciones_query.filter(
            Habitacion.precio <= precio_max)

    habitaciones = habitaciones_query.all()

    # Filtrar por fechas: solo mostrar habitaciones sin reservas que se crucen
    if fecha_entrada and fecha_salida:
        try:
            entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d").date()
            salida = datetime.strptime(fecha_salida, "%Y-%m-%d").date()
            disponibles = []
            for hab in habitaciones:
                reservas = db.session.query(Reserva).join(DetalleReserva).filter(
                    DetalleReserva.habitaciones_idhabitaciones == hab.idhabitaciones,
                    Reserva.estado.in_([0, 1]),
                    Reserva.checkin < salida,
                    Reserva.checkout > entrada
                ).first()
                if not reservas:
                    disponibles.append(hab)
            habitaciones = disponibles
        except Exception:
            pass

    # Obtener categorías para el filtro
    categorias = Categoria.query.all()
    # Calcular rango de precios para el slider
    min_precio = db.session.query(db.func.min(Habitacion.precio)).scalar() or 0
    max_precio = db.session.query(db.func.max(Habitacion.precio)).scalar() or 0

    return render_template(
        'cliente/habitaciones.html',
        habitaciones=habitaciones,
        categorias=categorias,
        min_precio=min_precio,
        max_precio=max_precio
    )


@cliente_bp.route('/imagen_habitacion/<int:idfoto>')
def imagen_habitacion(idfoto):
    foto = Foto.query.get_or_404(idfoto)
    return Response(foto.fotos, mimetype='image/jpeg')


@cliente_bp.route('/reservas_por_habitacion')
def reservas_por_habitacion():
    id = request.args.get('id', type=int)
    if not id:
        return jsonify([])
    # Buscar reservas activas o pendientes para la habitación
    reservas = db.session.query(Reserva).join(DetalleReserva).filter(
        DetalleReserva.habitaciones_idhabitaciones == id,
        Reserva.estado.in_([0, 1])
    ).all()
    resultado = []
    for r in reservas:
        resultado.append({
            'checkin': r.checkin.strftime('%Y-%m-%d'),
            'checkout': r.checkout.strftime('%Y-%m-%d'),
            'estado': r.estado
        })
    return jsonify(resultado)


@cliente_bp.route('/reservar/<int:id>', methods=['GET', 'POST'])
def reservar_habitacion(id):
    habitacion = Habitacion.query.get_or_404(id)

    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        departamento = request.form['departamento']
        ciudad = request.form['ciudad']
        entrada = datetime.strptime(request.form['entrada'], "%Y-%m-%d").date()
        salida = datetime.strptime(request.form['salida'], "%Y-%m-%d").date()
        metodo_pago = request.form['metodo_pago']
        abono = int(request.form.get('abono', 0))

        # Calcular el valor total de la reserva
        precio_total = habitacion.precio * (salida - entrada).days
        if abono > precio_total:
            flash(
                f'❌ El abono no puede ser mayor al valor total de la reserva (${precio_total:,}).', 'danger')
            return redirect(url_for('cliente.reservar_habitacion', id=habitacion.idhabitaciones))

        # -------------------------------
        # Validación de disponibilidad
        # -------------------------------
        reserva_conflicto = db.session.query(Reserva).join(DetalleReserva).filter(
            DetalleReserva.habitaciones_idhabitaciones == habitacion.idhabitaciones,
            Reserva.estado.in_([0, 1]),  # solo reservas activas o pendientes
            Reserva.checkin < salida,
            Reserva.checkout > entrada
        ).first()

        if reserva_conflicto:
            flash(
                '❌ La habitación ya está ocupada en las fechas seleccionadas.', 'danger')
            return redirect(url_for('cliente.reservar_habitacion', id=habitacion.idhabitaciones))

        # -------------------------------
        # Crear persona si no existe
        # -------------------------------
        persona = Persona.query.get(cedula)
        if not persona:
            persona = Persona(
                cedula=cedula,
                nombre=nombre,
                correo=correo,
                telefono=telefono,
                direccion=None,
                contrasena=None,
                roles_idroles=2
            )
            db.session.add(persona)
            db.session.flush()

        # -------------------------------
        # Crear cliente
        # -------------------------------
        cliente = Cliente(
            departamento=departamento,
            ciudad=ciudad,
            personas_cedula=cedula
        )
        db.session.add(cliente)
        db.session.flush()

        # -------------------------------
        # Crear reserva
        # -------------------------------
        reserva = Reserva(
            checkin=entrada,
            checkout=salida,
            abono=abono or 0,
            estado=0,  # Pendiente, para que aparezca en check-in
            clientes_idclientes=cliente.idclientes
        )
        db.session.add(reserva)
        db.session.flush()

        # -------------------------------
        # Crear detalle
        # -------------------------------
        detalle = DetalleReserva(
            reservas_idreservas=reserva.idreservas,
            habitaciones_idhabitaciones=habitacion.idhabitaciones
        )
        db.session.add(detalle)
        db.session.commit()

        flash('✅ ¡Reserva realizada con éxito!', 'success')
        return redirect(url_for('cliente.ver_habitaciones'))

    return render_template('cliente/reserva_form.html', habitacion=habitacion, hoy=date.today())
