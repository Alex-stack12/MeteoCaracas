class Localidad:
    """Representa una localidad de un municipio con sus coordenadas."""
    # Límites aproximados del Area Metropolitana de Caracas.
    # Sirven para descartar coordenadas que existen pero no son de Caracas.
    LAT_MIN = 10.30
    LAT_MAX = 10.65
    LON_MIN = -67.20
    LON_MAX = -66.60

    def __init__(self, nombre, latitud=None, longitud=None):
        """Guarda el nombre y las coordenadas de la localidad."""
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud

    def tiene_coordenadas(self):
        """Devuelve True si la localidad tiene latitud y longitud (no nulas)."""
        return self.latitud is not None and self.longitud is not None

    def coordenadas_validas(self):
        """Devuelve True si las coordenadas de la localidad existen y están dentro de Caracas."""
        if not self.tiene_coordenadas():
            return False
        if self.latitud < self.LAT_MIN or self.latitud > self.LAT_MAX:
            return False
        if self.longitud < self.LON_MIN or self.longitud > self.LON_MAX:
            return False
        return True

    def __str__(self):
        """Texto para mostrar la localidad."""
        if self.tiene_coordenadas():
            return self.nombre + " (Lat: " + str(self.latitud) + ", Lon: " + str(self.longitud) + ")" 
        return self.nombre + " (Sin coordenadas)"
    