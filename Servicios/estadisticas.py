class RegistroConsulta:
    """Guarda una consulta de clima hecha durante la sesion."""

    def __init__(self, municipio, localidad, clima):
        """Guarda el municipio, la localidad y su clima."""
        self.municipio = municipio
        self.localidad = localidad
        self.clima = clima

    def es_la_misma(self, municipio, localidad):
        """Devuelve True si el registro es de esa misma localidad."""
        return self.municipio == municipio and self.localidad == localidad


class GestorEstadisticas:
    """Guarda las consultas de la sesion y calcula los reportes."""

    def __init__(self):
        """Crea la lista vacia de consultas y el contador de veces consultadas."""
        self.consultas_realizadas = []
        self.veces_consultadas = 0

    def registrar_consulta(self, municipio, localidad, clima):
        """Guarda la consulta. Si la localidad ya estaba, actualiza su clima."""
        self.veces_consultadas = self.veces_consultadas + 1

