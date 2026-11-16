#Sistema gestor de clientes......

ROJO = "\033[91m"   #Defino colores de fuente en base a las validaciones y errores
VERDE = "\033[92m"
AMARILLO = "\033[93m"
RESET = "\033[0m"
import re
#from entidades import EntidadBase Como comentario para funcionamiento "local" o independiente a otros modulos, cualquier cosa quitar el #


class ErrorSoftwareFJ(Exception):
    """Base de todos los errores del sistema. El gestor atrapa esta."""

class ParametroFaltanteError(ErrorSoftwareFJ):
    """Falta un dato obligatorio."""

class ClienteInvalidoError(ErrorSoftwareFJ):
    """El dato existe pero tiene un formato incorrecto."""

#class Cliente(EntidadBase)
class Cliente:
    def __init__(self, nombre, documento, correo, telefono):
        self._nombre = self._validar_nombre(nombre)
        self._documento = self._validar_documento(documento)
        self._correo = self._validar_correo(correo)
        self._telefono = self._validar_telefono(telefono)
       #super().__init__()    aqui tambien el #

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

    def __str__(self):
         return (f"Cliente '{self._nombre}' - doc {self._documento}, "f"{self._correo}, tel {self._telefono}")

  




datos_clientes = [ #ingresan datos y si validan, entran al portafolio

    ("Ana Torres", "1012345678", "ana@mail.com", "3101234567"),
    ("Luis Pérez", "80123456", "luis@mail.com", "3209876543"),
    ("Pedro Gil", "12345678", "pedro-sin-arroba", "3001112233"),
    ("Laura Pinto", "12345678", "laura@", "3001112233"),
    ("Hugo Mora", "12345678", "", "3001112233"),
    ("Jo", "12345678", "jo@mail.com", "3001112233"),                   
    ("Nora Luna", "12345678", "nora@mail.com", "2001112233"),         
    ("Omar Silva", "", "omar@mail.com", "31011122ab")       
    #ver si un cliente ya esta en el portafolio, para no repetir clientes
]

portafolio_clientes = [] #ete portafolio

for datos in datos_clientes:
    try:
        cliente = Cliente(*datos)
    except ParametroFaltanteError as e:
        print(f"{AMARILLO}Falta un dato{RESET} --> {e}")
    except ClienteInvalidoError as e:
        print(f"{ROJO}Mal ingreso de datos{RESET} --> {e}")
    else:
        portafolio_clientes.append(cliente)
        print(f"{VERDE}Ingreso de datos acertado{RESET} --> {cliente}")