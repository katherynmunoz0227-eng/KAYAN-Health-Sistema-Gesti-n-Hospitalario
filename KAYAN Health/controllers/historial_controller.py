from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import HiddenField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional
from database import db
from models import Pacientes, Historial, Medicos
from datetime import datetime
from controllers.decorators import requiere_roles
from flask_login import login_required
from flask_login import current_user

historial_bp = Blueprint('historial_bp', __name__)

# -------------------------
# FORMULARIO AJUSTADO
# -------------------------
class HistorialForm(FlaskForm):
    pacientes_id = HiddenField()
    diagnostico = TextAreaField('Diagnóstico', validators=[DataRequired()])
    tratamiento = TextAreaField('Tratamiento', validators=[Optional()])
    observaciones = TextAreaField('Observaciones', validators=[Optional()])
    medicos_id = SelectField('Médico responsable', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')


# -------------------------
# VER HISTORIAL
# -------------------------
@historial_bp.route('/historial/<int:paciente_id>', methods=['GET'])
@login_required
@requiere_roles('Admin', 'Medico', 'Recepcion')
def ver_historial(paciente_id):
    paciente = Pacientes.query.get_or_404(paciente_id)
    registros = Historial.query.filter_by(pacientes_id=paciente_id).all()
    return render_template('historial/listar.html', paciente=paciente, registros=registros)

# -------------------------
# NUEVO REGISTRO
# -------------------------
@historial_bp.route('/historial/nuevo/<int:paciente_id>', methods=['GET', 'POST'])
@login_required
@requiere_roles('Admin', 'Medico')
def nuevo_registro(paciente_id):
    paciente = Pacientes.query.get_or_404(paciente_id)
    form = HistorialForm()
    form.pacientes_id.data = paciente_id

    # -------------------------
    # CARGAR MÉDICOS EN EL SELECT (solo para Admin)
    # -------------------------
    form.medicos_id.choices = [
        (0,"Seleccione un médico")
    ] + [
        (m.id, f"{m.nombre} {m.apellido}") for m in Medicos.query.all()
    ]

    # -------------------------
    # VALIDACIÓN DEL FORMULARIO
    # -------------------------
    if form.validate_on_submit():

        # -------------------------
        # SI EL USUARIO ES MÉDICO → SE ASIGNA A SÍ MISMO
        # -------------------------
        if current_user.role == "Medico":
            medico_id = current_user.medico_id

        # -------------------------
        # SI ES ADMIN → USA EL SELECT
        # -------------------------
        else:
            medico_id = form.medicos_id.data
            if medico_id == 0:
                flash("Debe seleccionar un médico responsable.", "danger")
                return render_template("historial/nuevo.html", form=form, paciente=paciente)


        # -------------------------
        # CREAR REGISTRO
        # -------------------------
        nuevo = Historial(
            pacientes_id=paciente_id,
            medicos_id=medico_id,
            fecha=datetime.now().date(),
            diagnostico=form.diagnostico.data,
            tratamiento=form.tratamiento.data,
            observaciones=form.observaciones.data
        )

        db.session.add(nuevo)
        db.session.commit()

        flash("Entrada agregada al historial clínico.", "success")
        return redirect(url_for('historial_bp.ver_historial', paciente_id=paciente_id))

    # -------------------------
    # RENDER INICIAL
    # -------------------------
    return render_template('historial/nuevo.html', form=form, paciente=paciente)

# -------------------------
# DETALLE
# -------------------------
@historial_bp.route('/historial/detalle/<int:id>')
def detalle_registro(id):
    registro = Historial.query.get_or_404(id)
    return render_template('historial/detalle.html', registro=registro)

# -------------------------
# EDITAR
# -------------------------
@historial_bp.route('/historial/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@requiere_roles('Admin', 'Medico')
def editar_registro(id):
    registro = Historial.query.get_or_404(id)
    form = HistorialForm(obj=registro)

    if form.validate_on_submit():
        registro.diagnostico = form.diagnostico.data
        registro.tratamiento = form.tratamiento.data
        registro.observaciones = form.observaciones.data

        db.session.commit()
        flash('Registro actualizado!', 'success')
        return redirect(url_for('historial_bp.ver_historial', paciente_id=registro.pacientes_id))

    return render_template('historial/editar.html', form=form, registro=registro)

# -------------------------
# ELIMINAR
# -------------------------
@historial_bp.route('/historial/eliminar/<int:id>', methods=['POST'])
def eliminar_registro(id):
    registro = Historial.query.get_or_404(id)
    paciente_id = registro.pacientes_id

    db.session.delete(registro)
    db.session.commit()

    flash('Registro eliminado!', 'success')
    return redirect(url_for('historial_bp.ver_historial', paciente_id=paciente_id))




