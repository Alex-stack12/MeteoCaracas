import time

import requests
from modelos.clima import ClimaActual
from modelos.registro_historico import RegistroHistorico


class ServicioMeteo:
    """Se encarga de consultar la API de Open-Meteo."""

    INTENTOS = 3

    def __init__(self):
        """Guarda las direcciones de la API de clima actual e historico."""
        self.url_actual = "https://api.open-meteo.com/v1/forecast"
        self.url_historico = "https://archive-api.open-meteo.com/v1/archive"

    def pedir_datos(self, url, parametros, segundos):
        """Consulta la API y devuelve los datos, reintentando si falla."""
        intento = 1
        while intento <= self.INTENTOS:
            try:
                respuesta = requests.get(url, params=parametros, timeout=segundos)
                respuesta.raise_for_status()
                return respuesta.json()
            except Exception as error:
                if intento < self.INTENTOS:
                    print("  Fallo la consulta. Reintentando (" +
                          str(intento + 1) + " de " + str(self.INTENTOS) + ")...")
                    time.sleep(1)
                else:
                    print("Error al consultar la API:", error)
            intento = intento + 1
        return None

    def obtener_clima_actual(self, lat, lon):
        """Consulta el clima actual y devuelve un objeto ClimaActual o None."""
        parametros = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
        }
        datos = self.pedir_datos(self.url_actual, parametros, 20)
        if datos is None:
            return None

        actual = datos.get("current", {})
        clima = ClimaActual(
            actual.get("temperature_2m", 0),
            actual.get("relative_humidity_2m", 0),
            actual.get("wind_speed_10m", 0),
            self.decodificar_estado(actual.get("weather_code", 0))
        )
        return clima

    def obtener_historico_rango(self, lat, lon, fecha_inicio, fecha_fin):
        """Consulta el historico y devuelve una lista de objetos RegistroHistorico."""
        parametros = {
            "latitude": lat,
            "longitude": lon,
            "start_date": fecha_inicio,
            "end_date": fecha_fin,
            "daily": "temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_max",
            "timezone": "auto"
        }

        registros = []
        datos = self.pedir_datos(self.url_historico, parametros, 30)
        if datos is None:
            return registros

        try:
            diario = datos.get("daily", {})

            if not diario or "time" not in diario:
                return registros

            tiempos = diario.get("time", [])
            temperaturas = diario.get("temperature_2m_mean", [])
            humedades = diario.get("relative_humidity_2m_mean", [])
            precipitaciones = diario.get("precipitation_sum", [])
            vientos = diario.get("wind_speed_10m_max", [])

            i = 0
            while i < len(tiempos):
                registro = RegistroHistorico(
                    tiempos[i],
                    self.valor(temperaturas, i),
                    self.valor(humedades, i),
                    self.valor(precipitaciones, i),
                    self.valor(vientos, i)
                )
                registros.append(registro)
                i = i + 1

            return registros

        except Exception as error:
            print("Error al procesar el historico:", error)

        return registros

    def valor(self, lista, i):
        """Devuelve el valor de la lista en la posicion i, o None si no existe.

        Se devuelve None y no 0 a proposito: un dia sin dato no es un dia
        de 0 grados. Si se guardara 0 se danarian los promedios.
        """
        if i < len(lista):
            return lista[i]
        return None

        def decodificar_estado(self, codigo):
        """Convierte el codigo del tiempo de la API en un texto en espanol."""
        codigos = {
            0: "Despejado",
            1: "Mayormente despejado",
            2: "Parcialmente nublado",
            3: "Nublado",
            45: "Niebla",
            48: "Niebla con escarcha",
            51: "Llovizna ligera",
            53: "Llovizna moderada",
            55: "Llovizna densa",
            56: "Llovizna helada ligera",
            57: "Llovizna helada densa",
            61: "Lluvia ligera",
            63: "Lluvia moderada",
            65: "Lluvia fuerte",
            66: "Lluvia helada ligera",
            67: "Lluvia helada fuerte",
            71: "Nevada ligera",
            73: "Nevada moderada",
            75: "Nevada fuerte",
            77: "Granos de nieve",
            80: "Chubascos ligeros",
            81: "Chubascos moderados",
            82: "Chubascos violentos",
            85: "Chubascos de nieve ligeros",
            86: "Chubascos de nieve fuertes",
            95: "Tormenta electrica",
            96: "Tormenta con granizo ligero",
            99: "Tormenta con granizo fuerte"
        }
        if codigo in codigos:
            return codigos[codigo]
        return "Desconocido (codigo " + str(codigo) + ")"