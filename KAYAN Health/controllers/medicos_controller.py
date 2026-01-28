from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, DateField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Optional
from database import db
from models import Medicos, Especialidad, Pacientes
from flask_login import login_required
from controllers.decorators import requiere_roles

medicos_bp = Blueprint('medicos_bp', __name__)


class MedicosForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    direccion = TextAreaField('Dirección')
    telefono = StringField('Teléfono')
    email = StringField('Email')
# para elegir la especialidad
    especialidad_id = SelectField('Especialidad', coerce=int, validators=[DataRequired()])

    submit = SubmitField('Registrar Médico') # Este es tu botón

# ------------------------- 
        # LISTAR 
# ------------------------
#Ruta para mostrar listado de médicos
@medicos_bp.route('/medicos')
@login_required 
@requiere_roles('Admin')
def listar():
    # Aquí iría la lógica para obtener y mostrar los médicos
    listar_medicos = Medicos.query.all()
    return render_template('medicos/listar.html', medicos=listar_medicos)


# ------------------------- 
        # NUEVO 
# ------------------------
#Ruta para agregar un nuevo paciente
@medicos_bp.route('/medicos/nuevo', methods=['GET', 'POST'])  
@login_required
@requiere_roles('Admin')      
def nuevo_medico():
    form = MedicosForm()

    form.especialidad_id.choices = [(e.id, e.nombre_especialidad) for e in Especialidad.query.all()]

    #validacion del formulario
    if form.validate_on_submit():
        nuevo_medico = Medicos(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            telefono=form.telefono.data,
            email=form.email.data,
            especialidad_id=form.especialidad_id.data
        )
        # guardar en la base de datos
        db.session.add(nuevo_medico)
        db.session.commit()
        flash('Médico registrado exitosamente!', 'success')
        return redirect(url_for('medicos_bp.listar'))
    return render_template('medicos/nuevo.html', form=form)

# ------------------------- 
        # EDITAR 
# ------------------------
@medicos_bp.route('/medicos/editar/<int:id>', methods=['GET', 'POST'])
@login_required 
@requiere_roles('Admin')
def editar_medico(id):  
    medico = Medicos.query.get_or_404(id) 
    form = MedicosForm(obj=medico) 
    form.especialidad_id.choices = [(e.id, e.nombre_especialidad) for e in Especialidad.query.all()] 
    if form.validate_on_submit(): 
        form.populate_obj(medico) 
        db.session.commit() 
        flash('Médico actualizado correctamente!', 'success')
        return redirect(url_for('medicos_bp.listar')) 

    return render_template('medicos/editar.html', form=form, medico=medico)

# ------------------------- 
        # ELIMINAR 
# ------------------------

@medicos_bp.route('/medicos/eliminar/<int:id>', methods=['POST']) 
@login_required
@requiere_roles('Admin')
def eliminar_medico(id): 
    medico = Medicos.query.get_or_404(id) 
    db.session.delete(medico) 
    db.session.commit() 
    flash('Médico eliminado correctamente!', 'success') 

    return redirect(url_for('medicos_bp.listar'))
# ------------------------- 
        # DETALLE 
# ------------------------

@medicos_bp.route('/medicos/detalle/<int:id>')
@login_required 
@requiere_roles('Admin','Medico')
def detalle_medico(id):
    medico = Medicos.query.get_or_404(id)
    return render_template('medicos/detalle.html', medico=medico)