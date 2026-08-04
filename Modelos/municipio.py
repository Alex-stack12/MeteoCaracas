class Municipio:
    """Representa un municipio que tiene una lista de localidades."""

    def __init__(self, nombre):
        """Guarda el nombre del municipio y crea la lista de localidades vacia."""
        self.nombre = nombre
        self.localidades = []

        def agregar_localidades(self, localidad):
            """Agrega una localidad a la lista del municipio."""
            self.localidades.append(localidad)

            def obtener_localidades_con_coordenadas(self):
                """Devuelve la lista de localidades que tienen coordenadas (no nulas)."""
                resultado = []
                for loc in self.localidades:
                    if loc.coordenadas():
                        resultado.append(loc)
                return resultado

            def obtener_localidades_sin_coordenadas(self):
                """Devuelve la lista de localidades que no tienen coordenadas (nulas)."""
                resultado = []
                for loc in self.localidades:
                    if not loc.tiene_coordenadas():
                        resultado.append(loc)
                return resultado

            def obtener_localidades_validas(self):
                """Devuelve las localidades con coorddnadas validas dentro de Caracas."""
                resultado = []
                for loc in self.localidades:
                    if loc.coordenadas_validas():
                        resultado.append(loc)
                return resultado