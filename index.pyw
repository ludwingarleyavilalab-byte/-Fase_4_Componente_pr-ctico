import tkinter as tk

color_1 = "#241B1C"
color_2 = "#3D3539"
color_3 = "#4F484F"
color_4 = "#F4EAEA"
color_5 = "#F0B569"


class Aplicacion:

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("SOFTWARE HJ")
        self.ventana.attributes("-fullscreen", True)
        self.ventana.configure(bg=color_4)
        self.ventana.columnconfigure(0, weight=1)


        #Seccion superior, no tiene mucho realmente. Aguantaria un logo y un exit ciertamente.
        self.seccion_superior = tk.Frame(self.ventana,bg=color_5)
        self.seccion_superior.grid(row=0,column=0,padx=10,pady=5,sticky="ew")
        self.seccion_superior.columnconfigure(0, weight=1) # me come todo lo disponible en x
        self.titulo = tk.Label(self.seccion_superior,text="APLICATIVO GESTOR DE SERVICIOS",bg=color_1,fg=color_5, font=("Arial", 20 ))
        self.titulo.grid(row=0, column=0, sticky="ew")

        #Seccion de navegacion, ha de tener boton de servicios, clientes, reserva e historial?
        self.seccion_navegacion = tk.Frame(self.ventana,bg=color_5)
        self.seccion_navegacion.grid(row=1,column=0,padx=10,pady=5)
        self.seccion_navegacion.columnconfigure(0, weight=1)
        self.boton_ofertas = tk.Button(self.seccion_navegacion, text="Clientes",bg=color_1,fg=color_5, font=("Arial", 15 ))
        self.boton_ofertas.grid(row=0, column=0)
        self.boton_servicios = tk.Button(self.seccion_navegacion, text="Servicios",bg=color_1,fg=color_5, font=("Arial", 15 ))
        self.boton_servicios.grid(row=0, column=1)
        self.boton_Reservas = tk.Button(self.seccion_navegacion, text="Reservas",bg=color_1,fg=color_5, font=("Arial", 15 ))
        self.boton_Reservas.grid(row=0, column=2)
    
    def mostrar(self):
        self.ventana.mainloop()

xd = Aplicacion()
xd.mostrar()