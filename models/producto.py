# models/producto.py
# Modelo de Producto

from config.database import conectar_bd, cerrar_conexion

class Producto:
    
    @staticmethod
    def obtener_todos():
        """Obtiene todos los productos disponibles"""
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.id, p.nombre, p.descripcion, p.precio, p.categoria, u.nombre as restaurante
            FROM productos p
            JOIN usuarios u ON p.restaurante_id = u.id
            WHERE p.disponible = 1
            ORDER BY p.nombre ASC
        """)
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados