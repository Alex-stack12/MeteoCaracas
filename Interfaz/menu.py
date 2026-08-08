import datetime

from servicios.api_meteo import ServicioMeteo
from servicios.estadisticas import GestorEstadisticas
from servicios.analisis_historico import AnalizadorHistorico


class MenuInterfaz:
    """Muestra el menu y maneja lo que elige el usuario."""
    DIAS_RETRASO_ARCHIVO = 7

    def __init__(self, municipios):
        """Guarda los municipios y crea los objetos de los servicios."""
        self.municipios = municipios
        self.api = ServicioMeteo()
        self.estadisticas = GestorEstadisticas()
        self.analizador = AnalizadorHistorico()

    def iniciar(self):
        """Muestra el menu principal en un bucle hasta que el usuario sale."""
        while True:
            print("\n==================================================")
            print("           SISTEMA METEOCARACAS - MENU")
            print("==================================================")
            print("1. Consultar clima por municipio y localidad")
            print("2. Buscar localidad por nombre")
            print("3. Reportes y estadisticas de la sesion")
            print("4. Analizar historico (por rango de fechas)")
            print("5. Salir")
            print("--------------------------------------------------")

            opcion = input("Seleccione una opcion (1-5): ").strip()

            if opcion == "1":
                self.consultar_por_municipio()
            elif opcion == "2":
                self.busqueda_directa()
            elif opcion == "3":
                self.mostrar_menu_reportes()
            elif opcion == "4":
                self.analizar_historico()
            elif opcion == "5":
                print("\nGracias por usar MeteoCaracas. Hasta pronto.")
                break
            else:
                print("\nOpcion no valida. Intente de nuevo.")

    def consultar_por_municipio(self):
        """Consulta el clima eligiendo primero el municipio y luego la localidad."""
        print("\n--- MUNICIPIOS DISPONIBLES ---")
        numero = 1
        for muni in self.municipios:
            print(str(numero) + ". " + muni.nombre)
            numero = numero + 1

        entrada = input("\nNumero de municipio: ").strip()
        if not entrada.isdigit():
            print("Debe ingresar un numero.")
            return
        indice = int(entrada) - 1
        if indice < 0 or indice >= len(self.municipios):
            print("Numero de municipio fuera de rango.")
            return

        municipio = self.municipios[indice]
        validas = municipio.obtener_localidades_validas()

        if len(validas) == 0:
            print(municipio.nombre + " no tiene localidades con coordenadas validas.")
            return
        
        total = len(municipio.localidades)
        sin_coords = len(municipio.obtener_localidades_sin_coordenadas())
        fuera_del_area = total - sin_coords - len(validas)

        print("\n--- LOCALIDADES EN " + municipio.nombre.upper() + " ---")
        print("(De " + str(total) + " localidades del archivo se pueden consultar " +
              str(len(validas)) + ".")
        print(" " + str(sin_coords) + " vienen sin coordenadas y " + str(fuera_del_area) +
              " tienen coordenadas fuera de Caracas.")
        print(" El detalle completo esta en el reporte 3c.)")
        numero = 1
        for loc in validas:
            print(str(numero) + ". " + loc.nombre)
            numero = numero + 1

        entrada = input("\nNumero de localidad: ").strip()
        if not entrada.isdigit():
            print("Debe ingresar un numero.")
            return
        indice = int(entrada) - 1
        if indice < 0 or indice >= len(validas):
            print("Numero de localidad fuera de rango.")
            return

        self.procesar_consulta_clima(municipio.nombre, validas[indice])

        def busqueda_directa(self):
         """Busca localidades validas por nombre y consulta la elegida."""
        criterio = input("\nNombre (o parte) de la localidad: ")
        par = self.seleccionar_localidad_valida(criterio)
        if par is None:
            return

        self.procesar_consulta_clima(par[0], par[1])

    def quitar_acentos(self, texto):
        """Devuelve el texto en minusculas, sin acentos ni dieresis."""
        texto = texto.lower()
        con_acento = "aeiouun"
        acentuadas = ["á", "é", "í", "ó", "ú", "ü", "ñ"]
        i = 0
        while i < len(acentuadas):
            texto = texto.replace(acentuadas[i], con_acento[i])
            i = i + 1
        return texto

    def buscar_coincidencias(self, criterio):
        """Devuelve una lista de pares [municipio, localidad] con coordenadas validas."""
        coincidencias = []
        for muni in self.municipios:
            for loc in muni.obtener_localidades_validas():
                if criterio in self.quitar_acentos(loc.nombre):
                    coincidencias.append([muni.nombre, loc])
        return coincidencias

    def buscar_todas_las_coincidencias(self, criterio):
        """Devuelve los pares [municipio, localidad] que coinciden, validos o no."""
        coincidencias = []
        for muni in self.municipios:
            for loc in muni.localidades:
                if criterio in self.quitar_acentos(loc.nombre):
                    coincidencias.append([muni.nombre, loc])
        return coincidencias

    def explicar_sin_resultados(self, criterio):
        """Explica por que no hubo resultados validos para el criterio buscado."""
        todas = self.buscar_todas_las_coincidencias(criterio)

        if len(todas) == 0:
            print("No existe ninguna localidad que coincida con '" + criterio + "'.")
            return
        print("\nSe encontraron localidades con ese nombre, pero ninguna se puede consultar:")
        for par in todas:
            loc = par[1]
            if not loc.tiene_coordenadas():
                motivo = "no tiene coordenadas registradas en el archivo"
            else:
                motivo = ("sus coordenadas (Lat " + str(loc.latitud) + ", Lon " +
                          str(loc.longitud) + ") caen fuera del Area Metropolitana de Caracas")
            print("  - " + loc.nombre + " (" + par[0] + "): " + motivo + ".")
        print("Por eso el sistema no consulta el clima de esas localidades.")

    def seleccionar_localidad_valida(self, criterio):
        """Muestra las coincidencias y deja al usuario elegir una. Devuelve el par o None."""
        criterio = self.quitar_acentos(criterio.strip())
        if criterio == "":
            print("Debe ingresar al menos una letra.")
            return None

        coincidencias = self.buscar_coincidencias(criterio)
        if len(coincidencias) == 0:
            self.explicar_sin_resultados(criterio)
            return None

        print("\n--- RESULTADOS PARA '" + criterio + "' ---")
        numero = 1
        for par in coincidencias:
            print(str(numero) + ". " + par[1].nombre + " (" + par[0] + ")")
            numero = numero + 1

        entrada = input("\nNumero de la localidad: ").strip()
        if not entrada.isdigit():
            print("Debe ingresar un numero.")
            return None
        indice = int(entrada) - 1
        if indice < 0 or indice >= len(coincidencias):
            print("Seleccion invalida.")
            return None

        return coincidencias[indice]

    def procesar_consulta_clima(self, nombre_municipio, localidad):
        """Consulta el clima de una localidad, lo muestra y lo guarda."""
        print("\nConsultando clima para " + localidad.nombre + "...")
        clima = self.api.obtener_clima_actual(localidad.latitud, localidad.longitud)

        if clima is None:
            print("No se pudo obtener el clima. Verifique su conexion.")
            return

        print("\n==================================================")
        print("  INFORMACION METEOROLOGICA - " + localidad.nombre.upper())
        print("==================================================")
        print("  - Municipio: " + nombre_municipio)
        print("  - Localidad: " + localidad.nombre)
        print("  - Coordenadas: Lat " + str(localidad.latitud) + ", Lon " + str(localidad.longitud))
        print(clima)
        print("==================================================")

        self.estadisticas.registrar_consulta(nombre_municipio, localidad.nombre, clima)