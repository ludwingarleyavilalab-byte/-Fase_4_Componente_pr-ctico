"""Configuración del archivo de logs (único uso de archivos del sistema)."""

import logging                      # Módulo estándar de registro de eventos
from pathlib import Path            # Manejo de rutas independiente del sistema operativo

# Carpeta donde se guardará el log, junto a este archivo
RUTA_LOGS = Path(__file__).resolve().parent / "logs"
# Ruta completa del archivo de logs
ARCHIVO_LOG = RUTA_LOGS / "software_fj.log"


def obtener_logger():
    """Devuelve el logger del sistema, configurándolo solo la primera vez."""
    logger = logging.getLogger("SoftwareFJ")   # Se obtiene (o crea) el logger por nombre
    if logger.handlers:                        # Si ya fue configurado...
        return logger                          # ...se reutiliza sin duplicar manejadores
    logger.setLevel(logging.DEBUG)             # Se registran todos los niveles
    logger.propagate = False                   # Evita imprimir los logs en consola
    RUTA_LOGS.mkdir(exist_ok=True)             # Crea la carpeta logs si no existe
    # Manejador que escribe en el archivo (modo "a": agrega al final)
    manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    # Formato: fecha y hora | nivel | mensaje
    manejador.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    )
    logger.addHandler(manejador)               # Se conecta el manejador al logger
    return logger
