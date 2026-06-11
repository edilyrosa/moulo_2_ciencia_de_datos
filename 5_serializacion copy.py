"""
=============================================================
MÓDULO 1 — LECCIÓN 4: Serialización de datos (JSON, CSV, Parquet)
=============================================================

serializar = transformar objetos vivos de Python en bytes o texto que se puedan almacenar y luego reconstruir.
Ejemplo:
En memoria (Python)               Serialización (archivo en disco)
┌─────────────────┐                     ┌──────────────────────────────┐
│ {"nombre": "Ana",│  ────json.dump───► │ {"nombre": "Ana",             │
│  "edad": 30,     │                    │  "edad": 30,                  │
│  "activo": True} │                    │  "activo": true}              │
└─────────────────┘                     └──────────────────────────────┘
💡True (Python) se convierte en true (JSON) → se serializa.
💡Al leer (json.load) se recupera el diccionario original con True.
👀 Ojo: no es lo mismo que "guardar"
Guardar un archivo binario con pickle también es serialización, pero no es legible por humanos ni seguro.

OBJETIVO:
    Saber leer y escribir los 3 formatos más usados en
    analítica de datos, y entender cuándo usar cada uno.

CUÁNDO USAR CADA FORMATO:
    JSON    → Configuraciones, APIs, datos con anidamiento
    CSV     → Reportes para personas, compatibilidad Excel
    Parquet → Pipelines internos, big data, eficiencia

CÓMO EJECUTAR:
    pip install pyarrow   (solo la primera vez, para Parquet)
    python leccion4_serializacion.py
"""

import json
import csv
import pandas as pd
from pathlib import Path
from datetime import datetime


RAIZ          = Path(__file__).parent
RAW_DIR       = RAIZ / "data" / "raw"
PROCESSED_DIR = RAIZ / "data" / "processed"
OUTPUT_DIR    = RAIZ / "data" / "output"

#* Creamos las carperas PROCESSED_DIR y OUTPUT_DIR
# Itera sobre una lista de las rutas: PROCESSED_DIR y OUTPUT_DIR.
for d in [PROCESSED_DIR, OUTPUT_DIR]: #ya tenemos "processed/"
    d.mkdir(parents=True, exist_ok=True)
# mkdir() Crea un directorio.
# parents=True: si el directorio padre no existe, lo crea automáticamente.
# Por ejemplo, si data no existe, crea data y después processed.
# exist_ok=True: si el directorio ya existe, no lanza error (solo ignora y continúa).

# ─────────────────────────────────────────────────────────
#* PARTE 1: JSON — leer y escribir
# ─────────────────────────────────────────────────────────

print("=" * 55)
print("PARTE 1: JSON")
print("=" * 55)

#* --- LEER JSON ---
# Func que espera un Path y devuelve un dict
def cargar_config(ruta: Path) -> dict: 
    """Lee un archivo JSON y lo devuelve como diccionario."""
    # Abre el archivo en modo lectura ("r") con codificación UTF‑8. 
    # El with asegura que el archivo se cierre automáticamente al salir.
    with open(ruta, "r", encoding="utf-8") as f:
        # carga el contenido JSON del archivo y lo convierte en un diccionario (o lista) de Python.
        # no carga los datos a un archivo externo, sino que LOS CARGA EN MEMORIA, como un objeto de Py 
        # (dict, list...), y luego devuelve ese objeto.
        return json.load(f)

# La función abre ese archivo, lee su JSON y lo devuelve como dict, guardandose en la var config.
config = cargar_config(RAW_DIR / "config_pipeline.json")
print('El JSON en TDD OBJ (dict) PY \n', config)

# config['pipeline'] accede al valor asociado a la clave "pipeline" dentro del dict "config".
print(f"\nConfiguración cargada: '{config['pipeline']}' v{config['version']}")
print(f"Fuentes de datos     : {len(config['fuentes'])}")

#* Acceder a valores anidados: config["filtros"] es otro dict.
# :, en el f‑string es un formato de miles: si el número es 10000, se muestra como 10,000.
print(f"Valor mínimo filtro  : ${config['filtros']['valor_minimo']:,}")
print(f"Etapas válidas       : {config['filtros']['etapas_validas']}")
print(f"Primer pais activo       : {config['filtros']['paises_activos'][0]}")
print(f"Primer pais activo       : {config.get('filtros')['paises_activos'][0]}")
print(f"Primer pais activo       : {config.get('filtros').get('paises_activos')[0]}")


