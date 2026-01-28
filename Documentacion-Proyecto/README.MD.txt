# KAYAN_Health – Sistema de Gestión Hospitalaria

## 📌 Descripción
KAYAN_Health es una aplicación web para la gestión integral de un hospital. Permite administrar:
- Pacientes, médicos y roles de usuario
- Citas médicas y horarios de médicos
- Habitaciones y camas
- Ingresos hospitalarios
- Facturación y detalle de servicios
- Recetas y historial clínico
- Reportes y consultas

La aplicación está desarrollada en **Python / Flask**, utilizando **SQLAlchemy** como ORM y **SQL Server** como base de datos.

---
## 🛠 Instalación
### Requisitos
- Python 3.9 o superior
- SQL Server
- pip
- Git (opcional)

### Pasos de instalación
1. Clonar el repositorio:
```bash
git clone <URL_DEL_REPOSITORIO>
cd KAYAN_Health

2. Instalar dependencias:
pip install -r requirements.txt

3. Configurar la base de datos:
Ejecutar el archivo script.sql en SQL Server para crear la base de datos y los datos de prueba.

Configurar la conexión en database.py o config.py:
SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://usuario:password@localhost/KAYAN_Health?driver=ODBC+Driver+17+for+SQL+Server"

4.Ejecutar la aplicación:
python app.py
5.Abrir el navegador en:
http://127.0.0.1:5000
🖥 Uso de la aplicación
Pacientes
Crear, editar, eliminar y listar pacientes
Gestión de historial clínico y recetas
Médicos
Gestión de médicos y especialidades
Asignación de horarios médicos
Citas
Registro de citas médicas
Estados: pendiente, confirmada, cancelada, atendida
Habitaciones y Camas
Administración de habitaciones
Control de disponibilidad de camas

Ingresos
Registro de ingresos hospitalarios
Asignación de cama y médico responsable
Facturación
Creación de facturas
Detalle de servicios y cálculo de totales
Reportes
Citas por médico
Ingresos activos
Facturación por paciente o fecha

### Herramientas
- **Git**: Control de versiones
- **VS Code**: Editor de código recomendado
- **SQL Server Management Studio (SSMS)**: Gestión de BD

📷 Capturas de pantalla






