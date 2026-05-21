"""
FOODEXPRESS - VERSIÓN CON ERRORES
Archivo: models/pago.py
ERRORES: 10 errores intencionales
"""

from config.database import conectar_bd, cerrar_conexion
from datetime import datetime

class Pago:
    
    @staticmethod
    def registrar(pedido_id, monto, metodo, referencia):
        """Registra un pago en la base de datos"""
        # ERROR 1: No valida que pedido_id exista en la base de datos
        if not pedido_id:
            return False
        
        # ERROR 2: No valida que el monto sea positivo
        if monto <= 0:
            return False
        
        # ERROR 3: No valida que el método de pago sea válido
        metodos_validos = ['tarjeta', 'nequi', 'efectivo']
        if metodo not in metodos_validos:
            return False
        
        conexion = conectar_bd()
        if not conexion:
            return False
        
        cursor = conexion.cursor()
        try:
            cursor.execute("""
                INSERT INTO pagos (pedido_id, monto, metodo, referencia, estado)
                VALUES (%s, %s, %s, %s, 'completado')
            """, (pedido_id, monto, metodo, referencia))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al registrar pago: {e}")
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def obtener_por_pedido(pedido_id):
        """Obtiene los pagos asociados a un pedido"""
        # ERROR 4: No valida que pedido_id exista
        if not pedido_id:
            return []
        
        conexion = conectar_bd()
        if not conexion:
            return []
        
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, monto, metodo, referencia, estado, fecha_pago
            FROM pagos
            WHERE pedido_id = %s
            ORDER BY fecha_pago DESC
        """, (pedido_id,))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        
        # ERROR 5: No formatea las fechas correctamente
        return resultados
    
    @staticmethod
    def actualizar_estado(pago_id, nuevo_estado):
        """Actualiza el estado de un pago"""
        # ERROR 6: No valida que el estado sea permitido
        estados_permitidos = ['pendiente', 'completado', 'fallido', 'reembolsado']
        if nuevo_estado not in estados_permitidos:
            return False
        
        conexion = conectar_bd()
        if not conexion:
            return False
        
        cursor = conexion.cursor()
        try:
            cursor.execute("UPDATE pagos SET estado = %s WHERE id = %s", (nuevo_estado, pago_id))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar estado: {e}")
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def reembolsar(pago_id):
        """Reembolsa un pago"""
        # ERROR 7: No verifica el estado actual antes de reembolsar
        conexion = conectar_bd()
        if not conexion:
            return False
        
        cursor = conexion.cursor()
        
        # Verificar estado actual
        cursor.execute("SELECT estado FROM pagos WHERE id = %s", (pago_id,))
        resultado = cursor.fetchone()
        
        if not resultado:
            cerrar_conexion(conexion)
            return False
        
        estado_actual = resultado[0]
        
        # ERROR 8: Solo permite reembolsar pagos completados
        if estado_actual != 'completado':
            cerrar_conexion(conexion)
            return False
        
        try:
            cursor.execute("UPDATE pagos SET estado = 'reembolsado' WHERE id = %s", (pago_id,))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error al reembolsar: {e}")
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def verificar_duplicado(pedido_id, metodo, referencia):
        """Verifica si ya existe un pago duplicado"""
        # ERROR 9: No valida los parámetros
        conexion = conectar_bd()
        if not conexion:
            return False
        
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id FROM pagos
            WHERE pedido_id = %s AND metodo = %s AND referencia = %s
        """, (pedido_id, metodo, referencia))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado is not None
    
    @staticmethod
    def obtener_total_recaudado(fecha_inicio, fecha_fin):
        """Obtiene el total recaudado en un periodo"""
        # ERROR 10: No valida el formato de las fechas
        conexion = conectar_bd()
        if not conexion:
            return 0
        
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT SUM(monto) FROM pagos
            WHERE estado = 'completado'
            AND fecha_pago BETWEEN %s AND %s
        """, (fecha_inicio, fecha_fin))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado[0] if resultado and resultado[0] else 0