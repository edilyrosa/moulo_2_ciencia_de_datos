"""
=============================================================
DESAFÍO 1 — Explorando pathlib
=============================================================

INSTRUCCIONES DE ENTREGA:
    Resuelve cada tarea en este mismo archivo.
    Escribe tu código debajo de cada comentario que dice
    # TU CÓDIGO AQUÍ

SETUP PREVIO (hazlo antes de abrir este archivo):
─────────────────────────────────────────────────
    1. Crea una carpeta para este desafío, por ejemplo:
           C:\\mis_proyectos\\desafio_pathlib

    2. Copia este archivo dentro de esa carpeta.

    3. Abre una terminal, entra a la carpeta:
           cd C:\\mis_proyectos\\desafio_pathlib

    4. Crea el entorno virtual y actívalo.

    5. pathlib es parte de Python, no necesitas instalar nada.

    6. Ejecuta el desafío:
           python 1_desafio_pathlib.py

─────────────────────────────────────────────────
MÉTODOS que debes investigar y usar:
─────────────────────────────────────────────────
  Nuevos en este desafío:
    .rename()         → renombrar o mover un archivo/carpeta
    .read_text()      → leer el contenido de un archivo
    .write_text()     → escribir texto en un archivo
    .parts            → partes de la ruta como tupla
    .with_suffix()    → obtener la ruta con otra extensión
    .unlink()         → eliminar un archivo
    .rmdir()          → eliminar una carpeta (debe estar vacía)

  Ya vistos en clase:
    Path()  /  .exists()  /  .mkdir()  /  .iterdir()
    .glob() /  .suffix    /  .stem     /  .parent
    .name   /  .resolve() /  Path(__file__).parent
    .stat().st_size /   .touch() 

=============================================================
"""

from pathlib import Path

RAIZ = Path(__file__).parent

print("=" * 50)
print("DESAFÍO 1 — Explorando pathlib")
print("=" * 50)


# ─────────────────────────────────────────────────
#* TAREA 1
# Crea esta estructura de carpetas dentro de la
# carpeta donde está este script:
#
#   entrega/
#   ├── notas/
#   └── reportes/
#
# ─────────────────────────────────────────────────
print("\n--- TAREA 1: Crear carpetas ---")

# TU CÓDIGO AQUÍ


# ─────────────────────────────────────────────────
#* TAREA 2
# Dentro de entrega/notas/ crea un archivo llamado
# mi_nota.txt y escribe adentro este texto:
#   "Aprendiendo pathlib con Python."
#
# Usa .write_text() para escribirlo.
# ─────────────────────────────────────────────────
print("\n--- TAREA 2: Crear y escribir un archivo ---")

# TU CÓDIGO AQUÍ


# ─────────────────────────────────────────────────
#* TAREA 3
# Lee el archivo mi_nota.txt que acabas de crear
# e imprime su contenido en consola.
#
# Usa .read_text() para leerlo.
# ─────────────────────────────────────────────────
print("\n--- TAREA 3: Leer el archivo ---")

# TU CÓDIGO AQUÍ


# ─────────────────────────────────────────────────
#* TAREA 4
# Imprime esta información sobre mi_nota.txt:
#   - nombre completo del archivo  (.name)
#   - nombre sin extensión         (.stem)
#   - extensión                    (.suffix)
#   - carpeta donde está           (.parent)
#   - tamaño en bytes              (.stat().st_size)
# ─────────────────────────────────────────────────
print("\n--- TAREA 4: Inspeccionar el archivo ---")

# TU CÓDIGO AQUÍ


# ─────────────────────────────────────────────────
#* TAREA 5
# Renombra mi_nota.txt a nota_final.txt
# usando .rename()
# Usa Try/except para evitar el error FileExistsError

# Luego imprime:
#   "Renombrado: mi_nota.txt → nota_final.txt"
# ─────────────────────────────────────────────────
print("\n--- TAREA 5: Renombrar el archivo ---")

# TU CÓDIGO AQUÍ


