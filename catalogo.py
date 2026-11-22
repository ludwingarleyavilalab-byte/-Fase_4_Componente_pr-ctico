"""Datos de ejemplo de Software FJ: clientes y servicios de prueba.

Este módulo reúne los datos de muestra que antes estaban en los bloques de prueba
de clientes.py y servicios.py. No interviene en la simulación de main.py; se ejecuta
por separado con: python3 catalogo.py
"""

from datetime import date    # Tipo de fecha que usa el servicio en la nube

from clientes import Cliente    # Clase Cliente (validaciones de datos personales)
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada, ServicioNube    # Servicios especializados
from excepciones import ParametroFaltanteError, ClienteInvalidoError    # Errores que pueden lanzar los clientes

# Códigos de color ANSI para resaltar los mensajes en la consola
ROJO = "\033[91m"
VERDE = "\033[92m"
AMARILLO = "\033[93m"
RESET = "\033[0m"    # Vuelve al color normal de la consola

# Datos de ejemplo de clientes: (nombre, documento, correo, teléfono)
# Algunos son inválidos a propósito para comprobar las validaciones
DATOS_CLIENTES = [
    ("Ana Torres", "1012345678", "ana@mail.com", "3101234567"),
    ("Luis Pérez", "80123456", "luis@mail.com", "3209876543"),
    ("Pedro Gil", "12345678", "pedro-sin-arroba", "3001112233"),    # Correo sin arroba
    ("Laura Pinto", "12345678", "laura@", "3001112233"),    # Correo incompleto
    ("Hugo Mora", "12345678", "", "3001112233"),    # Correo vacío
    ("Jo", "12345678", "jo@mail.com", "3001112233"),    # Nombre demasiado corto
    ("Nora Luna", "12345678", "nora@mail.com", "2001112233"),    # Teléfono que no empieza en 3
    ("Carlos Torres", "1012345678", "carlos@mail.com", "3111234567"),    # Mismo documento que Ana
    ("Omar Silva", "", "omar@mail.com", "31011122ab"),    # Documento vacío y teléfono con letras
]


def crear_catalogo_servicios():
    """Devuelve una lista nueva con los servicios de ejemplo (se crean al llamar la función)."""
    return [
        # Salas: (código, nombre, tarifa por hora, capacidad)
        ReservaSala("S01", "Sala de reuniones pequeña", 25000, 8),
        ReservaSala("S02", "Auditorio principal", 85000, 100),
        ReservaSala("S03", "Sala de capacitaciones", 45000, 30),
        # Equipos: (código, nombre, tarifa por hora, unidades disponibles)
        AlquilerEquipo("E07", "Escáner documental", 10000, 6),
        AlquilerEquipo("E08", "Micrófono inalámbrico", 7000, 12),
        AlquilerEquipo("E09", "Cámara profesional", 25000, 4),
        AlquilerEquipo("E10", "Router empresarial", 12000, 8),
        AlquilerEquipo("E11", "Servidor físico", 50000, 3),
        AlquilerEquipo("E12", "Switch de red", 18000, 10),
        # Asesorías: (código, nombre, tarifa por hora, especialidad)
        AsesoriaEspecializada("A11", "Inteligencia artificial", 100000, "Inteligencia artificial"),
        AsesoriaEspecializada("A12", "Seguridad de redes", 90000, "Ciberseguridad"),
        AsesoriaEspecializada("A13", "Optimización SQL", 70000, "Bases de datos"),
        AsesoriaEspecializada("A14", "Desarrollo Python", 60000, "Programación"),
        # Nube: (código, nombre, tarifa por TB al mes, TB estimados, meses, fecha de inicio)
        ServicioNube("N11", "Respaldo empresarial avanzado", 30000, 40, 12, date(2026, 11, 17)),
        ServicioNube("N12", "Entorno de desarrollo en la nube", 28000, 10, 5, date(2026, 11, 17)),
        ServicioNube("N13", "Almacenamiento de documentos", 10000, 5, 2, date(2026, 11, 17)),
    ]


def probar_clientes():
    """Intenta registrar los clientes de ejemplo y muestra cuáles se aceptan y cuáles no."""
    portafolio_clientes = []    # Clientes que pasaron todas las validaciones

    for datos in DATOS_CLIENTES:    # Se procesa cada cliente de ejemplo
        try:
            cliente = Cliente(*datos)    # Si algún dato es inválido, aquí se lanza la excepción

            # Se verifica si el cliente ya existe en el portafolio, comparando por documento
            repetido = any(c.documento == cliente.documento for c in portafolio_clientes)

            if repetido:
                print(f"{AMARILLO}Cliente repetido{RESET} --> {cliente.documento}")
                continue    # Se pasa al siguiente cliente sin agregarlo

        except ParametroFaltanteError as e:    # Falta un dato obligatorio
            print(f"{AMARILLO}Falta un dato{RESET} --> {e}")

        except ClienteInvalidoError as e:    # El dato existe pero tiene un formato incorrecto
            print(f"{ROJO}Mal ingreso de datos{RESET} --> {e}")

        else:    # Solo se ejecuta si no hubo ninguna excepción
            portafolio_clientes.append(cliente)
            print(f"{VERDE}Ingreso de datos acertado{RESET} --> {cliente}")


def probar_servicios():
    """Crea el catálogo de servicios de ejemplo y muestra la descripción de cada uno."""
    for servicio in crear_catalogo_servicios():
        print(servicio.describir())    # Descripción propia de cada tipo de servicio (polimorfismo)
        print("-" * 50)    # Línea separadora


# Prueba de los datos de ejemplo: solo se ejecuta con "python3 catalogo.py"
if __name__ == "__main__":
    probar_clientes()
    print()    # Línea en blanco entre las dos pruebas
    probar_servicios()
