from abc import ABC, abstractmethod
from datetime import datetime


class EntidadBase(ABC):
    def __init__(self, identificador):
        self._identificador = identificador
        self._fecha_creacion = datetime.now()

    @abstractmethod
    def describir(self):
        """Cada clase hija devuelve un texto que la describe."""

    @abstractmethod
    def validar(self):
        """Cada clase hija comprueba que sus datos sean correctos."""

    @property
    def identificador(self):
        return self._identificador

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    def __str__(self):
        return self.describir()

    def __eq__(self, otro):
        return type(self) is type(otro) and self._identificador == otro._identificador

    def __hash__(self):
        return hash((type(self).__name__, self._identificador))


# Prueba rápida: solo se ejecuta con "python entidades.py"
if __name__ == "__main__":

    class Prueba(EntidadBase):
        def describir(self):
            return "Entidad de prueba " + self.identificador

        def validar(self):
            pass

    p = Prueba("S01")
    print(p)
    print("Misma entidad:", p == Prueba("S01"))
    print("Otra entidad:", p == Prueba("S02"))
    print("En un conjunto:", len({p, Prueba("S01"), Prueba("S02")}))