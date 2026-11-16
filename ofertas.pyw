from abc import ABC, abstractmethod
from datetime import date, timedelta

class ServicioError(Exception):
    pass


class ParametroInvalidoError(ServicioError):
    pass


class ServicioNoDisponibleError(ServicioError):
    pass


class Servicio(ABC): # tenemos el global de los servicios, luego definimos reserva de salas, alquileres y asesorias que tienen en si cositas ajenas entre sí
    def __init__(self, codigo_servicio, valor_servicio, texto_servicio):
        self.codigo_servicio = codigo_servicio
  
        self.valor_servicio  = valor_servicio
        self.texto_servicio  = texto_servicio

    
    def tributacion(self, impuesto = 0.19, descuento_porcentaje = 0): #Vamos a ponerle iva por defecto a los servicios pq aja, bonito..de manera si colocamos 100k por defecto sea 119k
        if descuento_porcentaje>=100:
         descuento_pocentaje = int(input("Confirme el valor del porcetaje"))
        if descuento_pocentaje>100:
           raise ParametroInvalidoError("El descuento debe estar entre 0 y 100")
        
        descuento = descuento_porcentaje / 100 #opero como decimal
        valor_impuesto = self.valor_servicio * impuesto 
        subtotal = valor_impuesto + self.valor_servicio
        valor_descuento = subtotal * descuento #el descuento despues del sonbrecosto del impuesto
        return subtotal - valor_descuento
        

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def describir_servicio(self):
        pass

    @abstractmethod
    def validar_parametros(self):
        pass

    def _validar_basicos(self):
        if not self.codigo_servicio:
            raise ParametroInvalidoError("El servicio necesita un código")
        if self.valor_servicio <= 0:
            raise ParametroInvalidoError("El valor del servicio debe ser mayor que 0")
        
    def __str__(self):
        return self.describir_servicio()



class Reserva_Salas(Servicio): 
    def __init__(self, codigo_servicio, valor_servicio, texto_servicio, nombre_sala, capacidad_sala, equipo_sala):
     super().__init__(codigo_servicio, valor_servicio, texto_servicio)
     self.nombre_sala = nombre_sala
     self.capacidad_sala = capacidad_sala
     self.equipo_sala = equipo_sala
     self.validar_parametros()

    def validar_parametros(self):
        self._validar_basicos()
        if not self.nombre_sala:
            raise ParametroInvalidoError("La sala necesita un nombre")
        if self.capacidad_sala <= 0:
            raise ParametroInvalidoError("La capacidad de la sala debe ser mayor que 0")

    def calcular_costo(self, duracion, impuesto=0.19, descuento_porcentaje=0):
        # duracion = horas ... se cobra por horas vale?
        if duracion <= 0:
            raise ParametroInvalidoError("Las horas deben ser mayores que 0")
        base = self.valor_servicio * duracion
        return self.tributacion(base, impuesto, descuento_porcentaje)

    def describir_servicio(self):
        return (f"Sala {self.nombre_sala} | Capacidad: {self.capacidad_sala} personas | "f"Equipo: {self.equipo_sala} | ${self.valor_servicio:,.0f} por hora")
    


class Alquiler_De_Equipos(Servicio):
      def __init__(self, codigo_servicio , valor_servicio, texto_servicio,nombre_equipo, stock_equipo, fecha_alquiler, tiempo_alquiler):
       super().__init__(codigo_servicio, valor_servicio, texto_servicio)
       self.nombre_equipo = nombre_equipo
       self.stock_equipo = stock_equipo 
       self.fecha_alquiler = fecha_alquiler 
       self.tiempo_alquiler = tiempo_alquiler
       self.validar_parametros()


      def validar_parametros(self):
        self._validar_basicos()
        if not self.nombre_equipo:
            raise ParametroInvalidoError("El equipo amerita un nombre")
        if self.tiempo_alquiler <= 0:
            raise ParametroInvalidoError("El tiempo del alquiler no puede ser negativo")
        if self.stock_equipo < 0:
            raise ParametroInvalidoError("El stock no puede ser negativo")

      def calcular_costo(self, duracion=None, impuesto=0.19, descuento_porcentaje=0):
        # duracion = días; si no se manda, usa el tiempo con el que se creó
        if self.stock_equipo == 0:
            raise ServicioNoDisponibleError(f"No hay stock de {self.nombre_equipo}")
        if duracion is None:
            duracion = self.tiempo_alquiler
        if duracion <= 0:
            raise ParametroInvalidoError("Los días deben ser mayores que 0")
        base = self.valor_servicio * duracion
        return self.tributacion(base, impuesto, descuento_porcentaje)

      def fecha_devolucion(self):
        return self.fecha_alquiler + timedelta(days=self.tiempo_alquiler)

      def describir_servicio(self):
        return (f"Equipo {self.nombre_equipo} | Stock: {self.stock_equipo} | "f"Alquiler desde {self.fecha_alquiler} por {self.tiempo_alquiler} días | "f"${self.valor_servicio:,.0f} por día")


class Asesoria_Especializada(Servicio):
    def __init__(self, codigo_servicio, valor_servicio, texto_servicio, tipo_de_servicio):
        super().__init__(codigo_servicio, valor_servicio, texto_servicio)
        self.tipo_de_servicio = tipo_de_servicio
        self.validar_parametros()

    def validar_parametros(self):
        self._validar_basicos()
        if not self.tipo_de_servicio:
            raise ParametroInvalidoError("La asesoría necesita un tipo")

    def calcular_costo(self, duracion, impuesto=0.19, descuento_porcentaje=0):
        # duracion = horas
        if duracion <= 0:
            raise ParametroInvalidoError("Las horas deben ser mayores que 0")
        base = self.valor_servicio * duracion
        return self.tributacion(base, impuesto, descuento_porcentaje)

    def describir_servicio(self):
        return (f"Asesoría de {self.tipo_de_servicio} | "f"${self.valor_servicio:,.0f} por hora")


class Servicio_Nube(Servicio):
    def __init__(self, codigo_servicio, valor_servicio, texto_servicio,
                 espacio_estimado, tiempo_del_servicio, fecha_del_servicio):
        super().__init__(codigo_servicio, valor_servicio, texto_servicio)
        self.espacio_estimado = espacio_estimado      # vamos a llevarlo en teras pq mas facil generalizar
        self.tiempo_del_servicio = tiempo_del_servicio  # mesesotes
        self.fecha_del_servicio = fecha_del_servicio  
        self.validar_parametros()

    def validar_parametros(self):
        self._validar_basicos()
        if self.espacio_estimado <= 0:
            raise ParametroInvalidoError("El espacio debe ser mayor a 0 Teras")
        if self.tiempo_del_servicio <= 0:
            raise ParametroInvalidoError("Los meses deben ser mayores que 0")

    def calcular_costo(self, duracion=None, impuesto=0.19, descuento_porcentaje=0):
        if duracion is None: #meses(duracion) 
            duracion = self.tiempo_del_servicio
        if duracion <= 0:
            raise ParametroInvalidoError("Los meses deben ser mayores que 0")
        base = self.valor_servicio * self.espacio_estimado * duracion
        return self.tributacion(base, impuesto, descuento_porcentaje)

    def fecha_final(self):
        return self.fecha_del_servicio + timedelta(days=30 * self.tiempo_del_servicio) #meses de 30 dias pq aja

    def describir_servicio(self):
        return (f"Nube {self.espacio_estimado} TB por {self.tiempo_del_servicio} meses | "f"Inicio: {self.fecha_del_servicio} | Fin: {self.fecha_final()} | "f"${self.valor_servicio:,.0f} por TB al mes")


         

