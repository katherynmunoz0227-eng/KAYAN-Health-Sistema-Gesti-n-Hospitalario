from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from database import db
from models import Habitacion, Cama

habitaciones_bp = Blueprint('habitaciones_bp', __name__, url_prefix='/habitaciones')


# ---------------------------
#   VALIDACIÓN DE PERMISOS
# ---------------------------
def puede_gestionar():
    return current_user.role.nombre in ['Admin', 'Recepcion']


# ---------------------------
#   LISTAR HABITACIONES
# ---------------------------
@habitaciones_bp.route('/')
def listar():
    habitaciones = Habitacion.query.all()
    return render_template('habitaciones/listar.html', habitaciones=habitaciones)


# ---------------------------
#   CREAR HABITACIÓN Y CAMAS
# ---------------------------
@habitaciones_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if not puede_gestionar():
        flash("No tienes permiso para crear habitaciones", "danger")
        return redirect(url_for('habitaciones_bp.listar'))

    if request.method == 'POST':
        numero = request.form['numero']
        piso = request.form['piso']
        cantidad_camas = int(request.form['cantidad_camas'])

        # Validación de máximo 4 camas
        if cantidad_camas < 1 or cantidad_camas > 4:
            flash("La habitación debe tener entre 1 y 4 camas", "danger")
            return redirect(url_for('habitaciones_bp.crear'))

        # Crear habitación
        nueva = Habitacion(numero=numero, piso=piso)
        db.session.add(nueva)
        db.session.commit()

        # Crear camas automáticamente
        for i in range(cantidad_camas):
            cama = Cama(
                habitacion_id=nueva.id,
                codigo=f"{numero}-{i+1}",
                estado="Libre"
            )
            db.session.add(cama)

        db.session.commit()

        flash("Habitación y camas creadas correctamente", "success")
        return redirect(url_for('habitaciones_bp.listar'))

    return render_template('habitaciones/nuevo.html')

# ---------------------------
#   EDITAR HABITACIÓN   
# ---------------------------

@habitaciones_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    habitacion = Habitacion.query.get_or_404(id)

    if request.method == 'POST':
        habitacion.numero = request.form['numero']
        habitacion.piso = request.form['piso']
        habitacion.estado = request.form['estado']

        db.session.commit()
        flash('Habitación actualizada', 'success')
        return redirect(url_for('habitaciones_bp.listar'))

    return render_template('habitaciones/editar.html', habitacion=habitacion)


# ---------------------------
#   ELIMINAR HABITACIÓN
# ---------------------------

@habitaciones_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    habitacion = Habitacion.query.get_or_404(id)
    db.session.delete(habitacion)
    db.session.commit()

    flash('Habitación eliminada', 'info')
    return redirect(url_for('habitaciones_bp.listar'))

