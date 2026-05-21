# utils/security.py
# Funciones de seguridad: hash, validaciones, 2FA

import hashlib
import re
import random
import string
from datetime import datetime, timedelta

def hash_password(password):
    """Hashea una contraseña usando SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def validar_email(email):
    """Valida el formato de un email"""
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def generar_codigo_2fa():
    """Genera un código de 6 dígitos para autenticación en dos pasos"""
    return ''.join(random.choices(string.digits, k=6))

def enviar_codigo_2fa(email, codigo):
    """
    Simula el envío de código 2FA por email/SMS
    En producción, aquí iría la integración con servicio de correo/SMS
    """
    print(f"[SIMULACIÓN] Código 2FA para {email}: {codigo}")
    return True

def validar_telefono(telefono):
    """Valida formato de teléfono colombiano"""
    return telefono and len(telefono) >= 10 and telefono.isdigit()