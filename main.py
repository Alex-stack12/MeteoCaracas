from servicios.cargador import CargadorDatos
from interfaz.menu import MenuInterfaz

def main():
    """Carga los datos, muestra el reporte inicial y abre el menu."""
    cargador = CargadorDatos()

    try:
        municipios = cargador.cargar_desde_json("zonas_caracas.json")
        cargador.mostrar_reporte_inicial(municipios)

        menu = MenuInterfaz(municipios)
        menu.iniciar()
    except Exception as error:
        print("Ocurrio un error al iniciar el programa:", error)

main()
