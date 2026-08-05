class RegistroHistorico:
    """Guarda el clima de un dia del historico (no usa diccionarios)."""

    def __init__(self, fecha, temperatura, humedad, precipitacion, viento):
        """Guarda la fecha y las magnitudes de un dia."""
        self.fecha = fecha
        self.temperatura = temperatura
        self.humedad = humedad
        self.precipitacion = precipitacion
        self.viento = viento

    def __str__(self):
        """Texto con los datos del dia."""
        return (str(self.fecha) + ": " + str(self.temperatura) + " C, " +
                str(self.humedad) + " %, " + str(self.precipitacion) + " mm, " +
                str(self.viento) + " km/h")
