"""
=============================================================
MÓDULO 1 — LECCIÓN 1: Arquitectura de proyectos con pathlib
=============================================================

OBJETIVO:
    Aprender a estructurar un proyecto analítico profesional
    y a navegar el sistema de archivos con pathlib.

QUÉ ES pathlib:
    Módulo estándar de Python para manejar rutas de archivos
    de forma orientada a objetos. Reemplaza os.path con una
    sintaxis mucho más limpia y segura.

CÓMO EJECUTAR:
    python leccion1_arquitectura.py
"""

from pathlib import Path

# ─────────────────────────────────────────────────────────
#* PARTE 1: pathlib — navegación de rutas
# ─────────────────────────────────────────────────────────

#& Path() representa una ruta. 
ruta_proyecto = Path(".") #Carpeta actual del script
print("=" * 55)
print("PARTE 1: Trabajando con rutas (pathlib)")
print("=" * 55)

print(ruta_proyecto)
# #& Construir rutas con el operador (El operador / une rutas)
ruta_datos = ruta_proyecto / "data"
ruta_raw = ruta_datos / 'raw'
ruta_processed = ruta_datos / 'processed'


#& .resolve() convierte la ruta relativa a ruta absoluta completa
print('Ubicacion del proyecto', ruta_proyecto.resolve())
print(ruta_processed)
print(ruta_processed.resolve())



# #& Verificar si algo existe
print(f"¿Existe data/raw?      : {ruta_raw.exists()}")  #F
print(f"¿Es una carpeta?       : {ruta_raw.is_dir()} ") #F

# # 🚀No existen aun, asi que vamos a crearlas en la siguiente sección.

# # ─────────────────────────────────────────────────────────
# #* PARTE 2: Crear la estructura estándar del proyecto
# # ─────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("PARTE 2: Creando estructura del proyecto")
print("=" * 55)

# #*  CARPETAS_PROYECTO
CARPETAS_PROYECTO = [
'data/raw',      # datos originales — NUNCA los modifiques
'data/processed', # datos limpios después de transformar
'data/out',       # reportes y resultados finales
'src',              # código fuente (scripts Python)
'notebooks', # exploración (Jupyter) — no producción
'logs', # registros de ejecución automáticos
]

def crear_estructa_poryecto( base: str = '.') -> Path:
    base_path = Path(base)
    for carpeta in CARPETAS_PROYECTO:
        ruta = base_path / carpeta              #?1. creo la ruta
        ruta.mkdir(parents=True, exist_ok=True) #? 2. creamos el directorio
        (ruta/'.gitkeep').touch()               #? 3. creo un archivo vacío para mantener la carpeta en git
        print(f'✅ Creada carpeta: {ruta}')
        # No, no faltó. Al hacer notas.mkdir(parents=True, exist_ok=True) y reportes.mkdir(parents=True, exist_ok=True), 
        # el argumento parents=True crea automáticamente todos los padres necesarios, incluyendo entrega/.
    for a in ['.env', 'requirements.txt', 'README.md']:
        ruta_archivo = base_path / a #1. creo la ruta
        if not ruta_archivo.exists():
            ruta_archivo.touch() #2. creo el archivo vacío
            print(f'✅ Creada archivo: {ruta_archivo}')
    return base_path

# llamamos a la fun que crea los directorios y archivos
raiz = crear_estructa_poryecto('.')
print(f'Proyecto listo en {raiz.resolve()}')


# ─────────────────────────────────────────────────────────
#* PARTE 3: Listar y explorar archivos con pathlib
# ─────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("PARTE 3: Explorar archivos existentes en data/raw")
print("=" * 55)

# .iterdir()
for archivo in ruta_raw.iterdir():
    if archivo.is_file() and archivo.name != '.gitkeep':
        # print(f"Archivo encontrado: {archivo.name}")
        # .stat() #metadada el documkento: peso, fecha de creación, etc
        # st.size # me da el tamanio, en bytes
        tamanio_kb = archivo.stat().st_size / 1024
        print(f'{archivo.name: <35} {tamanio_kb} KB')

#* .glob() → Busca archivos que coincidan con un patrón.
for csv in ruta_proyecto.glob('**/*.csv'):
    print(csv)
    # . "**/*.csv" es un patrón glob recursivo:
    # . ** significa "cualquier número de subdirectorios (incluyendo cero)".
    # . *.csv busca archivos con extensión .csv.
    #? "*.csv" → busca archivos .csv solo en la carpeta actual, no en subcarpetas
    #? "**/*.csv" → busca archivos .csv en la carpeta actual y en todas las subcarpetas a cualquier profundidad.
    #? "***/*.csv" → NO es un patrón válido.


# ATRB
# # .suffix → extensión del archivo
# # .stem   → nombre sin extensión
# # .parent → carpeta que contiene el archivo
archivo_ejemplo = ruta_raw / 'clientes.csv'
print(archivo_ejemplo.name)   
print(archivo_ejemplo.suffix)   
print(archivo_ejemplo.stem)   
print(archivo_ejemplo.parent)   
print(archivo_ejemplo.exists())   

# # ─────────────────────────────────────────────────────────
# #* PARTE 4: Patrón profesional — rutas relativas al script
# # ─────────────────────────────────────────────────────────
print("\n" + "=" * 55)
print("PARTE 4: Rutas relativas al script (patrón profesional)")
print("=" * 55)

RAIZ = Path(__file__).parent # me da la carpeta donde se encuentra el script, sin importar desde dónde lo ejecute

RAW_DIR = RAIZ / 'data' / 'raw'
PROCESSED_DIR = RAIZ / 'data' / 'processed'
OUP_DIR = RAIZ / 'data' / 'out'
LOGS_DIR = RAIZ / 'logs'

print("Raíz del proyecto : ", RAIZ)       
print(f"Datos crudos      : {RAW_DIR}")     
print(f"Datos procesados  :  {PROCESSED_DIR}")

def verificar_estructura() -> bool:
    carperas_criticas = [RAW_DIR, PROCESSED_DIR, LOGS_DIR, Path('D:\csc_dato_ingenio'), 'D:\csc_dato_ingenio']
    todo_ok = True
    for carpeta in carperas_criticas:
        try:
            if carpeta.exists(): #! aca error cuando no paso un ele TDD Path, sino un string
                print(f'\n✅ Carpeta existe: {carpeta.relative_to(RAIZ)}')
            else:
                print(f'❌ FALTA CARPETA: {carpeta.relative_to(RAIZ)}')
                todo_ok = False 
                
        except PermissionError as e:
            print(f'❌ ERROR la autorizacion: {e}')
            todo_ok = False
            
        except OSError as e:
            print(f'❌❌❌ ERROR la autorizacion: {e}')
            todo_ok = False
            
        except ValueError as e:
            print(f'❌❌❌ ERROR la carpeta {carpeta} No existe: {e}')
            todo_ok = False
        except Exception as e: #GENERICO, atrapa tdos los errores
            print(f'❌ ERROR verificando carpeta: {e}')
            todo_ok = False
            
            
    return todo_ok

print('Verificando estructura del proyecto...')
ok = verificar_estructura()
print(f'Estructura {'Completa ✅' if ok else 'Incompleta ❌'}' )