#* --- ESCRIBIR JSON con tipos especiales (datetime) ---
# Func q escribe un dict en un JSON manejando tipos especiales como datetime.
def guardar_json(datos: dict, ruta: Path) -> None:
    #  los datos dict que queremos guardar como JSON, su Path, sin return, solo crea el archivo.
    def serializer(obj):
        # El formato JSON solo entiende: dict, list, str, int, float, bool, None
        # → el TDD datetime debe ser convertida a string ISO 
        if isinstance(obj, datetime):
            return obj.isoformat() # → "2025-06-08T15:30:00"
        #! Cualquier otro tipo (un set, etc.) no soportado lanza error descriptivo
        raise TypeError(f"Tipo no serializable: {type(obj).__name__}")
        # lanza un error indicando cuál es el tipo problemático. Así el programador sabe qué debe ajustar.

    # "w" : write mode – crea o sobreescribe el archivo, cuya ruta pasare por parametro.
    # "w" crea el archivo desde cero o lo trunca si ya existe. No se añade información nueva, simplemente se reemplaza.
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(
            datos,
            f,
            default=serializer,
            indent=2,               # sangría para que sea legible
            ensure_ascii=False      # permite caracteres como ó, ñ, é
        )
        
# json.dump() escribe directamente en un archivo 
# json.dumps() devuelve una cadena de texto (string) con el JSON.

# datos : el dict a guardar.
# f : el archivo abierto donde se escribirá.
# default=serializer : Cuando json.dump() encuentra un objeto que no es nativamente serializable 
    # llama a la función que le hayas pasado en default, pasándole ese objeto problemático como argumento.
    # La función debe devolver una versión serializable de ese objeto (normalmente un string, número, lista o diccionario).
    # Si no se proporciona default y aparece un objeto no serializable, json.dump() lanza un TypeError.
    # Maneja: bytes, datetime, Decimal, set o cualquier clase personalizada.
    # Lo que esa función devuelva (en este caso un string ISO) se usará en el JSON. 
    # Esto permite manejar cualquier tipo que queramos, siempre que implementemos la lógica dentro de serializer.

# indent=2 : formatea el JSON con sangría de 2 espacios, haciéndolo legible para humanos (no todo en una línea). 
# ensure_ascii=False : por defecto, json.dump escapa caracteres no ASCII como ñ a \u00f1. 
# Con ensure_ascii=False, los escribe tal cual ("España" en lugar de "Espa\u00f1a"). 
# Combinado con encoding="utf-8", el archivo resultante tendrá directamente los caracteres acentuados.


#* Crear un resultado de pipeline para guardar como JSON
resultado_pipeline = {
    "ejecutado_en": datetime.now(),         # tipo datetime — necesita serializer
    "pipeline": "crm_analytics",
    "registros_procesados": 15,
    "registros_validos": 12,
    "tasa_validez": 0.80,
    "activo": True,
    "tipos": ["primera", "basica", "PRO"],
    "resumen_por_pais": {
        "CO": {"clientes": 6, "valor_total": 29750},
        "MX": {"clientes": 4, "valor_total": 16300},
        "CL": {"clientes": 2, "valor_total": 11100},
        "AR": {"clientes": 3, "valor_total": 5200},
    }
}
#?💡 Las comillas simples NO causan error;
# Cuando llamas a guardar_json(datos, ruta), el módulo json internamente convierte 
# todas las claves y strings a dobles comillas según el estándar JSON. 
# python: datos = {'nombre': 'Ana', 'edad': 30}   # comillas simples
# json: { "nombre": "Ana", "edad": 30 } 

#* 💡 si datos es una lista de diccionarios [{}, {}, {}]
resultado_pipeline_list = [
  {"clave1": "valor1"},
  {"clave2": datetime.now()},
  {"clave3": [1,2,3, False]}
]
# La anotación "datos: dict" sugiere que se debe pasar un dict, pero Python 
# no la exige. Puedes pasar una lista perfectamente, json.dump() acepta listas como objeto raíz. 
# Si quieres que la función admita cualquier estructura (dict o lista), puedes cambiar la anotación a 
# Any o Union[dict, list]. O incluso dejarlo sin anotación.

