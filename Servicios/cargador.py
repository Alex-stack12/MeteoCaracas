import json
from modelos.municipio import Municipio
from modelos.localidad import Localidad


class CargadorDatos:
    """Lee el archivo JSON y lo convierte en objetos Municipio y Localidad."""

    def cargar_desde_json(self, ruta_archivo):
        """Lee el archivo y devuelve la lista de municipios con sus localidades."""
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
        if not isinstance(datos, dict):
            raise ValueError("El archivo no tiene la estructura esperada de municipios.")

        municipios = []
        for nombre_municipio in datos:
            nombre = nombre_municipio.replace("_", " ")
            municipio = Municipio(nombre)

            lista_localidades = datos[nombre_municipio]
            if not isinstance(lista_localidades, list):
                print("Aviso: el municipio '" + nombre + "' no trae una lista de localidades.")
                municipios.append(municipio)
                continue

            for loc in lista_localidades:
                if not isinstance(loc, dict):
                    continue
                nombre_loc = loc.get("localidad", "Sin nombre")
                latitud = loc.get("latitud")
                longitud = loc.get("longitud")
                municipio.agregar_localidad(Localidad(nombre_loc, latitud, longitud))

            municipios.append(municipio)

        return municipios
