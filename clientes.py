#Sistema gestor de clientes......


import re
from entidades import EntidadBase 
from excepciones import ParametroFaltanteError, ClienteInvalidoError

class Cliente(EntidadBase):
    def __init__(self, nombre, documento, correo, telefono):
        self._nombre = self._validar_nombre(nombre)
        self._documento = self._validar_documento(documento)
        self._correo = self._validar_correo(correo)
        self._telefono = self._validar_telefono(telefono)
        super().__init__(self._documento)

    @staticmethod
    def _validar_nombre(nombre):
        if nombre is None or not str(nombre).strip():
            raise ParametroFaltanteError("El nombre es obligatorio.")
        nombre = str(nombre).strip()
        if len(nombre) < 3 or any(c.isdigit() for c in nombre):
            raise ClienteInvalidoError(f"Nombre inválido: {nombre!r}.")
        return nombre

    @staticmethod
    def _validar_documento(documento):
        if documento is None or not str(documento).strip():
            raise ParametroFaltanteError("El documento es obligatorio.")
        documento = str(documento).strip()
        if not documento.isdigit() or not 6 <= len(documento) <= 12:
            raise ClienteInvalidoError(f"Documento inválido (6 a 12 dígitos): {documento!r}.")
        return documento

    @staticmethod
    def _validar_correo(correo):
        if correo is None or not str(correo).strip():
            raise ParametroFaltanteError("El correo es obligatorio.")
        correo = str(correo).strip()
        if not re.match(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$", correo):
            raise ClienteInvalidoError(f"Correo inválido: {correo!r}.")
        return correo.lower()

    @staticmethod
    def _validar_telefono(telefono):
        if telefono is None or not str(telefono).strip():
            raise ParametroFaltanteError("El teléfono es obligatorio.")
        telefono = str(telefono).strip()
        if not (telefono.isdigit() and len(telefono) == 10 and telefono.startswith("3")):
            raise ClienteInvalidoError(f"Teléfono inválido (10 dígitos, empieza en 3): {telefono!r}.")
        return telefono
    
    @property
    def nombre(self):
        return self._nombre

    @property
    def documento(self):
        return self._documento

    @property
    def correo(self):
        return self._correo

    @property
    def telefono(self):
        return self._telefono

    def describir(self):return (f"Cliente '{self._nombre}' - doc {self._documento}, "f"{self._correo}, tel {self._telefono}")

    def validar(self):
        self._validar_nombre(self._nombre)
        self._validar_documento(self._documento)
        self._validar_correo(self._correo)
        self._validar_telefono(self._telefono)

