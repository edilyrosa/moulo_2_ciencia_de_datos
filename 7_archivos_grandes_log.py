# =============================================================
#* MÓDULO 2 — LECCIÓN 6: Manejo eficiente de archivos grandes
# =============================================================
import pandas as pd
from pathlib import Path
import time                                            # time.time() retorna el timestamp Unix
from errores_logging import (
    crear_logger, 
    validar_columnas,
    validar_tipo_columna,
    ArchivoNoEncontradoError,
    DatosInvalidosError,
    ColumnaFaltanteError,
    TipoIncompatibleError
    )

# =============================================================
#* CONFIG DEL LOG 
# # =============================================================
log = crear_logger('pipeline_archivos_grandes')


RAIZ = Path(__file__).parent
RAW_DIR = RAIZ / "data" / "raw"
PROCESSED_DIR = RAIZ / "data" / "processed"

CSV_PATH = RAW_DIR / "sample-csv-10000-row.csv"         #* ← Usaremos este
if not CSV_PATH.exists():
    log.error(f'El archivo de entrada no se encuentra en {CSV_PATH}') #!Not
    raise ArchivoNoEncontradoError(
        f'No existe {CSV_PATH}\n'
        f'Verifica en data/raw'
    )
log.debug('√ Archivo {CSV_PATH} enontrado')


print(f"✓ Archivo encontrado: {CSV_PATH.name}")         # Nombre + extension ( .stem, .suffix)     # Nombre + extension ( .stem, .suffix)
print(f"✓ Tamanio en disco: {(CSV_PATH.stat().st_size / 1024**2):.2f} MB")         # Nombre + extension ( .stem, .suffix)     # Nombre + extension ( .stem, .suffix)
tamaño_disco_mb = CSV_PATH.stat().st_size / 1024**2 #TODO




# ============================================================
#* FUNCIONES INTERMEDIAS
# ============================================================
print("\n" + "=" * 55)
print("PARTE 1: CARGA NORMAL (todo a la vez)")
print("=" * 55)

def cargar_y_validar_csv(ruta:Path, log) -> pd.DataFrame:
    try:
        log.info(f'Cargando el archivo {ruta.name}')
        df = pd.read_csv(ruta) 
        validar_columnas(df, 'age', int, log)
        validar_tipo_columna()
        # query(df['age'] >40)
    except:
        pass
        






#* I--------------------------------⏲️ MEDIMOS TIEMPO TOTAL
inicio_normal = time.time()
#* II ------------------------------⭐ LEEMOS EL CSV COMPELTO: + RAM, - TIEMPO



df_completo = pd.read_csv(CSV_PATH)



len_df_completo = len(df_completo)
#* III -----------------------------🏋🏻MEDIR RAM TOTAL DEL FD COMPLETO CARGADO EN PY
#? memory_usage() 
# Método de DF y retorna una Serie de: key (índice, cada columnas) Value (memoria RAM que ocupan cada una)
# deep=True incluye strings
#? .sum()
# Llamado por la Serie que retornó memory_usage()
# Retorna: Un int (la suma total de bytes)
memoria_normail_bytes = df_completo.memory_usage(deep=True).sum() 
memoria_normail_mb = memoria_normail_bytes  / 1024**2 # despues para comparacion 
# print('TOTAL DEL DF COMPLETO ', memoria_normail_bytes)

#* IV ----------------------------- 📊 ANALIZA TU DATA EN PY
# FILTRAR FILAS POR "age" > 40
# df_filtrado = df_a_ser_filtrado[ serie bool, retuen de solo los True]  
# df_mayores_40 = df_completo[ df_completo['city'] > 40 ]
# df_mayores_40 = df_completo[ df_completo.age > 40 ] #⚠️ puede ocurrir error por el nombre de la col
df_mayores_40 = df_completo[ df_completo.loc[:, 'age'] > 40 ]

print('aqui', df_mayores_40.dtypes.to_string()) #* ... age → int64, entonces df_completo['age'] > 40 ✅


#? seleccionamos solol algunas col
df_reporte = df_mayores_40[ ['name', 'age', 'city'] ]  #⭐💡

# FILTRO Y SELECCION con loc[fila, col]
df_reporte_loc = df_completo.loc[ df_completo['age'] > 40 , ['name', 'age', 'city'] ]

print('-----------------------------LOS PRIMEROS 5 REGISTROS FILTARDOS CLIENTES MAYORES DE 40 --------------------') 
print(df_reporte_loc.head())
print(df_reporte.head())

#? Resumen de las formas correctas
#? Objetivo                                  	                  Código
# Seleccionar columnas específicas (todas las filas)	→ df[ ["col1", "col2"] ]
# Filtrar filas por condición	                        → df[ df["col"] > valor ]
# Filtrar filas Y seleccionar columnas	              → df.loc[ df["col"] > valor, ["col1", "col2"] ]
# Seleccionar columnas con .loc	                      → df.loc[:, ["col1", "col2"]]


