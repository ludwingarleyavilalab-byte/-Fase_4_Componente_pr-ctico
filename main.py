"""Simulación de más de 10 operaciones de Software FJ (válidas e inválidas)."""

from datetime import date

from gestor import GestorSoftwareFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada, ServicioNube, Servicio
from logger_config import ARCHIVO_LOG, obtener_logger

logger = obtener_logger()
IVA = 0.19    # Impuesto usado en la simulación

_numero = 0    # Contador de operaciones para numerar la salida


def mostrar(descripcion, resultado):
    """Imprime el resultado de cada operación sin detener el programa."""
    global _numero
    _numero += 1
    estado = "OK    " if resultado is not None else "FALLÓ "
    print(f"{_numero:>2}. [{estado}] {descripcion}")
    if resultado is not None:
        print(f"      -> {resultado}")


def main():
    logger.info("===== INICIO DE LA SIMULACIÓN =====")
    g = GestorSoftwareFJ()

    print("\n--- CLIENTES ---")
    ana = g.registrar_cliente(nombre="Ana Torres", documento="1012345678",
                              correo="ana@mail.com", telefono="3101234567")
    mostrar("Cliente válido (Ana)", ana)
    luis = g.registrar_cliente(nombre="Luis Pérez", documento="80123456",
                               correo="luis@mail.com", telefono="3209876543")
    mostrar("Cliente válido (Luis)", luis)
    mostrar("Cliente con correo inválido",
            g.registrar_cliente(nombre="Pedro Gil", documento="12345678",
                                correo="pedro-sin-arroba", telefono="3001112233"))
    mostrar("Cliente sin teléfono (parámetro faltante)",
            g.registrar_cliente(nombre="Marta Ríos", documento="55667788",
                                correo="marta@mail.com"))

    mostrar("Cliente repetido (mismo documento que Ana)",
            g.registrar_cliente(nombre="Ana Torres Copia", documento="1012345678",
                                correo="copia@mail.com", telefono="3151112233"))

    print("\n--- SERVICIOS ---")
    sala = g.registrar_servicio(ReservaSala, codigo_servicio="S01", nombre="Sala Innovación",
                                tarifa_base=50000, capacidad=10)
    mostrar("Servicio válido: sala", sala)
    equipo = g.registrar_servicio(AlquilerEquipo, codigo_servicio="E01", nombre="Portátil Pro",
                                  tarifa_base=15000, unidades=5)
    mostrar("Servicio válido: equipo", equipo)
    asesoria = g.registrar_servicio(AsesoriaEspecializada, codigo_servicio="A01", nombre="Asesoría Cloud",
                                    tarifa_base=80000, especialidad="Arquitectura en la nube")
    mostrar("Servicio válido: asesoría", asesoria)
    nube = g.registrar_servicio(ServicioNube, codigo_servicio="N01", nombre="Almacenamiento de documentos",
                                tarifa_base=10000, espacio_estimado=5, tiempo_del_servicio=2,
                                fecha_del_servicio=date(2026, 12, 1))
    mostrar("Servicio válido: nube", nube)
    mostrar("Servicio con tarifa negativa",
            g.registrar_servicio(ReservaSala, codigo_servicio="S02", nombre="Sala Rota", tarifa_base=-100, capacidad=4))
    mostrar("Instanciar clase abstracta Servicio",
            g.registrar_servicio(Servicio, codigo_servicio="X01", nombre="Genérico", tarifa_base=1000))
    sala_cerrada = g.registrar_servicio(ReservaSala, codigo_servicio="S03", nombre="Sala en Mantenimiento",
                                        tarifa_base=40000, capacidad=6, disponible=False)

    print("\n--- RESERVAS ---")
    r1 = g.crear_reserva(ana, sala, 3, asistentes=8)
    mostrar("Reserva de sala (Ana, 3 h)", r1)
    mostrar("Confirmar reserva de sala", g.confirmar_reserva(r1))
    mostrar("Procesar con IVA y 10% de descuento", g.procesar_reserva(r1, IVA, 0.10))

    mostrar("Sala con más asistentes que la capacidad",
            g.crear_reserva(luis, sala, 2, asistentes=25))
    mostrar("Reserva de servicio no disponible",
            g.crear_reserva(luis, sala_cerrada, 2))
    mostrar("Asesoría sin indicar el nivel",
            g.crear_reserva(ana, asesoria, 2))

    r2 = g.crear_reserva(luis, equipo, 4, cantidad=2)
    mostrar("Reserva de equipo (Luis, 2 unidades, 4 h)", r2)
    mostrar("Confirmar reserva de equipo", g.confirmar_reserva(r2))
    mostrar("Procesar con descuento imposible (150%)", g.procesar_reserva(r2, IVA, 1.5))
    mostrar("Procesar de nuevo con valores correctos", g.procesar_reserva(r2, IVA))

    r3 = g.crear_reserva(ana, asesoria, 2, nivel="senior")
    mostrar("Reserva de asesoría senior (Ana, 2 h)", r3)
    mostrar("Cancelar reserva de asesoría", g.cancelar_reserva(r3))
    mostrar("Cancelar de nuevo (operación no permitida)", g.cancelar_reserva(r3))
    mostrar("Confirmar reserva ya cancelada", g.confirmar_reserva(r3))
    mostrar("Reserva con duración no numérica", g.crear_reserva(ana, sala, "dos horas"))

    r4 = g.crear_reserva(luis, nube, 3)
    mostrar("Reserva de servicio en la nube (Luis, 3 meses)", r4)
    mostrar("Confirmar reserva de nube", g.confirmar_reserva(r4))
    mostrar("Procesar reserva de nube con IVA", g.procesar_reserva(r4, IVA))
    mostrar("Reserva de nube con 200 meses (fuera de rango)", g.crear_reserva(ana, nube, 200))

    print("\n--- RESUMEN FINAL (el sistema siguió activo) ---")
    print(f"Clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} | Reservas: {len(g.reservas)}")
    for reserva in g.reservas:
        print("  ", reserva)
    print(f"\nRegistro de errores y eventos en: {ARCHIVO_LOG}")
    logger.info("===== FIN DE LA SIMULACIÓN =====")

def esperar_tecla():
    """Pausa el programa para que la ventana no se cierre sola al abrirlo con doble clic."""
    print("\nPresione cualquier tecla (Windows) o Enter (Linux) para terminar el programa...")
    try:
        import msvcrt    # Módulo que solo existe en Windows
        msvcrt.getch()    # Espera una tecla, sin necesidad de pulsar Enter
    except ImportError:
        input()    # En Linux y Mac se espera la tecla Enter


if __name__ == "__main__":
    try:
        main()
    except Exception:    # Si algo falla, se muestra el error y la ventana no se cierra
        import traceback
        traceback.print_exc()
    esperar_tecla()
