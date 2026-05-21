# models/pedido.py
# Modelo de Pedido

from config.database import conectar_bd, cerrar_conexion

class Pedido:
    
    @staticmethod
    def crear(cliente_id, direccion_entrega, metodo_pago):
        """Crea un nuevo pedido a partir del carrito"""
        conexion = conectar_bd()
        if not conexion:
            return None
        
        cursor = conexion.cursor()
        
        # Calcular total
        cursor.execute("""
            SELECT SUM(p.precio * c.cantidad)
            FROM carrito c
            JOIN productos p ON c.producto_id = p.id
            WHERE c.cliente_id = %s
        """, (cliente_id,))
        total = cursor.fetchone()[0] or 0
        
        if total <= 0:
            cerrar_conexion(conexion)
            return None
        
        try:
            cursor.execute("""
                INSERT INTO pedidos (cliente_id, total, direccion_entrega, metodo_pago, estado)
                VALUES (%s, %s, %s, %s, 'pagado')
            """, (cliente_id, total, direccion_entrega, metodo_pago))
            pedido_id = cursor.lastrowid
            
            # Agregar detalles
            cursor.execute("""
                SELECT c.producto_id, c.cantidad, p.precio
                FROM carrito c
                JOIN productos p ON c.producto_id = p.id
                WHERE c.cliente_id = %s
            """, (cliente_id,))
            
            for producto_id, cantidad, precio in cursor.fetchall():
                subtotal = cantidad * precio
                cursor.execute("""
                    INSERT INTO detalle_pedidos (pedido_id, producto_id, cantidad, precio_unitario, subtotal)
                    VALUES (%s, %s, %s, %s, %s)
                """, (pedido_id, producto_id, cantidad, precio, subtotal))
            
            # Vaciar carrito
            cursor.execute("DELETE FROM carrito WHERE cliente_id = %s", (cliente_id,))
            
            conexion.commit()
            
            # Buscar repartidor cercano (simulado)
            cursor.execute("""
                SELECT r.id FROM repartidores r
                WHERE r.disponible = 1
                LIMIT 1
            """)
            repartidor = cursor.fetchone()
            
            if repartidor:
                cursor.execute("""
                    UPDATE pedidos SET repartidor_id = %s, estado = 'asignado'
                    WHERE id = %s
                """, (repartidor[0], pedido_id))
                conexion.commit()
            
            return pedido_id
        except Exception as e:
            print(f"Error al crear pedido: {e}")
            return None
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def obtener_por_cliente(cliente_id):
        """Obtiene todos los pedidos de un cliente"""
        conexion = conectar_bd()
        if not conexion:
            return []
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT id, fecha_pedido, total, estado, metodo_pago
            FROM pedidos
            WHERE cliente_id = %s
            ORDER BY fecha_pedido DESC
        """, (cliente_id,))
        resultados = cursor.fetchall()
        cerrar_conexion(conexion)
        return resultados