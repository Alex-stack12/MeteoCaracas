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

        import time
import requests


class ServidorClima:

    def pedir_datos(self, url, parametros, segundos):
        """Consulta la API y devuelve los datos, reintentando si falla."""
        intento = 1
        while intento <= self.INTENTOS:
            try:
                respuesta = requests.get(
                    url, params=parametros, timeout=segundos
                )
                respuesta.raise_for_status()
                return respuesta.json()
            except Exception as error:
                if intento < self.INTENTOS:
                    print(
                        "  Fallo la consulta. Reintentando ("
                        + str(intento + 1)
                        + " de "
                        + str(self.INTENTOS)
                        + ")..."
                    )
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
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
        }
        datos = self.pedir_datos(self.url_actual, parametros, 20)
        if datos is None:
            return None

        actual = datos.get("current", {})
        clima = ClimaActual(
            actual.get("temperature_2m", 0),
            actual.get("relative_humidity_2m", 0),
            actual.get("wind_speed_10m", 0),
            self.decodificar_estado(actual.get("weather_code", 0)),
        )
        return clima

    def obtener_historico_rango(self, lat, lon, fecha_inicio, fecha_fin):
        """Consulta el historico y devuelve una lista de objetos RegistroHistorico."""
        parametros = {
            "latitude": lat,
            "longitude": lon,
            "start_date": fecha_inicio,
            "end_date": fecha_fin,
            "daily": "temperature_2m_mean,relative_humidity_2m,precipitation_sum,wind_speed_10m_max",
            "timezone": "auto",
        }