import logging as log


"""         Sin explicaciones
log.basicConfig(level=log.DEBUG,
                format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                datefmt='%I:%M:%S %p',
                handlers=[
                    log.FileHandler('capa_datos.log'),
                    log.StreamHandler()
                ])
# Handler = Manejado
"""
# Configuramos el logging
log.basicConfig(
    # Establecemos el nivel de logging a DEBUG, esto significa que se registrarán todos
    # los mensajes de nivel DEBUG y superiores
    level=log.DEBUG,

    # Definimos el formato de los mensajes de logging
    # %(asctime)s: agrega la hora en que se creó el LogRecord
    # %(levelname)s: agrega el nivel del mensaje (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    # %(filename)s: agrega el nombre del archivo desde donde se emitió el mensaje
    # %(lineno)s: agrega el número de línea desde donde se emitió el mensaje
    # %(message)s: agrega el mensaje de logging
    format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',

    # Definimos el formato de la hora
    datefmt='%I:%M:%S %p',

    # Definimos los manejadores de logging que queremos usar
    # FileHandler: envía los mensajes de logging a un archivo
    # StreamHandler: envía los mensajes de logging a la salida estándar (stdout)
    handlers=[
        log.FileHandler('capa_datos.log'),
        log.StreamHandler()
    ]
)
# Handler = Manejado


if __name__ == "__main__":
    log.debug('Mensaje a nivel debug')
    log.info('Mensaje a nivel de info')
    log.warning('Mensaje a nivel warning')
    log.error('Mensaje a nivel error')
    log.critical('Mensaje a nivel critico')