ruta_resultado = OUTPUT_DIR / "resultado_pipeline.json"
guardar_json(resultado_pipeline, ruta_resultado)
print(f"\nResultado guardado en: {ruta_resultado}")

ruta_resultado_list = OUTPUT_DIR / "list.json"
guardar_json(resultado_pipeline_list, ruta_resultado_list)
print(f"\nResultado guardado en: {ruta_resultado_list}")

#* Verificar que se guardó bien leyéndolo de vuelta
con_verificacion_list = cargar_config(ruta_resultado_list)
# la pos 2 es un Dict, se accede al value a travez de su key
print(f"Verificación Bool: ='{con_verificacion_list[2]['clave3'][-1]}'") 

con_verificacion = cargar_config(ruta_resultado)
print(f"Verificación: pipeline='{con_verificacion['pipeline']}', "
f"registros={con_verificacion['registros_procesados']}")



# ─────────────────────────────────────────────────────────
#* PARTE 2: CSV — leer y escribir
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("PARTE 2: CSV")
print("=" * 55)

df_clientes = pd.read_csv(RAW_DIR / "clientes.csv")
print('\n\nsin tipar\n', df_clientes)
# pd.read_csv() infiere los tipos de datos automáticamente 
# (por ejemplo, si ve números los pone como int64, fechas como object si no se le indica, etc.).
# Esto puede funcionar mal en algunos casos: por ejemplo:
# ❌ una fecha puede quedar como string o 
# ❌ una columna de IDs numéricos largos podría interpretarse como entero y luego dar error, 
# el problema es que pandas y muchos programas (incluyendo Excel) no pueden representar con precisión 
# enteros muy grandes (por ejemplo, de más de 15‑18 dígitos) si los leen como tipo int64 o float64. 
# Eso provoca redondeos o pérdida de información.
# Excel también maneja números de hasta 15 dígitos de precisión; pasados esos, los últimos se convierten en 0.
# Además, los IDs no se usan para operaciones aritméticas (no sumas IDs, no calculas promedios). 
# Por tanto es más seguro tratarlos como string.
#? 💡¿Cuándo usar int y cuándo string para IDs?
# int → solo si los IDs tienen pocos dígitos (< 10, ~2 mil millones) y realmente los necesitas como 
# número (por ejemplo, un secuencial de base de datos).
# string → casi siempre: evitas problemas de precisión, preservas ceros a la izquierda (ej. 00123), 
# y el ID sigue siendo único.
#* ---✅ Leer CSV con tipos correctos: (buena práctica) ---
# Por defecto pandas infiere los tipos, a veces mal
# Es mejor especificarlos explícitamente:
df_tipado = pd.read_csv(RAW_DIR / "clientes.csv",
    dtype={ # dict que asigna a cada columna un tipo específico de pandas.
        "id":             "int32",  # "int32" : entero de 32 bits (ahorra memoria).
        "nombre":         "string", # "string" : tipo específico para texto (mejor que object).
        "pais":           "category", #"category" : tipo para datos categóricos (poco volumen, rápida agrupación). Útil para pais, industria, etapa.
        "industria":      "category",
        "valor_contrato": "float64", # "float64" : número decimal.
        "etapa":          "category",
    },
    parse_dates=["fecha_cierre"],  # convierte la columna a datetime, para hacer operaciones temporales (restar fechas, extraer año, etc.).
    true_values=["True"],          # convierte "True" string a booleano Python
    false_values=["False"]
)
print('\n\nDF Tipado\n', df_tipado)

# ?parámetro dtype={} || dtype='string'... 
# especificar de forma explícita el tipo de dato con el que se deben leer las columnas de un archivo CSV. 
# Esta función puede asignar tipos de manera global a todas las columnas, como en dtype='string',
# o de forma personalizada para cada una usando un diccionario de Python.

print(f"\nDatos cargados: {len(df_tipado)} filas")
print("\nTipos de datos:")
print(df_tipado.dtypes.to_string())
# df.dtypes muestra el tipo de cada columna.
# .to_string() evita que pandas acorte la salida si hay muchas columnas.

