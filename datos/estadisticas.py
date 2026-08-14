# -*- coding: utf-8 -*-
"""Ampliación del Integrador — Parte 3: medidas de tendencia central.

Lee con Pandas (`pandas.read_sql`) los álbumes ya cargados en la base y
calcula media, mediana y moda del año de lanzamiento (columna numérica de
la entidad Álbum). No usa groupby, solo lectura y cálculo directo con
Pandas, tal como pide la consigna.
"""

import pandas as pd

from datos.conexion import conectar


def calcular_estadisticas_anio():
    """Calcula media, mediana y moda del año de los álbumes cargados.

    Devuelve un diccionario con los tres valores y un texto de interpretación,
    o None si todavía no hay álbumes cargados en la base.
    """

    conexion = conectar()
    df_albumes = pd.read_sql("SELECT * FROM albumes", conexion)
    conexion.close()

    if df_albumes.empty:
        return None

    media = df_albumes["anio"].mean()
    mediana = df_albumes["anio"].median()
    moda = df_albumes["anio"].mode()[0]

    # --- Interpretación automática ---
    if abs(media - mediana) < 3:
        texto_comparacion = (
            "la media y la mediana son bastante parecidas, lo que indica que los años "
            "de lanzamiento están distribuidos de forma pareja, sin valores extremos que "
            "tiren el promedio para un lado."
        )
    else:
        texto_comparacion = (
            "la media y la mediana difieren bastante, lo que sugiere que hay algunos "
            "álbumes con años muy alejados del resto que están corriendo el promedio."
        )

    cantidad_moda = int((df_albumes["anio"] == moda).sum())

    if cantidad_moda >= 3:
        texto_moda = (
            f"Además, {int(moda)} aparece como una moda bastante clara, repitiéndose "
            f"en {cantidad_moda} álbumes."
        )
    else:
        texto_moda = (
            "La moda no es demasiado marcada: los años están bastante repartidos y no "
            "hay un valor que se repita mucho más que los demás."
        )

    interpretacion = f"Con los datos cargados, {texto_comparacion} {texto_moda}"

    return {
        "media": media,
        "mediana": mediana,
        "moda": moda,
        "cantidad_albumes": len(df_albumes),
        "interpretacion": interpretacion,
    }


if __name__ == "__main__":
    resultado = calcular_estadisticas_anio()

    if resultado is None:
        print("Todavía no hay álbumes cargados para analizar.")
    else:
        print(f"Media: {resultado['media']:.2f}")
        print(f"Mediana: {resultado['mediana']}")
        print(f"Moda: {resultado['moda']}")
        print(resultado["interpretacion"])
