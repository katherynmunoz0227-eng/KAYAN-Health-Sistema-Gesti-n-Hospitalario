from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user
from database import db
from models import Ingreso, Pacientes, Medicos, Habitacion, Cama
from sqlalchemy import func

ingresos_bp = Blueprint('ingresos_bp', __name__, url_prefix='/ingresos')


# ---------------------------
#   VALIDACIÓN DE PERMISOS
# ---------------------------
def puede_gestionar():
    return current_user.role.nombre in ['Admin', 'Recepcion']


# ---------------------------
#   LISTAR INGRESOS
# ---------------------------
@ingresos_bp.route('/')
def listar():
    # Obtener médico asociado al usuario
    medico = Medicos.query.filter_by(user_id=current_user.id).first()

    if medico:
        # Médico → solo ve sus ingresos
        ingresos = (
            Ingreso.query
            .join(Pacientes)
            .join(Cama)
            .filter(Ingreso.medicos_id == medico.id)   # ← CORREGIDO
            .all()
        )
    else:
        # Admin y Recepción ven todos
        ingresos = (
            Ingreso.query
            .join(Pacientes)
            .join(Cama)
            .all()
        )

    return render_template('ingresos/listar.html', ingresos=ingresos)


# ---------------------------
#   OBTENER CAMAS LIBRES POR HABITACIÓN (AJAX)
# ---------------------------
@ingresos_bp.route('/camas/<int:habitacion_id>')
def camas_por_habitacion(habitacion_id):
    camas = Cama.query.filter_by(habitacion_id=habitacion_id, estado='Libre').all()
    return {
        "camas": [
            {"id": c.id, "codigo": c.codigo}
            for c in camas
        ]
    }


# ---------------------------
#   CREAR INGRESO
# ---------------------------
@ingresos_bp.route('/crear', methods=['GET', 'POST'])
def crear():
    if not puede_gestionar():
        flash("No tienes permiso para registrar ingresos", "danger")
        return redirect(url_for('ingresos_bp.listar'))

    pacientes = Pacientes.query.all()
    medicos = Medicos.query.all()
    habitaciones = Habitacion.query.all()

    if request.method == 'POST':
        pacientes_id = request.form['pacientes_id']
        medico_id = request.form['medico_id']
        habitacion_id = request.form['habitacion_id']
        cama_id = request.form['cama_id']
        motivo = request.form['motivo']

        # Validar que la cama está libre
        cama = Cama.query.get(cama_id)

        # 1. Validar por estado
        if cama.estado != "Libre":
            flash("La cama seleccionada no está disponible", "danger")
            return redirect(url_for('ingresos_bp.crear'))

        # 2. Validar por ingresos activos (VALIDACIÓN REAL)
        ingreso_activo = Ingreso.query.filter_by(cama_id=cama_id, estado='Activo').first()
        if ingreso_activo:
            flash("La cama ya está asignada a otro paciente.", "danger")
            return redirect(url_for('ingresos_bp.crear'))


        # Crear ingreso
        ingreso = Ingreso(
            pacientes_id=pacientes_id,
            medicos_id=medico_id,   # ← CORREGIDO
            cama_id=cama_id,
            motivo=motivo
        )

        db.session.add(ingreso)

        # Cambiar estado de cama a OCUPADA
        cama.estado = 'Ocupada'

        db.session.commit()

        flash("Ingreso registrado correctamente", "success")
        return redirect(url_for('ingresos_bp.listar'))

    return render_template(
        'ingresos/nuevo.html',
        pacientes=pacientes,
        medicos=medicos,
        habitaciones=habitaciones
    )


# ---------------------------
#   DAR ALTA
# ---------------------------
@ingresos_bp.route('/alta/<int:id>', methods=['POST'])
def alta(id):
    if not puede_gestionar():
        flash("No tienes permiso para dar altas", "danger")
        return redirect(url_for('ingresos_bp.listar'))

    ingreso = Ingreso.query.get_or_404(id)

    ingreso.fecha_alta = func.now()
    ingreso.estado = 'Alta'

    # Cambiar cama a LIMPIEZA
    cama = Cama.query.get(ingreso.cama_id)
    cama.estado = 'Limpieza'

    db.session.commit()

    flash("Alta registrada correctamente", "success")
    return redirect(url_for('ingresos_bp.listar'))


# ---------------------------
#   DETALLE DE INGRESO
# ---------------------------
@ingresos_bp.route('/detalle/<int:id>')
def detalle(id):
    ingreso = Ingreso.query.get_or_404(id)

    # Obtener médico asociado al usuario
    medico = Medicos.query.filter_by(user_id=current_user.id).first()

    # Si es médico, solo puede ver sus propios ingresos
    if medico and ingreso.medicos_id != medico.id:   # ← CORREGIDO
        flash("No tienes permiso para ver este ingreso.", "danger")
        return redirect(url_for('ingresos_bp.listar'))

    return render_template('ingresos/detalle.html', ingreso=ingreso)


# ---------------------------
#   ELIMINAR INGRESO
# ---------------------------
@ingresos_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    if not puede_gestionar():
        flash("No tienes permiso para eliminar ingresos", "danger")
        return redirect(url_for('ingresos_bp.listar'))

    ingreso = Ingreso.query.get_or_404(id)

    try:
        # Liberar cama si estaba ocupada
        cama = Cama.query.get(ingreso.cama_id)
        if cama:
            # Si el ingreso estaba activo → la cama queda Libre
            # Si el ingreso estaba en Alta → la cama queda en Limpieza
            if ingreso.estado == 'Activo':
                cama.estado = 'Libre'
            else:
                cama.estado = 'Limpieza'

        db.session.delete(ingreso)
        db.session.commit()

        flash("Ingreso eliminado correctamente", "success")

    except Exception as e:
        db.session.rollback()
        flash("No se pudo eliminar el ingreso. Verifique dependencias.", "danger")

    return redirect(url_for('ingresos_bp.listar'))