#* --- Escribir CSV para reporte ---
#? En resumen: CSV → DF tipado → DF filtrado → CSV legible por Excel (vía UTF‑8 con BOM).
#  puede abrirse en Excel sin caracteres extraños.  También se podría exportar directamente a .xlsx 
# con df.to_excel(), pero optamos por CSV porque es más universal y el BOM 
# resuelve el problema típico de Excel con UTF‑8.

#? Función para exportar CSV a informe (compatible con Excel)
def exportar_reporte_csv(df: pd.DataFrame, ruta: Path) -> None:
    """
    Exporta un DataFrame como CSV listo para abrir en Excel.
    utf-8-sig agrega un BOM (Byte Order Mark) que le dice
    a Excel que el archivo está en UTF-8 → sin caracteres raros.
    """
    df.to_csv(
        ruta,
        index=False,          # no incluir el índice numérico de pandas
        encoding="utf-8-sig", #? BOM: Para Excel en español, sin BOM no reconoce UTF‑8
        sep=","               # separador estándar
    )
#? ¿cuándo se necesita el BOM? CSV → Excel. Excel no asume UTF‑8 por defecto.
# Solo para archivos CSV que quieras abrir con Excel. El CSV es texto plano y Excel, por defecto, 
# asume la codificación ANSI de tu sistema (por ejemplo, Windows-1252 en español). Si el CSV está en UTF-8 sin BOM,
# Excel no lo detecta y muestra caracteres raros (como Ã± en vez de ñ).
# Al usar encoding="utf-8-sig" en df.to_csv(), se añaden tres bytes al inicio (BOM) 
# que le indican a Excel que el archivo es UTF-8, y entonces lee bien los caracteres especiales.
# Conclusión: 
#     Usa BOM solo cuando tu destino sea abrir el CSV directamente con Microsoft Excel y quieras preservar tildes, 
#     eñes o cualquier carácter no ASCII. En cualquier otro caso (incluyendo DataFrame a Excel), no hace falta.


#? Reporte: DF de clientes activos con contrato cerrado
reporte = (
    df_tipado
    .query("etapa == 'cerrado' and activo == True")     # Filtra las filas que cumplen ambas condiciones:
    [["nombre", "pais", "industria", "valor_contrato", "fecha_cierre"]] # Selecciona solo esas columnas, en ese orden.
    .sort_values("valor_contrato", ascending=False)     # Ordena de mayor a menor valor de contrato (clientes más valiosos arriba).
    .reset_index(drop=True) # Después de filtrar y ordenar, el índice original ya no corresponde, genera uno nuevo.
)

#**** Crea el CSV BOM en "reporte_clientes_cerrados.csv"
ruta_reporte = OUTPUT_DIR / "reporte_clientes_cerrados.csv"
exportar_reporte_csv(reporte, ruta_reporte)
print(f"\nReporte exportado: {ruta_reporte}")
print(f"Registros en reporte: {len(reporte)}")
print(reporte.to_string(index=False)) # imprime el contenido en consola sin el índice, de forma legible

#💡 Este enfoque garantiza que los datos se lean e interpreten correctamente, 
# y que el CSV de salida sea compatible con herramientas de oficina.

#**** Crea el EXCEL en "reporte_clientes_cerrados.xlsx"
ruta_excel = OUTPUT_DIR / "reporte_clientes_cerrados.xlsx"
reporte.to_excel(ruta_excel, index=False, sheet_name="Clientes Cerrados")       # ✅ tildes y fechas 
#  pandas almacena la fecha como un objeto datetime con hora 00:00:00 (medianoche) en UTC por defecto, 
# Mi zona horaria es GMT-0400 (Venezuela), restarle 4 horas (UTC-4) obtienes 2024-04-04 20:00:00.
df_clientes.to_excel(ruta_excel, index=False, sheet_name="Clientes Cerrados")   # ✅ tildes

#! to_excel requiere: openpyxl
#! Ejecuta en tu terminal (el mismo entorno virtual que usas, .venv):
# .venv\Scripts\activate
# python -m pip install --upgrade pip
# python -m pip install openpyxl
# python -c "import openpyxl; print(openpyxl.__version__)" #Verificamos instalacion 3.1.5 



