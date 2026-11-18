"""Gestor central: mantiene las listas internas y protege al sistema de errores."""

from clientes import Cliente
from servicios import Servicio
from reserva import Reserva
from logger_config import obtener_logger
from excepciones import (
    ErrorSoftwareFJ,
    ClienteInvalidoError,
    ParametroFaltanteError,
    ServicioInvalidoError,
)

logger = obtener_logger()


def _cadena_de_causas(error):
    """Devuelve el texto 'error <- causa <- causa' siguiendo __cause__."""
    partes = []
    while error is not None:    # Recorre el encadenamiento
        partes.append(f"{type(error).__name__}: {error}")
        error = error.__cause__
    return " <- ".join(partes)


class GestorSoftwareFJ:
    """Administra clientes, servicios y reservas SIN base de datos (solo listas)."""

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    # Consultas de solo lectura (copias para proteger las listas internas)
    @property
    def clientes(self):
        return list(self._clientes)

    @property
    def servicios(self):
        return list(self._servicios)

    @property
    def reservas(self):
        return list(self._reservas)

    def _ejecutar(self, descripcion, funcion):
        """Ejecuta una operación de forma segura: ningún error detiene el programa."""
        try:
            resultado = funcion()
        except ErrorSoftwareFJ as error:    # Errores propios del sistema
            logger.error("%s | %s", descripcion, _cadena_de_causas(error))
            return None
        except Exception as error:    # Errores inesperados (último recurso)
            logger.critical("%s | Error inesperado: %s", descripcion, _cadena_de_causas(error),
                            exc_info=True)
            return None
        else:
            logger.info("%s | OK", descripcion)    # Solo si no hubo excepción
            return resultado
        finally:
            logger.debug("Operación finalizada: %s", descripcion)

    def registrar_cliente(self, **datos):
        def operacion():
            try:
                cliente = Cliente(**datos)
            except TypeError as error:    # Faltan o sobran argumentos
                raise ParametroFaltanteError("Datos del cliente incompletos o inesperados.") from error
            if cliente in self._clientes:    # Usa __eq__ de EntidadBase (mismo documento)
                raise ClienteInvalidoError(f"Ya existe un cliente con el documento {cliente.documento}.")
            self._clientes.append(cliente)
            return cliente
        return self._ejecutar(f"Registrar cliente {datos.get('nombre')!r}", operacion)

    def registrar_servicio(self, clase, **datos):
        def operacion():
            if not (isinstance(clase, type) and issubclass(clase, Servicio)):
                raise ServicioInvalidoError(f"{clase!r} no es un tipo de servicio.")
            try:
                servicio = clase(**datos)
            except TypeError as error:    # Clase abstracta o parámetros incorrectos
                raise ServicioInvalidoError(
                    f"No se pudo crear el servicio {clase.__name__}."
                ) from error
            self._servicios.append(servicio)
            return servicio
        return self._ejecutar(f"Registrar servicio {clase.__name__} {datos.get('nombre')!r}", operacion)

    def crear_reserva(self, cliente, servicio, duracion, **extras):
        def operacion():
            reserva = Reserva(cliente, servicio, duracion, **extras)
            self._reservas.append(reserva)
            return reserva
        return self._ejecutar(f"Crear reserva (duración={duracion!r}, extras={extras})", operacion)

    def confirmar_reserva(self, reserva):
        return self._ejecutar(f"Confirmar reserva {getattr(reserva, 'identificador', '?')}",
                              lambda: (reserva.confirmar(), reserva)[1])

    def cancelar_reserva(self, reserva):
        return self._ejecutar(f"Cancelar reserva {getattr(reserva, 'identificador', '?')}",
                              lambda: (reserva.cancelar(), reserva)[1])

    def procesar_reserva(self, reserva, impuesto=0.0, descuento=0.0):
        return self._ejecutar(f"Procesar reserva {getattr(reserva, 'identificador', '?')}",
                              lambda: (reserva.procesar(impuesto, descuento), reserva)[1])
