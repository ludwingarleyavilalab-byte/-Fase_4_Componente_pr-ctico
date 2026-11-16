"""Clase abstracta Servicio y los tres servicios especializados de Software FJ."""

from abc import ABC, abstractmethod                  # Clases abstractas

from entidades import EntidadBase
from excepciones import (
    ParametroFaltanteError,
    ServicioInvalidoError,
    CalculoInconsistenteError,
)


class Servicio(EntidadBase, ABC):
    """Servicio genérico. Define lo que TODO servicio debe saber hacer."""

    DURACION_MAXIMA = 12   # Horas máximas permitidas por reserva

    def __init__(self, nombre, tarifa_base, disponible=True):
        # Validaciones antes de asignar (si fallan, no se consume id)
        if nombre is None or not str(nombre).strip():
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")
        if isinstance(tarifa_base, bool) or not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ServicioInvalidoError(f"Tarifa base inválida: {tarifa_base!r}.")
        self._nombre = str(nombre).strip()    # Atributo protegido
        self._tarifa_base = float(tarifa_base)  # Tarifa por hora
        self._disponible = bool(disponible)   # Si se puede reservar o no
        super().__init__()

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        self._disponible = bool(valor)

    def _validar_duracion(self, duracion):
        """Validación común de la duración (en horas) para todos los servicios."""
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ServicioInvalidoError(f"La duración debe ser numérica: {duracion!r}.")
        if duracion <= 0 or duracion > self.DURACION_MAXIMA:
            raise ServicioInvalidoError(
                f"Duración fuera de rango (1 a {self.DURACION_MAXIMA} h): {duracion}."
            )

    # ---- Métodos abstractos: cada servicio los sobrescribe a su manera ----
    @abstractmethod
    def calcular_costo(self, duracion, **extras):
        """Costo base (sin impuestos ni descuentos)."""

    @abstractmethod
    def validar_parametros(self, duracion, **extras):
        """Valida la duración y los parámetros propios del servicio."""

    # ---- Método "sobrecargado" mediante parámetros opcionales ----
    def calcular_costo_total(self, duracion, impuesto=0.0, descuento=0.0, **extras):
        """Variantes de uso (sobrecarga emulada con parámetros opcionales):
           calcular_costo_total(2)             -> solo costo base
           calcular_costo_total(2, 0.19)       -> con impuesto
           calcular_costo_total(2, 0.19, 0.10) -> con impuesto y descuento
        """
        # Los porcentajes deben ser números entre 0 y 1
        for nombre, valor in (("impuesto", impuesto), ("descuento", descuento)):
            if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not 0 <= valor <= 1:
                raise CalculoInconsistenteError(f"{nombre.capitalize()} inválido: {valor!r}.")
        base = self.calcular_costo(duracion, **extras)       # Costo según el servicio (polimorfismo)
        total = base * (1 - descuento) * (1 + impuesto)      # Se aplican descuento e impuesto
        if total <= 0:                                       # Un costo no positivo es incoherente
            raise CalculoInconsistenteError(f"Costo total inconsistente: {total}.")
        return round(total, 2)


class ReservaSala(Servicio):
    """Servicio 1: reserva de salas (costo por hora, con capacidad máxima)."""

    def __init__(self, nombre, tarifa_base, capacidad, disponible=True):
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError(f"Capacidad inválida: {capacidad!r}.")
        super().__init__(nombre, tarifa_base, disponible)
        self._capacidad = capacidad

    def validar_parametros(self, duracion, **extras):
        self._validar_duracion(duracion)
        asistentes = extras.get("asistentes", 1)             # Por defecto 1 asistente
        if not isinstance(asistentes, int) or asistentes <= 0:
            raise ServicioInvalidoError(f"Número de asistentes inválido: {asistentes!r}.")
        if asistentes > self._capacidad:
            raise ServicioInvalidoError(
                f"{asistentes} asistentes superan la capacidad ({self._capacidad})."
            )

    def calcular_costo(self, duracion, **extras):
        self.validar_parametros(duracion, **extras)          # Siempre se valida antes de calcular
        return self._tarifa_base * duracion

    def describir(self):
        return (f"Sala '{self._nombre}' (#{self.id}) - capacidad {self._capacidad}, "
                f"${self._tarifa_base:,.0f}/h")


class AlquilerEquipo(Servicio):
    """Servicio 2: alquiler de equipos (costo por hora y por unidad)."""

    def __init__(self, nombre, tarifa_base, unidades, disponible=True):
        if isinstance(unidades, bool) or not isinstance(unidades, int) or unidades <= 0:
            raise ServicioInvalidoError(f"Unidades inválidas: {unidades!r}.")
        super().__init__(nombre, tarifa_base, disponible)
        self._unidades = unidades

    def validar_parametros(self, duracion, **extras):
        self._validar_duracion(duracion)
        cantidad = extras.get("cantidad", 1)                 # Por defecto 1 unidad
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ServicioInvalidoError(f"Cantidad inválida: {cantidad!r}.")
        if cantidad > self._unidades:
            raise ServicioInvalidoError(
                f"Se piden {cantidad} unidades y solo hay {self._unidades}."
            )

    def calcular_costo(self, duracion, **extras):
        self.validar_parametros(duracion, **extras)
        return self._tarifa_base * duracion * extras.get("cantidad", 1)

    def describir(self):
        return (f"Equipo '{self._nombre}' (#{self.id}) - {self._unidades} unidades, "
                f"${self._tarifa_base:,.0f}/h por unidad")


class AsesoriaEspecializada(Servicio):
    """Servicio 3: asesoría (la tarifa cambia según el nivel del asesor)."""

    # Multiplicador de tarifa por nivel del asesor
    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre, tarifa_base, especialidad, disponible=True):
        if especialidad is None or not str(especialidad).strip():
            raise ParametroFaltanteError("La especialidad es obligatoria.")
        super().__init__(nombre, tarifa_base, disponible)
        self._especialidad = str(especialidad).strip()

    def validar_parametros(self, duracion, **extras):
        self._validar_duracion(duracion)
        nivel = extras.get("nivel")                          # El nivel es obligatorio
        if nivel is None:
            raise ParametroFaltanteError("Falta el parámetro 'nivel' de la asesoría.")
        if nivel not in self.NIVELES:
            raise ServicioInvalidoError(
                f"Nivel '{nivel}' no existe. Opciones: {', '.join(self.NIVELES)}."
            )

    def calcular_costo(self, duracion, **extras):
        self.validar_parametros(duracion, **extras)
        return self._tarifa_base * duracion * self.NIVELES[extras["nivel"]]

    def describir(self):
        return (f"Asesoría '{self._nombre}' (#{self.id}) - {self._especialidad}, "
                f"${self._tarifa_base:,.0f}/h base")