# ─────────────────────────────────────────────────────────
#* PARTE 3: Parquet — el formato de pipelines analíticos
# ─────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("PARTE 3: Parquet")
print("=" * 55)

#*  Parquet es formato de almacenamiento columnar — Eficiente para analítica.
# Guarda los datos por columnas, no por filas. 
# Ventajas vs CSV (grandes volúmenes de datos):
#   ✓ Compresión automática (snappy, gzip)
#   ✓ Preserva los tipos de datos (fechas, booleanos, categorías, etc.) – no tienes que volver a especificarlos al leer.
#   ✓ Lectura selectiva de columnas – puedes leer solo las columnas que necesitas, ignorando el resto.
#   ✓ Particionamiento – puedes dividir el archivo en carpetas por fecha, país, etc., y luego leer solo las particiones relevantes.


import pyarrow 
# .venv\Scripts\activate
# python -m pip install pyarrow
# python -c "import pyarrow; print(pyarrow.__version__)" # 24.0.0
#💡 to_parquet(), read_parquet() → metodos de pandas q pyarrow (o fastparquet) como motor para trabajar con formato Parquet.

ruta_csv_largo = RAW_DIR / 'sample-csv-10000-rows.csv'

#* --- Escribir Parquet ---
ruta_parquet = PROCESSED_DIR / "clientes.parquet" # Esta sera su ruta
pd_csv_largo = pd.read_csv(ruta_csv_largo) 
pd_csv_largo.to_parquet(
    ruta_parquet,          #Su ruta
    compression="snappy",  # compresión rápida, buen ratio. Usar "gzip" (más compresión, más lento), "lz4", o None.
    index=False
)

#? fue creado, pero se puede ver?
# VS Code no puede abrirlos de forma nativa porque son un formato binario optimizado,
# no un archivo de texto simple, y para verlos se necesitan extensiones específicas
#? Parquet Viewer

#* ------------ Comparando el tamano de ambos (CSV vs. Parquet)
tamaño_csv     = ruta_csv_largo.stat().st_size
tamaño_parquet = ruta_parquet.stat().st_size
print(f"\nArchivo original (CSV)   : {tamaño_csv:,} bytes")
print(f"Archivo comprimido (parquet): {tamaño_parquet:,} bytes")
print(f"Reducción de tamaño      : {(1 - tamaño_parquet/tamaño_csv)*100:.0f}%")


#* --- Leer Parquet completo ---
df_leido = pd.read_parquet(ruta_parquet)
print(f"\nLeído desde Parquet: {len(df_leido)} filas")
print(f"Tipos preservados  :")
print(df_leido.dtypes.to_string())



#* --- Leer solo columnas necesarias (enorme ventaja en big data) ---
# En un archivo de 50 columnas, esto lee solo 3 → mucho más rápido
df_solo_cols = pd.read_parquet(ruta_parquet,
    columns=["name", "email", "city"]
)

print(f"\nSolo columnas de interés:")
print(df_solo_cols.to_string(index=False))

print(f"\nParquet guardado: {ruta_parquet}")


## ─────────────────────────────────────────────────────────
#* PARTE 4: Comparación — cuándo usar cada formato
# ─────────────────────────────────────────────────────────

print("\n" + "=" * 55)
print("PARTE 4: Guía de decisión de formatos")
print("=" * 55)

guia = [
    ("JSON",    "APIs, configs, datos anidados",         "❌ analítica tabular grande"),
    ("CSV",     "Reportes a personas, Excel, intercambio","❌ pipelines internos"),
    ("Parquet", "Pipelines, big data, entre pasos ETL",  "❌ reportes a no-técnicos"),
]

print(f"\n{'Formato':<10} {'Úsalo para':<40} {'No uses para'}")
print("-" * 80)
for fmt, usar, no_usar in guia:
    print(f"{fmt:<10} {usar:<40} {no_usar}")

print("\n" + "=" * 55)
print("¡Lección 4 completada!")
print("Archivos generados:")
print(f"  {OUTPUT_DIR}/resultado_pipeline.json")
print(f"  {OUTPUT_DIR}/reporte_clientes_cerrados.csv")
print(f"  {PROCESSED_DIR}/clientes.parquet  (si pyarrow instalado)")
print("=" * 55)
