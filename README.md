# KAYAN-Health-Sistema-Gesti-n-Hospitalario


🏥 KAYAN Health 

Sistema de Gestión HospitalariaKAYAN Health es una aplicación web robusta diseñada para centralizar y optimizar la gestión administrativa y clínica de centros médicos. Este sistema permite el control de pacientes, citas y personal, asegurando la integridad de los datos y una experiencia de usuario fluida.🛠️ Tecnologías y ArquitecturaEl proyecto se ha desarrollado siguiendo los más altos estándares de calidad exigidos en la rúbrica:+1Arquitectura: Patrón MVC (Modelo-Vista-Controlador) para una separación clara de responsabilidades.Backend: Python 3.x con Flask.ORM: SQLAlchemy para la gestión eficiente de la base de datos.Base de Datos: Microsoft SQL Server con diseño normalizado en 3FN.Frontend: Interfaz responsive construida con HTML5, CSS3, JavaScript y Bootstrap 5.Motor de Plantillas: Jinja2.⚙️ Instalación y ConfiguraciónSigue estos pasos para desplegar el entorno de desarrollo localmente:1. Requisitos PreviosPython 3.8 o superior.Microsoft SQL Server.ODBC Driver 17 para SQL Server.2. Clonar y Preparar EntornoBash# Clonar repositorio
git clone https://github.com/tu-usuario/kayan-health.git
cd kayan-health

# Crear y activar entorno virtual
python -m venv venv
# En Windows:
venv\Scripts\activate
3. Instalar DependenciasBashpip install -r requirements.txt
4. Configuración de Base de DatosEjecuta el script SQL ubicado en /database/script.sql en tu instancia de SQL Server para crear las tablas y cargar los datos de prueba (10+ registros por tabla requeridos).+1Configura tu cadena de conexión en el archivo .env o config.py:mssql+pyodbc://usuario:password@servidor/KayanHealth?driver=ODBC+Driver+17+for+SQL+Server🚀 Uso de la AplicaciónPara iniciar el sistema, ejecuta:Bashflask run
Luego, abre tu navegador en http://127.0.0.1:5000.Funcionalidades principales:+1Gestión CRUD: Registro, edición, visualización y eliminación de pacientes y citas médicos con validaciones completas.Reportes Avanzados: Consultas con Joins y agregaciones para estadísticas de consultas y ocupación.Validaciones: Control de errores tanto en Frontend (JS) como en Backend (Python).+1📸 ScreenshotsDashboard de ControlRegistro de Pacientes📂 Estructura del Proyecto (MVC)PlaintextKAYAN_HEALTH/
├── app/
│   ├── models/       # Modelos de SQLAlchemy (Base de Datos) 
│   ├── controllers/  # Lógica de rutas y controladores 
│   ├── static/       # Archivos CSS, JS e imágenes
│   └── templates/    # Vistas en Jinja2 (HTML + Bootstrap) [cite: 27]
├── database/         # Scripts SQL de estructura y datos [cite: 61]
├── requirements.txt  # Dependencias del proyecto
└── run.py            # Punto de entrada de la aplicación
📝 Documentación de CódigoTodo el código fuente cuenta con Docstrings y comentarios detallados que explican la lógica de negocio y el manejo de excepciones, cumpliendo con los estándares de calidad técnica.¿Qué sigue ahora?Para que el archivo quede perfecto, te sugiero lo siguiente:Asegúrate de tener el archivo requirements.txt listo. Si no sabes cómo crearlo, dime y te doy el comando.Sube un par de fotos de tu programa a una carpeta llamada screenshots para que los enlaces del README funcionen.¿Te gustaría que te ayude a redactar la sección de "Reportes" basándome en alguna consulta SQL que ya tengas?
