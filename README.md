# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

Proyecto de **Programación** (Fase 4, componente práctico). 
Sistema orientado a objetos en Python, **sin base de datos**, con manejo de excepciones
personalizadas. Los archivos solo se usan para registrar eventos y errores (logs).

**Resultado de aprendizaje:** Implementar el manejo de excepciones en aplicaciones orientadas a objetos,
buscando estabilidad, robustez y una gestión adecuada de errores.

## Requisitos

- Python en su ultima version estable.
- No hay que instalar librerías: solo se usa la librería estándar.

## Cómo ejecutarlo

1. Clona el repositorio y entra a la carpeta:
   ```
   git clone https://github.com/ludwingarleyavilalab-byte/-Fase_4_Componente_pr-ctico.git
   cd -Fase_4_Componente_pr-ctico
   ```
2. Ejecuta el archivo principal:
   ```
   python3 main.py
   ```
3. Al terminar se crea la carpeta `logs/` con el archivo `software_fj.log`, donde queda el registro de
   todos los eventos y errores. Esa carpeta se genera sola y no se sube al repositorio.

## Archivos del proyecto 

| Archivo | Para qué sirve |
|---|---|
| `main.py` | Archivo principal. Simula más de 10 operaciones, válidas e inválidas (registro de clientes y servicios, reservas exitosas y fallidas) y muestra un resumen final. |
| `gestor.py` | Clase `GestorSoftwareFJ`. Mantiene las listas internas de clientes, servicios y reservas, y ejecuta cada operación de forma segura: captura los errores, los registra en el log y evita que el programa se detenga. |
| `servicios.py` | Clase abstracta `Servicio` y tres servicios especializados que heredan de ella: `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`. Cada uno sobrescribe el cálculo de costo, la validación de parámetros y la descripción. Incluye el cálculo con impuesto y descuento opcionales. |
| `logger_config.py` | Configuración del archivo de logs (`logs/software_fj.log`) donde se registran los errores y eventos relevantes. |

## Conceptos de programación orientada a objetos aplicados

- **Abstracción:** clase abstracta `Servicio`.
- **Herencia y polimorfismo:** los tres servicios sobrescriben los mismos métodos con comportamiento propio.
- **Sobrecarga (emulada con parámetros opcionales):** `calcular_costo_total(duracion, impuesto=0.0, descuento=0.0)`.
- **Manejo de excepciones:** `try/except/else/finally`, registro de cada error en el log y ejecución segura
  de las operaciones desde el gestor.

## Estado actual

El proyecto está en desarrollo en equipo. `main.py` y `gestor.py` dependen de módulos de cliente, reserva
y excepciones que se integrarán a medida que el grupo suba y unifique sus archivos; hasta entonces es
posible que la ejecución dé errores de importación.

