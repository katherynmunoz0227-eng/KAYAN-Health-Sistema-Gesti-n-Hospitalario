from flask import Flask, render_template, session
from database import db
from models import Medicos, Pacientes, Cita, Historial, Especialidad, Horarios_Medicos, User
from sqlalchemy import func
from flask_login import LoginManager, login_required
from flask import redirect, url_for

app = Flask(__name__)
connection_string = "mssql+pyodbc://DESKTOP-96AU1TL/PruebaH?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"

app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SECRET_KEY'] = 'una_clave_muy_secreta_123'

db.init_app(app)

@app.route('/')
def inicio():
    return redirect(url_for('auth_bp.login'))

# Blueprints
from controllers.medicos_controller import medicos_bp
from controllers.pacientes_controller import pacientes_bp
from controllers.citas_controller import citas_bp
from controllers.especialidad_controller import especialidad_bp
from controllers.historial_controller import historial_bp
from controllers.horario_controller import horario_bp
from controllers.auth_controller import auth_bp   # ← IMPORTANTE
from controllers.reportes_controller import reportes_bp
from controllers.usuarios_controller import usuarios_bp 
from controllers.servicios_controller import servicios_bp
from controllers.facturas_controller import facturas_bp
from controllers.habitaciones_controller import habitaciones_bp
from controllers.camas_controller import camas_bp
from controllers.ingresos_controller import ingresos_bp
from controllers.receta_controller import recetas_bp

app.register_blueprint(recetas_bp)
app.register_blueprint(ingresos_bp)
app.register_blueprint(camas_bp)
app.register_blueprint(habitaciones_bp)
app.register_blueprint(facturas_bp)
app.register_blueprint(servicios_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(medicos_bp)
app.register_blueprint(pacientes_bp)
app.register_blueprint(citas_bp)
app.register_blueprint(especialidad_bp)
app.register_blueprint(historial_bp)
app.register_blueprint(horario_bp)
app.register_blueprint(auth_bp)  # ← IMPORTANTE
app.register_blueprint(reportes_bp)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth_bp.login'


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/logout')
def logout():
    session.clear()   # Limpia toda la sesión
    return redirect('inicio')


if __name__ == '__main__':
    app.run(debug=True)



