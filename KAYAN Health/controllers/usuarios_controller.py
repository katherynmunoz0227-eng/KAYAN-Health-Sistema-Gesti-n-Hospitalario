from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import User, Role, db
from werkzeug.security import generate_password_hash
from controllers.decorators import requiere_roles

usuarios_bp = Blueprint('usuarios_bp', __name__, url_prefix='/usuarios')


# ============================
#     LISTAR TODOS
# ============================
@usuarios_bp.route('/')
@login_required
@requiere_roles('Admin')
def listar_usuarios():
    usuarios = User.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios, filtro="Todos")


# ============================
#     LISTAR SOLO ADMIN
# ============================
@usuarios_bp.route('/admin')
@login_required
@requiere_roles('Admin')
def listar_admin():
    usuarios = User.query.filter_by(roles_id=1).all()
    return render_template('usuarios/listar.html', usuarios=usuarios, filtro="Admin")


# ============================
#     LISTAR SOLO MÉDICOS
# ============================
@usuarios_bp.route('/medicos')
@login_required
@requiere_roles('Admin')
def listar_medicos():
    usuarios = User.query.filter_by(roles_id=3).all()
    return render_template('usuarios/listar.html', usuarios=usuarios, filtro="Médicos")


# ============================
#     LISTAR SOLO RECEPCIÓN
# ============================
@usuarios_bp.route('/recepcion')
@login_required
@requiere_roles('Admin')
def listar_recepcion():
    usuarios = User.query.filter_by(roles_id=2).all()
    return render_template('usuarios/listar.html', usuarios=usuarios, filtro="Recepción")


# ============================
#     CREAR USUARIO
# ============================
@usuarios_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@requiere_roles('Admin')
def crear():
    roles = Role.query.all()

    if request.method == 'POST':
        username = request.form['username']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        password = request.form['password']
        rol_id = request.form['rol']

        nuevo = User(
            username=username,
            nombre=nombre,
            apellido=apellido,
            password_user=generate_password_hash(password),
            roles_id=rol_id
        )

        db.session.add(nuevo)
        db.session.commit()

        flash('Usuario creado correctamente', 'success')
        return redirect(url_for('usuarios_bp.listar_usuarios'))

    return render_template('usuarios/nuevo.html', roles=roles)


# ============================
#     EDITAR USUARIO
# ============================
@usuarios_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@requiere_roles('Admin')
def editar(id):
    usuario = User.query.get_or_404(id)
    roles = Role.query.all()

    if request.method == 'POST':
        usuario.username = request.form['username']
        usuario.nombre = request.form['nombre']
        usuario.apellido = request.form['apellido']
        usuario.roles_id = request.form['rol']

        if request.form['password']:
            usuario.password_user = generate_password_hash(request.form['password'])

        db.session.commit()
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('usuarios_bp.listar_usuarios'))

    return render_template('usuarios/editar.html', usuario=usuario, roles=roles)


# ============================
#     ELIMINAR USUARIO
# ============================
@usuarios_bp.route('/eliminar/<int:id>', methods=['POST'])
@login_required
@requiere_roles('Admin')
def eliminar(id):
    usuario = User.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()

    flash('Usuario eliminado correctamente', 'success')
    return redirect(url_for('usuarios_bp.listar_usuarios'))
