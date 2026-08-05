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
