import json
from modelos.municipio import Municipio
from modelos.localidad import Localidad
class CargadorDatos
    """Lee el archivo JSON y lo convierte en objetos Municipio y Localidad."""

    def cargar_desde_json(ruta_archivo):
        """Lee el archivo y devuelve la lista de municipios con sus localidades."""
        with open(ruta_archivo, "r", enconding="utf-8") as archivo:
            datos = jason.load(archivo)
            
         if not isinstance(datos, dict):
        raise ValueError("El archivo no tiene la estructura esperada de municipios.")

