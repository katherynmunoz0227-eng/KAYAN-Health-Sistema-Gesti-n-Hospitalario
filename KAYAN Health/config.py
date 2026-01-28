import os

""""class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    
    # Chaîne de connexion corrigée pour ton instance SQL Server Express
    SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://DESKTOP-96AU1TL\\SQLEXPRESS01/HospitalDB?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False """"

#Configuración de la conexión a SQL Server"""

import os
import pyodbc

class Config:
    SERVER = r'localhost'
    DATABASE = 'PruebaH'
    USERNAME = 'sa'
    PASSWORD = '12345'
    DRIVER = 'ODBC Driver 17 for SQL Server'

    @staticmethod
    def get_connection_string(use_windows_auth=True):
        if use_windows_auth:
            return (
                f"DRIVER={{{Config.DRIVER}}};"
                f"SERVER={Config.SERVER};"
                f"DATABASE={Config.DATABASE};"
                f"Trusted_Connection=yes;"
            )
        else:
            return (
                f"DRIVER={{{Config.DRIVER}}};"
                f"SERVER={Config.SERVER};"
                f"DATABASE={Config.DATABASE};"
                f"UID={Config.USERNAME};"
                f"PWD={Config.PASSWORD};"
            )

    @staticmethod
    def verificar_drivers_disponibles():
        return pyodbc.drivers()

    @staticmethod
    def test_conexion(use_windows_auth=True):
        try:
            conn_string = Config.get_connection_string(use_windows_auth)
            conn = pyodbc.connect(conn_string)

            print("✓ Conexión exitosa a SQL Server")

            cursor = conn.cursor()
            cursor.execute("SELECT @@VERSION")
            version = cursor.fetchone()[0]

            print("\nVersión de SQL Server:")
            print(version)

            cursor.close()
            conn.close()

            return True, "Conexión correcta"

        except Exception as e:
            return False, str(e)

def main():
    print("="*60)
    print("CONFIGURACIÓN CONEXIÓN SQL SERVER")
    print("="*60)

    print("\nDrivers ODBC disponibles:")
    print(Config.verificar_drivers_disponibles())

    print("\nProbando conexión con Windows Authentication...")
    success, message = Config.test_conexion(use_windows_auth=True)

    if success:
        print("[OK]", message)
    else:
        print("[ERROR]", message)

if __name__ == "__main__":
    main()