
"""
=============================================================
MÓDULO 2 — LECCIÓN 7: Manejo de errores y logging
=============================================================

RESPONSABILIDAD DE ESTE ARCHIVO:
    Este módulo tiene UNA sola responsabilidad:
    proveer infraestructura de logging y excepciones
    reutilizables para cualquier pipeline del proyecto.

    Lo que SÍ pertenece aquí:
      ✓ Configuración del logger (crear_logger)
      ✓ Excepciones personalizadas del pipeline
      ✓ Funciones de validación puras (no tocan datos de negocio)

    Lo que NO pertenece aquí:
      ✗ Carga de DataFrames (eso es lógica de negocio)
      ✗ Filtros de clientes (eso es lógica de negocio)
      ✗ Rutas específicas de un proyecto

    Esta separación sigue el principio de responsabilidad única:
    cada archivo hace una sola cosa y la hace bien.

CÓMO EJECUTAR (demo):
    python errores_logging.py
    Revisa logs/pipeline_crm_YYYYMMDD.log al terminar.

CÓMO IMPORTAR DESDE OTRO ARCHIVO:
    from errores_logging import crear_logger, TipoIncompatibleError, ...
    Al importar, el bloque if __name__ == "__main__" NO se ejecuta —
    solo se cargan las definiciones que el otro archivo necesita.
"""

import logging
import pandas as pd
from pathlib import Path
from datetime import datetime


# ─────────────────────────────────────────────────────────
# CONSTANTES DE INFRAESTRUCTURA
# Solo rutas necesarias para el sistema de logging.
# Las rutas de datos de cada proyecto van en su propio archivo.
# ─────────────────────────────────────────────────────────

RAIZ     = Path(__file__).parent
LOGS_DIR = RAIZ / "logs"
LOGS_DIR.mkdir(exist_ok=True)  # crea la carpeta si no existe, sin error si ya existe


# ─────────────────────────────────────────────────────────
#* PARTE 1: Configuración del sistema de logging
# ─────────────────────────────────────────────────────────

def crear_logger(nombre: str) -> logging.Logger: #? para loder log.info('Opps...! ')
    # logging (módulo)
    # └── Logger (clase) ← Esto es logging.Logger
    #         └── logger (objeto) ← El que usas en tu código.
    
    # Instanciacion del log
    #& logger = logging.getLogger(nombre) # Instancia la clase Logger, espera el nombre con el que se creara el log
    
    # Establecimiento del nivel de log
    #& logger.setLevel(logging.DEBUG) ← Define el nivel mínimo de mensajes que el logger procesa.
    # log.debug("Mensaje debug")  ← Solo para desarrollo
    # log.info("Proceso normal")  ← Para seguimiento
    # log.warning("Algo raro")    ← Atención, pero sigue
    # log.error("Algo falló")     ← Error recuperable
    # log.critical("Fatal!")      ← Detener todo
    
    
    #& formato = logging.Formatter()    ← Formate el style de los logs 
                                        # Los handlers usan ese formato al escribir
                                        # consola.setFormatter(formato)
                                        # archivo.setFormatter(formato)

# 🎯 HANDLER = DESTINO DE LOGS/ Envía mensajes de log a un lugar específico.
#& logging.StreamHandler()             → Consola (terminal)	Ver logs en tiempo real
# logging.FileHandler()               → Archivo en disco	Guardar logs para después
# SMTPHandler 	                      → Correo electrónico	Alertas por email
# SocketHandler	                      → Red	Enviar logs a otro sistema

# logger.handlers → [] LISTA VACÍA → Primera vez que usas el logger
    #&  logger.addHandler(consola)  # ← Agrega handler
    #  logger.addHandler(archivo)  # ← Agrega handler
