from flask import Blueprint, render_template, request
from models import Cita, Pacientes, Medicos, Especialidad
from datetime import datetime
from sqlalchemy import func
from database import db

reportes_bp = Blueprint('reportes_bp', __name__)

# ----------------------------------------------------
# MENÚ PRINCIPAL DE REPORTES
# ----------------------------------------------------
@reportes_bp.route('/reportes')
def reportes_menu():
    return render_template('reportes/menu_reportes.html')


# ----------------------------------------------------
# REPORTE: CITAS POR DÍA
# ----------------------------------------------------
@reportes_bp.route('/reportes/citas-por-dia', methods=['GET', 'POST'])
def citas_por_dia():
    citas = []
    fecha_seleccionada = None
    total_citas = 0

    if request.method == 'POST':
        fecha_seleccionada = request.form.get('fecha')

        if fecha_seleccionada:
            fecha_dt = datetime.strptime(fecha_seleccionada, "%Y-%m-%d").date()
            citas = Cita.query.filter_by(fecha=fecha_dt).all()
            total_citas = len(citas)

    return render_template(
        'reportes/citas_por_dia.html',
        citas=citas,
        fecha=fecha_seleccionada,
        total_citas=total_citas
    )


# ----------------------------------------------------
# REPORTE: PACIENTES POR MÉDICO
# ----------------------------------------------------
@reportes_bp.route('/reportes/pacientes-por-medico', methods=['GET', 'POST'])
def pacientes_por_medico():
    medicos = Medicos.query.all()
    medico = None
    citas = []
    datos_grafico = {}

    if request.method == 'POST':
        medico_id = request.form.get('medico_id')

        if medico_id:
            medico = Medicos.query.get(medico_id)
            citas = Cita.query.filter_by(medicos_id=medico_id).all()

            # Contar citas por paciente
            for c in citas:
                nombre_paciente = f"{c.paciente.nombre} {c.paciente.apellido}"
                datos_grafico[nombre_paciente] = datos_grafico.get(nombre_paciente, 0) + 1

    return render_template(
        'reportes/pacientes_por_medico.html',
        medicos=medicos,
        medico=medico,
        citas=citas,
        datos_grafico=datos_grafico
    )



# ----------------------------------------------------
# REPORTE: ESPECIALIDADES MÁS SOLICITADAS
# ----------------------------------------------------
@reportes_bp.route('/reportes/especialidades-mas-solicitadas')
def especialidades_mas_solicitadas():

    resultados = (
        db.session.query(
            Especialidad.nombre_especialidad,
            func.count(Cita.id).label('total_citas')
        )
        .join(Medicos, Medicos.especialidad_id == Especialidad.id)
        .join(Cita, Cita.medicos_id == Medicos.id)
        .group_by(Especialidad.nombre_especialidad)
        .order_by(func.count(Cita.id).desc())
        .all()
    )

    return render_template(
        'reportes/especialidades_mas_solicitadas.html',
        resultados=resultados
    )
