

# ─────────────────────────────────────────────────────────
#* PARTE 1: dict — índice de búsqueda rápida (O(1))
# ─────────────────────────────────────────────────────────
import pandas as pd
from pathlib import Path


RAIZ = Path(__file__).parent

RAW_DIR= RAIZ /'data' / 'raw'
# quiero un dataframe de clientes.csv
print('\nDataframe de clientes.csv ') #👀 es una tabla.
df =  pd.read_csv(RAW_DIR / 'clientes.csv')
print(df)
print(df.head())
print(df.describe())
print(df.shape) # (filas, columnas)
print(df['nombre']) # 
print(df[ df['nombre'] == ' Delta Ltd'] ) # 


#! ✗  listas/DataFrame — BUSCAR por valor es O(n)
clientes = ['Delta Ltd', 'Gamma Inc', 'Beta LLC', 'Alpha Co']



# 💡Convertir el DataFrame a un dict, para tener acceso O(1) a los clientes por su id o nombre, 
# sin importar la cantidad de registros que haya. Despues veremos como hacerlo.

#! ✗  listas/DataFrame — BUSCAR por valor es O(n)


#? Se RECORRE!! iterables con Operador "in" 
print('\n\nImpresion de elemento por elemento de una lista')

    
for c in clientes:
    if c == 'Delta Ltd':
        print('si esta ', c)

#? Saber si un elemento existe en el iterable con Operador "in"
mi_tupla = (1, 2, 3, 4, 5)
esta = 10 in mi_tupla
respuesta =  'si 'if esta else 'no'
print(respuesta, 'esta el 10 en la tupla') #no

#? list.index(ele) → Retorna la pos o indice del ele parametro
#! ✗  El método RECORRE LA LISTA! elemento por elemento (búsqueda lineal) 
# hasta encontrar el valor o llegar al final. 
# TODO: list.index() es O(n)?
clientes.index('Alpha Co') #

print()

#* Diccionario:  key → value. La búsqueda es O(1)
# Con dict: acceso instantáneo sin importar cuántos registros haya
# Estructuras de rápido acceso para búsquedas frecuentes, mediante una key (nombre)
#? √ El dict es O(1) porque usa hash, no posición
indice = {
          'Alpha Co': 1,
            'Beta LLC': 2,
            'Gamma Inc': 3,
            'Delta Ltd': 4
          }
print(indice['Delta Ltd'])



# https://pokeapi.co/api/v2/
# https://pokeapi.co/api/v2/pokemon/pikachu
# https://jsonplaceholder.typicode.com/users []

# ? La notación O(n) (llamada “Big O”) 
# es una forma de describir cómo crece el tiempo de ejecución de un algoritmo 
# cuando aumenta la cantidad de datos (n).
# ? O(n) 
# El tiempo es proporcional al tamaño de los datos (crecimiento lineal).
# Si tienes 1.000 clientes, el algoritmo tardará ~1.000 pasos.
# Ejemplo: buscar en una lista sin índice (recorriendo elemento por elemento).
# ?	O(1) 
# El tiempo es constante, no importa cuántos datos haya.
# Con 1 cliente o con 1.000.000 de clientes, el acceso toma el mismo tiempo (un paso).
# Ejemplo: buscar por clave en un diccionario (dict).

#?  Eficiencia de BUSQUEDA entre: 
#! ✗ lista o DataFrame (por índice posicional) — O(1) si conoces la posición, pero O(n) si buscas por valor
#* √ diccionario (por clave), busqueda precisa por clave, sin importar posición o cantidad de registros


#* LOS DICT SON UNA COLECCIÓN DE PARES CLAVE-VALOR.
# Son mutables (puedes modificar sus elementos). Se crean entre llaves {} o con el constructor dict().
# Cada clave es única y se asocia a un valor. Deben ser hashables (no cambian mientras existan, son inmutables → int, str, tuple).
personaje = {
    # key:value,
    # key:value,
    'nombre': 'Edily',
    'nombre': 'Mujer Maravilla',
    'edad': 33,
    'peso': 56.66,
    'poder': ['volar', 'fuerza'],
    True: 'Mujer',
    2: 'dos',
    "posicion": {
        (0,0):0,
        (0,1):1,
        (0,2):'Qubit cuantico ',
        # ([1,3],2):'Soy posible ', #!unhashable type: 'list'
    } 
}

