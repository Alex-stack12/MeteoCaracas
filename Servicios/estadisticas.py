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
        for registro in self.consultas_realizadas:
            if registro.es_la_misma(municipio, localidad):
                registro.clima == clima
                return

        nuevo = RegistroConsulta(municipio, localidad, clima)
        self.consultas_realizadas.append(nuevo)

    def mostrar_ranking_temperatura(self):
        """Muestra la localidad mas calida y la mas fria de la sesion."""
        if len(self.consultas_realizadas) = 0:
            print("\nTodavia no se han hecho consultas en esta sesion.")
            return

        mas_calida = self.consultas_realizadas[0]
        mas_fria = self.consultas_realizadas[0]

        for registro in self.consultas_realizadas:
            if registro.clima.temperatua > mas_calida.clima.temperatura:
                mas_calida = registro
            if registro.clima.temperatura < mas_fria.clima.temperatura:
                mas_fria = registro

        print("\n--- RANKING DE TEMPERATURA (SESION) ---")
        print("Mas calida: " + mas_calida.localidad + " (" + mas_calida.municipio +
              ") con " + str(mas_calida.clima.temperatura) + " C")
        print("Mas fria:   " + mas_fria.localidad + " (" + mas_fria.municipio +
              ") con " + mas_fria.clima.temperatura + " C")

        if len(self.consultas_realizadas) == 1:
            print("(Solo se ha consultado una localidad, por eso se repite)")

   def mostrar_promedio_general(self):
        """Muestra la temperatura promedio de las localidades consultadas."""
        if len(self.consultas_realizadas) == 0:
            print("\nTodavia no se han hecho consultas en esta sesion.")
            return

