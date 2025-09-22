# app/routes/ventas.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.models import Inventario, Ventas
from app.extensions import db
from datetime import datetime

ventas_bp = Blueprint("ventas", __name__, url_prefix="/ventas")

@ventas_bp.route("/", methods=["GET", "POST"])
def ventas():
    if request.method == "POST":
        try:
            producto_id = request.form.get("producto_id")   # viene del select
            cantidad_vendida = int(request.form.get("cantidad"))

            # Buscar producto en inventario
            producto = Inventario.query.get(producto_id)
            if not producto:
                flash("❌ Producto no encontrado.", "danger")
                return redirect(url_for("ventas.ventas"))

            # Verificar stock
            if producto.cantidad < cantidad_vendida:
                flash("⚠️ No hay suficiente stock disponible.", "warning")
                return redirect(url_for("ventas.ventas"))

            # Registrar venta
            nueva_venta = Ventas(
                fecha=datetime.now(),
                cantidad=cantidad_vendida,
                precio=producto.precio,
                id_inventario=producto.idinventario  # ✅ aquí estaba el error
            )
            db.session.add(nueva_venta)

            # Actualizar stock
            producto.cantidad -= cantidad_vendida
            db.session.commit()

            flash("✅ Venta registrada con éxito.", "success")
            return redirect(url_for("ventas.ventas"))

        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error al registrar la venta: {str(e)}", "danger")
            return redirect(url_for("ventas.ventas"))

    # Si es GET: mostrar productos y ventas
    productos = Inventario.query.all()
    ventas = Ventas.query.all()
    return render_template("admin/ventas.html", productos=productos, ventas=ventas)
