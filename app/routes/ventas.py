from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.extensions import db
from app.models.models import Inventario, Ventas
from datetime import datetime

# Registrar el Blueprint
ventas_bp = Blueprint('ventas', __name__, url_prefix='/ventas')

@ventas_bp.route("/", methods=["GET", "POST"])
def ventas():
    productos = Inventario.query.all()

    if request.method == "POST":
        producto_id = request.form["producto_id"]
        cantidad_vendida = int(request.form["cantidad"])

        producto = Inventario.query.get(producto_id)

        if not producto:
            flash("Producto no encontrado.", "danger")
        elif cantidad_vendida > producto.cantidad:
            flash("No hay suficiente stock para esta venta.", "danger")
        else:
            # Crear registro de venta
            nueva_venta = Ventas(
                fecha=datetime.now(),
                cantidad=cantidad_vendida,
                precio=producto.precio,
                id_inventario=producto.id_inventario
            )
            db.session.add(nueva_venta)

            # Actualizar inventario
            producto.cantidad -= cantidad_vendida
            db.session.commit()

            flash("Venta registrada con éxito.", "success")
            return redirect(url_for('ventas.ventas'))

    return render_template("admin/ventas.html", productos=productos)

