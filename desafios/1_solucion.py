"""
=============================================================
DESAFÍO 1 — Explorando pathlib  ★ SOLUCIÓN ★
=============================================================
"""

from pathlib import Path

RAIZ = Path(__file__).parent

print("=" * 50)
print("DESAFÍO 1 — Explorando pathlib  ★ SOLUCIÓN ★")
print("=" * 50)


# ─────────────────────────────────────────────────
# TAREA 1: Crear carpetas
# ─────────────────────────────────────────────────
print("\n--- TAREA 1: Crear carpetas ---")

entrega   = RAIZ / "entrega"
notas     = entrega / "notas"
reportes  = entrega / "reportes"

notas.mkdir(parents=True, exist_ok=True)
reportes.mkdir(parents=True, exist_ok=True)

#& falto: entrega.mkdir(parents=True, exist_ok=True)
# No, no faltó. Al hacer notas.mkdir(parents=True, exist_ok=True) y 
# reportes.mkdir(parents=True, exist_ok=True), el argumento parents=True 
# crea automáticamente todos los padres necesarios, incluyendo entrega/.

print("Carpetas creadas:")
print(f"  {notas}")
print(f"  {reportes}")


# ─────────────────────────────────────────────────
# TAREA 2: Crear y escribir un archivo
# ─────────────────────────────────────────────────
print("\n--- TAREA 2: Crear y escribir un archivo ---")

mi_nota = notas / "mi_nota.txt"
mi_nota.write_text("Aprendiendo pathlib con Python.", encoding="utf-8")
#& basta con escribir se crea el archivo

print(f"Archivo creado: {mi_nota.name}")


# ─────────────────────────────────────────────────
# TAREA 3: Leer el archivo
# ─────────────────────────────────────────────────
print("\n--- TAREA 3: Leer el archivo ---")

contenido = mi_nota.read_text(encoding="utf-8")
print(f"Contenido: {contenido}")


# ─────────────────────────────────────────────────
# TAREA 4: Inspeccionar el archivo
# ─────────────────────────────────────────────────
print("\n--- TAREA 4: Inspeccionar el archivo ---")

print(f"Nombre completo : {mi_nota.name}")
print(f"Nombre sin ext  : {mi_nota.stem}")
print(f"Extensión       : {mi_nota.suffix}")
print(f"Carpeta padre   : {mi_nota.parent}")
print(f"Tamaño (bytes)  : {mi_nota.stat().st_size}")


# ─────────────────────────────────────────────────
#* TAREA 5: Renombrar el archivo
# ─────────────────────────────────────────────────
print("\n--- TAREA 5: Renombrar el archivo ---")

nota_final = notas / "nota_final.txt"
try:
    mi_nota.rename(nota_final) #! si la existe FileExistsError:
    print("Renombrado: mi_nota.txt → nota_final.txt")
except FileExistsError:
    print("Ya existe nota_final.txt, no se renombró.")

print("Renombrado: mi_nota.txt → nota_final.txt")


# ─────────────────────────────────────────────────
#* TAREA 6: Partes de la ruta
# ─────────────────────────────────────────────────
print("\n--- TAREA 6: Partes de la ruta ---")

ruta_absoluta = nota_final.resolve()
for i, parte in enumerate(ruta_absoluta.parts):
    print(f"  Parte {i} : {parte}")


# ─────────────────────────────────────────────────
#* TAREA 7: Listar archivos con .glob()
# ─────────────────────────────────────────────────
print("\n--- TAREA 7: Listar archivos ---")

print("Archivos dentro de entrega/:")
for archivo in entrega.glob("**/*"):
    if archivo.is_file():
        print(f"  {archivo}")


# ─────────────────────────────────────────────────
# TAREA 8: .touch() y escritura masiva
# ─────────────────────────────────────────────────
print("\n--- TAREA 8: .touch() y escritura masiva ---")

meses = ["reporte_enero.txt", "reporte_febrero.txt", "reporte_marzo.txt"]

# Crear archivos vacíos con .touch()
for nombre in meses:
    (reportes / nombre).touch()

# Escribir contenido en cada uno e imprimir info
for archivo in reportes.iterdir():
    if archivo.is_file():
        archivo.write_text(
            f"Reporte del mes: {archivo.stem}",
            encoding="utf-8"
        )
        print(f"  {archivo.name}  —  {archivo.stat().st_size} bytes")


# ─────────────────────────────────────────────────
#* TAREA 9: .with_suffix() y renombrado
# ─────────────────────────────────────────────────
print("\n--- TAREA 9: .with_suffix() y renombrado ---")

# Imprimir rutas .csv sin crearlas
print("Rutas con extensión .csv (solo visualización):")
for archivo in reportes.glob("*.txt"):
    #& .with_suffix()    → obtener la ruta con otra extensión
    print(f"  {archivo.with_suffix('.csv')}")

# Renombrar solo reporte_marzo.txt → reporte_marzo.csv
marzo_txt = reportes / "reporte_marzo.txt"
marzo_csv = marzo_txt.rename(marzo_txt.with_suffix(".csv"))

print(f"Renombrado: reporte_marzo.txt → {marzo_csv.name}")


# ─────────────────────────────────────────────────
#* TAREA 10: Eliminar archivos y carpetas (try/except)
#
# ¿Por qué try/except?
#
# .rmdir() solo elimina carpetas VACÍAS. Si la carpeta
# todavía tiene archivos dentro, Python lanza:
#
#   OSError: [WinError 145] The directory is not empty
#   (Linux/Mac → OSError: [Errno 39] Directory not empty)
#
# Como en un programa real no siempre sabemos si la
# carpeta está vacía, envolvemos la llamada en try/except
# para capturar el error y reaccionar: vaciar la carpeta
# y luego intentar borrarla de nuevo.
# ─────────────────────────────────────────────────
print("\n--- TAREA 10: Eliminar archivos y carpetas (try/except) ---")

# ── Eliminar entrega/notas/ ──────────────────────
try:
    notas.rmdir()  # Fallará: todavía tiene nota_final.txt
except OSError as e:
    print(f"Error: la carpeta notas/ no está vacía. Vaciándola...")
    print(f"  Detalle del error → {e}")
    for archivo in notas.glob("*"):
        if archivo.is_file():
            archivo.unlink()
            print(f"  Eliminado: {archivo.name}")
    notas.rmdir()

print("✓ Carpeta notas/ eliminada correctamente.")

# ── Eliminar entrega/reportes/ ───────────────────
for archivo in reportes.glob("*"):
    if archivo.is_file():
        archivo.unlink()
        print(f"  Eliminado: {archivo.name}")

reportes.rmdir()
print("✓ Carpeta reportes/ eliminada correctamente.")

# ── Eliminar entrega/ ────────────────────────────
entrega.rmdir()
print("✓ Carpeta entrega/ eliminada correctamente.")


print("\n" + "=" * 50)
print("¡Desafío completado!")
print("=" * 50)