#SERIALIZAMOS EL REPORTE A UN .csv(ruta)
salida_normal = PROCESSED_DIR / 'clientes_mayores_40_normal_csv'
df_reporte.to_csv(salida_normal, index=False)

#* V --------------------------------⏲️ CERRAMOS CRONOMETRO
tiempo_normal = time.time() - inicio_normal
clintes_filtrados_normal = len(df_reporte)

print(f"\n📊 RESULTADOS CARGA NORMAL:")
print(f"  Filas procesadas      : {len(df_completo):,}")          #10,000         
print(f"  Clientes > 40 años    : {clintes_filtrados_normal}")    #6641          
print(f"  ⏱️  Tiempo total        : {tiempo_normal:.4f} segundos")    #0.4657 segundos
print(f"  💾 Memoria RAM: {memoria_normail_mb:.2f} MB")     # 0.96 MB  
print(f"  📁 Reporte guardado en : {salida_normal}")       #c:\Users\edily\Desktop\moulo_2_c\data\processed\clientes_mayores_40_norma          

# libermos memoria RAM
del df_completo, df_mayores_40,  df_reporte, df_reporte_loc

# ============================================================
#* PARTE 2: PROCESAMIENTO POR CHUNKS
# ============================================================
print("\n" + "=" * 55)
print("PARTE 2: PROCESAMIENTO POR CHUNKS")
print("=" * 55)
CHUNK_SIZE = 500
print(f"\n🔄 Procesando con chunks de {CHUNK_SIZE} filas...")


#* I--------------------------------⏲️ MEDIMOS TIEMPO TOTAL
inicio_chunking = time.time()
# variables a ocuopar
total_filas_procesadas = 0 # deberia llegar a 10,000 de 500 en 500
total_filas_filtradas = 0 
ram_max_chunk_mb = 0
archivo_creado = False #🏳️ para saber si uso modo "w" o "a"
salida_chunk = PROCESSED_DIR / 'clientes_mayores_40_chunk_csv'

#* II ------------------------------⭐ LEEMOS EL CSV COMPELTO: - RAM, + TIEMPO
# No carga todo el CSV. 
# Iterable que va entregando DataFrames de 500 filas cada vez, 
#* iterador_reporte_chunks = pd.read_csv(salida_chunk, chunksize=CHUNK_SIZE)

for i, chunk in enumerate(pd.read_csv(CSV_PATH, chunksize=CHUNK_SIZE)):
    #* III -----------------------------🏋🏻MEDIR RAM TOTAL DEL FD COMPLETO CARGADO EN PY
    ram_chunk_mb =  (chunk.memory_usage(deep=True).sum()) / 1024**2
    ram_max_chunk_mb = max(ram_max_chunk_mb, ram_chunk_mb) 
    total_filas_procesadas += len(chunk) 

    #* IV ----------------------------- 📊 ANALIZA TU DATA EN PY
    chunk_reporte = chunk.loc[ chunk['age'] > 40 , ['name', 'age', 'city'] ]
    total_filas_filtradas += len(chunk_reporte)

# SERIALIZACION POR CHUNKS
    if len(chunk_reporte) > 0: #si hay reporte
        if not archivo_creado: #🏳️ es la primera vez + jay reportes (clientes >40)
            chunk_reporte.to_csv(salida_chunk, mode='w', index=False)
            archivo_creado = True
        else:
            chunk_reporte.to_csv(salida_chunk, mode='a', header=False, index=False)

#* V --------------------------------⏲️ CERRAMOS CRONOMETRO
tiempo_chunking = time.time() - inicio_chunking

print('\n\n\n\n')



#?-------------------💡 EXPLICACION: pd.read_csv() con chunksize devuelve un iterador, no un DataFrame.
# No carga todo el CSV. 
# Iterable que va entregando DataFrames de 500 filas cada vez, 
#* iterador_reporte_chunks = pd.read_csv(salida_chunk, chunksize=CHUNK_SIZE)

# # print(iterador_reporte_chunks.head(10).to_string(index=False)) #!chunksize devuelve un iterador, no un DataFrame.

#? El iterador es perezoso (lazy loading): solo carga cuando le pides.
# √ Debe ser recorrido dentro del loop
# √ SOLO 1 chunk, Carga bajo demanda.
# * primer_chunk = next(iterador_reporte_chunks)  #* ← Obtienes el primer chunk, 
# segundo_chunk = next(iterador)  # ← Chunk 2
# tercer_chunk = next(iterador)   # ← Chunk 3

