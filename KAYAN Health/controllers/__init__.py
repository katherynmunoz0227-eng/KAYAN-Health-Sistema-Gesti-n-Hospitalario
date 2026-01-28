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


__all__ = [
    "medicos_bp",
    "pacientes_bp",
    "citas_bp",
    "especialidad_bp",
    "historial_bp",
    "horario_bp",
    "reportes_bp",
    "auth_bp",
    "usuarios_bp",
    "servicios_bp", 
    "facturas_bp",
    "habitaciones_bp",
    "camas_bp",
    "ingresos_bp"
    "recetas_bp"
]
