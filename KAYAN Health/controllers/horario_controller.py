# controllers/horario_controller.py

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, TimeField
from wtforms.validators import DataRequired
from controllers.decorators import requiere_roles
from database import db
from models import Horarios_Medicos, Medicos


horario_bp = Blueprint('horario_bp', __name__)

# --- AQUÍ VA EL CÓDIGO DEL FORMULARIO ---
class HorarioForm(FlaskForm):
    dia_semana = SelectField('Día de la Semana', choices=[
        ('Lunes', 'Lunes'),
        ('Martes', 'Martes'), 
        ('Miércoles', 'Miércoles'), 
        ('Jueves', 'Jueves'), 
        ('Viernes', 'Viernes'), 
        ('Sábado', 'Sábado'), 
        ('Domingo', 'Domingo')
    ], validators=[DataRequired()])
    
    hora_inicio = TimeField('Hora de Inicio', validators=[DataRequired()])
    hora_fin = TimeField('Hora de Fin', validators=[DataRequired()])
    
    # Este SelectField se llenará dinámicamente en la ruta
    medicos_id = SelectField('Médico', coerce=int, validators=[DataRequired()])
    
    submit = SubmitField('Asignar Horario')

# -------------------------
#        LISTAR
# -------------------------
@horario_bp.route('/horarios')
def listar(): 
    horarios = Horarios_Medicos.query.all() 
    return render_template('horarios/listar.html', horarios=horarios)

# -------------------------
#        NUEVO
# -------------------------
@horario_bp.route('/horarios/nuevo', methods=['GET', 'POST'])
@login_required 
@requiere_roles('Admin')
def nuevo_horario():
    form = HorarioForm()
    # Importante: llenar los médicos antes de validar
    form.medicos_id.choices = [(m.id, f"{m.nombre} {m.apellido}") for m in Medicos.query.all()]
    if form.validate_on_submit():
        nuevo_horario = Horarios_Medicos(
            dia_semana=form.dia_semana.data,
            hora_inicio=form.hora_inicio.data,
            hora_fin=form.hora_fin.data,
            medicos_id=form.medicos_id.data
        )
        db.session.add(nuevo_horario)
        db.session.commit()
        flash('Horario asignado correctamente.', 'success')
        return redirect(url_for('horario_bp.listar'))
    return render_template('horarios/nuevo.html', form=form)

# -------------------------
#        EDITAR
# -------------------------

@horario_bp.route('/horarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@requiere_roles('Admin')
def editar(id): 
    horario = Horarios_Medicos.query.get_or_404(id)
    form = HorarioForm(obj=horario)
    form.medicos_id.choices = [(m.id, f"{m.nombre} {m.apellido}") for m in Medicos.query.all()]

    if form.validate_on_submit():
        form.populate_obj(horario)
        db.session.commit()
        flash('Horario actualizado!', 'success')
        return redirect(url_for('horario_bp.listar'))

    return render_template('horarios/editar.html', form=form, horario=horario)


# -------------------------
#        ELIMINAR
# -------------------------

@horario_bp.route('/horarios/eliminar/<int:id>', methods=['POST'])
@login_required 
@requiere_roles('Admin')
def eliminar(id):
    horario = Horarios_Medicos.query.get_or_404(id)
    db.session.delete(horario)
    db.session.commit()
    flash('Horario eliminado!', 'success')
    return redirect(url_for('horario_bp.listar'))
