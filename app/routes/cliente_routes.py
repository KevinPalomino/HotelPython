# app/routes/cliente_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from app import db
from app.models.models import Habitacion, Cliente, Persona, Reserva, DetalleReserva, Foto
from datetime import datetime, date

cliente_bp = Blueprint('cliente', __name__)


@cliente_bp.route('/')
def inicio():
    return redirect(url_for('cliente.ver_habitaciones'))


@cliente_bp.route('/habitaciones')
def ver_habitaciones():
    habitaciones = Habitacion.query.filter_by(estado=True).all()
    return render_template('cliente/habitaciones.html', habitaciones=habitaciones)


@cliente_bp.route('/imagen_habitacion/<int:idfoto>')
def imagen_habitacion(idfoto):
    foto = Foto.query.get_or_404(idfoto)
    return Response(foto.fotos, mimetype='image/jpeg')


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
        entrada = request.form['entrada']
        salida = request.form['salida']
        metodo_pago = request.form['metodo_pago']
        abono = request.form.get('abono', 0)

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

        cliente = Cliente(
            departamento=departamento,
            ciudad=ciudad,
            personas_cedula=cedula
        )
        db.session.add(cliente)
        db.session.flush()

        reserva = Reserva(
            checkin=entrada,
            checkout=salida,
            abono=abono or 0,
            estado=1,
            clientes_idclientes=cliente.idclientes
        )
        db.session.add(reserva)
        db.session.flush()

        detalle = DetalleReserva(
            reservas_idreservas=reserva.idreservas,
            habitaciones_idhabitaciones=habitacion.idhabitaciones
        )
        db.session.add(detalle)
        db.session.commit()

        flash('¡Reserva realizada con éxito!', 'success')
        return redirect(url_for('cliente.ver_habitaciones'))

    return render_template('cliente/reserva_form.html', habitacion=habitacion, hoy=date.today())
