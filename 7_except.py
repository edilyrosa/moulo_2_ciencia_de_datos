# ============================================================
#* NIVEL 1: DETECTA y LANZA (NO maneja)
# ============================================================






# ============================================================
#* NIVEL 2: VALIDA y RE-LANZA (log detallado)
# ============================================================





# ============================================================
#* NIVEL 3: DECIDE y MANEJA (la decisión final)
# ============================================================





# ============================================================
#* EJECUCIÓN
# ============================================================


#? Regla	                                            Explicación
# raise no obliga a try/except	                Puedes lanzar errores libremente
# El error sube hasta que alguien lo capture	Si nadie captura → crash
# Usa try/except donde quieras manejar	        No en todas las llamadas
# Re-lanza (raise) para añadir contexto	        Capturas, logueas, y subes

# raise es para NOTIFICAR, no para MANEJAR. El manejo es opcional. ✅

