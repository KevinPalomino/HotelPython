# app/routes/auth_routes.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app.models.models import Persona
from app import db
from flask_login import login_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['correo']
        contrasena = request.form['contrasena']
        persona = Persona.query.filter_by(correo=correo).first()

        if not persona:
            flash("Usuario no encontrado", "danger")
            return redirect(url_for('auth.login'))

        rol_nombre = persona.rol.nombre.lower()  # <-- convertir a minúscula

        if rol_nombre not in ['administrador', 'recepcionista']:
            flash("No tienes permiso para iniciar sesión.", "danger")
            return redirect(url_for('auth.login'))

        if check_password_hash(persona.contrasena, contrasena):
            login_user(persona)
            flash(f"Bienvenido, {persona.nombre}", "success")

            if rol_nombre == 'administrador':
                return redirect(url_for('admin.panel_admin'))
            elif rol_nombre == 'recepcionista':
                return redirect(url_for('recepcion.panel_recepcionista'))
        else:
            flash("Contraseña incorrecta", "danger")

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada", "success")
    return redirect(url_for('auth.login'))
