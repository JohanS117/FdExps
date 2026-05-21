# services/pago_service.py
# Servicio de pagos simulado

import random

class PagoService:
    
    @staticmethod
    def procesar_tarjeta(numero_tarjeta, fecha_expiracion, cvv, monto):
        """Simula el procesamiento de pago con tarjeta"""
        if len(numero_tarjeta) < 15:
            return False, "Número de tarjeta inválido"
        if len(cvv) != 3:
            return False, "CVV inválido"
        return True, "Pago aprobado"
    
    @staticmethod
    def procesar_nequi(telefono, monto):
        """Simula el procesamiento de pago con Nequi"""
        if len(telefono) < 10:
            return False, "Número de teléfono inválido"
        return True, "Solicitud de pago enviada a Nequi"
    
    @staticmethod
    def procesar_efectivo(monto):
        """Confirma pago en efectivo"""
        return True, "Pago confirmado en efectivo"