from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from database import db
from models import Habitacion, Cama
from controllers.decorators import requiere_roles
from flask_login import current_user, login_required

camas_bp = Blueprint('camas_bp', __name__, url_prefix='/camas')


# ---------------------------
#   VALIDACIÓN DE PERMISOS
# ---------------------------
def puede_gestionar():
    return current_user.role.nombre in ['Admin', 'Recepcion']


# ---------------------------
#   LISTAR CAMAS POR HABITACIÓN
# ---------------------------
@camas_bp.route('/<int:habitacion_id>')
def listar(habitacion_id):
    habitacion = Habitacion.query.get_or_404(habitacion_id)
    camas = Cama.query.filter_by(habitacion_id=habitacion_id).all()

    return render_template('camas/listar.html', habitacion=habitacion, camas=camas)


# ---------------------------
#   CREAR CAMA
# ---------------------------
@camas_bp.route('/crear/<int:habitacion_id>', methods=['GET', 'POST'])
def crear(habitacion_id):
    if not puede_gestionar():
        flash("No tienes permiso para crear camas", "danger")
        return redirect(url_for('habitaciones_bp.listar'))

    habitacion = Habitacion.query.get_or_404(habitacion_id)

    if request.method == 'POST':
        codigo = request.form['codigo']
        estado = request.form['estado']

        nueva = Cama(
            habitacion_id=habitacion_id,
            codigo=codigo,
            estado=estado
        )

        db.session.add(nueva)
        db.session.commit()

        flash("Cama creada correctamente", "success")
        return redirect(url_for('camas_bp.listar', habitacion_id=habitacion_id))

    return render_template('camas/nuevo.html', habitacion=habitacion)


# ---------------------------
#   CAMBIAR ESTADO DE CAMA
# ---------------------------
@camas_bp.route('/estado/<int:id>', methods=['POST'])
def cambiar_estado(id):
    if not puede_gestionar():
        flash("No tienes permiso para cambiar estados", "danger")
        return redirect(url_for('habitaciones_bp.listar'))

    cama = Cama.query.get_or_404(id)
    nuevo_estado = request.form['estado']

    cama.estado = nuevo_estado
    db.session.commit()

    flash("Estado actualizado correctamente", "success")
    return redirect(url_for('camas_bp.listar', habitacion_id=cama.habitacion_id))


# ---------------------------
#   ELIMINAR 
# ---------------------------

@camas_bp.route('/camas/eliminar/<int:id>', methods=['POST'])
@login_required
@requiere_roles('Admin', 'Recepcion')
def eliminar_cama(id):
    cama = Cama.query.get_or_404(id)

    try:
        db.session.delete(cama)
        db.session.commit()
        flash('Cama eliminada correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la cama: {str(e)}', 'danger')

    return redirect(url_for('camas_bp.listar', habitacion_id=cama.habitacion_id))
