# services/maps_service.py
# Servicio de Google Maps

import webbrowser

class MapsService:
    
    def __init__(self, api_key=""):
        self.api_key = api_key
    
    def mostrar_mapa(self, lat, lng, zoom=15):
        """Abre Google Maps en el navegador"""
        url = f"https://www.google.com/maps?q={lat},{lng}&z={zoom}"
        webbrowser.open(url)
    
    def obtener_coordenadas(self, direccion):
        """Simula obtener coordenadas (para desarrollo)"""
        return 4.6097, -74.0817