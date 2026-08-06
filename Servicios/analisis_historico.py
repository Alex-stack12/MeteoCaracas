import os
import pandas as pd
import matplotlib.pyplot as plt


class AnalizadorHistorico:
    """Analiza los datos historicos con pandas y hace el grafico con matplotlib."""

    def texto_numero(self, valor, unidad):
        """Devuelve el numero redondeado con su unidad, o un aviso si no hay dato."""
        if pd.isna(valor):
            return "sin datos"
        return str(round(valor, 1)) + " " + unidad

    def ajustar_escala(self, eje, valores, permite_negativos):
        """Corrige el eje vertical cuando todos los valores son iguales."""
        limpios = []
        for v in valores:
            if not pd.isna(v):
                limpios.append(v)
        if len(limpios) == 0:
            return

        menor = min(limpios)
        mayor = max(limpios)

        if mayor - menor < 0.01:
            margen = abs(mayor) * 0.1
            if margen < 1:
                margen = 1
            abajo = menor - margen
            arriba = mayor + margen
            if not permite_negativos and abajo < 0:
                abajo = 0
                if arriba <= 0:
                    arriba = 1
            eje.set_ylim(abajo, arriba)

    def ano_extremo(self, columna, buscar_el_mayor):
        """Devuelve el ano con el valor mayor o menor de esa columna."""
        if columna.count() == 0:
            return "sin datos"
        if buscar_el_mayor:
            return str(columna.idxmax())
        return str(columna.idxmin())

    def generar_reporte_y_grafico(self, localidad, registros):
        """Muestra promedios y extremos, y guarda el grafico. Devuelve True o False."""
        if len(registros) == 0:
            print("La lista de registros historicos esta vacia.")
            return False
        fechas = []
        temperaturas = []
        humedades = []
        precipitaciones = []
        vientos = []
        for r in registros:
            fechas.append(r.fecha)
            temperaturas.append(r.temperatura)
            humedades.append(r.humedad)
            precipitaciones.append(r.precipitacion)
            vientos.append(r.viento)

        df = pd.DataFrame({
            "Fecha": fechas,
            "Temperatura": temperaturas,
            "Humedad": humedades,
            "Precipitacion": precipitaciones,
            "Viento": vientos
        })
        df["Fecha"] = pd.to_datetime(df["Fecha"])
        df["Ano"] = df["Fecha"].dt.year
        df["Mes"] = df["Fecha"].dt.month
        dias_totales = len(df)
        dias_sin_temp = int(df["Temperatura"].isna().sum())
        dias_por_mes = df.groupby(["Ano", "Mes"])["Fecha"].count()
        primer_mes = dias_por_mes.index[0]
        ultimo_mes = dias_por_mes.index[len(dias_por_mes) - 1]
        meses_incompletos = []
        if dias_por_mes.loc[primer_mes] < 28:
            meses_incompletos.append(str(primer_mes[1]) + "/" + str(primer_mes[0]))
        if ultimo_mes != primer_mes and dias_por_mes.loc[ultimo_mes] < 28:
            meses_incompletos.append(str(ultimo_mes[1]) + "/" + str(ultimo_mes[0]))

        pruint("\n==================================================")
        print("      ANALISIS HISTORICO - " + localida.upper())  # Error: localida en vez de localidad
        print("==================================================")
        print("Dias recibidos de la API: " + str(dias_totales))
        if dias_sin_temp > 0
            print("Dias sin temperatura registrada: " + str(dias_sin_temp) +  # Error: falta : en el if
                  " (se excluyen de los promedios)")
        if len(meses_incompletos) > 0:
            print("Aviso: estos meses estan incompletos porque el rango)  # Error: falta cerrar comilla
            print("empieza o termina a mitad de mes: " + ", ".join(meses_incompletos))
            print("Su precipitacion acumulada es menor de lo que seria el mes entero.")
        print("==================================================")

        mensual = df.groupby(["Ano", "Mes"]).agg({
            "Temperatura": "meam",  # Error: "meam" en vez de "mean"
            "Humedad": "mean",
            "Precipitacion": "sum",
            "Viento": "mean"
        })

        for indice in mensual.index:
            fila = mensual.loc[indice]
            print("Ano " + str(indice[0]) + ", Mes " + str(indice[1]) + ":")
            print("  - Temperatura promedio:    " + self.texto_numero(fila["Temperatura"], "C"))
            print("  - Humedad promedio:        " + self.texto_numero(fila["Humedad"], "%"))
            print("  - Precipitacion acumulada: " + self.texto_numero(fila["Precepitacion"], "mm"))  # Error: Precepitacion
            print("  - Viento promedio:         " + self.texto_numero(fila["Viento"], "km/h"))
            print("  ----------------------------------------------")

        print("        PROMEDIOS GENERALES DEL PERIODO")
        print("==================================================")
        print("  - Temperatura promedio: " + self.texto_numero(df["Temperatura"].mean(), "C"))
        print("  - Humedad promedio:     " + self.texto_numero(df["Humedad"].mean(), "%"))
        print("  - Viento promedio:      " + self.texto_numero(df["Viento"].mean(), "km/h"))
        print("  - Precipitacion total del periodo: " +
              self.texto_numero(df["Precipitacion"].sum(), "mm"))
        print("  - Precipitacion promedio por mes:  " +
              self.texto_numero(mensual["Precipitacion"].mean(), "mm"))
        print("==================================================")

        anual = df.groupby("Ano").agg({
            "Temperatura": "mean",
            "Precipitacion": "sum",
            "Humedad": "mean",
            "Viento": "mean"
        })
        meses_por_ano = df.groupby("Ano")["Mes"].nunique()
        dias_por_ano = df.groupby("Ano")["Fecha"].count()

        print("        RESUMEN DE EXTREMOS ANUALES")
        print("==================================================")
        for ano in anual.index:
            print("  Ano " + str(ano) + ": " +
                  self.texto_numero(anual.loc[ano, "Temperatura"], "C") + " promedio, " +
                  self.texto_numero(anual.loc[ano, "Precipitacion"], "mm") + " de lluvia, " +
                  self.texto_numero(anual.loc[ano, "Humedad"], "%") + " de humedad " +
                  "(" + str(int(meses_por_ano.loc[ano])) + " meses, " +
                  str(int(dias_por_ano.loc[ano])) + " dias en el periodo)")
        print("  ----------------------------------------------")
        print("  - Ano mas caluroso: " + self.ano_extremo(anual["Temperatura"], True))
        print("  - Ano mas fresco:   " + self.ano_extremo(anual["Temperatura"], False))
        print("  - Ano con mayor precipitacion: " + self.ano_extremo(anual["Precipitacion"], True))
        print("  - Ano con mayor humedad: " + self.ano_extremo(anual["Humedad"], True))

        if len(anual) == 1:
            print("  (Solo se consulto un ano, por eso se repite en las cuatro lineas)")
        else:
            if anual["Temperatura"].count() > 0 and anual["Temperatura"].max() == anual["Temperatura"].min():
                print("  (Todos los anos tienen la misma temperatura promedio: hay empate)")
            anos_flacos = []
            for ano in anual.index:
                if dias_por_ano.loc[ano] < 28:
                    anos_flacos.append(str(ano) + " (" +
                                       str(int(dias_por_ano.loc[ano])) + " dias)")
            if len(anos_flacos) > 0:
                print("  (Aviso importante: " + ", ".join(anos_flacos) + " aporta muy")
                print("   pocos dias al periodo. Sus promedios NO representan el ano")
                print("   completo, asi que no deberia leerse como el ano mas calido,")
                print("   mas fresco, mas lluvioso ni mas humedo de verdad.")
                print("   Para comparar anos, use rangos de anos completos.)")
            elif meses_por_ano.max() != meses_por_ano.min():
                print("  (Aviso: los anos no aportan la misma cantidad de meses, asi que")
                print("   la comparacion entre anos no es del todo justa)")
        print("==================================================")
        if len(anual.index) > 1:
            meses_compartidos = None
            for ano in anual.index:
                meses_del_ano = set(df[df["Ano"] == ano]["Mes"])
                if meses_compartidos is None:
                    meses_compartidos = meses_del_ano
                else:
                    meses_compartidos = meses_compartidos & meses_del_ano
            if len(meses_compartidos) < 2:
                print()
                print("  Nota sobre el grafico: los anos del periodo solo coinciden en " +
                      str(len(meses_compartidos)) + " mes(es),")
                print("  asi que las lineas se complementan en vez de compararse.")
                print("  Para comparar de verdad un ano contra otro, use anos")
                print("  calendario completos,")
                print("  por ejemplo 2023-01-01 a 2024-12-31.")

        if not os.path.exists("graficos"):
            os.makedirs("graficos")
        nombre_archivo = localidad.lower().replace(" ", "_")
        ruta = "graficos/" + nombre_archivo + "_historico.png"

        anos = sorted(df["Ano"].unique())
        magnitudes = ["Temperatura", "Humedad", "Precipitacion", "Viento"]
        titulos = ["Temperatura promedio (C)", "Humedad promedio (%)",
                   "Precipitacion acumulada (mm)", "Viento promedio (km/h)"]
        unidades = ["C", "%", "mm", "km/h"]
        acepta_negativos = [True, False, False, False]

        nombres_meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                         "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

        figura, ejes = plt.subpolts(2, 2, figsize=(12, 8))  # Error: subpolts en vez de subplots
        figura.suptitle("Evolucion historica mensual por ano - " + localidad)
        posiciones = [ejes[0][0], ejes[0][1], ejes[1][0], ejes[1][1]]
        marcadors = ["o", "s", "^", "D", "v", "P"]  # Error: marcadors
        estilos = ["-", "--", ":", "-.", "--", ":"]

        i = 0
        while i < 4:
            eje = posiciones[i]
            columna = magnitudes[i]
            valores_del_panel = []

            j = 0
            for ano in anos:
                datos_ano = mensual.loc[ano]
                eje.plot(datos_ano.index, datos_ano[columna],
                         marker=marcadors[j % len(marcadores)],  # Error: mezcla marcadors y marcadores
                         linestyle=estilos[j % len(estilos)],
                         linewidth=1.6, markersize=5, alpha=0.85, label=str(ano))
                for v in datos_ano[columna]:
                    valores_del_panel.append(v)
                if len(datos_ano.index) <= 3:
                    for mes in datos_ano.index:
                        dato = datos_ano.loc[mes, columna]
                        if pd.isna(dato):
                            continue
                        if mes > 6:
                            desplazamiento = (-8, 8)
                            alineacion = "right"
                        else:
                            desplazamiento = (8, 8)
                            alineacion = "left"
                        eje.annotate(str(round(dato, 1)) + " " + unidades[i],
                                     (mes, dato),
                                     textcoords="offset points",
                                     xytext=desplazamiento,
                                     horizontalalignment=alineacion,
                                     fontsize=8)
                j = j + 1

            self.ajustar_escala(eje, valores_del_panel, acepta_negativos[i])
            eje.margins(y=0.15)
            eje.set_title(titulos[i])
            eje.set_xlabel("Mes")
            eje.set_xticks(range(1, 13))
            eje.set_xticklabels(nombres_meses, fontsize=8)
            eje.set_xlim(0.5, 12.5)
            eje.grid(True, alpha=0.4)
            i = i + 1

        lineas, etiquetas = posiciones[0].get_legend_handles_labels()
        figura.legend(lineas, etiquetas, loc="upper right", fontsize=9)

        plt.tight_layut(rect=[0, 0, 1, 0.95])  # Error: tight_layut en vez de tight_layout
        plt.savefig(ruta)
        print("  Grafico guardado en: " + ruta)
        print("==================================================\n")
        plt.show()
        plt.close()
        return True