# ─────────────────────────────────────────────────
#* TAREA 6
# Usa .parts para imprimir cada parte de la ruta
# absoluta de nota_final.txt
#
# Ejemplo de salida esperada:
#   Parte 0 : C:\
#   Parte 1 : mis_proyectos
#   Parte 2 : desafio_pathlib
#   ...
# ─────────────────────────────────────────────────
print("\n--- TAREA 6: Partes de la ruta ---")

# TU CÓDIGO AQUÍ


# ─────────────────────────────────────────────────
#* TAREA 7
# Lista todos los archivos dentro de entrega/
# y sus subcarpetas usando .glob("**/*")
# Imprime solo los que sean archivos (no carpetas).
# ─────────────────────────────────────────────────
print("\n--- TAREA 7: Listar archivos ---")

# TU CÓDIGO AQUÍ


# ─────────────────────────────────────────────────
#* TAREA 8
# Usa .touch() para crear 3 archivos vacíos dentro
# de entrega/reportes/:
#   reporte_enero.txt
#   reporte_febrero.txt
#   reporte_marzo.txt
#
# Luego recorre esa carpeta con .iterdir() y escribe
# en cada archivo (con .write_text()):
#   "Reporte del mes: <stem_del_archivo>"
#
# Finalmente imprime el nombre y el tamaño en bytes
# de cada archivo creado.
# ─────────────────────────────────────────────────
print("\n--- TAREA 8: .touch() y escritura masiva ---")

# TU CÓDIGO AQUÍ


# ─────────────────────────────────────────────────
#* TAREA 9
# Usa .with_suffix() para obtener la ruta de cada
# archivo .txt de entrega/reportes/ pero con
# extensión .csv, e imprime esas nuevas rutas
# (sin crearlas todavía).
#
# Luego renombra SOLO reporte_marzo.txt a
# reporte_marzo.csv combinando .rename() y
# .with_suffix(".csv").
#
# Imprime:
#   "Renombrado: reporte_marzo.txt → reporte_marzo.csv"
# ─────────────────────────────────────────────────
print("\n--- TAREA 9: .with_suffix() y renombrado ---")

# TU CÓDIGO AQUÍ


# ─────────────────────────────────────────────────
#* TAREA 10 — try / except
# ─────────────────────────────────────────────────
#
# PASO 1 — Intenta eliminar entrega/notas/ con .rmdir()
#          SIN vaciarla primero.
#
# ¿Por qué es necesario try/except aquí?
# ─────────────────────────────────────────────────
# .rmdir() SOLO puede eliminar carpetas VACÍAS.
# Si la carpeta contiene archivos u otras carpetas,
# Python lanza:
#
#   OSError: [WinError 145] The directory is not empty
#   (en Linux/Mac: OSError: [Errno 39] Directory not empty)
#
# Además, si por error pasaras un dato de tipo
# incorrecto —por ejemplo Path(123) en vez de Path("nombre")—
# Python lanzaría un TypeError al construir el objeto.
# El manejo de excepciones protege el programa de ambos casos.
# ─────────────────────────────────────────────────
#
# PASO 2 — En el bloque except, captura el OSError e
#          imprime un mensaje descriptivo como:
#   "Error: la carpeta notas/ no está vacía. Vaciándola..."
#
# PASO 3 — Después del try/except (o dentro del except):
#   a. Elimina todos los archivos de entrega/notas/
#      usando .glob("*") + .unlink()
#   b. Elimina la carpeta vacía con .rmdir()
#   c. Imprime: "✓ Carpeta notas/ eliminada correctamente."
#
# PASO 4 — Repite el proceso para entrega/reportes/:
#   a. Elimina todos sus archivos con .unlink()
#   b. Elimina la carpeta con .rmdir()
#   c. Elimina entrega/ con .rmdir()
#   d. Imprime: "✓ Carpeta entrega/ eliminada correctamente."
#
# ─────────────────────────────────────────────────
print("\n--- TAREA 10: Eliminar archivos y carpetas (try/except) ---")

# TU CÓDIGO AQUÍ


print("\n" + "=" * 50)
print("¡Desafío completado!")
print("=" * 50)
