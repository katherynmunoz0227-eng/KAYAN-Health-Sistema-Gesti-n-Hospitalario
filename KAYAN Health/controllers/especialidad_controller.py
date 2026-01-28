from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional
from controllers.decorators import requiere_roles
from controllers.medicos_controller import MedicosForm
from database import db
from models import Especialidad, Medicos

especialidad_bp = Blueprint('especialidad_bp', __name__)

class EspecialidadForm(FlaskForm):
    nombre_especialidad = StringField('Nombre de la Especialidad', validators=[DataRequired()])
    descripcion = StringField('Descripción', validators=[DataRequired()])

    submit = SubmitField('Registrar Especialidad') # Este es tu botón

# ------------------------- 
#        LISTAR 
# -------------------------

#Ruta para mostrar listado de especialidades
@especialidad_bp.route('/especialidades')
def listar():
    # Aquí iría la lógica para obtener y mostrar las especialidades
    lista_especialidades = Especialidad.query.all()
    return render_template('especialidad/listar.html', especialidades=lista_especialidades)

# ------------------------- 
#        NUEVO 
# -------------------------
#Ruta para agregar un nuevo especialidad
@especialidad_bp.route('/especialidad/nuevo', methods=['GET', 'POST'])   
@login_required 
@requiere_roles('Admin')     
def nuevo_especialidad():
    form = EspecialidadForm()

    #validacion del formulario
    if form.validate_on_submit():
        nueva_especialidad = Especialidad(
            nombre_especialidad=form.nombre_especialidad.data,
            descripcion=form.descripcion.data
        )
        # guardar en la base de datos
        db.session.add(nueva_especialidad)
        db.session.commit()
        flash('Especialidad registrada exitosamente!', 'success')
        return redirect(url_for('especialidad_bp.listar'))
    return render_template('especialidad/nuevo.html', form=form)

# ------------------------- 
#        EDITAR 
# -------------------------
#Ruta para editar un especialidad existente
@especialidad_bp.route('/especialidad/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@requiere_roles('Admin')
def editar_especialidad(id):
    especialidad = Especialidad.query.get_or_404(id)
    form = EspecialidadForm(obj=especialidad)

    if form.validate_on_submit():
        especialidad.nombre_especialidad = form.nombre_especialidad.data
        especialidad.descripcion = form.descripcion.data

        db.session.commit()
        flash('Especialidad actualizada exitosamente!', 'success')
        return redirect(url_for('especialidad_bp.listar'))

    return render_template('especialidad/editar.html', form=form, especialidad=especialidad)

# ------------------------- 
#        ELIMINAR 
# -------------------------
#Ruta para eliminar un especialidad
@especialidad_bp.route('/especialidad/eliminar/<int:id>', methods=['POST'])
@login_required
@requiere_roles('Admin')
def eliminar_especialidad(id):  
    especialidad = Especialidad.query.get_or_404(id)
    db.session.delete(especialidad)
    db.session.commit()
    flash('Especialidad eliminada exitosamente!', 'success')
    return redirect(url_for('especialidad_bp.listar'))

# ------------------------- 
#        VER DETALLES 
# -------------------------
#Ruta para ver detalles de un especialidad
@especialidad_bp.route('/especialidad/<int:id>')
def ver_especialidad(id):
    especialidad = Especialidad.query.get_or_404(id)
    return render_template('especialidad/detalle.html', especialidad=especialidad)      

# ------------------------- 
#        ASIGNAR ESPECIALIDAD 
# -------------------------
#Ruta para asignar especialidad a un medico
"""""@especialidad_bp.route('/asignar_especialidad', methods=['GET', 'POST'])
def asignar_especialidad():
    class AsignarEspecialidadForm(FlaskForm):
        medico = SelectField('Médico', coerce=int, validators=[DataRequired()])
        especialidad = SelectField('Especialidad', coerce=int, validators=[DataRequired()])
        submit = SubmitField('Asignar Especialidad')

    form = AsignarEspecialidadForm()
    form.medico.choices = [(medico.id, medico.nombre) for medico in Medicos.query.all()]
    form.especialidad.choices = [(esp.id, esp.nombre_especialidad) for esp in Especialidad.query.all()]

    if form.validate_on_submit():
        medico = Medicos.query.get(form.medico.data)
        especialidad = Especialidad.query.get(form.especialidad.data)

        if especialidad not in medico.especialidades:
            medico.especialidades.append(especialidad)
            db.session.commit()
            flash('Especialidad asignada exitosamente!', 'success')
        else:
            flash('El médico ya tiene esta especialidad asignada.', 'warning')

        return redirect(url_for('especialidad_bp.asignar_especialidad'))

    return render_template('especialidad/asignar.html', form=form)"""
