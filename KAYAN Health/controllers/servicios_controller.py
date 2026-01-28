from flask import render_template, request, redirect, url_for, flash
from database import db
from models import Servicio, Especialidad
from flask_login import current_user

from flask import Blueprint
servicios_bp = Blueprint('servicios_bp', __name__, url_prefix='/servicios')

class ServiciosController:

    @staticmethod
    @servicios_bp.route('/')
    def listar():
        if current_user.role.nombre not in ['Admin']:
            flash("No tienes permiso para ver servicios", "danger")
            return redirect(url_for('dashboard'))

        servicios = Servicio.query.join(Especialidad).all()
        return render_template('servicios/listar.html', servicios=servicios)

    @staticmethod
    @servicios_bp.route('/crear', methods=['GET', 'POST'])
    def crear():
        if current_user.role.nombre not in ['Admin']:
            flash("No tienes permiso para crear servicios", "danger")
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            nombre = request.form['nombre']
            precio = request.form['precio']
            especialidad_id = request.form['especialidad_id']

            nuevo_servicio = Servicio(
                nombre=nombre,
                precio=precio,
                especialidad_id=especialidad_id
            )

            db.session.add(nuevo_servicio)
            db.session.commit()

            flash("Servicio registrado correctamente", "success")
            return redirect(url_for('servicios_bp.listar'))

        especialidades = Especialidad.query.all()
        return render_template('servicios/nuevo.html', especialidades=especialidades)
    
    
    @staticmethod
    @servicios_bp.route('/eliminar/<int:id>', methods=['POST'])
    def eliminar(id):
        if current_user.role.nombre not in ['Admin']:
            flash("No tienes permiso para eliminar servicios", "danger")
            return redirect(url_for('dashboard'))

        servicio = Servicio.query.get_or_404(id)

        try:
            db.session.delete(servicio)
            db.session.commit()
            flash("Servicio eliminado correctamente", "success")

        except Exception as e:
            db.session.rollback()
            flash("No se pudo eliminar el servicio. Verifique dependencias.", "danger")

        return redirect(url_for('servicios_bp.listar'))
