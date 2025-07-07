# app/routes/recepcion_routes.py
from flask import Blueprint, render_template, redirect, request, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from app import db

from app.models.models import Habitacion, Reserva


recepcion_bp = Blueprint('recepcion', __name__)


@recepcion_bp.route('/recepcion')
@login_required
def panel_recepcionista():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('recepcion/panel.html')

# MODULO DE CHECKIN


@recepcion_bp.route('/recepcion/checkin')
@login_required
def ver_reservas_checkin():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    hoy = date.today()
    reservas = Reserva.query.filter_by(checkin=hoy, estado=0).all()
    return render_template('recepcion/checkin.html', reservas=reservas)

# MODULO DE CHECKOUT


@recepcion_bp.route('/recepcion/checkout')
@login_required
def ver_reservas_checkout():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    hoy = date.today()

    # 1 = En curso → es cuando los clientes están hospedados actualmente
    reservas = Reserva.query.filter_by(checkout=hoy, estado=1).all()

    return render_template('recepcion/checkout.html', reservas=reservas)

# MODULO PARA REGISTRAR CLIENTE


@recepcion_bp.route('/recepcion/cliente/nuevo', methods=['GET', 'POST'])
@login_required
def registrar_cliente():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso denegado', 'danger')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        from app.models.models import Persona
        cedula = request.form['cedula']
        nombre = request.form['nombre']
        correo = request.form['correo']
        telefono = request.form['telefono']
        direccion = request.form['direccion']

        nuevo_cliente = Persona(
            cedula=cedula,
            nombre=nombre,
            correo=correo,
            telefono=telefono,
            direccion=direccion,
            roles_idroles=2  # Suponiendo que 3 es 'Cliente'
        )
        db.session.add(nuevo_cliente)
        db.session.commit()

        flash('Cliente registrado correctamente', 'success')
        return redirect(url_for('recepcion.panel_recepcionista'))

    return render_template('recepcion/registrar_cliente.html')


@recepcion_bp.route('/recepcion/reserva/nueva', methods=['GET', 'POST'])
@login_required
def nueva_reserva():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    from app.models.models import Persona, Habitacion, Reserva
    from app import db

    if request.method == 'POST':
        cliente_cedula = request.form['cliente_cedula']
        habitacion_id = request.form['habitacion']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        comentario = request.form.get('comentario', '')
        abono = request.form.get('abono', 0)

        cliente = Persona.query.get(cliente_cedula)
        habitacion = Habitacion.query.get(habitacion_id)

        if not cliente or not habitacion:
            flash('Cliente o habitación inválidos', 'danger')
            return redirect(request.url)

        nueva_reserva = Reserva(
            fecha=date.today(),
            checkin=checkin,
            checkout=checkout,
            comentario=comentario,
            estado=0,  # 0 = Pendiente
            abono=abono,
            clientes_idclientes=cliente.cedula,
            habitaciones_idhabitaciones=habitacion.idhabitaciones
        )
        db.session.add(nueva_reserva)
        db.session.commit()

        flash('Reserva registrada con éxito', 'success')
        return redirect(url_for('recepcion.panel_recepcionista'))

    habitaciones_disponibles = Habitacion.query.filter_by(estado=True).all()
    clientes = Persona.query.filter_by(
        roles_idroles=2).all()  # Rol cliente = 2

    return render_template('recepcion/reserva_nueva.html',
                           habitaciones=habitaciones_disponibles,
                           clientes=clientes)


@recepcion_bp.route('/clientes_personal')
@login_required
def clientes_personal():
    if current_user.rol.nombre != 'Recepcionista':
        flash('Acceso no autorizado', 'danger')
        return redirect(url_for('auth.login'))

    from app.models.models import Persona, Rol

    # Filtra solo CLIENTES y RECEPCIONISTAS
    roles_permitidos = ['Recepcionista', 'Cliente']
    personas = Persona.query.join(Rol).filter(
        Rol.nombre.in_(roles_permitidos)).order_by(Rol.nombre).all()

    return render_template('recepcion/clientes_personal.html', personas=personas)
