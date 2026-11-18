"""Módulo de excepciones personalizadas del sistema Software FJ."""


class ErrorSoftwareFJ(Exception):
    """Excepción base: todas las excepciones del sistema heredan de ella."""

    def __init__(self, mensaje="Error en el sistema Software FJ"):
        # Se envía el mensaje a la clase Exception para que str(error) lo muestre
        super().__init__(mensaje)
        # Se guarda el mensaje también como atributo para usarlo en los logs
        self.mensaje = mensaje


class ErrorValidacion(ErrorSoftwareFJ):
    """Error general de validación de datos de entrada."""


class ClienteInvalidoError(ErrorValidacion):
    """Los datos de un cliente no cumplen las reglas de validación."""


class ParametroFaltanteError(ErrorValidacion):
    """Falta un parámetro obligatorio (o llegó vacío / None)."""


class ServicioInvalidoError(ErrorValidacion):
    """Los datos o parámetros de un servicio no son válidos."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio solicitado no está disponible para reservar."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """La operación no es válida para el estado actual del objeto."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """No fue posible crear o procesar la reserva solicitada."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """El cálculo de costos produjo un valor o parámetros incoherentes."""
