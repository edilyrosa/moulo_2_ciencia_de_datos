"""
=============================================================
MÓDULO 1 — LECCIÓN 4: Serialización de datos (JSON, CSV, Parquet)
=============================================================

serializar = transformar objetos vivos de Python en bytes o texto que se puedan almacenar y luego reconstruir. Ejemplo:
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
    Saber leer y escribir los 3 formatos más usados en analítica de datos, y entender cuándo usar cada uno.

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

#* Func que espera por parametro Path, return Dict
def cargar_config(ruta: Path) -> dict: # [{}, {}, {}, ]
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)
    
# ********************CARGAR UN .json a TDD PY CON json.load(f) 
# devuelve un objeto de Py (como un diccionario, lista, cadena, número, etc.)
# que resulta de parsear el contenido del archivo f en formato JSON.
# Si el archivo JSON contiene un objeto (entre llaves {}), devuelve un diccionario (dict).
# Si contiene un array (entre corchetes []), devuelve una lista (list).
# También puede devolver otros tipos como str, int, float, bool o None, según los valores del JSON.

#& La función abre ese archivo, lee su JSON y lo retornandose el obj PY, guardandose en la var config.
config = cargar_config(RAW_DIR / "config_pipeline.json")
print('\n"config_pipeline.json" de JSON A dict PY\n', config)

#* COMO ACCE A LA INFO DE ESTE DICT (ANTES UN JSON)
print('\n\n\n')
print('Acc a TDD Primitivo', config['pipeline']) #crm_analytics
print( type(config.get('pipeline')) ) # <class str>
print('Acc a TDD Estrcutural - list de dicts', config.get("fuentes"))
print('Acc a TDD Estrcutural - Dict (pos 0 de la lista) ', config.get("fuentes")[0]) #
print('valor "CO" ', config.get("filtros").get('paises_activos')) # → ["CO", "MX", "CL", "AR"]
print('valor "CO" ', config.get("filtros").get('paises_activos')[0]) # "CO"

config_lista = cargar_config(RAW_DIR / "productos.json")
print('\n\n\n  "productos.json"de JSON A list de dicts PY\n', config_lista)

print('\n\n\n  acc al JSON → LISTA DIC post 0', config_lista[0]) #{'id': 1, 'nombre': 'Laptop Gamer XT-100', 'precio': 12500.0, 'categoria': 'Electrónica', 'stock': 15},
print(config_lista[0].get('nombre')) # Laptop Gamer XT-100'



#*********************** LEER EL JSON EN TDD PANDAS (→ DF || Serie) CON pd.read_json()
# pd.read_json(path del json)  del JSON → DF o Serie
# pd.to_csv(path del nuevo CSV)  DF o Serie → Formato 
#👀 identica la diferencia entre un dict, lista y DF O SERIE pandas, ejempl dict → key, list → post, df → loc[f, c]
df_json_dict = pd.read_json(RAW_DIR / "config_pipeline.json", orient='index')
print('\n\n\n imprimiendo el DF → JSON DICT \n', df_json_dict)
print('la row fuentes', df_json_dict.loc['fuentes']) # → la fila 
print('la row fuentes', df_json_dict.loc['fuentes', 0]) # → el valor
print('la row fuentes', df_json_dict.iloc[2, 0]) # → el valor
print('la row fuentes', df_json_dict.iloc[2, 0][0]) # →  {'nombre': 'clientes', 'tipo': 'csv', 'ruta': 'data/raw/clientes.csv', 'encoding': 'utf-8'}, 
# la row fuentes 
# [
# {'nombre': 'clientes', 'tipo': 'csv', 'ruta': 'data/raw/clientes.csv', 'encoding': 'utf-8'}, 
# {'nombre': 'transacciones', 'tipo': 'csv', 'ruta': 'data/raw/transacciones.csv', 'encoding': 'utf-8'}
# ]


df_json_list = pd.read_json(RAW_DIR / "productos.json")
print('\n\n\n ✅imprimiendo el DF → JSON LISTA\n', df_json_list)

print('Acc a una col nombre \n', df_json_list['nombre'])
print('Acc a una col id, nombre y stock \n', df_json_list[ ['id', 'nombre', 'stock'] ])
print('Acc a una col id, nombre y stock con loc[] \n', df_json_list.loc[:, ['id', 'nombre', 'stock'] ])


sabores = 'resa', "chl", "mani" #<class 'tuple'>
sabores = ('resa', "chl", "mani") #<class 'tuple'>
mi_set = {1,2,3, 5,5,5,6} 
print(type(sabores))



#* SERIALIZAR UN DICT PY → .JSON CON TIPOS DE DATOS ESPECIALES (datetime)
def guardar_json(datos: dict, ruta:Path) -> None:
    
    def serializer(obj): #obj es TDD que el standar JSON, NO SABE TRATAR, != str, num, bool, list, obj
        if isinstance(obj, datetime): #!⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️En clase coloque paréntesis extra, ya aca esta arreglado 
            return obj.isoformat() #str ISO
        raise TypeError(f'Tipo no es serializable {type(obj).__name__}') # pudo ser un set...
    
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(
            datos, # dict, list, str
            f,
            default=serializer,
            indent=4,               #* valores 0-4 y \t
            ensure_ascii=False      #* para que reconoazca UTF-8
        )

# TODO: INVESTIGAR: json.dump(), json.dumps()

print('tiempo', datetime.now().year)
resultado_pipeline = {
    'ejecutado_en': datetime.now(), #?"2026-06-10 20:31:26.802390"
    'activo': True,                 #?
    "pipeline": "crm_analytics, después, tamaño",
    "version": "1.0",
    "fuentes": [
    {
      "nombre": "clientes",
      "tipo": "csv",
      "ruta": "data/raw/clientes.csv",
      "encoding": "utf-8"
    },
    {
      "nombre": "transacciones",
      "tipo": "csv",
      "ruta": "data/raw/transacciones.csv",
      "encoding": "utf-8"
    }
  ],
  "filtros": {
    "valor_minimo": 1000,
    "etapas_validas": ["prospecto", "negociacion", "cerrado"],
    "paises_activos": ["CO", "MX", "CL", "AR"]
  },
  "output": {
    "formato": "parquet",
    "ruta": "data/processed/",
    "compresion": "snappy"
  },
  "notificaciones": {
    "email": "analytics@empresa.com",
    "alertar_si_registros_menor_a": 5
  }
}

# TODO:EJECUTEMOS LA FUNCION QUE SERIAMIZA guardar_json()******************

ruta_resultado_pipeline = OUTPUT_DIR / 'resultado_pipeline.json'
guardar_json(resultado_pipeline, ruta_resultado_pipeline )
print('El json se ha guardado en: ', ruta_resultado_pipeline)


resultado_pipeline_list = [
    {'clave1':'valor1'},
    {'clave2':datetime.now()},
    {'clave3': [1,2,3, False]}, #el ultimo de este
    {'clave4': (1,2,3, False)},
    # {'clave5': {1,2,3, False}}, #este no es un TDD serialzable por JSON, entonc debiste controlarlo en serializer()
]

ruta_resultado_pipeline_lista = OUTPUT_DIR / 'resultado_pipeline_lista.json'
guardar_json(resultado_pipeline_list, ruta_resultado_pipeline_lista )
print('El json list se ha guardado en: ', ruta_resultado_pipeline_lista)


#* verificando la carga del JSON en PY
con_verificacion_lista  = cargar_config(ruta_resultado_pipeline_lista)
print(con_verificacion_lista[2]['clave3'][3])   # False
print(con_verificacion_lista[2]['clave3'][-1])  # False

con_verificacion  = cargar_config(ruta_resultado_pipeline)
print(con_verificacion["ejecutado_en"])  # "2026-06-15T19:30:02.194561"
print(type(con_verificacion["ejecutado_en"]))  # <class str>


#? dtype={} para regularizar estas salidas → 2026-06-15T10:57:10.091003
# Es de Pandas (por ejemplo, pd.read_csv() o pd.read_json()). 
# Con json.load() obtienes diccionarios y listas nativas de Python, no un DataFrame.
#TODO TAREA USA DF: 💡Si quieres usar dtype para definir tipos de columnas necesitas pandas:
# df = pd.read_json('archivo.json', orient='records', dtype={'columna': 'str', 'otra_columna': 'int'})

# ─────────────────────────────────────────────────────────
#* PARTE 2: CSV — leer y escribir
# ─────────────────────────────────────────────────────────
print("\n\n\n" + "=" * 55)
print("PARTE 2: CSV")
print("=" * 55)

df_clientes = pd.read_csv( RAW_DIR / 'clientes.csv')
print('\nSIN TIPAR \n', df_clientes)

df_tipado = pd.read_csv( RAW_DIR / 'clientes.csv', #Ruta del CSV a leer
                        #   dtype= {} dtype='string' COMO DEEB ALMACENAR PANDAS ESE COLUMN EN MEMORIA
                        dtype= {
                            "id":"int32",
                            "nombre":"string",
                            "pais":"category",
                            "industria":"category",
                            "valor_contrato":"float64",
                            "etapa":"category",
                        },
#* Regla de conversión
    # Qué VALORES ESPECIFICOS debe considerar Pandas como el TDD ESPECIFICADO al parsear el archivo, antes de asignar el tipo.
                        parse_dates=["fecha_cierre"],  # Columna de str → datetime, para hacer operaciones temporales (restar fechas, extraer año, etc.).
                        true_values=["True"],          # De "True" str → a bool Python
                        false_values=["False"],
    # true_values=["Sí", "Si", "1", "True", "YES"],   # ← todos estos se convierten a True
    # false_values=["No", "0", "False", "NO"]         # ← estos a False
                        )
    #* Otros parámetros que dan control fino sobre cómo se lee el archivo CSV
    #* 📊 Tipos y memoria
    # dtype : dict con tipos específicos
    # converters : dict con funciones para convertir columnas (ej: {"precio": lambda x: float(x.replace("$", ""))}).
    # low_memory : True, lee por fragmentos (menos memoria, más lento). False, carga todo antes de tipar (cuando dtype está especificado).
    # memory_map : mapea el archivo en memoria para mejor rendimiento en archivos grandes.
    
    #*📅 Fechas y horas
    # parse_dates : convierte columnas a datetime.
    # date_parser : función personalizada para parsear fechas (ej: lambda x: pd.to_datetime(x, format='%d/%m/%Y')).
    # dayfirst : INTERPRETA QUE en el date, el día va primero (ej: dd/mm/aaaa en lugar de mm/dd/aaaa).
    # date_format : especifica el formato de fecha (ej: "%Y-%m-%d").
    
    #* 🎯 Manejo de valores nulos
    # keep_default_na : si False, no convierte automáticamente cadenas como "null", "NULL", "NA" a NaN.
    # na_values : lista de valores adicionales a tratar como NaN (ej: ["N/A", "Missing", "-"]).
    # keep_default_na + na_values : personaliza por completo qué es nulo.


print('\n⭐ TIPARDO \n', df_tipado)
print('\n⭐ Filas', len(df_tipado))
print('\n⭐ TDD ', df_tipado.dtypes.to_string())
print('\n⭐ TDD NO TIPADOS', df_clientes.dtypes.to_string())


#* FUNC QUE SERIALIZA EL DF tipado  →  DF filtrado →  .CSV comp con excel
def exportar_reporte_csv(df: pd.DataFrame, ruta: Path) -> None:
    df.to_csv(
        ruta,
        index=False,
        encoding='utf-8-sig', # BOM (Byte Order Mark) oblig de CSV → EXCEL
        sep=','  
    ) 

reporte = (
    df_tipado
    .query(" etapa == 'cerrado' and activo == True ")
    # [ ["id", "nombre", "pais", "industria", "fecha_cierre" ,"fecha_cierre"] ]
    #*Para ordenar por columna, debe existir. ✅
    [ ["id", "nombre", "pais", "industria", "valor_contrato" ,"fecha_cierre"] ] 
    .sort_values("valor_contrato", ascending=False) #TODO⚠️ 
    .reset_index(drop=True)
    
)
ruta_reporte  = OUTPUT_DIR / 'reporte_clientes_cerrados.csv'
exportar_reporte_csv(reporte, ruta_reporte)
print('se creo ', ruta_reporte)
print(' REPORTE FILTRADO \n', reporte.to_string(index=False))


#**** EXTRA: SERIALIZAMOS DF →  EXCEL en "reporte_clientes_cerrados.xlsx"

ruta_excel = OUTPUT_DIR / 'reporte_clientes_cerrados.xlsx'
reporte.to_excel(ruta_excel, index=False, sheet_name='Clientes_cerrados')
print('se creo ', ruta_reporte)
print(' REPORTE FILTRADO \n', reporte.to_string(index=False))


#! ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️ to_excel requiere: openpyxl
# TODO: INVESTIGA LA DIFERENTE ENTER openpyxl y xlsxwriter
#! Ejecuta en tu terminal (el mismo entorno virtual que usas, .venv):
# .venv\Scripts\activate
# python -m pip install --upgrade pip
# python -m pip install openpyxl
# python -c "import openpyxl; print(openpyxl.__version__)" #Verificamos instalacion 3.1.5 
# TODO: INVESTIGA COMO LEER CON PANDAS UN EXCEL: df = pd.read_excel('archivo.xlsx'), investiga los parametros mas utilies


# ─────────────────────────────────────────────────────────
#* PARTE 3: Parquet — el formato de pipelines analíticos
# ─────────────────────────────────────────────────────────
print("\n\n\n" + "=" * 55)
print("PARTE 3: Parquet")
print("=" * 55)
#*  Parquet es formato BINARIO de almacenamiento columnar — Eficiente para analítica.
# Guarda los datos por columnas, no por filas. 
# Ventajas:
#   ✓ Compresión automática (snappy, gzip)
#   ✓ Preserva los TDD (fechas, booleanos, categorías, etc.) – no tienes que volver a especificarlos al leer.
#   ✓ Lectura selectiva de columnas – puedes leer solo las columnas que necesitas, ignorando el resto.
#   ✓ Particionamiento – puedes dividir el archivo en carpetas por fecha, país, etc., y luego leer solo las particiones relevantes.
#! ⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️⚠️ to_parquet(), read_parquet() requiere: pyarrow (o fastparquet)
# como motor para trabajar con formato Parquet.
import pyarrow 
# .venv\Scripts\activate
# python -m pip install pyarrow
# python -c "import pyarrow; print(pyarrow.__version__)" # 24.0.0
#? Parquet Viewer

ruta_csv_largo = RAW_DIR /'sample-csv-10000-rows.csv'
ruta_parquet = RAW_DIR /'clientes.parquet'

pd_csv_largo = pd.read_csv(ruta_csv_largo)
pd_csv_largo.to_parquet(  # df a SERIALIZAR como parquet
    ruta_parquet,         # Ruta del parquet
    compression='snappy', #⭐ Comprime Archivo grande, Lectura/escritura más rápida, Ocupa más disco
    engine='pyarrow',     #⭐ Motor usa pandas para leer/escribir Parquet.
    index=False
)

# TODO: *************************LO QUE FALTO 

#* ------------ Comparando el tamano de ambos (CSV vs. Parquet)
tamaño_csv     = ruta_csv_largo.stat().st_size
tamaño_parquet = ruta_parquet.stat().st_size
print(f"\nArchivo original (CSV)   : {tamaño_csv:,} bytes")
print(f"Archivo comprimido (parquet): {tamaño_parquet:,} bytes")
print(f"Reducción de tamaño      : {(1 - tamaño_parquet/tamaño_csv)*100:.0f}%")  # Redondea

#* --- Leer Parquet completo ---
df_leido = pd.read_parquet(ruta_parquet)
print(f"\nLeído desde Parquet: {len(df_leido)} filas")
print(f"Tipos preservados  :") #?Si tu serializas un TDD time, eso mismo recuperas. 
print(df_leido.dtypes.to_string())
print(df_leido[ ["name", "email", "city"] ].head()) 

    
#* --- Leer solo columnas necesarias (enorme ventaja en big data) ---
# En un archivo de 50 columnas, esto lee solo 3 → mucho más rápido
df_solo_cols = pd.read_parquet(
    ruta_parquet,
    columns=["name", "email", "city"]
)
print(f"\nSolo columnas de interés:")
# print(df_solo_cols.to_string(index=False)) #!muy largo
print(df_solo_cols.head()) #!muy largo
print(f"\nParquet guardado: {ruta_parquet}")




## ─────────────────────────────────────────────────────────
#* PARTE 4: Comparación — cuándo usar cada formato
# ─────────────────────────────────────────────────────────

print("\n\n\n" + "=" * 55)
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
