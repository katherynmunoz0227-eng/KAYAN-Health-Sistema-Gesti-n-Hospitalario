from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


# este decorador verifica si el usuario tiene uno de los roles permitidos
#Decoradores → controlan permisos y login


def requiere_roles(*roles_permitidos):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Debes iniciar sesión primero", "warning")
                return redirect(url_for("auth_bp.login"))

            if not current_user.role or current_user.role.nombre not in roles_permitidos:
                flash("No tienes permiso para acceder a esta sección", "danger")
                return redirect(url_for("dashboard"))

            return f(*args, **kwargs)
        return decorated_function
    return wrapper
