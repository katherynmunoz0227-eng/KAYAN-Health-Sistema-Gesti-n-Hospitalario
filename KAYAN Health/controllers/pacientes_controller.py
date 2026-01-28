from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional
from database import db
from models import Pacientes, Cita, Ingreso, Medicos, Cama, Habitacion
from controllers.decorators import requiere_roles
from flask_login import current_user, login_required

pacientes_bp = Blueprint('pacientes_bp', __name__)


class PatientForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    fecha_nacimiento = DateField('Fecha de nacimiento', format='%Y-%m-%d', validators=[Optional()])
    direccion = TextAreaField('Dirección')
    telefono = StringField('Teléfono')
    email = StringField('Email')

    submit = SubmitField('Registrar Paciente')


# -------------------------
# LISTAR
# -------------------------
@pacientes_bp.route('/pacientes')
@login_required
@requiere_roles('Admin', 'Medico', 'Recepcion')
def listar():

    # Obtener médico asociado al usuario logueado
    medico = Medicos.query.filter_by(user_id=current_user.id).first()

    if medico:
        # Pacientes que tienen citas o ingresos con este médico
        pacientes = (
            Pacientes.query
            .outerjoin(Cita, Cita.pacientes_id == Pacientes.id)
            .outerjoin(Ingreso, Ingreso.pacientes_id == Pacientes.id)
            .filter(
                (Cita.medicos_id == medico.id) |
                (Ingreso.medicos_id == medico.id)
            )
            .distinct()
            .all()
        )
    else:
        pacientes = Pacientes.query.all()

    return render_template('pacientes/listar.html', pacientes=pacientes)


# -------------------------
# NUEVO
# -------------------------
@pacientes_bp.route('/pacientes/nuevo', methods=['GET', 'POST'])
@login_required
@requiere_roles('Admin', 'Recepcion')
def nuevo_paciente():
    form = PatientForm()

    if form.validate_on_submit():
        nuevo_paciente = Pacientes(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            fecha_nacimiento=form.fecha_nacimiento.data,
            direccion=form.direccion.data,
            telefono=form.telefono.data,
            email=form.email.data
        )

        db.session.add(nuevo_paciente)
        db.session.commit()
        flash('Paciente registrado exitosamente!', 'success')
        return redirect(url_for('pacientes_bp.listar'))

    return render_template('pacientes/nuevo.html', form=form)


# -------------------------
# EDITAR
# -------------------------
@pacientes_bp.route('/pacientes/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@requiere_roles('Admin', 'Medico', 'Recepcion')
def editar_paciente(id):
    paciente = Pacientes.query.get_or_404(id)
    form = PatientForm(obj=paciente)

    if form.validate_on_submit():
        form.populate_obj(paciente)
        db.session.commit()
        flash('Paciente actualizado correctamente!', 'success')
        return redirect(url_for('pacientes_bp.listar'))

    return render_template('pacientes/editar.html', form=form, paciente=paciente)


# -------------------------
# DETALLE
# -------------------------
@pacientes_bp.route('/pacientes/<int:id>')
@login_required
@requiere_roles('Admin', 'Medico', 'Recepcion')
def detalle_paciente(id):

    paciente = Pacientes.query.get_or_404(id)

    # Obtener médico logueado
    medico = Medicos.query.filter_by(user_id=current_user.id).first()

    # Si es médico, validar que este paciente le pertenece
    if medico:
        tiene_relacion = (
            Cita.query.filter_by(pacientes_id=id, medicos_id=medico.id).first() or
            Ingreso.query.filter_by(pacientes_id=id, medicos_id=medico.id).first()
        )

        if not tiene_relacion:
            flash("No tienes permiso para ver este paciente.", "danger")
            return redirect(url_for('pacientes_bp.listar'))

    # Obtener ingresos del paciente (historial)
    ingresos = (
        Ingreso.query 
        .join(Cama) 
        .join(Habitacion) 
        .filter(Ingreso.pacientes_id == id) 
        .order_by(Ingreso.fecha_ingreso.desc()) 
        .all()
    )

    # Obtener ingreso actual (si está internado)
    ingreso_actual = (
        Ingreso.query 
        .join(Cama) 
        .join(Habitacion) 
        .filter(Ingreso.pacientes_id == id, Ingreso.estado == 'Activo') 
        .first()
    )

    # Obtener citas del paciente con este médico
    citas = None
    if medico:
        citas = Cita.query.filter_by(pacientes_id=id, medicos_id=medico.id).all()
    else:
        citas = Cita.query.filter_by(pacientes_id=id).all()

    return render_template(
        'pacientes/detalle.html',
        paciente=paciente,
        ingresos=ingresos,
        ingreso_actual=ingreso_actual,
        citas=citas
    )

# -------------------------
# ELIMINAR
# -------------------------
@pacientes_bp.route('/pacientes/eliminar/<int:id>', methods=['POST'])
@login_required
@requiere_roles('Admin', 'Recepcion')
def eliminar_paciente(id):
    paciente = Pacientes.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    flash('Paciente eliminado correctamente!', 'success')
    return redirect(url_for('pacientes_bp.listar'))
