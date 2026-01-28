from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from database import db 
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func

class Especialidad(db.Model):
    __tablename__ = 'Especialidad'
    id = db.Column(db.Integer, primary_key=True)
    nombre_especialidad = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    medicos = db.relationship('Medicos', back_populates='especialidad')

class Medicos(db.Model):
    __tablename__ = 'Medicos' 
    id = db.Column(db.Integer, primary_key=True) 
    nombre = db.Column(db.String(50), nullable=False) 
    apellido = db.Column(db.String(50), nullable=False) 
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('Especialidad.id'), nullable=True) 
 
    # RELACIONES:
    especialidad = db.relationship('Especialidad', back_populates='medicos')
    citas = db.relationship('Cita', back_populates='medico') 
    horarios = db.relationship('Horarios_Medicos', back_populates='medico')
    historial = db.relationship('Historial', backref='medico', lazy=True)

    user_id = db.Column(db.Integer, db.ForeignKey('Usuarios.id'))

class Pacientes(db.Model):
    __tablename__ = 'Pacientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date)
    direccion = db.Column(db.Text)
    telefono = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    
    # Se recomienda 'citas' en plural
    citas = db.relationship('Cita', back_populates='paciente')
    historial_medico = db.relationship('Historial', back_populates='paciente')

class Cita(db.Model):
    __tablename__ = 'Cita'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    motivo = db.Column(db.Text)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')
    
    medicos_id = db.Column(db.Integer, db.ForeignKey('Medicos.id'), nullable=False)
    pacientes_id = db.Column(db.Integer, db.ForeignKey('Pacientes.id'), nullable=False)
    
    # RELACIONES CORREGIDAS:
    # 'medico' (singular) coincide con Medicos.citas
    medico = db.relationship('Medicos', back_populates='citas')
    # 'paciente' (singular) coincide con Pacientes.citas
    paciente = db.relationship('Pacientes', back_populates='citas')

class Historial(db.Model):
    __tablename__ = 'Historial_clinico'
    id = db.Column(db.Integer, primary_key=True)
    medicos_id = db.Column(db.Integer, db.ForeignKey('Medicos.id'), nullable=False)
    pacientes_id = db.Column(db.Integer, db.ForeignKey('Pacientes.id'), nullable=False)

    fecha = db.Column(db.Date) # coincide con SQL 
    diagnostico = db.Column(db.Text) 
    tratamiento = db.Column(db.Text) 
    observaciones = db.Column(db.Text)

    # Relacion
    paciente = db.relationship('Pacientes', back_populates='historial_medico')

class Horarios_Medicos(db.Model):
    __tablename__ = 'horarios_medicos'
    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.String(20), nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)    
    hora_fin = db.Column(db.Time, nullable=False)   
    medicos_id = db.Column(db.Integer, db.ForeignKey('Medicos.id'), nullable=False)
    
    # 'medico' (singular) coincide con Medicos.horarios
    medico = db.relationship('Medicos', back_populates='horarios')

#-------------------------
# CREACION DE TABLAS PARA LOGIN
#------------------------

class Role(db.Model): 
    __tablename__ = 'Roles'
    id = db.Column(db.Integer, primary_key=True) 
    nombre = db.Column(db.String(50), unique=True, nullable=False) 
    usuarios = db.relationship('User', backref='role', lazy=True)
    
class User(UserMixin, db.Model): 
    __tablename__ = 'Usuarios'
    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(50), unique=True, nullable=False) 
    password_user = db.Column(db.String(200), nullable=False) # ← tu campo 
    roles_id = db.Column(db.Integer, db.ForeignKey('Roles.id'))
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))

   #medicos_id  = db.Column(db.Integer, db.ForeignKey('Medicos.id'))

# MÉTODO PARA GUARDAR CONTRASEÑA 

    def set_password(self, password): 
        self.password_user = generate_password_hash(password) 

# MÉTODO PARA VALIDAR CONTRASEÑA 
    def check_password(self, password): 
        return check_password_hash(self.password_user, password)
    

class Receta(db.Model):
     __tablename__ = 'recetas' 
     id = db.Column(db.Integer, primary_key=True) 
     fecha = db.Column(db.DateTime, default=datetime.utcnow) 
     pacientes_id = db.Column(db.Integer, db.ForeignKey('Pacientes.id'), nullable=False) 
     medicos_id = db.Column(db.Integer, db.ForeignKey('Medicos.id'), nullable=False) 
     diagnostico = db.Column(db.String(255), nullable=True) 
     indicaciones_generales = db.Column(db.Text, nullable=True)

     # Relaciones (si ya tienes modelos Pacientes y Medicos)
     paciente = db.relationship('Pacientes', backref='recetas', lazy=True)
     medico = db.relationship('Medicos', backref='recetas', lazy=True)

     def __repr__(self): return f'<Receta {self.id}>'


class Servicio(db.Model):
    __tablename__ = 'Servicios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    especialidad_id = db.Column(db.Integer, db.ForeignKey('Especialidad.id'), nullable=False)

    especialidad = db.relationship('Especialidad', backref='servicios')

class Factura(db.Model):
    __tablename__ = 'Facturas'

    id = db.Column(db.Integer, primary_key=True)
    pacientes_id = db.Column(db.Integer, db.ForeignKey('Pacientes.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=func.now())
    metodo_pago = db.Column(db.String(50), nullable=False)
    total = db.Column(db.Float, default=0)

    paciente = db.relationship('Pacientes', backref='facturas')
    detalles = db.relationship('FacturaDetalle', backref='factura', cascade="all, delete-orphan")

class FacturaDetalle(db.Model):
    __tablename__ = 'FacturaDetalle'

    id = db.Column(db.Integer, primary_key=True)
    factura_id = db.Column(db.Integer, db.ForeignKey('Facturas.id'), nullable=False)
    servicio_id = db.Column(db.Integer, db.ForeignKey('Servicios.id'), nullable=True)
    descripcion = db.Column(db.String(255), nullable=True)
    precio = db.Column(db.Float, nullable=False)

    servicio = db.relationship('Servicio')

class Habitacion(db.Model):
    __tablename__ = 'Habitaciones'

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), nullable=False)
    piso = db.Column(db.String(10), nullable=False)

    camas = db.relationship('Cama', backref='habitacion', cascade="all, delete-orphan")

class Cama(db.Model):
    __tablename__ = 'Camas'

    id = db.Column(db.Integer, primary_key=True)
    habitacion_id = db.Column(db.Integer, db.ForeignKey('Habitaciones.id'), nullable=False)
    codigo = db.Column(db.String(20), nullable=False)
    estado = db.Column(db.String(20), default='Libre')  # Libre, Ocupada, Limpieza, Mantenimiento

    ingresos = db.relationship('Ingreso', backref='cama')

class Ingreso(db.Model):
    __tablename__ = 'Ingresos'

    id = db.Column(db.Integer, primary_key=True)
    pacientes_id = db.Column(db.Integer, db.ForeignKey('Pacientes.id'), nullable=False)
    cama_id = db.Column(db.Integer, db.ForeignKey('Camas.id'), nullable=False)
    medicos_id = db.Column(db.Integer, db.ForeignKey('Medicos.id'), nullable=False)

    fecha_ingreso = db.Column(db.DateTime, default=func.now())
    fecha_alta = db.Column(db.DateTime, nullable=True)
    motivo = db.Column(db.String(255), nullable=False)
    estado = db.Column(db.String(20), default='Activo')  # Activo, Alta, Traslado

    paciente = db.relationship('Pacientes', backref='ingresos')
    medico = db.relationship('Medicos')

