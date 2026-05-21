# models/repartidor.py
# Modelo de Repartidor

from config.database import conectar_bd, cerrar_conexion

class Repartidor:
    
    @staticmethod
    def obtener_id(usuario_id):
        """Obtiene el ID del repartidor a partir del usuario_id"""
        conexion = conectar_bd()
        if not conexion:
            return None
        cursor = conexion.cursor()
        cursor.execute("SELECT id, disponible FROM repartidores WHERE usuario_id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado
    
    @staticmethod
    def obtener_pedidos_asignados(usuario_id):
        """Obtiene los pedidos asignados a un repartidor"""
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT p.id, u.nombre, p.direccion_entrega, p.total, p.estado
            FROM pedidos p
            JOIN repartidores r ON p.repartidor_id = r.id
            JOIN usuarios u ON p.cliente_id = u.id
            WHERE r.usuario_id = %s AND p.estado IN ('asignado', 'en_camino')
        """, (usuario_id,))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados
    
    @staticmethod
    def actualizar_estado_pedido(pedido_id, nuevo_estado):
        """Actualiza el estado de un pedido"""
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE pedidos SET estado = %s WHERE id = %s", (nuevo_estado, pedido_id))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)