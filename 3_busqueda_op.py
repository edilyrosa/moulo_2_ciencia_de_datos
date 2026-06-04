import pandas as pd
from pandas.errors import EmptyDataError
from pathlib import Path

#* ================= CONFIGURACIÓN DE RUTAS =================
JSON_PRODUCTOS_RAW_DIR = Path(__file__).parent / "data" / "raw" / "productos.json"       
JSON_CONFIG_RAW_DIR = Path(__file__).parent / "data" / "raw" / "config_pipeline.json"   

CSV_DATA_RAW_DIR = Path(__file__).parent / "data" / "raw" / "clientes.csv"       
CSV_DATA_RAW_DIR =  Path(__file__).parent / "data" / "raw" / "sample-csv-10000-rows.csv" # (10,000 filas)

#* =============================================================== CARGA DE DATOS =================

df_json = pd.read_json(JSON_PRODUCTOS_RAW_DIR) #*✅
df_json = pd.read_json(JSON_CONFIG_RAW_DIR, orient='index') #*👀orient='index'
# print(df_json.head(5))

    #************************************* ATRIBUTO orient= en los JSON
# TODO: orient='index', 'columns'... 

    
    #*********************************** VAMOS A TRABAJAR CON EL CSV LARGO
try:
    # df_csv = pd.read_json(CSV_DATA_RAW_DIR) #! FrameParser(json, **kwargs).parse()
    df = pd.read_csv(CSV_DATA_RAW_DIR) #*??
    print('\nArchivo CSV cargado!!' )
    print(df.head(5))
    
except FileExistsError as e:
    print(f'❌ Error el archivo en {CSV_DATA_RAW_DIR} no existe, {type(e).__name__} - {e}') #No such file or directory
    exit()
except FileNotFoundError as e:
    print(f'❌❌ Error el archivo en {CSV_DATA_RAW_DIR} no existe, {type(e).__name__} - {e}') #No such file or directory
    exit()
    
except EmptyDataError as e:
    print(f'❌❌ Error el archivo en {CSV_DATA_RAW_DIR} no tiene data, {type(e).__name__} - {e}') #No such file or directory
    exit()
    
except pd.errors.ParserError as e: #si lo llamas asi (sin importatlo arriba), debes acceder a la subcll error de pandas
    print(f'❌ el archivo {CSV_DATA_RAW_DIR} no tiene ext requuerida, {type(e).__name__} - {e}') #No such file or directory
    exit()
    
except ValueError as e:
    print(f'❌ el archivo {CSV_DATA_RAW_DIR} no tiene ext requuerida, {type(e).__name__} - {e}') #No such file or directory
    exit()
except Exception as e:
    print(f'❌ Error inesperado {type(e).__name__} - {e}') #No such file or directory
    exit()

    
#* ============================================== SELECCIÓN DINÁMICA DE COLUMNA =================
# ?FACIL
# columna_city = input('Ingrese el nombre de la columna donde desea realizar la busqueda: ')
# city = input('Ingrese el valor qur sea buscar en la columna (Criterio de busqueda): ')

#? DIFICIL: PRACTICAMOS METODOS DE PANDA
columna_city = df.columns[2] #* Return nombre en str de la columna cuya le pase por parametro
print(columna_city) #city
print('\nla col city')
print(df[columna_city])
print(df[columna_city].loc[9999]) # New Golda
print(df[columna_city].loc[0])    # Darianamouth
print('\n\nEl DF de la fila 0')
print(df.loc[0])    # Retorna un DF o una Serie
city = df[columna_city].loc[9999] #*
print('QUE SOY', df.iloc[9999, 2]) # New Golda

# df.loc[fila || fila, columna] # key, o sea spera string, pero las claves de las filas con num
# df.iloc[fila || fila, columna] #numero

#* 💡 Resumen:
# df.columns[2] → devuelve el nombre de la columna (string).
# df[columna_city_str] → devuelve la serie completa de esa columna.
# df.iloc[999, 2] → devuelve el valor en la fila 999, columna posicional 2.
# df[columna_city].iloc[10] → devuelve el valor en la fila 999 de la columna cuyo nombre guardas en columna_city.


#* ========================================= PRUEBA DE BUSQUEDA CON ÍNDICE (O(1) esperado) =================
columna_city = input('Ingrese el nombre de la columna donde desea realizar la busqueda: ')
city = input('Ingrese el valor que sea buscar en la columna (Criterio de busqueda): ') #New Golda

df_indexado = df.set_index(columna_city)
print('DATAFRAME INDEX POR LA COL CITY')
print(df_indexado)
print('RESULTADO DE BUSQUEDA INDEXDA POR CIUDAD')

import time                              #********************⏲️

inicio_dict = time.perf_counter()        #********************⏲️
#* ....programacion a cronometrar....
resultado_index  = df_indexado.loc[city] #& Programacion (1)
fin_dict = time.perf_counter()           #********************⏲️
tiempo_index = fin_dict - inicio_dict #* RESULTADO ⏲️
print(resultado_index)

# if isinstance(3, (int, bool)): #T
#     pass
if isinstance(resultado_index, pd.DataFrame): # Si hay mas de 1 registro q cumple con el criterio (city)
    filas_index = len(resultado_index) # Es un dataframe y puede usar el method len()
else:
    filas_index = 1 # Ya se que es una serie, con un unico elemento o registro dentro, entonces:
    
print('RESULTADO !!', tiempo_index, filas_index)

#* =========================================== PRUEBA DE BUSQUEDA CON FILTRO (O(n)) =================
inicio_filtro = time.perf_counter()         #***************⏲️

df[city] == city

#* ================= RESULTADOS =================

# print('\n\n\n*************RESULTADOS*************')
# print(f"\n📊 Tamaño del DataFrame: {} filas")                          # 10,000
# print(f"⚡ Tiempo con índice (O(1) esperado): {} segundos")     # 0.00163050 segundos
# print(f"   → Filas encontradas: {}")                                  # 2
# print(f"⚡ Tiempo con filtro (O(n) vectorizado): {} segundos") # 0.00198520 segundos
# print(f"   → Filas encontradas: {}")                                # 2

