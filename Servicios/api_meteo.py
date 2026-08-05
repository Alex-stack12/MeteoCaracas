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
                intento = intento + 1
            else:
                print("Error al consultar la API:", error)
    return None