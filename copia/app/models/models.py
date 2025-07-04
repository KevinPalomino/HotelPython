# app/models/models.py
from app.extensions import db
from flask_login import UserMixin


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
    cama = db.relationship('Cama', backref='relaciones')


class Habitacion(db.Model):
    __tablename__ = 'habitaciones'
    idhabitaciones = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.Integer)
    capacidad = db.Column(db.Integer)
    estado = db.Column(db.Boolean)
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

    fotos = db.relationship('Foto', backref='habitacion', lazy=True)
    camas = db.relationship('RelacionCama', backref='habitacion', lazy=True)


class Cliente(db.Model):
    __tablename__ = 'clientes'
    idclientes = db.Column(db.Integer, primary_key=True)
    departamento = db.Column(db.String(45))
    ciudad = db.Column(db.String(45))
    personas_cedula = db.Column(
        db.BigInteger, db.ForeignKey('personas.cedula'))


class Reserva(db.Model):
    __tablename__ = 'reservas'
    idreservas = db.Column(db.Integer, primary_key=True)
    checkin = db.Column(db.Date, nullable=False)
    checkout = db.Column(db.Date, nullable=False)
    clientes_idclientes = db.Column(db.Integer, db.ForeignKey(
        'clientes.idclientes'), nullable=False)
    abono = db.Column(db.BigInteger, nullable=False)
    estado = db.Column(db.Boolean, nullable=True)


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
        return str(self.cedula)  # Flask-Login requiere que sea string


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
