from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, SelectField, DateField, TextAreaField
from wtforms.validators import DataRequired
from flask import Blueprint, render_template, redirect, url_for, flash
from database import db
from models import Cita, Pacientes, Medicos, Especialidad
from datetime import datetime, timedelta, date

citas_bp = Blueprint('citas_bp', __name__)

# -------------------------
# FORMULARIO
# -------------------------
class CitaForm(FlaskForm):
    paciente_id = HiddenField()

    especialidad_id = SelectField(
        'Especialidad',
        coerce=int,
        validators=[DataRequired()]
    )

    medicos_id = SelectField(
        'Médico',
        coerce=int,
        validators=[DataRequired()]
    )

    fecha = DateField(
        'Fecha',
        format='%Y-%m-%d',
        validators=[DataRequired()]
    )

    hora = SelectField(
        'Hora',
        choices=[],
        validators=[DataRequired()]
    )

    motivo = TextAreaField(
        'Motivo',
        validators=[DataRequired()]
    )

    estado = SelectField(
        'Estado',
        choices=[
            ('pendiente', 'Pendiente'),
            ('confirmada', 'Confirmada'),
            ('cancelada', 'Cancelada')
        ],
        default='pendiente'
    )

    submit = SubmitField('Guardar Cita')


# -------------------------
# CREAR CITA
# -------------------------
@citas_bp.route('/citas/nueva/<int:paciente_id>', methods=['GET', 'POST'])
def nueva_cita(paciente_id):
    paciente = Pacientes.query.get_or_404(paciente_id)
    form = CitaForm()
    form.paciente_id.data = paciente_id

    # Especialidades
    especialidades = Especialidad.query.all()
    form.especialidad_id.choices = [
        (e.id, e.nombre_especialidad) for e in especialidades
    ]

    # Médicos según especialidad
    if form.especialidad_id.data:
        medicos = Medicos.query.filter_by(
            especialidad_id=form.especialidad_id.data
        ).all()
        form.medicos_id.choices = [
            (m.id, f"{m.nombre} {m.apellido}") for m in medicos
        ]
    else:
        form.medicos_id.choices = []

    # -------------------------
    # HORAS DISPONIBLES
    # -------------------------
    horas_posibles = []
    horas_ocupadas = set()

    if form.medicos_id.data and form.fecha.data:
        medico_id = form.medicos_id.data
        fecha = form.fecha.data

        citas_existentes = Cita.query.filter_by(
            medicos_id=medico_id,
            fecha=fecha
        ).all()

        horas_ocupadas = {
            c.hora.strftime("%H:%M") for c in citas_existentes
        }

        inicio = datetime.strptime("08:00", "%H:%M").time()
        fin = datetime.strptime("17:00", "%H:%M").time()

        current = inicio
        while current <= fin:
            h = current.strftime("%H:%M")
            if h not in horas_ocupadas:
                horas_posibles.append(h)
            current = (
                datetime.combine(date.today(), current)
                + timedelta(minutes=30)
            ).time()

        form.hora.choices = [(h, h) for h in horas_posibles]
    else:
        form.hora.choices = []

    # -------------------------
    # GUARDAR CITA
    # -------------------------
    if form.validate_on_submit():
        nueva_cita = Cita(
            pacientes_id=paciente_id,
            medicos_id=form.medicos_id.data,
            fecha=form.fecha.data,
            hora=datetime.strptime(form.hora.data, "%H:%M").time(),
            motivo=form.motivo.data,
            estado=form.estado.data
        )

        db.session.add(nueva_cita)
        db.session.commit()

        flash("Cita creada correctamente", "success")
        return redirect(url_for('citas_bp.listar_citas'))

    return render_template(
        "citas/nuevo.html",
        form=form,
        paciente=paciente,
        horas_posibles=horas_posibles,
        horas_ocupadas=horas_ocupadas
    )


# -------------------------
# LISTAR CITAS
# -------------------------
@citas_bp.route('/citas')
def listar_citas():
    citas = Cita.query.order_by(
        Cita.fecha.desc(),
        Cita.hora.asc()
    ).all()
    return render_template('citas/listar.html', citas=citas)


# -------------------------
# DETALLE
# -------------------------
@citas_bp.route('/citas/detalle/<int:id>')
def detalle_cita(id):
    cita = Cita.query.get_or_404(id)
    return render_template('citas/detalle.html', cita=cita)


# -------------------------
# ELIMINAR
# -------------------------
@citas_bp.route('/citas/eliminar/<int:id>', methods=['POST'])
def eliminar_cita(id):
    cita = Cita.query.get_or_404(id)
    db.session.delete(cita)
    db.session.commit()
    flash("Cita eliminada correctamente", "success")
    return redirect(url_for('citas_bp.listar_citas'))

@citas_bp.route('/citas/editar/<int:id>', methods=['GET', 'POST'])
def editar_cita(id):
    cita = Cita.query.get_or_404(id)
    form = CitaForm(obj=cita)

    # Especialidades
    especialidades = Especialidad.query.all()
    form.especialidad_id.choices = [
        (e.id, e.nombre_especialidad) for e in especialidades
    ]

    # Médicos
    medicos = Medicos.query.all()
    form.medicos_id.choices = [
        (m.id, f"{m.nombre} {m.apellido}") for m in medicos
    ]

    # HORAS DISPONIBLES
    horas_posibles = []
    horas_ocupadas = set()

    if form.medicos_id.data and form.fecha.data:
        citas_existentes = Cita.query.filter_by(
            medicos_id=form.medicos_id.data,
            fecha=form.fecha.data
        ).all()

        horas_ocupadas = {
            c.hora.strftime("%H:%M")
            for c in citas_existentes if c.id != cita.id
        }

        inicio = datetime.strptime("08:00", "%H:%M").time()
        fin = datetime.strptime("17:00", "%H:%M").time()

        current = inicio
        while current <= fin:
            h = current.strftime("%H:%M")
            if h not in horas_ocupadas:
                horas_posibles.append(h)
            current = (
                datetime.combine(date.today(), current)
                + timedelta(minutes=30)
            ).time()

        form.hora.choices = [(h, h) for h in horas_posibles]

    if form.validate_on_submit():
        cita.medicos_id = form.medicos_id.data
        cita.fecha = form.fecha.data
        cita.hora = datetime.strptime(form.hora.data, "%H:%M").time()
        cita.motivo = form.motivo.data
        cita.estado = form.estado.data

        db.session.commit()
        flash("Cita actualizada correctamente", "success")
        return redirect(url_for('citas_bp.listar_citas'))

    return render_template(
        'citas/editar.html',
        form=form,
        cita=cita,
        horas_posibles=horas_posibles,
        horas_ocupadas=horas_ocupadas
    )
