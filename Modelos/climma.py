class ClimaActual:
    """Guardar la información del clima actual de una localidad."""

    def __init__(self, temperatura, humedad, velocidad_viento, estado_tiempo):
        """Guarda las magnitudes obtenidas de la API"""
        self.temperatura = temperatura
        self.humedad = humedad
        self.velocidad_viento = velocidad_viento
        self.estado_tiempo = estado_tiempo

    def __str__(self):
        """Texto con los detalles del clima."""
        texto = ""
        texto += " - Temperatura actual: " + str(self.temperatura) + "C\n"
        texto += " - Humedad: " + str(self.humedad) + "%\n"
        texto += " - Velocidad del viento: " + str(self.velocidad_viento) + " km/h\n"
        texto += " - Estado del tiempo: " + self.estado_tiempo
        return texto
