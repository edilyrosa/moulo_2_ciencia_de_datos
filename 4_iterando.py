
#? Recorrer el DataFrame
# Alternativas eficientes con pandas, que evitan recorrerlo fila por fila con iterrows() (lento en conjuntos grandes). 
# Usa groupby() y otros metodos para agrupar valor(es) por una columna.
# iterrows vs. groupby es superior en rendimiento para datos tabulares.
# ─────────────────────────────────────────────────────────
#* PARTE 2: defaultdict — agrupar sin verificar si clave existe
# ─────────────────────────────────────────────────────────

import pandas as pd
# Tus datos
data = [
    (2,"Beta Inc","MX","Ciudad de México","Retail",2200,"negociacion","2024-06-01",True),
    (1,"Acme Corp","CO","Bogotá","Tecnología",4500,"cerrado","2024-03-15",True),
    (3,"Gamma SA","CO","Medellín","Manufactura",8100,"cerrado","2024-02-28",True),
    (4,"Delta Ltd","AR","Buenos Aires","Tecnología",1500,"prospecto","2024-07-15",True),
    (5,"Epsilon SAS","CO","Cali","Retail",950,"prospecto","2024-08-01",False),
    (6,"Zeta Corp","MX","Guadalajara","Salud",6700,"negociacion","2024-05-20",True),
    (7,"Eta Inc","CL","Santiago","Manufactura",3300,"cerrado","2024-01-10",True),
    (8,"Theta SA","CO","Bogotá","Tecnología",12000,"cerrado","2024-04-05",True),
    (9,"Iota Ltd","AR","Córdoba","Retail",800,"prospecto","2024-09-01",True),
    (10,"Kappa SAS","MX","Monterrey","Salud",5400,"negociacion","2024-06-15",True),
    (11,"Lambda Corp","CO","Bogotá","Tecnología",320,"prospecto","2024-10-01",False),
    (12,"Mu Inc","CL","Valparaíso","Manufactura",7800,"cerrado","2024-03-22",True),
    (13,"Nu SA","AR","Buenos Aires","Tecnología",2900,"negociacion","2024-07-01",True),
    (15,"Omicron Corp","MX","Ciudad de México","Retail",1100,"prospecto","2024-08-20",True),
    (14,"Xi Ltd","CO","Medellín","Salud",4100,"cerrado","2024-02-14",True)
]

columns = ["id","nombre","pais","ciudad","industria","valor_contrato","etapa","fecha_cierre","activo"]
df = pd.DataFrame(data, columns=columns)
print('\n DATAFRAME COMPLETO \n', df)

print(df.groupby('pais')) #<pandas.api.typing.DataFrameGroupBy object at 0x000001B86BC9ABA0>
print(df.groupby('pais')['nombre']) #<pandas.api.typing.SeriesGroupBy object at 0x0000018D87E9AA50>
print(df.groupby('pais')['nombre'].count()) #serie que cuenta ocurrencia
print(df.groupby('pais')['nombre'].agg(tuple)) #aagrega la lista de todos los nombres por pais

print("\n SERIE !   \n", df.groupby('pais')['nombre'].agg(list)) #aagrega la lista de todos los nombres por pais
print("\n DICT PY !   \n", df.groupby('pais')['nombre'].agg(list).to_dict()) #PREFIERO TRABAJA CON dict por el acc rapido !!
# ...


clientes_por_pais = df.groupby('pais')['nombre'].agg(list).to_dict()
for k, v in clientes_por_pais.items(): # return lista de tupa [(k, v), (k,v)]
# for k, v in clientes_por_pais.values(): # return valores 
# for k, v in clientes_por_pais.keys(): # return valores 
    print(f'{k} -- {', '.join(v)}')
    

#*************************** Entonces, ¿para qué sirve .to_dict()?
# Si necesitas manipular la estructura como un diccionario puro de Python 
# 💡(por ejemplo, pasarlo a una función que solo acepta dict, 
# o modificarlo con métodos de diccionario como .update()), entonces to_dict() es útil.
# Para el simple recorrido e impresión, la Serie funciona igual.

#* agregar un nuevo pais remplazar
nuevos_datos = {
    'VE': ['Polar', 'PDVSA'],
    'MX': [None] * 4 #  [None, None, None, None]
}

clientes_por_pais.update(nuevos_datos) #de aqui en adelante esta sta ACTUALIZADO
print('\nDespues del update\n', clientes_por_pais)
# ...
#? ¿Qué hace setdefault() en un diccionario?
# setdefault(key, default) busca la key en el diccionario:
# Si existe, devuelve su valor.obtiene la lista asociada y le agrega 'Lamosa'.
# Si no existe, inserta la key con el valor default y devuelve ese default. Crea la entrada 'MX': [] y luego
# agrega 'Lamosa' a esa lista vacía. Así evitas tener que comprobar primero si la clave existe.

clientes_por_pais.setdefault('MX', []).append('Lamosa')
# print('Agregando elementos a MX', clientes_por_pais['Mexico']) #!KeyError: 'Mexico'
print('Agregando elementos a MX', clientes_por_pais.get('Mexico', 'la key no existe'))
print('Agregando elementos a MX', clientes_por_pais.get('MX', 'la key no existe'))

print('\n MX + "Lamosa" ', clientes_por_pais)



