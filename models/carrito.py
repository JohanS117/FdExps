# models/carrito.py
# Modelo de Carrito

from config.database import conectar_bd, cerrar_conexion

class Carrito:
    
    @staticmethod
    def agregar(cliente_id, producto_id, cantidad):
        """Agrega un producto al carrito"""
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        
        cursor.execute("""
            SELECT id, cantidad FROM carrito 
            WHERE cliente_id = %s AND producto_id = %s
        """, (cliente_id, producto_id))
        existente = cursor.fetchone()
        
        try:
            if existente:
                nueva_cantidad = existente[1] + cantidad
                cursor.execute("""
                    UPDATE carrito SET cantidad = %s WHERE id = %s
                """, (nueva_cantidad, existente[0]))
            else:
                cursor.execute("""
                    INSERT INTO carrito (cliente_id, producto_id, cantidad)
                    VALUES (%s, %s, %s)
                """, (cliente_id, producto_id, cantidad))
            conexion.commit()
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def obtener(cliente_id):
        """Obtiene el contenido del carrito"""
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT c.id, p.nombre, p.precio, c.cantidad
            FROM carrito c
            JOIN productos p ON c.producto_id = p.id
            WHERE c.cliente_id = %s
        """, (cliente_id,))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados
    
    @staticmethod
    def calcular_total(cliente_id):
        """Calcula el total del carrito"""
        conexion = conectar_bd()
        if not conexion:
            return 0
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT SUM(p.precio * c.cantidad)
            FROM carrito c
            JOIN productos p ON c.producto_id = p.id
            WHERE c.cliente_id = %s
        """, (cliente_id,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado[0] if resultado and resultado[0] else 0
    
    @staticmethod
    def vaciar(cliente_id):
        """Vacía el carrito del cliente"""
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM carrito WHERE cliente_id = %s", (cliente_id,))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def eliminar_item(item_id):
        """Elimina un item específico del carrito"""
        conexion = conectar_bd()
        if not conexion:
            return False
        cursor = conexion.cursor()
        try:
            cursor.execute("DELETE FROM carrito WHERE id = %s", (item_id,))
            conexion.commit()
            return True
        except:
            return False
        finally:
            cerrar_conexion(conexion)