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
