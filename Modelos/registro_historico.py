class RegistroHistorico:
    """Guarda el clima de un dia del historico (no usa diccionarios)."""

    def __init__(self, fecha, temperatura, humedad, precipitacion, viento):
        """Guarda la fecha y las magnitudes de un dia."""
        self.fecha = fecha
        self.temperatura = temperatura
        self.humedad = humedad
        self.precipitacion = precipitacion
        self.viento = viento
