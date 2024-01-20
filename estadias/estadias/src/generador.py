from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from tkinter import Tk, Label, Button, Entry, filedialog
from PIL import Image
import os

class AplicacionPDF:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Generador de PDF")

        # Variables de entrada
        self.carpeta_imagenes = ""
        self.ruta_pdf = ""
        self.nombre_pdf = ""

        # Etiquetas
        self.etiqueta_carpeta = Label(ventana, text="Carpeta de Imágenes:")
        self.etiqueta_carpeta.grid(row=0, column=0, padx=10, pady=10)

        self.etiqueta_ruta_pdf = Label(ventana, text="Ruta para guardar el PDF:")
        self.etiqueta_ruta_pdf.grid(row=1, column=0, padx=10, pady=10)

        self.etiqueta_nombre_pdf = Label(ventana, text="Nombre del PDF:")
        self.etiqueta_nombre_pdf.grid(row=2, column=0, padx=10, pady=10)

        # Entradas de texto
        self.entrada_carpeta = Entry(ventana, width=40)
        self.entrada_carpeta.grid(row=0, column=1, padx=10, pady=10)

        self.entrada_ruta_pdf = Entry(ventana, width=40)
        self.entrada_ruta_pdf.grid(row=1, column=1, padx=10, pady=10)

        self.entrada_nombre_pdf = Entry(ventana, width=40)
        self.entrada_nombre_pdf.grid(row=2, column=1, padx=10, pady=10)

        # Botones
        self.boton_seleccionar_carpeta = Button(ventana, text="Seleccionar Carpeta", command=self.seleccionar_carpeta)
        self.boton_seleccionar_carpeta.grid(row=0, column=2, padx=10, pady=10)

        self.boton_seleccionar_ruta_pdf = Button(ventana, text="Seleccionar Ruta para PDF", command=self.seleccionar_ruta_pdf)
        self.boton_seleccionar_ruta_pdf.grid(row=1, column=2, padx=10, pady=10)

        self.boton_generar_pdf = Button(ventana, text="Generar PDF", command=self.generar_pdf)
        self.boton_generar_pdf.grid(row=3, column=1, pady=20)

    def seleccionar_carpeta(self):
        self.carpeta_imagenes = filedialog.askdirectory()
        self.entrada_carpeta.delete(0, 'end')
        self.entrada_carpeta.insert(0, self.carpeta_imagenes)

    def seleccionar_ruta_pdf(self):
        self.ruta_pdf = filedialog.askdirectory()
        self.entrada_ruta_pdf.delete(0, 'end')
        self.entrada_ruta_pdf.insert(0, self.ruta_pdf)

    def generar_pdf(self):
        if not self.carpeta_imagenes or not self.ruta_pdf:
            return  # No se ha seleccionado la carpeta o la ruta del PDF

        nombre_pdf = self.entrada_nombre_pdf.get()
        if not nombre_pdf:
            nombre_pdf = "documento_pdf"

        ruta_pdf = os.path.join(self.ruta_pdf, f"{nombre_pdf}.pdf")

        pdf = canvas.Canvas(ruta_pdf, pagesize=letter)

        for archivo_imagen in os.listdir(self.carpeta_imagenes):
            if archivo_imagen.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                ruta_imagen = os.path.join(self.carpeta_imagenes, archivo_imagen)
                try:
                    imagen = Image.open(ruta_imagen)
                    ancho, alto = imagen.size

                    # Ajustar proporcionalmente el tamaño de la imagen para que se ajuste en la página
                    proporcion = min(letter[0] / ancho, letter[1] / alto)
                    nuevo_ancho = int(ancho * proporcion)
                    nuevo_alto = int(alto * proporcion)

                    # Dibujar la imagen centrada en la página
                    x = (letter[0] - nuevo_ancho) / 2
                    y = (letter[1] - nuevo_alto) / 2

                    pdf.drawImage(ruta_imagen, x, y, width=nuevo_ancho, height=nuevo_alto)
                    pdf.showPage()
                except FileNotFoundError:
                    print(f"¡Advertencia! No se encontró la imagen en la ruta: {ruta_imagen}")

        pdf.save()
        print("PDF creado exitosamente.")

if __name__ == "__main__":
    root = Tk()
    app = AplicacionPDF(root)
    root.mainloop()
