from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from database import db
from models import Factura, FacturaDetalle, Pacientes, Servicio
import pdfkit
from datetime import datetime
from flask import make_response


facturas_bp = Blueprint('facturas_bp', __name__, url_prefix='/facturas')


# ---------------------------
#   VALIDACIÓN DE PERMISOS
# ---------------------------
def validar_acceso():
    if not current_user.is_authenticated:
        return False
    return current_user.role.nombre in ['Admin', 'Recepcion']


# ---------------------------
#   LISTAR FACTURAS
# ---------------------------
@facturas_bp.route('/')
def listar():
    if not validar_acceso():
        flash("No tienes permiso para ver facturas", "danger")
        return redirect(url_for('dashboard'))

    facturas = Factura.query.join(Pacientes).all()
    return render_template('facturas/listar.html', facturas=facturas)


# ---------------------------
#   CREAR FACTURA
# ---------------------------
@facturas_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if not validar_acceso():
        flash("No tienes permiso para crear facturas", "danger")
        return redirect(url_for('dashboard'))

    pacientes = Pacientes.query.all()
    servicios = Servicio.query.all()

    if request.method == 'POST':
        pacientes_id = request.form['pacientes_id']
        metodo_pago = request.form['metodo_pago']

        # Crear factura vacía (total se calcula luego)
        factura = Factura(
            pacientes_id=pacientes_id,
            metodo_pago=metodo_pago,
            total=0
        )
        db.session.add(factura)
        db.session.commit()

        # Procesar líneas de factura
        total = 0
        servicios_ids = request.form.getlist('servicio_id')
        descripciones = request.form.getlist('descripcion')
        precios = request.form.getlist('precio')

        for i in range(len(precios)):
            if precios[i].strip() == "":
                continue

            detalle = FacturaDetalle(
                factura_id=factura.id,
                servicio_id=servicios_ids[i] if servicios_ids[i] != "" else None,
                descripcion=descripciones[i],
                precio=float(precios[i])
            )

            total += float(precios[i])
            db.session.add(detalle)

        # Actualizar total
        factura.total = total
        db.session.commit()

        flash("Factura registrada correctamente", "success")
        return redirect(url_for('facturas_bp.listar'))

    return render_template('facturas/nuevo.html', pacientes=pacientes, servicios=servicios)


# ---------------------------
#   VER DETALLE DE FACTURA
# ---------------------------
@facturas_bp.route('/detalle/<int:id>')
def detalle(id):
    if not validar_acceso():
        flash("No tienes permiso para ver facturas", "danger")
        return redirect(url_for('dashboard'))

    factura = Factura.query.get_or_404(id)
    return render_template('facturas/detalle.html', factura=factura)

# ---------------------------
#   DESCARGAR PDF
# ---------------------------
@facturas_bp.route('/<int:id>/pdf')
def descargar_pdf(id):
    if not validar_acceso():
        flash("No tienes permiso para descargar facturas", "danger")
        return redirect(url_for('dashboard'))

    factura = Factura.query.get_or_404(id)

    html = render_template(
        "facturas/pdf_factura.html",
        factura=factura,
        fecha_actual=datetime.now()
    )

    config = pdfkit.configuration(
        wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    )

    pdf = pdfkit.from_string(html, False, configuration=config)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename=factura_{id}.pdf"

    return response

# ---------------------------
#   ELIMINAR FACTURA
# ---------------------------
@facturas_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    if not validar_acceso():
        flash("No tienes permiso para eliminar facturas", "danger")
        return redirect(url_for('dashboard'))

    factura = Factura.query.get_or_404(id)

    try:
        # Eliminar detalles primero (evita errores de FK)
        FacturaDetalle.query.filter_by(factura_id=id).delete()

        # Eliminar factura
        db.session.delete(factura)
        db.session.commit()

        flash("Factura eliminada correctamente", "success")

    except Exception as e:
        db.session.rollback()
        flash("No se pudo eliminar la factura. Verifique dependencias.", "danger")

    return redirect(url_for('facturas_bp.listar'))

# ---------------------------
#   EDITAR FACTURA
# ---------------------------
@facturas_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if not validar_acceso():
        flash("No tienes permiso para editar facturas", "danger")
        return redirect(url_for('dashboard'))

    factura = Factura.query.get_or_404(id)
    pacientes = Pacientes.query.all()
    servicios = Servicio.query.all()

    if request.method == 'POST':
        factura.pacientes_id = request.form['pacientes_id']
        factura.metodo_pago = request.form['metodo_pago']

        # Borrar detalles anteriores
        FacturaDetalle.query.filter_by(factura_id=id).delete()

        # Crear nuevos detalles
        total = 0
        servicios_ids = request.form.getlist('servicio_id')
        descripciones = request.form.getlist('descripcion')
        precios = request.form.getlist('precio')

        for i in range(len(precios)):
            if precios[i].strip() == "":
                continue

            detalle = FacturaDetalle(
                factura_id=factura.id,
                servicio_id=servicios_ids[i] if servicios_ids[i] != "" else None,
                descripcion=descripciones[i],
                precio=float(precios[i])
            )

            total += float(precios[i])
            db.session.add(detalle)

        factura.total = total
        db.session.commit()

        flash("Factura actualizada correctamente", "success")
        return redirect(url_for('facturas_bp.listar'))

    return render_template(
        'facturas/editar.html',
        factura=factura,
        pacientes=pacientes,
        servicios=servicios
    )
