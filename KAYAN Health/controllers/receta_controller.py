from flask import Blueprint, render_template, request, redirect, url_for, flash
from database import db
from models import Receta, Pacientes, Medicos
from flask_login import current_user
from controllers.decorators import requiere_roles
from flask_login import current_user, login_required



recetas_bp = Blueprint('recetas_bp', __name__, url_prefix='/recetas')


# ---------------------------------------------------------
# LISTAR RECETAS
# ---------------------------------------------------------
@recetas_bp.route('/')
def listar():
    # Obtener médico asociado al usuario (si es médico)
    medico = Medicos.query.filter_by(user_id=current_user.id).first()

    if medico:
        # Médico: solo ve sus recetas
        recetas = (
            db.session.query(Receta, Pacientes, Medicos)
            .join(Pacientes, Receta.pacientes_id == Pacientes.id)
            .join(Medicos, Receta.medicos_id == Medicos.id)
            .filter(Receta.medicos_id == medico.id)
            .all()
        )
    else:
        # Admin o Recepción: ven todas
        recetas = (
            db.session.query(Receta, Pacientes, Medicos)
            .join(Pacientes, Receta.pacientes_id == Pacientes.id)
            .join(Medicos, Receta.medicos_id == Medicos.id)
            .all()
        )

    return render_template('recetas/listar.html', recetas=recetas)


# ---------------------------------------------------------
# CREAR RECETA (ADMIN / RECEPCIÓN)
# ---------------------------------------------------------
@recetas_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        pacientes_id = request.form['pacientes_id']
        medicos_id = request.form['medicos_id']
        diagnostico = request.form['diagnostico']
        indicaciones = request.form['indicaciones']

        nueva_receta = Receta(
            pacientes_id=pacientes_id,
            medicos_id=medicos_id,
            diagnostico=diagnostico,
            indicaciones_generales=indicaciones
        )

        db.session.add(nueva_receta)
        db.session.commit()

        flash("Receta creada correctamente", "success")
        return redirect(url_for('recetas_bp.listar'))

    pacientes = Pacientes.query.all()
    medicos = Medicos.query.all()

    return render_template('recetas/crear.html', pacientes=pacientes, medicos=medicos)


# ---------------------------------------------------------
# CREAR RECETA (MÉDICO)
# ---------------------------------------------------------
@recetas_bp.route('/medico/crear', methods=['GET', 'POST'])
def crear_por_medico():
    # Obtener médico asociado al usuario
    medico = Medicos.query.filter_by(user_id=current_user.id).first()

    if not medico:
        flash("No tienes permiso para crear recetas como médico.", "danger")
        return redirect(url_for('recetas_bp.listar'))

    if request.method == 'POST':
        pacientes_id = request.form['paciente_id']
        diagnostico = request.form['diagnostico']
        indicaciones = request.form['indicaciones']

        nueva_receta = Receta(
            pacientes_id=pacientes_id,
            medicos_id=medico.id,
            diagnostico=diagnostico,
            indicaciones_generales=indicaciones
        )

        db.session.add(nueva_receta)
        db.session.commit()

        flash("Receta creada correctamente", "success")
        return redirect(url_for('recetas_bp.crear_por_medico'))

    pacientes = Pacientes.query.all()
    return render_template('recetas/crear_medico.html', pacientes=pacientes)


# ---------------------------------------------------------
# VER RECETA
# ---------------------------------------------------------
@recetas_bp.route('/ver/<int:id>')
def ver(id):
    receta = Receta.query.get_or_404(id)

    # Obtener médico asociado al usuario
    medico = Medicos.query.filter_by(user_id=current_user.id).first()

    # Si es médico, solo puede ver sus propias recetas
    if medico and receta.medicos_id != medico.id:
        flash("No tienes permiso para ver esta receta.", "danger")
        return redirect(url_for('recetas_bp.listar'))

    return render_template('recetas/ver.html', receta=receta)

# ---------------------------------------------------------
# ELIMNAR
# ---------------------------------------------------------

@recetas_bp.route('/recetas/eliminar/<int:id>', methods=['POST'])
@login_required
@requiere_roles('Admin', 'Medico')
def eliminar_receta(id):
    receta = Receta.query.get_or_404(id)
    try:
        db.session.delete(receta)
        db.session.commit()
        flash('Receta eliminada correctamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la receta: {str(e)}', 'danger')

    return redirect(url_for('recetas_bp.listar'))

