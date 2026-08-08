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