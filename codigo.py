
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import tkinter as tk
from tkinter import ttk, filedialog
import json

class Superficie3D:
    def __init__(self, x_range, y_range):
        self.x_range = x_range
        self.y_range = y_range
        self.x, self.y = np.meshgrid(np.linspace(x_range[0], x_range[1], 100), np.linspace(y_range[0], y_range[1], 100))

    def calcular_z(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")

    def generar_datos(self):
        self.z = self.calcular_z()
        return self.x, self.y, self.z

class Plano(Superficie3D):
    def __init__(self, x_range, y_range, pendiente):
        super().__init__(x_range, y_range)
        self.pendiente = pendiente

    def calcular_z(self):
        return self.pendiente * self.x

class Paraboloide(Superficie3D):
    def __init__(self, x_range, y_range, coef):
        super().__init__(x_range, y_range)
        self.coef = coef

    def calcular_z(self):
        return self.coef * (self.x**2 + self.y**2)

class Sinusoide(Superficie3D):
    def __init__(self, x_range, y_range, frecuencia):
        super().__init__(x_range, y_range)
        self.frecuencia = frecuencia

    def calcular_z(self):
        return np.sin(self.frecuencia * np.sqrt(self.x**2 + self.y**2))

class Hiperboloide(Superficie3D):
    def __init__(self, x_range, y_range, coef):
        super().__init__(x_range, y_range)
        self.coef = coef

    def calcular_z(self):
        return self.coef * (self.x**2 - self.y**2)

class Conica(Superficie3D):
    def __init__(self, x_range, y_range, a, b, c):
        super().__init__(x_range, y_range)
        self.a = a
        self.b = b
        self.c = c

    def calcular_z(self):
        return self.a * self.x**2 + self.b * self.y**2 + self.c

class Visualizador3D:
    def __init__(self, superficie):
        self.superficie = superficie

    def mostrar_con_matplotlib(self):
        x, y, z = self.superficie.generar_datos()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(x, y, z, cmap='viridis')
        plt.show()

class Visualizador3DPlotly(Visualizador3D):
    def mostrar_con_plotly(self):
        x, y, z = self.superficie.generar_datos()
        fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
        fig.update_layout(title='Superficie 3D', autosize=False, width=800, height=800)
        fig.show()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualizador de Superficies 3D")
        self.geometry("400x400")

        self.style = ttk.Style(self)
        self.style.theme_use('clam')  # Puedes probar otros temas como 'default', 'classic', 'alt', etc.
        
        # Personalizar los estilos de los widgets
        self.style.configure('TLabel', background='#333333', foreground='#ffffff')
        self.style.configure('TEntry', fieldbackground='#555555', foreground='#ffffff')
        self.style.configure('TCombobox', fieldbackground='#555555', foreground='#ffffff')
        self.style.configure('TButton', background='#444444', foreground='#ffffff')

        self.configure(background='#333333')  # Fondo de la ventana principal

        self.tipo_var = tk.StringVar()
        self.param1_var = tk.StringVar()
        self.param2_var = tk.StringVar()
        self.param3_var = tk.StringVar()

        self.crear_widgets()

    def crear_widgets(self):
        ttk.Label(self, text="Seleccione el tipo de superficie:").pack(pady=10)

        tipos = ["Plano", "Paraboloide", "Sinusoide", "Hiperboloide", "Cónica"]
        self.tipo_menu = ttk.Combobox(self, textvariable=self.tipo_var, values=tipos)
        self.tipo_menu.pack(pady=5)

        ttk.Label(self, text="Parámetro 1:").pack(pady=5)
        self.param1_entry = ttk.Entry(self, textvariable=self.param1_var)
        self.param1_entry.pack(pady=5)

        ttk.Label(self, text="Parámetro 2 (opcional):").pack(pady=5)
        self.param2_entry = ttk.Entry(self, textvariable=self.param2_var)
        self.param2_entry.pack(pady=5)

        ttk.Label(self, text="Parámetro 3 (opcional):").pack(pady=5)
        self.param3_entry = ttk.Entry(self, textvariable=self.param3_var)
        self.param3_entry.pack(pady=5)

        ttk.Button(self, text="Visualizar", command=self.visualizar).pack(pady=20)
        ttk.Button(self, text="Guardar Configuración", command=self.guardar_config).pack(pady=5)
        ttk.Button(self, text="Cargar Configuración", command=self.cargar_config).pack(pady=5)

    def visualizar(self):
        tipo = self.tipo_var.get()
        param1 = float(self.param1_var.get())
        param2 = self.param2_var.get()
        param3 = self.param3_var.get()

        if tipo == "Plano":
            superficie = Plano((-5, 5), (-5, 5), param1)
        elif tipo == "Paraboloide":
            superficie = Paraboloide((-5, 5), (-5, 5), param1)
        elif tipo == "Sinusoide":
            superficie = Sinusoide((-5, 5), (-5, 5), param1)
        elif tipo == "Hiperboloide":
            superficie = Hiperboloide((-5, 5), (-5, 5), param1)
        elif tipo == "Cónica":
            a = param1
            b = float(param2) if param2 else 0
            c = float(param3) if param3 else 0
            superficie = Conica((-5, 5), (-5, 5), a, b, c)
        else:
            print("Opción no válida.")
            return

        visualizador = Visualizador3DPlotly(superficie)
        visualizador.mostrar_con_plotly()

    def guardar_config(self):
        config = {
            'tipo': self.tipo_var.get(),
            'param1': self.param1_var.get(),
            'param2': self.param2_var.get(),
            'param3': self.param3_var.get()
        }

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'w') as file:
                json.dump(config, file)
            print("Configuración guardada en:", file_path)

    def cargar_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as file:
                config = json.load(file)

            self.tipo_var.set(config['tipo'])
            self.param1_var.set(config['param1'])
            self.param2_var.set(config['param2'])
            self.param3_var.set(config['param3'])
            print("Configuración cargada desde:", file_path)

if __name__ == "__main__":
    app = App()
    app.mainloop()
