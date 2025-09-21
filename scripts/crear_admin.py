from app import create_app, db
from app.models.models import Persona, Rol
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    # Buscar el rol administrador
    rol_admin = Rol.query.filter_by(nombre='Administrador').first()
    
    if not rol_admin:
        print("❌ Rol 'Administrador' no existe. Ejecuta primero setup_roles.py")
    else:
        cedula = 1234567890
        correo = 'admin@hotel.com'

        existente = Persona.query.filter_by(cedula=cedula).first()
        
        if existente:
            print("⚠️ Ya existe un usuario con esa cédula.")
        else:
            admin = Persona(
                cedula=cedula,
                nombre='Admin Principal',
                telefono=3001234567,
                direccion='Oficina Central',
                correo=correo,
                contrasena=generate_password_hash('admin123'),
                roles_idroles=rol_admin.idroles
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuario administrador creado correctamente.")
