# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from matplotlib.animation import FuncAnimation
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

class SimuladorPlanoInclinado:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de segunda ley de newton")
        self.root.geometry("1200x800")

        # variables fisicas
        self.angulo = 30.0  # grados
        self.masa = 1.0  # kg
        self.coef_friccion = 0.3
        self.fuerza_aplicada_magnitud = 0.0  # N
        self.fuerza_aplicada_angulo = 0.0  # grados respecto al plano
        self.g = 9.81  # m/s²

        # variables de la simulacion
        self.posicion_inicial_x = 0.0  # m - posicion inicial X
        self.posicion_inicial_y = 2.0  # m - posicion inicial Y (altura)
        self.posicion_x = 0.0  # m - posicion actual X
        self.posicion_y = 2.0  # m - posicion actual Y
        self.velocidad_x = 0.0  # m/s - velocidad en X
        self.velocidad_y = 0.0  # m/s - velocidad en Y
        self.aceleracion_x = 0.0  # m/s² - aceleracion en X
        self.aceleracion_y = 0.0  # m/s² - aceleracion en Y
        self.tiempo = 0.0  # s
        self.dt = 0.01  # paso de tiempo (mas pequeño para mejor precision)
        self.simulando = False

        # Estados del bloque
        self.estado = "aire"  # "aire", "plano", "suelo"

        # Configuracion del plano
        self.longitud_plano = 8.0  # m - longitud del plano inclinado

        # Datos para graficos
        self.tiempo_datos = []
        self.posicion_x_datos = []
        self.posicion_y_datos = []
        self.velocidad_x_datos = []
        self.velocidad_y_datos = []
        self.velocidad_total_datos = []
        self.energia_datos = []

        self.crear_interfaz()
        self.determinar_estado()
        self.calcular_fuerzas()

    #UI
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Panel de controles
        control_frame = ttk.LabelFrame(main_frame, text="Parametros de la Simulacion")
        control_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Configuracion del angulo
        ttk.Label(control_frame, text="angulo de la pendiente (°):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.angulo_var = tk.DoubleVar(value=self.angulo)
        angulo_scale = ttk.Scale(control_frame, from_=0, to=90, variable=self.angulo_var,
                                 command=self.actualizar_angulo, length=200)
        angulo_scale.grid(row=0, column=1, padx=5, pady=5)
        self.angulo_label = ttk.Label(control_frame, text=f"{self.angulo:.1f}°")
        self.angulo_label.grid(row=0, column=2, padx=5, pady=5)

        # Configuracion de la masa
        ttk.Label(control_frame, text="Masa del bloque (kg):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.masa_var = tk.DoubleVar(value=self.masa)
        masa_entry = ttk.Entry(control_frame, textvariable=self.masa_var, width=10)
        masa_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        masa_entry.bind('<KeyRelease>', self.actualizar_masa)

        # Configuracion del coeficiente de friccion
        ttk.Label(control_frame, text="Coeficiente de friccion:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.friccion_var = tk.DoubleVar(value=self.coef_friccion)
        friccion_scale = ttk.Scale(control_frame, from_=0, to=1, variable=self.friccion_var,
                                   command=self.actualizar_friccion, length=200)
        friccion_scale.grid(row=2, column=1, padx=5, pady=5)
        self.friccion_label = ttk.Label(control_frame, text=f"{self.coef_friccion:.2f}")
        self.friccion_label.grid(row=2, column=2, padx=5, pady=5)

        # Configuracion de fuerza aplicada
        ttk.Label(control_frame, text="Fuerza aplicada (N):").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.fuerza_mag_var = tk.DoubleVar(value=self.fuerza_aplicada_magnitud)
        fuerza_entry = ttk.Entry(control_frame, textvariable=self.fuerza_mag_var, width=10)
        fuerza_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        fuerza_entry.bind('<KeyRelease>', self.actualizar_fuerza)

        ttk.Label(control_frame, text="angulo de fuerza aplicada (°):").grid(row=4, column=0, sticky="w", padx=5,
                                                                             pady=5)
        self.fuerza_ang_var = tk.DoubleVar(value=self.fuerza_aplicada_angulo)
        fuerza_ang_scale = ttk.Scale(control_frame, from_=-90, to=90, variable=self.fuerza_ang_var,
                                     command=self.actualizar_angulo_fuerza, length=200)
        fuerza_ang_scale.grid(row=4, column=1, padx=5, pady=5)
        self.fuerza_ang_label = ttk.Label(control_frame, text=f"{self.fuerza_aplicada_angulo:.1f}°")
        self.fuerza_ang_label.grid(row=4, column=2, padx=5, pady=5)

        # Configuracion de posicion inicial
        ttk.Label(control_frame, text="Posicion inicial X (m):").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.pos_inicial_x_var = tk.DoubleVar(value=self.posicion_inicial_x)
        pos_inicial_x_entry = ttk.Entry(control_frame, textvariable=self.pos_inicial_x_var, width=10)
        pos_inicial_x_entry.grid(row=5, column=1, sticky="w", padx=5, pady=5)
        pos_inicial_x_entry.bind('<KeyRelease>', self.actualizar_posicion_inicial)

        ttk.Label(control_frame, text="Posicion inicial Y (m):").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.pos_inicial_y_var = tk.DoubleVar(value=self.posicion_inicial_y)
        pos_inicial_y_entry = ttk.Entry(control_frame, textvariable=self.pos_inicial_y_var, width=10)
        pos_inicial_y_entry.grid(row=6, column=1, sticky="w", padx=5, pady=5)
        pos_inicial_y_entry.bind('<KeyRelease>', self.actualizar_posicion_inicial)

        # Configuracion de longitud del plano
        ttk.Label(control_frame, text="Longitud del plano (m):").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.longitud_var = tk.DoubleVar(value=self.longitud_plano)
        longitud_entry = ttk.Entry(control_frame, textvariable=self.longitud_var, width=10)
        longitud_entry.grid(row=7, column=1, sticky="w", padx=5, pady=5)
        longitud_entry.bind('<KeyRelease>', self.actualizar_longitud_plano)

        # Botones de control
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=10)

        self.start_button = ttk.Button(button_frame, text="Iniciar simulacion", command=self.iniciar_simulacion)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Detener", command=self.detener_simulacion)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = ttk.Button(button_frame, text="Reiniciar", command=self.reiniciar_simulacion)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        # Panel de informacion
        info_frame = ttk.LabelFrame(control_frame, text="Estado Actual")
        info_frame.grid(row=9, column=0, columnspan=3, sticky="ew", pady=10)

        self.info_text = tk.Text(info_frame, height=30, width=40)
        self.info_text.pack(padx=5, pady=5)

        # Frame para graficos
        graph_frame = ttk.Frame(main_frame)
        graph_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Configurar el grafico
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Configurar grid weights
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # Inicializar graficos
        self.actualizar_graficos()

    #Logica
    def actualizar_angulo(self, value=None):
        self.angulo = float(value) if value else self.angulo_var.get()
        self.angulo_label.config(text=f"{self.angulo:.1f}°")
        self.determinar_estado()
        self.calcular_fuerzas()

    #Logica
    def actualizar_masa(self, event=None):
        try:
            self.masa = self.masa_var.get()
            self.calcular_fuerzas()
        except:
            pass

    #Logica
    def actualizar_friccion(self, value=None):
        self.coef_friccion = float(value) if value else self.friccion_var.get()
        self.friccion_label.config(text=f"{self.coef_friccion:.2f}")
        self.calcular_fuerzas()

    #Logica
    def actualizar_fuerza(self, event=None):
        try:
            self.fuerza_aplicada_magnitud = self.fuerza_mag_var.get()
            self.calcular_fuerzas()
        except:
            pass

    #Logica
    def actualizar_angulo_fuerza(self, value=None):
        self.fuerza_aplicada_angulo = float(value) if value else self.fuerza_ang_var.get()
        self.fuerza_ang_label.config(text=f"{self.fuerza_aplicada_angulo:.1f}°")
        self.calcular_fuerzas()

    #Logica
    def actualizar_posicion_inicial(self, event=None):
        try:
            nueva_pos_x = self.pos_inicial_x_var.get()
            nueva_pos_y = self.pos_inicial_y_var.get()

            if nueva_pos_y < 0:
                messagebox.showwarning("Advertencia", "La altura inicial debe ser mayor o igual a 0")
                self.pos_inicial_y_var.set(self.posicion_inicial_y)
                return

            self.posicion_inicial_x = nueva_pos_x
            self.posicion_inicial_y = nueva_pos_y

            # Si no esta simulando, tambien actualizar la posicion actual
            if not self.simulando:
                self.posicion_x = self.posicion_inicial_x
                self.posicion_y = self.posicion_inicial_y
                self.determinar_estado()
            self.calcular_fuerzas()
        except:
            pass

    #Logica
    def actualizar_longitud_plano(self, event=None):
        try:
            nueva_longitud = self.longitud_var.get()
            if nueva_longitud > 0:
                self.longitud_plano = nueva_longitud
                self.determinar_estado()
                self.calcular_fuerzas()
            else:
                messagebox.showwarning("Advertencia", "La longitud del plano debe ser mayor a 0")
                self.longitud_var.set(self.longitud_plano)
        except:
            pass

    #Logica
    def determinar_estado(self):
        # Estado del bloque
        # Calcular la altura del plano en la posicion X actual
        if self.posicion_x <= 0:
            altura_plano_en_x = 0
        elif self.posicion_x <= self.longitud_plano:
            altura_plano_en_x = self.posicion_x * math.tan(math.radians(self.angulo))
        else:
            altura_plano_en_x = 0  # Despues del plano, el suelo esta en y=0

        # Determinar estado con tolerancia
        tolerancia = 0.01
        if self.posicion_y > altura_plano_en_x + tolerancia:
            self.estado = "aire"
        elif (self.posicion_x >= 0 and self.posicion_x <= self.longitud_plano and
              abs(self.posicion_y - altura_plano_en_x) <= tolerancia):
            self.estado = "plano"
        elif abs(self.posicion_y) <= tolerancia and self.posicion_x >= 0:
            self.estado = "suelo"
        else:
            self.estado = "aire"

    #Logica
    ###Ejemplo de calculo
    def calcular_fuerzas(self):
        #Calcular fuerzas y aceleracion del bloque
        self.aceleracion_x = 0.0
        self.aceleracion_y = 0.0

        if self.estado == "aire":
            # Caida libre, solo gravedad
            self.aceleracion_x = 0.0
            self.aceleracion_y = -self.g

        elif self.estado == "plano":
            # Plano inclinado
            angulo_rad = math.radians(self.angulo)
            fuerza_ang_rad = math.radians(self.fuerza_aplicada_angulo)

            #peso
            peso_paralelo = self.masa * self.g * math.sin(angulo_rad)
            peso_perpendicular = self.masa * self.g * math.cos(angulo_rad)

            #fuerza aplicada en plano
            fuerza_paralelo = self.fuerza_aplicada_magnitud * math.cos(fuerza_ang_rad)
            fuerza_perpendicular = self.fuerza_aplicada_magnitud * math.sin(fuerza_ang_rad)

            #Fuerza normal
            normal = peso_perpendicular + fuerza_perpendicular

            #friccion
            friccion_maxima = self.coef_friccion * abs(normal)
            fuerza_neta_sin_friccion = fuerza_paralelo - peso_paralelo

            # Determinar friccion real
            if abs(fuerza_neta_sin_friccion) <= friccion_maxima and abs(self.velocidad_x) < 0.01:
                aceleracion_paralela = 0.0
            else:
                if fuerza_neta_sin_friccion > 0:
                    friccion_real = -friccion_maxima
                else:
                    friccion_real = friccion_maxima

                fuerza_neta = fuerza_neta_sin_friccion + friccion_real
                aceleracion_paralela = fuerza_neta / self.masa

            # Convertir acelaracion paralela a componentes X,Y globales
            self.aceleracion_x = aceleracion_paralela * math.cos(angulo_rad)
            self.aceleracion_y = aceleracion_paralela * math.sin(angulo_rad)

        elif self.estado == "suelo":
            fuerza_ang_rad = math.radians(self.fuerza_aplicada_angulo)

            peso_perpendicular = self.masa * self.g
            fuerza_horizontal = self.fuerza_aplicada_magnitud * math.cos(fuerza_ang_rad)
            fuerza_vertical = self.fuerza_aplicada_magnitud * math.sin(fuerza_ang_rad)

            normal = peso_perpendicular + fuerza_vertical
            friccion_maxima = self.coef_friccion * abs(normal)

            velocidad_horizontal = abs(self.velocidad_x)
            if abs(fuerza_horizontal) <= friccion_maxima and velocidad_horizontal < 0.01:
                self.aceleracion_x = 0.0
            else:
                if (fuerza_horizontal > 0 or self.velocidad_x > 0):
                    friccion_real = -friccion_maxima if self.velocidad_x > 0 else friccion_maxima
                else:
                    friccion_real = friccion_maxima if self.velocidad_x < 0 else -friccion_maxima

                fuerza_neta_x = fuerza_horizontal + friccion_real
                self.aceleracion_x = fuerza_neta_x / self.masa

            self.aceleracion_y = 0.0  # Sin aceleracion vertical en suelo

        # Actualizar informacion
        self.actualizar_info()

    #UI
    def actualizar_info(self):
        """Actualiza el panel de informacion"""
        energia_cinetica = 0.5 * self.masa * (self.velocidad_x ** 2 + self.velocidad_y ** 2)
        energia_potencial = self.masa * self.g * self.posicion_y
        energia_total = energia_cinetica + energia_potencial
        velocidad_total = math.sqrt(self.velocidad_x ** 2 + self.velocidad_y ** 2)

        info = f"""ESTADO DEL BLOQUE:
        Estado actual: {self.estado.upper()}
        
        POSICION:
        X: {self.posicion_x:.2f} m
        Y: {self.posicion_y:.2f} m
        
        VELOCIDAD:
        Vx: {self.velocidad_x:.2f} m/s
        Vy: {self.velocidad_y:.2f} m/s
        V total: {velocidad_total:.2f} m/s
        
        ACELERACION:
        Ax: {self.aceleracion_x:.2f} m/s²
        Ay: {self.aceleracion_y:.2f} m/s²
        
        ENERGIA:
        Cinetica: {energia_cinetica:.2f} J
        Potencial: {energia_potencial:.2f} J
        Total: {energia_total:.2f} J
        
        CONFIGURACION:
        Masa: {self.masa:.1f} kg
        Friccion: {self.coef_friccion:.2f}
        Tiempo: {self.tiempo:.2f} s
                """

        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)

    #UI
    def iniciar_simulacion(self):
        #Start
        if not self.simulando:
            self.simulando = True
            self.start_button.config(state="disabled")
            self.animar()

    #UI
    def detener_simulacion(self):
        #Stop
        self.simulando = False
        self.start_button.config(state="normal")

    #UI
    def reiniciar_simulacion(self):
        #Reset
        self.detener_simulacion()
        self.posicion_x = self.posicion_inicial_x
        self.posicion_y = self.posicion_inicial_y
        self.velocidad_x = 0.0
        self.velocidad_y = 0.0
        self.tiempo = 0.0
        self.tiempo_datos = []
        self.posicion_x_datos = []
        self.posicion_y_datos = []
        self.velocidad_x_datos = []
        self.velocidad_y_datos = []
        self.velocidad_total_datos = []
        self.energia_datos = []
        self.determinar_estado()
        self.calcular_fuerzas()
        self.actualizar_graficos()

    #UI
    def paso_simulacion(self):
        if self.simulando:
            self.calcular_fuerzas()

            nueva_velocidad_x = self.velocidad_x + self.aceleracion_x * self.dt
            nueva_velocidad_y = self.velocidad_y + self.aceleracion_y * self.dt

            nueva_posicion_x = self.posicion_x + nueva_velocidad_x * self.dt
            nueva_posicion_y = self.posicion_y + nueva_velocidad_y * self.dt

            self.verificar_colisiones(nueva_posicion_x, nueva_posicion_y, nueva_velocidad_x, nueva_velocidad_y)

            # coreccion para que no penetre el suelo
            if self.estado == "suelo" and self.posicion_y < 0:
                self.posicion_y = 0
                self.velocidad_y = 0

            self.tiempo += self.dt

            # Guardar datos para graficos
            self.tiempo_datos.append(self.tiempo)
            self.posicion_x_datos.append(self.posicion_x)
            self.posicion_y_datos.append(self.posicion_y)
            self.velocidad_x_datos.append(self.velocidad_x)
            self.velocidad_y_datos.append(self.velocidad_y)
            velocidad_total = math.sqrt(self.velocidad_x ** 2 + self.velocidad_y ** 2)
            if velocidad_total < -0.02:  # umbral pequeño para considerar "sin movimiento"
                self.tiempo_sin_movimiento += self.dt
            else:
                self.tiempo_sin_movimiento = 0.0

            if self.tiempo_sin_movimiento >= 5.0:  # 5 segundos sin movimiento
                self.detener_simulacion()
                print("Simulacion detenida por inactividad.")

            self.velocidad_total_datos.append(velocidad_total)
            energia_total = 0.5 * self.masa * (
                        self.velocidad_x ** 2 + self.velocidad_y ** 2) + self.masa * self.g * self.posicion_y
            self.energia_datos.append(energia_total)

            # Limitar datos para evitar memoria excesiva
            if len(self.tiempo_datos) > 2000:
                self.tiempo_datos.pop(0)
                self.posicion_x_datos.pop(0)
                self.posicion_y_datos.pop(0)
                self.velocidad_x_datos.pop(0)
                self.velocidad_y_datos.pop(0)
                self.velocidad_total_datos.pop(0)
                self.energia_datos.pop(0)

    #Logica
    def verificar_colisiones(self, nueva_x, nueva_y, nueva_vx, nueva_vy):
        # Calcular altura del plano en la nueva posicion X
        if nueva_x <= 0:
            altura_plano = 0
        elif nueva_x <= self.longitud_plano:
            altura_plano = nueva_x * math.tan(math.radians(self.angulo))
        else:
            altura_plano = 0

        # Verificar colision con el suelo
        if nueva_y <= 0:
            self.posicion_x = nueva_x
            self.posicion_y = 0  # Mantenerse en suelo
            self.velocidad_x = nueva_vx  # Conservar velocidad horizontal
            self.velocidad_y = 0  # Anular velocidad vertical
            self.estado = "suelo"
            return

        # Verificar colision con el plano inclinado (sin cambios)
        if (nueva_x >= 0 and nueva_x <= self.longitud_plano and
                nueva_y <= altura_plano and self.posicion_y > altura_plano):
            angulo_rad = math.radians(self.angulo)

            # Componente de velocidad paralela al plano
            vel_paralela = (nueva_vx * math.cos(angulo_rad) + nueva_vy * math.sin(angulo_rad))

            # Componente perpendicular se anula en la colision
            self.velocidad_x = vel_paralela * math.cos(angulo_rad)
            self.velocidad_y = vel_paralela * math.sin(angulo_rad)

            self.posicion_x = nueva_x
            self.posicion_y = altura_plano
            self.estado = "plano"
            return

        # Sin colision - actualizar normalmente
        self.posicion_x = nueva_x
        self.posicion_y = nueva_y
        self.velocidad_x = nueva_vx
        self.velocidad_y = nueva_vy

        self.determinar_estado()

    #UI
    def actualizar_graficos(self):
        # Limpiar graficos
        self.ax1.clear()
        self.ax2.clear()

        # Grafico del plano inclinado
        margen_vista = 4
        max_x = max(self.longitud_plano + margen_vista, self.posicion_x + margen_vista)
        max_y = max(self.longitud_plano * math.tan(math.radians(self.angulo)) + margen_vista, self.posicion_y + margen_vista)

        self.ax1.set_xlim(self.posicion_x - margen_vista, self.posicion_x + margen_vista)
        self.ax1.set_ylim(self.posicion_y - margen_vista, self.posicion_y + margen_vista)
        self.ax1.set_aspect('equal')

        # Dibujar suelo
        x_suelo = [-margen_vista, max_x]
        y_suelo = [0, 0]
        self.ax1.axhline(y=0, color='k', linewidth=3, label='Superficie horizontal (suelo)')

        # Dibujar plano inclinado
        x_plano = [0, self.longitud_plano]
        y_plano = [0, self.longitud_plano * math.tan(math.radians(self.angulo))]
        self.ax1.plot(x_plano, y_plano, 'k-', linewidth=3, label='Plano inclinado')

        # Dibujar bloque
        color_bloque = {'aire': 'red', 'plano': 'blue', 'suelo': 'green'}
        self.ax1.plot(self.posicion_x, self.posicion_y, 's', color=color_bloque[self.estado],
                      markersize=15, label=f'Bloque ({self.estado})')

        # Dibujar vectores de velocidad
        if len(self.tiempo_datos) > 0:
            velocidad_total = math.sqrt(self.velocidad_x ** 2 + self.velocidad_y ** 2)
            if velocidad_total > 0.1:
                escala = 0.5
                vx_display = self.velocidad_x * escala
                vy_display = self.velocidad_y * escala
                self.ax1.arrow(self.posicion_x, self.posicion_y, vx_display, vy_display,
                               head_width=0.2, head_length=0.2, fc='purple', ec='purple',
                               label=f'Velocidad ({velocidad_total:.1f} m/s)')

        # Dibujar trayectoria
        if len(self.posicion_x_datos) > 1:
            self.ax1.plot(self.posicion_x_datos, self.posicion_y_datos, 'r--', alpha=0.5, label='Trayectoria')

        self.ax1.set_xlabel('Posicion X (m)')
        self.ax1.set_ylabel('Posicion Y (m)')
        self.ax1.set_title('Simulacion del Plano Inclinado')
        self.ax1.legend()
        self.ax1.grid(True, alpha=0.3)

        # Grafico de variables vs tiempo
        if len(self.tiempo_datos) > 1:
            self.ax2.plot(self.tiempo_datos, self.velocidad_total_datos, 'r-', label='Velocidad total (m/s)')
            self.ax2.plot(self.tiempo_datos, self.energia_datos, 'g-', label='Energia total (J)')

            # Agregar lineas verticales para cambios de estado
            estado_anterior = None
            for i, t in enumerate(self.tiempo_datos):
                if i < len(self.posicion_x_datos):
                    x_pos = self.posicion_x_datos[i]
                    y_pos = self.posicion_y_datos[i]

                    # determinar estado del bloque
                    if y_pos > 0.1:
                        estado_actual = "aire"
                    elif x_pos <= self.longitud_plano and abs(
                            y_pos - x_pos * math.tan(math.radians(self.angulo))) < 0.1:
                        estado_actual = "plano"
                    else:
                        estado_actual = "suelo"

                    if estado_anterior is not None and estado_actual != estado_anterior:
                        self.ax2.axvline(x=t, color='gray', linestyle='--', alpha=0.7)

                    estado_anterior = estado_actual

        self.ax2.set_xlabel('Tiempo (s)')
        self.ax2.set_ylabel('Magnitud')
        self.ax2.set_title('Velocidad total y energia vs tiempo')
        self.ax2.grid(True, alpha=0.3)

        self.canvas.draw()

    #UI
    def animar(self):
        if self.simulando:
            self.paso_simulacion()
            self.actualizar_graficos()

            # detener movimiento si esta en suelo
            velocidad_total = math.sqrt(self.velocidad_x ** 2 + self.velocidad_y ** 2)
            if (self.estado == "suelo" and velocidad_total < 0.01 and
                    abs(self.aceleracion_x) < 0.01):
                self.detener_simulacion()
                return

            self.root.after(40, self.animar)  # 50 FPS


def main():
    root = tk.Tk()
    app = SimuladorPlanoInclinado(root)
    root.mainloop()


if __name__ == "__main__":
    main()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