# logger.handlers = [consola, archivo]  ← AHORA TIENE HANDLERS
# if not logger.handlers:  # ← False (NO está vacía)
#     # NO ejecuta addHandler → NO duplica, 🎯 SIN ESTA VALIDACIÓN (PROBLEMA) →
# Llamada 2 → handlers = [consola, archivo, consola, archivo] ← DUPLICADOS
    
    
# 📌 RESUMEN
# Logger: quien recibe el mensaje
# Formatter: cómo se ve el mensaje
# Handler: a dónde va el mensaje, consola, file, red, email...

    
    """
    Fábrica de loggers: crea y configura un logger con dos destinos.

    Destino 1 — Consola: muestra INFO y superior.
                          El analista ve el progreso sin ruido de DEBUG.
    Destino 2 — Archivo: guarda DEBUG y superior.
                          Registro completo para diagnóstico post-mortem.

    Por qué el nombre como parámetro:
      Python reutiliza loggers por nombre. Si dos archivos crean
      un logger con el mismo nombre, comparten el mismo handler
      y los mensajes se mezclan en el mismo .log.
      Cada pipeline debe usar un nombre único para tener su propio archivo.

    Niveles de severidad (menor → mayor):
      DEBUG    → detalles internos, solo en archivo
      INFO     → pasos normales del proceso
      WARNING  → algo inesperado, el proceso continúa
      ERROR    → algo falló, puede recuperarse
      CRITICAL → fallo grave, detener el proceso

    Args:
        nombre: identificador único del pipeline (e.g. "pipeline_crm")

    Returns:
        logging.Logger configurado con handler de consola y de archivo
    """
    #? 0. config para la ruta del log, del pipeline que lo ocupe.
    timestamp = datetime.now().strftime('%Y%m%d')
    ruta_log = LOGS_DIR / f"{nombre}_{timestamp}.log"
    
    #? 1. Crear la instancia del log
    logger = logging.getLogger(nombre)
    
    #? 2. Establecemos el nivel minimo del log
    logger.setLevel(logging.DEBUG)

    #? 3. Establecemos el style o forma qyue tendra el log
    # 2026-06-20 15:30:45 | INFO | pipeline_crm | INICIO: cargando clientes.csv
    formato = logging.Formatter(
    style='%', # →  '{', '$'
    fmt= "%(asctime)s | %(levelname)s  | %(name)s  | %(message)s ",
    datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    #? 4. HANDLERS: Destino del log: consola, file, red, email..
    #Consola
    consola = logging.StreamHandler() 
    consola.setLevel(logging.INFO)
    consola.setFormatter(formato)
    #file 
    archivo = logging.FileHandler(ruta_log, encoding='utf-8')
    archivo.setLevel(logging.DEBUG)
    archivo.setFormatter(formato)
    
    #? 5. Agregamos los handlers al log, PEROOOO LA PRIMERA VEZ
    if not logger.handlers: # lista de los manejadores AGREGADOScon add
        logger.addHandler(consola)
        logger.addHandler(archivo)
    
    return logger


# ─────────────────────────────────────────────────────────
#* PARTE 2: Excepciones personalizadas
#? 🎯 ¿POR QUÉ CREAR EXCEPCIONES PROPIAS? en lugar de usar Exception:
#   - Los mensajes de error son más descriptivos y específicos
#   - Se pueden capturar de forma selectiva con except
#   - La jerarquía permite capturar cualquier error del pipeline con un solo "except PipelineError"

#? Jerarquía:
#   Exception
#     └── PipelineError                 ← base: agrupa todos los errores del pipeline
#           ├── ArchivoNoEncontradoError
#           ├── DatosInvalidosError
#           ├── ColumnaFaltanteError
#           └── TipoIncompatibleError   ← desarrollada con atributos propios

#?      Beneficio	                    Ejemplo
# Semántica clara	            raise ArchivoNoEncontradoError() vs raise Exception()
# Captura selectiva	            except ColumnaFaltanteError:
# Mensajes específicos	        TipoIncompatibleError(columna="edad", ...)
# ─────────────────────────────────────────────────────────

class PipelineError(Exception):
    """Clase base para todos los errores del pipeline. 
    Agrupa las 4 excepciones hijas bajo un nombre común,
    permitiendo capturarlas todas con un solo except."""
    pass

class ArchivoNoEncontradoError(PipelineError):
    """
    El archivo de entrada no existe en la ruta especificada.
    Nivel de log sugerido: ERROR
    """
    pass

class DatosInvalidosError(PipelineError):
    """
    El archivo existe pero sus datos no son utilizables.
    Ejemplo: CSV vacío, archivo corrupto.
    Nivel de log sugerido: ERROR
    """
    pass

class ColumnaFaltanteError(PipelineError):
    """
    El DataFrame no contiene una columna requerida para la operación.
    Nivel de log sugerido: ERROR
    """
    pass

class TipoIncompatibleError(PipelineError):
    """Se intentó una operación con un tipo de dato incorrecto.

    Ocurre cuando:
    - Se compara una columna string con un número → df['city'] > 40
    - Se aplica una operación matemática a texto  → df['nombre'] * 2
    - El origen de datos cambió el tipo de columna sin aviso

    A diferencia de las otras excepciones, esta está desarrollada
    con atributos propios para que el log pueda registrar información
    estructurada: qué columna falló, qué tipo tenía y qué se esperaba.
    Esto permite diagnósticos más precisos sin abrir el CSV.

    Atributos:
        columna       : nombre de la columna con el problema
        tipo_real     : dtype que tiene la columna en el DataFrame
        tipo_esperado : dtype que el pipeline necesitaba"""
    
    #? 1. Constructor personalizado
    #* al lanzar esta exception, le pasamos como argumento los datos 
    #* necesarios par construir el mensaje descriptivo → str(e)
    # un obj exception tiene: type class ValueError, message "no puedes..." terackback, metodos → str(e)
    def __init__(self, columna:str, tipo_real:str, tipo_esperado:str):
        self.columna = columna
        self.tipo_real = tipo_real
        self.tipo_esperado = tipo_esperado

        mensaje = (
            f"Columna {columna} tiene tipo {tipo_real}, "
            f"Se esperaba el tipo {tipo_esperado}\n "
            f"Cambio el origen de datos?? Verifica el archivo de entrada."
        )
        super.__init__(mensaje)


# class Cliente():
#     def __ini__(self, id, nombre, saldo):
#         self.id = id
#         self.nombre =nombre
#         self.saldo = saldo
        
#     def retiro(self, cantidad):
#         if self.saldo < cantidad:
#             print('No puedes retirar mas del sald')
#         else:
#             self.saldo -= cantidad
            
# edily =  Cliente('20eee12', 'Edily Mora', 100)
# edily.retiro(50)



# ─────────────────────────────────────────────────────────
#* PARTE 3: Funciones de validación puras
#   - No contienen lógica de negocio (no saben qué es un "cliente")
#   - Son reutilizables por cualquier pipeline del proyecto
#   - Su única responsabilidad es validar estructura de datos
#
# Reciben el logger como parámetro (en lugar de usar uno global)
# para que cada pipeline que las llame escriba en su propio .log
# ─────────────────────────────────────────────────────────

#*Esta funct  verifica que el DF tenga las columnas necesarias antes de intentar operar sobre ellas.
def validar_columnas(df: pd.DataFrame, columnas_requeridas: list, log:logging.Logger) -> None:
    # RESTA DE ESTS = Op de diferencia, se basa en PERTENENCIA no en index o pos
    #*  (nombe, id, ciudad) - (id) # Retorna los elementos qu estan en el primer set y NOO en el segundo
    faltantes = set(columnas_requeridas) - set(df.columns)
    if faltantes:
        log.error(f'Columnas faltrantes {sorted(faltantes)}')
        pass