print(personaje)
print(personaje['nombre'])
# print(personaje['apellido']) #!
print(personaje.get('apellido'), 'No existe la key "ape"') #!
print(personaje['posicion'][(0,1)])
personaje['posicion'][(0,1)] = True
print(personaje['posicion'])

#? Acceso
print()
#? Modificar un valor de posición

#? los Dict tienen metodos interesantes:
# mi_dict.pop('peso') # Elimina el de la key argumento
# mi_dict.popitem()   # Elimina el ultimo
# mi_dict.clear()     # Elimina todas las key/value
# mi_dict.keys()      #dict_keys(['nombre', 'edad', 'peso', 'poder', 'hobbies', 'mujer', 2, False, ('nota', 'materia')])
# mi_dict.values()    #dict_values(['Mujer Maravilla', 33, 56.66, ['volar', 'fuerza'], ('salvar el mund
# mi_dict.items()   #dict_items([('nombre', 'Mujer Maravilla'), ('edad', 33), ('peso', 56.66), ('poder', ['volar', 'fue

#? ⭐ Dict compacto
claves = ['a', 'b', 'c', 'd']
valores = [1, 2, 3, 4]

#? ⭐ Metodo zip() Crear un dict a partir de dos listas: una de claves y otra de valores
# <zip object at 0x7f8c9c1e5b80>
dict_zip = dict(zip(claves, valores))
print('uno', dict_zip)

#? ⭐ Dict compacto
#?SINTAXIS:  {clave: valor  for elemento in iterable.iterrows(), .zip(), .items()...}
dict_compacto = {k:v for k, v in dict_zip.items()}
dict_compacto_filtrado = {k:v for k, v in dict_zip.items() if v % 2 == 0} # con condicion, solo pares
print( 'dos', dict_compacto)
print( 'tres', dict_compacto_filtrado)
#?⭐ Lista compacta: 

print('\n💡Impresion de listas compactas')
lista_original = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
lista_compacta_filtrada = [e for e in lista_original if not e % 2 == 0]
print('cuatro', lista_compacta_filtrada)
# #? 🤸🏻 EJERCICO: realiza una lista compacta con 24 elementos: "ciudad-1", "ciudad-2", ... "ciudad-24"
# num_ciudades = 25
# ciudades = [f'Ciudad-{num}' for num in range(1, num_ciudades)]
# print('💡Impresion de lista compacta de ciudades')
# print(ciudades)
    
    
#******************************VOLVAMOS AL DATAFRAME Y LOS DICT*************************************
#& Para ENCONTRAR un cliente debes recorrer TODA una columna del DataFrame
# Con dict: acceso instantáneo sin importar cuántos registros haya
#? Dict comprehension — construir índice en una línea
# {clave: valor  for elemento in iterable.iterrows()}
print('\n\n Dataframe convertido a dict, con id como clave')
print('\n\n Dataframe original')
print(df)
indice_por_id = {row['id']:row.to_dict() for _, row in df.iterrows()}
print('\nDict del df')
indice_por_queSoy = { row['id']:row['nombre'] for _, row in df.iterrows() } #→ {2:'Beta Inc',  1: 'Acme Corp'}
print(indice_por_id)
print('cliente en id 13')
print(indice_por_id[13]) #13: {'id': 13, 'nombre': 'Nu SA', 'pais': 'AR', 'ciudad': 'Buenos Aires', 'industria': 'Tecnología', 'valor_contrato': 2900, 'etapa': 'negociacion', 'fecha_cierre': '2024-07-01', 'activo': True},
print('dict por id con toda la info del nombre cliente')
print(indice_por_queSoy)
#? Ahora buscar por ID es instantáneo, si sabes el id del cliente.


#? También podemos indexar por nombre y traer solo el ID


#? .get() para evitar KeyError cuando la clave puede no existir



#*💡🐼 Forma pandas para crear Dict a partir de DataFrame 
#? set_index(): convierte la columna en un índice hash (o sea un dict).
# Ahora usemos "ciudad" como índice del DataFrame:# ✅ O(1) — índice hash:
 
# .loc[] es la forma de acceder por índice, no por posición.
#TODO:INVESTIGA .iloc[] es la forma de acceder por posición, no por índice.





# #TODO: ⭐ Desempaquetamiento de los iterables
# # para extraer facilmente los elementos de iterables en variables, 
# mi_tupla_empaquetada = False, 1,'dos', ['profesor', 'alumno'], (10, 20)
# uno, dos, tres, cuatro, cinco = mi_tupla_empaquetada
# print('💡Impresion elementos unpacking de tupla')
# print(uno)      # False
# print(dos)      # 1
# print(cuatro)   # ['profesor', 'alumno']

