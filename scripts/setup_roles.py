from app import create_app, db
from app.models.models import Rol

app = create_app()

with app.app_context():
    roles = ['Administrador', 'Recepcionista', 'Cliente']

    for nombre in roles:
        if not Rol.query.filter_by(nombre=nombre).first():
            nuevo_rol = Rol(nombre=nombre)
            db.session.add(nuevo_rol)

    db.session.commit()
    print("✅ Roles creados correctamente.")
