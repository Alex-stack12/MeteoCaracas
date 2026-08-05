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
        """Devuelve el año con el valor mayor o menor de esa columna.""
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