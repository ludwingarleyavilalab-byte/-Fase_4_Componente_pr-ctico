# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de **Programación** (Fase 4, componente práctico).
Sistema orientado a objetos en Python, **sin base de datos**, con manejo de excepciones
personalizadas. Los archivos solo se usan para registrar eventos y errores (logs).

**Resultado de aprendizaje:** Implementar el manejo de excepciones en aplicaciones orientadas a objetos,
buscando estabilidad, robustez y una gestión adecuada de errores.

## Requisitos

- Python 3 en su última versión estable.
- No hay que instalar librerías: solo se usa la librería estándar.

## Cómo ejecutarlo

### Opción 1: desde la consola (Linux, Mac o Windows)

1. Clona el repositorio con Git y entra a la carpeta del proyecto:
   ```
   git clone https://github.com/ludwingarleyavilalab-byte/-Fase_4_Componente_pr-ctico.git
   cd ./-Fase_4_Componente_pr-ctico
   ```
   El `./` es necesario porque el nombre de la carpeta empieza por un guion.
2. Ejecuta el archivo principal:
   ```
   python3 main.py
   ```
   En Windows, si `python3` no funciona, usa `python main.py` o `py main.py`.
3. Al final el programa pide una tecla para terminar: **cualquier tecla** en Windows o **Enter** en Linux y Mac.

### Opción 2: desde el escritorio (sin Git ni consola)

1. En la página del repositorio en GitHub, pulsa el botón verde **Code** y elige **Download ZIP**.
2. Descomprime el archivo descargado.
3. Entra a la carpeta del proyecto.
4. Haz **doble clic en `main.py`**: se abre una ventana de consola y se ejecuta el programa.
5. Cuando termine, la ventana queda abierta mostrando la salida. Presiona **cualquier tecla** (Windows) o
   **Enter** (Linux y Mac) para terminar el programa y cerrar la ventana.

Para esta opción Python debe estar instalado y asociado a los archivos `.py`. En Linux y Mac, si el doble
clic abre el archivo en un editor en vez de ejecutarlo, usa la Opción 1.

### Qué verás al ejecutarlo

El programa simula más de 10 operaciones numeradas (el sistema ejecuta 30), mezclando casos válidos e inválidos:

- `[OK]` indica que la operación se realizó correctamente.
- `[FALLÓ]` indica un caso inválido que se prueba a propósito (correo mal escrito, cliente repetido, tarifa
  negativa, capacidad excedida, servicio no disponible, descuento imposible, cancelar dos veces, etc.).
  El error queda registrado en el log y el programa continúa con la siguiente operación.

Al final muestra un resumen con los clientes, servicios y reservas, y sus costos calculados.

Se crea la carpeta `logs/` con el archivo `software_fj.log`, donde queda el registro de todos los eventos y
errores. Esa carpeta se genera sola y no se sube al repositorio.

### Datos de ejemplo (opcional)

`python3 catalogo.py` muestra qué clientes de ejemplo se aceptan o se rechazan y la descripción de los 16 servicios del catálogo. No modifica la salida de `main.py`.

## Archivos del proyecto

| Archivo | Para qué sirve |
|---|---|
| `main.py` | Archivo principal. Simula más de 10 operaciones, válidas e inválidas (registro de clientes y servicios, reservas exitosas y fallidas), muestra un resumen final y espera una tecla para terminar. |
| `gestor.py` | Clase `GestorSoftwareFJ`. Mantiene las listas internas de clientes, servicios y reservas, evita clientes repetidos y ejecuta cada operación de forma segura: captura los errores, los registra en el log y evita que el programa se detenga. |
| `entidades.py` | Clase abstracta `EntidadBase`, de la que heredan todas las entidades del sistema. Define el identificador, la fecha de creación, los métodos abstractos `describir()` y `validar()`, y la comparación entre entidades. |
| `clientes.py` | Clase `Cliente` con datos privados (encapsulación) y validaciones estrictas de nombre, documento, correo y teléfono. |
| `servicios.py` | Clase abstracta `Servicio` y cuatro servicios especializados que heredan de ella: `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada` y `ServicioNube`. Cada uno sobrescribe el cálculo de costo, la validación de parámetros y la descripción. Incluye el cálculo con impuesto y descuento opcionales. |
| `reserva.py` | Clase `Reserva` (cliente, servicio, duración y estado) y `EstadoReserva`. Implementa confirmar, cancelar y procesar con manejo de excepciones. |
| `excepciones.py` | Excepciones personalizadas del sistema, todas derivadas de `ErrorSoftwareFJ` (datos inválidos, parámetros faltantes, servicio no disponible, operación no permitida, reserva inválida y cálculo inconsistente). |
| `logger_config.py` | Configuración del archivo de logs (`logs/software_fj.log`) donde se registran los errores y eventos relevantes. |
| `Anexo 3 - Problema a desarrollar Fase 4.pdf` | Enunciado del ejercicio. |
| catalogo.py | Datos de ejemplo (clientes y servicios) y pruebas de validación sobre ellos. Se ejecuta por separado con python3 catalogo.py y no interviene en la simulación de main.py. |

## Conceptos de programación orientada a objetos aplicados

- **Abstracción:** clases abstractas `EntidadBase` y `Servicio`.
- **Herencia y polimorfismo:** los servicios sobrescriben los mismos métodos con comportamiento propio.
- **Encapsulación:** atributos privados con propiedades y validación de los datos.
- **Sobrecarga (emulada con parámetros opcionales):** `calcular_costo_total(duracion, impuesto=0.0, descuento=0.0)`.
- **Manejo de excepciones:** excepciones personalizadas, `try/except/else/finally`, encadenamiento con
  `raise ... from`, registro de cada error en el log y ejecución segura de las operaciones desde el gestor.
