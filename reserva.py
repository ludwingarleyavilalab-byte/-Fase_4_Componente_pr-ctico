"""Clase Reserva: integra cliente, servicio, duración y estado."""

from enum import Enum    # Estados como constantes

from entidades import EntidadBase
from clientes import Cliente
from servicios import Servicio
from logger_config import obtener_logger
from excepciones import (
    ErrorSoftwareFJ,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError,
)

logger = obtener_logger()    # Logger compartido del sistema


class EstadoReserva(Enum):
    """Estados posibles de una reserva."""
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    PROCESADA = "Procesada"
    CANCELADA = "Cancelada"


class Reserva(EntidadBase):
    """Reserva de un servicio por parte de un cliente."""

    _consecutivo = 0    # Contador para generar identificadores R001, R002, ...

    def __init__(self, cliente, servicio, duracion, **extras):
        # Se comprueba que los objetos recibidos sean del tipo correcto
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Servicio válido.")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")
        try:
            # El propio servicio valida duración y parámetros (polimorfismo)
            servicio.validar_parametros(duracion, **extras)
        except ErrorSoftwareFJ as error:
            # ENCADENAMIENTO: se conserva el error original con "from error"
            raise ReservaInvalidaError(
                f"No se pudo crear la reserva de '{servicio.nombre}'."
            ) from error
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._extras = extras                     # Parámetros propios del servicio
        self._estado = EstadoReserva.PENDIENTE    # Toda reserva inicia pendiente
        self._costo_final = None                  # Se calcula al procesar
        Reserva._consecutivo += 1                 # Solo se consume número si la reserva es válida
        super().__init__(f"R{Reserva._consecutivo:03d}")

    @property
    def estado(self):
        return self._estado

    @property
    def costo_final(self):
        return self._costo_final

    def validar(self):
        """Implementa el método abstracto de EntidadBase: revisa la reserva completa."""
        self._servicio.validar_parametros(self._duracion, **self._extras)

    def confirmar(self):
        """Pendiente -> Confirmada. Usa try/except/else/finally."""
        try:
            if self._estado is not EstadoReserva.PENDIENTE:
                raise OperacionNoPermitidaError(
                    f"Reserva {self.identificador} en estado {self._estado.value}: no se puede confirmar."
                )
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{self._servicio.nombre}' dejó de estar disponible."
                )
        except ErrorSoftwareFJ as error:
            logger.error("Confirmación fallida: %s", error)
            raise    # Se propaga para que el gestor decida
        else:
            self._estado = EstadoReserva.CONFIRMADA    # Solo si no hubo errores
            logger.info("Reserva %s confirmada.", self.identificador)
        finally:
            logger.debug("Fin del intento de confirmación de la reserva %s.", self.identificador)

    def cancelar(self):
        """Cancela la reserva si aún no fue procesada ni cancelada."""
        try:
            if self._estado in (EstadoReserva.CANCELADA, EstadoReserva.PROCESADA):
                raise OperacionNoPermitidaError(
                    f"Reserva {self.identificador} en estado {self._estado.value}: no se puede cancelar."
                )
        except OperacionNoPermitidaError as error:
            logger.error("Cancelación fallida: %s", error)
            raise
        else:
            self._estado = EstadoReserva.CANCELADA
            logger.info("Reserva %s cancelada.", self.identificador)
        finally:
            logger.debug("Fin del intento de cancelación de la reserva %s.", self.identificador)

    def procesar(self, impuesto=0.0, descuento=0.0):
        """Confirmada -> Procesada, calculando el costo final."""
        try:
            if self._estado is not EstadoReserva.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    f"Reserva {self.identificador} en estado {self._estado.value}: debe estar confirmada."
                )
            costo = self._servicio.calcular_costo_total(
                self._duracion, impuesto, descuento, **self._extras
            )
        except CalculoInconsistenteError as error:
            logger.error("Cálculo inconsistente en reserva %s: %s", self.identificador, error)
            # ENCADENAMIENTO: el error de cálculo queda como causa del error de reserva
            raise ReservaInvalidaError(f"No se pudo procesar la reserva {self.identificador}.") from error
        except ErrorSoftwareFJ as error:
            logger.error("Procesamiento fallido: %s", error)
            raise
        else:
            self._costo_final = costo
            self._estado = EstadoReserva.PROCESADA
            logger.info("Reserva %s procesada. Costo final: $%s", self.identificador, f"{costo:,.2f}")
        finally:
            logger.debug("Fin del intento de procesamiento de la reserva %s.", self.identificador)

    def describir(self):
        costo = f", total ${self._costo_final:,.2f}" if self._costo_final else ""
        unidad = getattr(self._servicio, "UNIDAD_DURACION", "h")    # Horas por defecto; la nube usa meses
        return (f"Reserva {self.identificador} [{self._estado.value}] {self._cliente.nombre} -> "
                f"{self._servicio.nombre} x {self._duracion} {unidad}{costo}")
