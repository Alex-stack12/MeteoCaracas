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

    def mostrar_reporte_inicial(self, municipios):
        """Muestra el reporte de carga pedido en el requerimiento 1."""
        print()
        print("==================================================")
        print("        REPORTE INICIAL DE CARGA DE DATOS")
        print("==================================================")

        total_general = 0
        total_conocidas = 0

        for muni in municipios:
            total = len(muni.localidades)
            con_coords = len(muni.obtener_localidades_con_coordenadas())
            sin_coords = len(muni.obtener_localidades_sin_coordenadas())
            validas = len(muni.obtener_localidades_validas())

            if total > 0:
                porcentaje = con_coords / total * 100
            else:
                porcentaje = 0

            total_general = total_general + total
            total_conocidas = total_conocidas + con_coords

            print()
            print("Municipio: " + muni.nombre)
            print("  a. Localidades cargadas: " + str(total))
            print("  b. Con coordenadas: " + str(con_coords))
            print("  c. Sin coordenadas: " + str(sin_coords))
            print("  d. Porcentaje con coordenadas: " + str(round(porcentaje, 1)) + " %")
            print("  (Validas dentro de Caracas: " + str(validas) + ")")

        print()
        print("--------------------------------------------------")
        print("Total de localidades cargadas: " + str(total_general))
        print("Total con coordenadas: " + str(total_conocidas))
        print("==================================================")
        print()