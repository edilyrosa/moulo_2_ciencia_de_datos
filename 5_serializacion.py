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
# ********************json.load(f) devuelve un objeto de Python (como un diccionario, lista, cadena, número, etc.)
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



#*********************** LEER EL JSON EN TDD PANDAS (→ DF || Serie) 
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



# SERIALIZAR UN DICT PY → .JSON CON TIPOS DE DATOS ESPECIALES (datetime)

def guardar_json(datos: dict, ruta:Path) -> None:
    
    def serializer(obj): #obj es TDD que el standar JSON, NO SABE TRATAR, != str, num, bool, list, obj
        if isinstance((obj, datetime)):
            return obj.isoformat() #str ISO
        raise TypeError(f'Tipo no es serializable {type(obj).__name__}') # pudo ser un set...
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(
            datos,
            f,
            default=serializer,
            indent=2,
            ensure_ascii=False
        )

# TODO: json.dump(), json.dumps()
print('tiempo', datetime.now().year)
resultado_pipeline = {
    'ejecutado_en': datetime.now(), #"2026-06-10 20:31:26.802390"
    'activo': True,
    "pipeline": "crm_analytics",
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

# ─────────────────────────────────────────────────────────
#* PARTE 1: JSON — leer y escribir
# ─────────────────────────────────────────────────────────



# # ## ─────────────────────────────────────────────────────────
# # #* PARTE 4: Comparación — cuándo usar cada formato
# # # ─────────────────────────────────────────────────────────

# # print("\n" + "=" * 55)
# # print("PARTE 4: Guía de decisión de formatos")
# # print("=" * 55)

# # guia = [
# #     ("JSON",    "APIs, configs, datos anidados",         "❌ analítica tabular grande"),
# #     ("CSV",     "Reportes a personas, Excel, intercambio","❌ pipelines internos"),
# #     ("Parquet", "Pipelines, big data, entre pasos ETL",  "❌ reportes a no-técnicos"),
# # ]

# # print(f"\n{'Formato':<10} {'Úsalo para':<40} {'No uses para'}")
# # print("-" * 80)
# # for fmt, usar, no_usar in guia:
# #     print(f"{fmt:<10} {usar:<40} {no_usar}")

# # print("\n" + "=" * 55)
# # print("¡Lección 4 completada!")
# # print("Archivos generados:")
# # print(f"  {OUTPUT_DIR}/resultado_pipeline.json")
# # print(f"  {OUTPUT_DIR}/reporte_clientes_cerrados.csv")
# # print(f"  {PROCESSED_DIR}/clientes.parquet  (si pyarrow instalado)")
# # print("=" * 55)
