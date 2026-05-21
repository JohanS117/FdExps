# models/usuario.py
# Modelo de Usuario

from config.database import conectar_bd, cerrar_conexion
from utils.security import hash_password

class Usuario:
    
    @staticmethod
    def crear(nombre, email, password, telefono, direccion, tipo):
        """Crea un nuevo usuario en la base de datos"""
        conexion = conectar_bd()
        if not conexion:
            return False, "Error de conexión"
        
        cursor = conexion.cursor()
        
        # Verificar email existente
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            cerrar_conexion(conexion)
            return False, "El email ya está registrado"
        
        password_hash = hash_password(password)
        
        try:
            cursor.execute("""
                INSERT INTO usuarios (nombre, email, password, telefono, direccion, tipo)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (nombre, email, password_hash, telefono, direccion, tipo))
            usuario_id = cursor.lastrowid
            
            # Si es repartidor, crear registro en tabla repartidores
            if tipo == 'repartidor':
                cursor.execute("""
                    INSERT INTO repartidores (usuario_id, vehiculo, licencia)
                    VALUES (%s, %s, %s)
                """, (usuario_id, 'moto', ''))
            
            conexion.commit()
            return True, "Usuario registrado correctamente"
        except Exception as e:
            return False, f"Error: {str(e)}"
        finally:
            cerrar_conexion(conexion)
    
    @staticmethod
    def obtener_por_id(usuario_id):
        """Obtiene un usuario por su ID"""
        conexion = conectar_bd()
        if not conexion:
            return None
        cursor = conexion.cursor()
        cursor.execute("SELECT id, nombre, tipo FROM usuarios WHERE id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        if resultado:
            return {"id": resultado[0], "nombre": resultado[1], "tipo": resultado[2]}
        return None
    
    @staticmethod
    def obtener_nombre(usuario_id):
        """Obtiene solo el nombre del usuario"""
        conexion = conectar_bd()
        if not conexion:
            return ""
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre FROM usuarios WHERE id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado[0] if resultado else ""
    
    @staticmethod
    def obtener_tipo(usuario_id):
        """Obtiene el tipo de usuario (cliente/restaurante/repartidor)"""
        conexion = conectar_bd()
        if not conexion:
            return None
        cursor = conexion.cursor()
        cursor.execute("SELECT tipo FROM usuarios WHERE id = %s", (usuario_id,))
        resultado = cursor.fetchone()
        cerrar_conexion(conexion)
        return resultado[0] if resultado else None