# print('💡Impresion elementos unpacking de tupla con operador "*"')
# #TODO: 💡unpacking (operadores con el operador "*")
# a, b, *rest = [1, 2, 3, 4]
# # a=1, b=2, rest=[3,4]
# print(a, b, rest)
# lst = [*range(3), 10]        # [0, 1, 2, 10]
# tup = (*range(3), 10)        # (0, 1, 2, 10)
# print(lst, tup)


# #TODO: ⭐ Slicing de los iterables: para extraer (retornando) todo o parte de sus elementos.
# # mi_lista[inicio: fin: paso] 
# # 1. inicio: índice desde donde comienza el corte.
# # Incluye el elemento en esta posición, Si se omite es indice 0.
# # Puede ser negativo, contando desde el final (-1 es el último elemento).
# # 2. fin: índice donde termina el corte. 
# # Excluye el elemento en esta posición, Si se omite va hasta el final.
# # También puede ser negativo para contar desde el final (-1 es el último elemento).
# # 3. paso: Indica de cuánto en cuánto se avanza para tomar elementos.
# # Por defecto es 1 → Toman elementos consecutivos de inicio a fin, -1 los toma a la inversa.
# # No puede ser 0 (causa Error). 

# lista_slicing = [1,2,3,4,5]
# print('💡Haciendo Slicing de iterables')

# print(lista_slicing[::])     # [1,2,3,4,5]      → Los toma todos de incio a fin, sin paso ni reversa
# print(lista_slicing[2::])    # [3,4,5]          → Los toma desde la pos 2 (incluyente) hasta el fin, sin paso ni reversa
# print(lista_slicing[::-1])   # [5, 4, 3, 2, 1]  → Los toma todos con reversa de 1 en 1.
# print(lista_slicing[::-2])   # [5, 3, 1]        → Los toma con reversa de 2 en 2.
# print(lista_slicing[:2:-1])  # [5, 4]           → Los toma con reversa hasta la posicion 2 (excluyente, por eso al ele 4)




#TODO: *************************************Tipo de dato SET
# # Es una colección *desordenada* de elementos **únicos**.
# # Es mutable (puedes añadir/quitar elementos) pero los elementos deben ser 
# # hashables (no cambia mientras exista, son inmutable → int, str, tuple).
# # (por ejemplo: números, strings, tuplas; NO listas ni diccionarios).
# # Se crean entre corchetes {} o con el constructor.

# #? ⭐ Creación:
# s = {1, 2, 3}               # literal
# s = set([1, 2, 3, 3])       # desde iterable (los duplicados se eliminan)
# s = set(range(5))           # desde cualquier iterable

# #? ⭐ Propiedades y operaciones comunes:
# #   - Añadir: s.add(x)
# #   - Quitar: s.remove(x)       # lanza KeyError si x no existe
# #             s.discard(x)      # no lanza si x no existe
# #   - Extraer arbitrario: s.pop() # como están desordenados, devuelve cualquier elemento
# #   - Limpiar: s.clear()
# #   - Unión: s | t     (o s.union(t))
# #   - Intersección: s & t  (o s.intersection(t))
# #   - Diferencia: s - t  (o s.difference(t))
# #   - Diferencia simétrica: s ^ t (o s.symmetric_difference(t))
# #   - Subconjunto/sobconjunto: s.issubset(t), s.issuperset(t)
# #   - Disjuntos: s.isdisjoint(t)

# #? Ejemplos:
# s1 = {1, 2, 2, 3}
# s2 = set([3, 4, 5])
# print('💡Set (duplicados eliminados):', s1)

# print('UNION DE SETS')
# union = s1 | s2
# union_metodo = s1.union(s2)
# print('💡s1 union s2:', union) # {1, 2, 3, 4, 5}
# print('💡s1 union s2 con metodo:', union)

# print('INTERSECION DE SETS')
# intersection = s1 & s2
# intersecion_metodo = s1.intersection(s2)
# print('💡s1 interseccion s2:', intersection) # {3}
# print('💡s1 interseccion s2 con metodo:', intersecion_metodo)

# print('DIFERENCIA DE SETS')
# diferencia = s1 - s2
# difencia_metodo = s1.difference(s2)
# print('💡s1 diferencia s2:', diferencia) # {1, 2}
# print('💡s1 diferencia s2:', difencia_metodo)
