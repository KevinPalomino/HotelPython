# app/models/models.py
from app.extensions import db
from flask_login import UserMixin
from datetime import datetime


class EstadoHabitacion:
    disponible = "disponible"
    ocupada = "ocupada"


class CategoriaInventario(db.Model):
    __tablename__ = 'categorias_inventario'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)

    productos = db.relationship(
        'Inventario', backref='categoria_obj', lazy=True)


class Categoria(db.Model):
    __tablename__ = 'categorias'
    idcategorias = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))
    descripcion = db.Column(db.String(45))
    habitaciones = db.relationship(
        'Habitacion', backref='categoria', lazy=True)


class Foto(db.Model):
    __tablename__ = 'fotos'
    idfotos = db.Column(db.Integer, primary_key=True)
    fotos = db.Column(db.LargeBinary)
    habitaciones_idhabitaciones = db.Column(
        db.Integer, db.ForeignKey('habitaciones.idhabitaciones'))


class Cama(db.Model):
    __tablename__ = 'camas'
    idcamas = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))


class RelacionCama(db.Model):
    __tablename__ = 'relacion_cama'
    idrelacion_cama = db.Column(db.Integer, primary_key=True)
    camas_idcamas = db.Column(db.Integer, db.ForeignKey('camas.idcamas'))
    habitaciones_idhabitaciones = db.Column(
        db.Integer, db.ForeignKey('habitaciones.idhabitaciones'))


class Habitacion(db.Model):
    __tablename__ = 'habitaciones'
    idhabitaciones = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Integer)
    capacidad = db.Column(db.Integer)
    estado = db.Column(db.String(25), nullable=False,
                       default=EstadoHabitacion.disponible)
    precio = db.Column(db.BigInteger)
    ventilador = db.Column(db.Boolean)
    aire_acondicionado = db.Column(db.Boolean)
    TV = db.Column(db.Boolean)
    tina = db.Column(db.Boolean)
    wifi = db.Column(db.Boolean)
    bar = db.Column(db.Boolean)
    aseo = db.Column(db.Boolean)
    caja_fuerte = db.Column(db.Boolean)
    categorias_idcategorias = db.Column(
        db.Integer, db.ForeignKey('categorias.idcategorias'))

    # ✅ Relación que te faltaba
    camas = db.relationship('RelacionCama', backref='habitacion', lazy=True)

    fotos = db.relationship('Foto', backref='habitacion', lazy=True)


class Cliente(db.Model):
    __tablename__ = 'clientes'
    idclientes = db.Column(db.Integer, primary_key=True)
    personas_cedula = db.Column(db.BigInteger, db.ForeignKey(
        'personas.cedula'), nullable=False)
    departamento = db.Column(db.String(50))
    ciudad = db.Column(db.String(50))
    persona = db.relationship('Persona', backref='cliente', uselist=False)


class Reserva(db.Model):
    __tablename__ = 'reservas'
    idreservas = db.Column(db.Integer, primary_key=True)
    checkin = db.Column(db.Date, nullable=False)
    checkout = db.Column(db.Date, nullable=False)
    abono = db.Column(db.BigInteger, nullable=False)
    estado = db.Column(db.Boolean, nullable=True)
    clientes_idclientes = db.Column(db.Integer, db.ForeignKey(
        'clientes.idclientes'), nullable=False)
    cliente = db.relationship('Cliente', backref='reservas', lazy=True)
    detalle = db.relationship('DetalleReserva', backref='reserva', lazy=True)


class Persona(db.Model, UserMixin):
    __tablename__ = 'personas'
    cedula = db.Column(db.BigInteger, primary_key=True)
    nombre = db.Column(db.String(150))
    telefono = db.Column(db.BigInteger)
    direccion = db.Column(db.String(100))
    correo = db.Column(db.String(60))
    contrasena = db.Column(db.String(200))
    roles_idroles = db.Column(db.Integer, db.ForeignKey('roles.idroles'))

    def get_id(self):
        return str(self.cedula)


class Rol(db.Model):
    __tablename__ = 'roles'
    idroles = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))
    personas = db.relationship('Persona', backref='rol', lazy=True)


class DetalleReserva(db.Model):
    __tablename__ = 'detalle_reserva'
    iddetalle_reserva = db.Column(db.Integer, primary_key=True)
    reservas_idreservas = db.Column(db.Integer, db.ForeignKey(
        'reservas.idreservas'), nullable=False)
    habitaciones_idhabitaciones = db.Column(db.Integer, db.ForeignKey(
        'habitaciones.idhabitaciones'), nullable=False)
    habitacion = db.relationship('Habitacion', backref='detalles', lazy=True)


class Inventario(db.Model):
    __tablename__ = 'inventario'
    idinventario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))
    categoria = db.Column(db.Integer, db.ForeignKey(
        'categorias_inventario.id'))  # FK correcta
    cantidad = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    precio = db.Column(db.BigInteger)


class Consumo(db.Model):
    __tablename__ = 'consumos'
    idconsumos = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    cantidad = db.Column(db.Integer)
    total = db.Column(db.Integer)
    estado = db.Column(db.Boolean, default=True)

    inventario_idinventario = db.Column(db.Integer, db.ForeignKey(
        'inventario.idinventario'), nullable=False)
    detalle_reserva_iddetalle_reserva = db.Column(db.Integer, db.ForeignKey(
        'detalle_reserva.iddetalle_reserva'), nullable=False)

    detalle_reserva = db.relationship(
        'DetalleReserva', backref='consumos', lazy=True)
