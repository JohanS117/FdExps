# config/database.py
# Capa de configuración - Conexión a base de datos

import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "foodexpress_db"
}

def get_connection():
    """Obtiene una conexión a la base de datos"""
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        return conexion
    except Error as e:
        print(f"Error de conexión: {e}")
        return None

def close_connection(conexion):
    """Cierra la conexión a la base de datos"""
    if conexion and conexion.is_connected():
        conexion.close()