#? En vez de ieteador ❌ list() hastas RAM
# fuerza la carga de TODOS los chunks en RAM, Todo el archivo está en memoria
# chunks = list (pd.read_csv(CSV_PATH, chunksize=CHUNK_SIZE))
# primer = chunks[0]   # ← Ahora sí por posición
# segundo = chunks[1]

# #? 📌 REGLA DE ORO
# # Los iteradores son de un solo uso y secuenciales
# # Si necesitas acceso aleatorio → usa lista (pero pierdes eficiencia de memoria)

#? 🎯 ¿CUÁNDO USARÍAS chunksize EN to_csv()?
# to_csv() también se puede usar por chunks usando el parámetro chunksize 
# Solo si el DataFrame que quieres escribir es MUY GRANDE.
# para escribir el DataFrame en lotes y así reducir el pico de uso de memoria durante la escritura.
# Escribe de a 500,000 filas por vez

#TODO: Practicalo: df.to_csv('archivo_grande.csv', index=False, chunksize=500_000) → 500000	== 500_000, el _ es un eparador visual
# El resultado final es un solo archivo CSV, pero el proceso de escritura es más eficiente en memoria.


print(f"\n📊 RESULTADOS CHUNKING:")
print(f"  Filas procesadas      : {total_filas_procesadas}")          
print(f"  Clientes > 40 años    : {total_filas_filtradas}")          
print(f"  ⏱️  Tiempo total        : {tiempo_chunking} segundos")   
print(f"  💾 Memoria RAM (máxima): {ram_max_chunk_mb} MB")        
print(f"  📁 Reporte guardado en : {salida_chunk}")                  


# ============================================================
#* PARTE 3: COMPARATIVA DE TIEMPO Y RAM (MEJORADA)
# ============================================================

print("\n" + "=" * 55)
print("PARTE 3: COMPARATIVA DE CONSUMO")
print("=" * 55)

#? Calcular porcentajes
ahorro_ram        = memoria_normail_mb - ram_max_chunk_mb
porcentaje_ram    = (ram_max_chunk_mb / memoria_normail_mb) * 100
porcentaje_tiempo = (tiempo_chunking  / tiempo_normal)     * 100


#* {cifra :>14.2f} ←  alineado a la derecha, ancho de 14 caracteres, 2 decimales
#* {cifra :>14,}  14 espacios, alineado a la derecha, con comas como separador de miles
print(f"""
┌────────────────────────────────────────────────────────────────┐
│                    COMPARATIVA DE CONSUMO                      │
├──────────────────────────┬─────────────────┬───────────────────┤
│ MÉTRICA                  │ CARGA NORMAL    │ CHUNKING          │
├──────────────────────────┼─────────────────┼───────────────────┤
│ Archivo en disco (MB)    │ {tamaño_disco_mb:>14.2f}  │ {tamaño_disco_mb:>13.2f}     │ 
│ ⏱️  Tiempo (segundos)     │ {tiempo_normal:>14.4f}  │ {tiempo_chunking:>13.4f}     │
│ 💾 RAM usada (MB)        │ {memoria_normail_mb:>14.2f}  │ {ram_max_chunk_mb:>13.2f}     │
│ Filas en memoria         │ {len_df_completo:>14,}  │ {CHUNK_SIZE:>13,}     │
│ Clientes > 40 años       │ {clintes_filtrados_normal:>14,}  │ {total_filas_filtradas:>13,}     │
├──────────────────────────┼─────────────────┼───────────────────┤
│ AHORRO DE RAM            │        -        │  {ahorro_ram:>8.2f} MB      │
│ REDUCCIÓN DE RAM         │        -        │     {100 - porcentaje_ram:>8.1f}%     │
│ INCREMENTO DE TIEMPO     │        -        │     {porcentaje_tiempo - 100:>8.1f}%     │
└──────────────────────────┴─────────────────┴───────────────────┘

📊 ANÁLISIS DE EFICIENCIA:
  • RAM: Chunking usa solo {porcentaje_ram:.1f}% de la RAM (ahorro de {ahorro_ram:.2f} MB)
  • Tiempo: Chunking es {tiempo_chunking/tiempo_normal:.1f}x más lento
""")


print("\n" + "=" * 55)
print("✅ LECCIÓN 6 COMPLETADA - REPORTE DE CLIENTES > 40 AÑOS")
print("=" * 55)
print(f"\n📁 Archivos generados:")
print(f"  - {salida_normal.name} (carga normal)")
print(f"  - {salida_chunk.name} (chunking)")


# TODO TAREA: PARQUET TAMBIÉN SOPORTA CHUNKS?
# HAGA ESTE MISMO EJERCICIO CON .parquet LOS RESULTADOS EN CHAT DE LA CLASE