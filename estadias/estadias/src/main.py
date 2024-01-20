from tkinter import Tk, Button, Label, filedialog
import os
import subprocess
import sys

class InterfazInicio:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Interfaz de Inicio")

        # Etiqueta
        self.etiqueta = Label(ventana, text="Seleccione una acción:")
        self.etiqueta.pack(pady=10)

        # Botón para editar imagenes
        self.boton_generar_pdf = Button(ventana, text="Procesar Imagenes", command=self.abrir_editor)
        self.boton_generar_pdf.pack(pady=10)

        # Botón para generar PDF
        self.boton_generar_pdf = Button(ventana, text="Generar PDF", command=self.abrir_generador_pdf)
        self.boton_generar_pdf.pack(pady=10)

    def abrir_generador_pdf(self):
        # Cambia a la carpeta del script actual antes de lanzar generador.py
        os.chdir(os.path.dirname(__file__))

        # Utiliza sys.executable para obtener el ejecutable del intérprete actual
        ruta_generador = os.path.join(os.path.dirname(__file__), "generador.py")
        subprocess.Popen([sys.executable, ruta_generador])

    def abrir_editor(self):
        # Cambia a la carpeta del script actual antes de lanzar generador.py
        os.chdir(os.path.dirname(__file__))

        # Utiliza sys.executable para obtener el ejecutable del intérprete actual
        ruta_editor = os.path.join(os.path.dirname(__file__), "editar.py")
        subprocess.Popen([sys.executable, ruta_editor])

if __name__ == "__main__":
    root = Tk()
    app = InterfazInicio(root)
    root.mainloop()
