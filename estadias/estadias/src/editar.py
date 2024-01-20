import os
from tkinter import Tk, Label, Button, Frame, filedialog, Scale
from PIL import Image, ImageTk, ImageEnhance

class EditorImagenes:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Editor de Imágenes")
        self.ventana.attributes("-fullscreen", True)

        self.factor_brillo = 1.0
        self.factor_contraste = 1.0
        self.corte_vertical = 0
        self.corte_horizontal = 0

        self.carpeta_imagenes = ""
        self.carpeta_guardado = ""
        self.lista_imagenes = []
        self.indice_imagen_actual = 0

        self.inicializar_interfaz()

    def inicializar_interfaz(self):
        # Panel izquierdo para la imagen original
        self.panel_izquierdo = Frame(self.ventana, width=self.ventana.winfo_screenwidth() // 3, height=self.ventana.winfo_screenheight())
        self.panel_izquierdo.pack(side="left", fill="both", expand=True)

        # Etiqueta para mostrar la imagen original
        self.etiqueta_imagen_original = Label(self.panel_izquierdo)
        self.etiqueta_imagen_original.pack(pady=20)

        # Panel central para controles de edición
        self.panel_central = Frame(self.ventana, width=self.ventana.winfo_screenwidth() // 3, height=self.ventana.winfo_screenheight())
        self.panel_central.pack(side="left", fill="both", expand=True)

        # Botón para seleccionar carpeta de imágenes
        boton_seleccionar_carpeta = Button(self.panel_central, text="Seleccionar Carpeta", command=self.seleccionar_carpeta)
        boton_seleccionar_carpeta.pack(pady=10)

        # Sliders para brillo, contraste, corte vertical y corte horizontal
        self.slider_brillo = Scale(self.panel_central, label="Brillo", from_=0, to=2, resolution=0.1, orient="horizontal", command=self.actualizar_edicion)
        self.slider_brillo.set(1.0)
        self.slider_brillo.pack(pady=10)

        self.slider_contraste = Scale(self.panel_central, label="Contraste", from_=0, to=2, resolution=0.1, orient="horizontal", command=self.actualizar_edicion)
        self.slider_contraste.set(1.0)
        self.slider_contraste.pack(pady=10)

        self.slider_corte_vertical = Scale(self.panel_central, label="Corte Vertical", from_=0, to=100, orient="horizontal", command=self.actualizar_edicion)
        self.slider_corte_vertical.pack(pady=10)

        self.slider_corte_horizontal = Scale(self.panel_central, label="Corte Horizontal", from_=0, to=100, orient="horizontal", command=self.actualizar_edicion)
        self.slider_corte_horizontal.pack(pady=10)

        # Botones para rotar la imagen
        boton_rotar_izquierda = Button(self.panel_central, text="Rotar 90° Izquierda", command=self.rotar_izquierda)
        boton_rotar_izquierda.pack(pady=10)

        boton_rotar_derecha = Button(self.panel_central, text="Rotar 90° Derecha", command=self.rotar_derecha)
        boton_rotar_derecha.pack(pady=10)

        # Botón para seleccionar carpeta de guardado
        boton_seleccionar_carpeta_guardado = Button(self.panel_central, text="Seleccionar Carpeta de Guardado", command=self.seleccionar_carpeta_guardado)
        boton_seleccionar_carpeta_guardado.pack(pady=10)

        # Panel derecho para la imagen editada
        self.panel_derecho = Frame(self.ventana, width=self.ventana.winfo_screenwidth() // 3, height=self.ventana.winfo_screenheight())
        self.panel_derecho.pack(side="right", fill="both", expand=True)

        # Etiqueta para mostrar la imagen editada
        self.etiqueta_imagen_editada = Label(self.panel_derecho)
        self.etiqueta_imagen_editada.pack(pady=20)

        # Botón para guardar los cambios
        boton_guardar = Button(self.panel_central, text="Guardar", command=self.guardar_cambios)
        boton_guardar.pack(pady=10)

    def seleccionar_carpeta(self):
        self.carpeta_imagenes = filedialog.askdirectory()
        self.lista_imagenes = [imagen for imagen in os.listdir(self.carpeta_imagenes) if imagen.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        self.indice_imagen_actual = 0
        self.mostrar_imagen()

    def seleccionar_carpeta_guardado(self):
        self.carpeta_guardado = filedialog.askdirectory()

    def rotar_izquierda(self):
        self.lista_imagenes[self.indice_imagen_actual] = self.lista_imagenes[self.indice_imagen_actual].rotate(90 * -1)
        self.mostrar_imagen()

    def rotar_derecha(self):
        self.lista_imagenes[self.indice_imagen_actual] = self.lista_imagenes[self.indice_imagen_actual].rotate(90)
        self.mostrar_imagen()

    def actualizar_edicion(self, *args):
        self.factor_brillo = float(self.slider_brillo.get())
        self.factor_contraste = float(self.slider_contraste.get())
        self.corte_vertical = int(self.slider_corte_vertical.get())
        self.corte_horizontal = int(self.slider_corte_horizontal.get())
        self.mostrar_imagen()

    def mostrar_imagen(self):
        if not self.carpeta_imagenes or not self.lista_imagenes:
            return

        ruta_imagen_actual = os.path.join(self.carpeta_imagenes, self.lista_imagenes[self.indice_imagen_actual])
        imagen_original = Image.open(ruta_imagen_actual)

        # Aplicar ajustes a la imagen original
        imagen_editada = imagen_original.copy()
        imagen_editada = ImageEnhance.Brightness(imagen_editada).enhance(self.factor_brillo)
        imagen_editada = ImageEnhance.Contrast(imagen_editada).enhance(self.factor_contraste)

        ancho_editado, alto_editado = imagen_editada.size
        corte_izquierda = int(ancho_editado * self.corte_horizontal / 100)
        corte_arriba = int(alto_editado * self.corte_vertical / 100)
        corte_derecha = ancho_editado - corte_izquierda
        corte_abajo = alto_editado - corte_arriba
        imagen_editada = imagen_editada.crop((corte_izquierda, corte_arriba, corte_derecha, corte_abajo))

        # Muestra la imagen original
        imagen_original.thumbnail((self.panel_izquierdo.winfo_width(), self.panel_izquierdo.winfo_height()))
        imagen_original_tk = ImageTk.PhotoImage(imagen_original)
        self.etiqueta_imagen_original.config(image=imagen_original_tk)
        self.etiqueta_imagen_original.image = imagen_original_tk

        # Muestra la imagen editada
        imagen_editada.thumbnail((self.panel_derecho.winfo_width(), self.panel_derecho.winfo_height()))
        imagen_editada_tk = ImageTk.PhotoImage(imagen_editada)
        self.etiqueta_imagen_editada.config(image=imagen_editada_tk)
        self.etiqueta_imagen_editada.image = imagen_editada_tk

    def guardar_cambios(self):
        if not self.carpeta_guardado:
            return

        for nombre_imagen in self.lista_imagenes:
            ruta_imagen_original = os.path.join(self.carpeta_imagenes, nombre_imagen)
            ruta_imagen_destino = os.path.join(self.carpeta_guardado, nombre_imagen)

            imagen_original = Image.open(ruta_imagen_original)

            # Aplicar ajustes a la imagen original
            imagen_editada = imagen_original.copy()
            imagen_editada = ImageEnhance.Brightness(imagen_editada).enhance(self.factor_brillo)
            imagen_editada = ImageEnhance.Contrast(imagen_editada).enhance(self.factor_contraste)

            ancho_editado, alto_editado = imagen_editada.size
            corte_izquierda = int(ancho_editado * self.corte_horizontal / 100)
            corte_arriba = int(alto_editado * self.corte_vertical / 100)
            corte_derecha = ancho_editado - corte_izquierda
            corte_abajo = alto_editado - corte_arriba
            imagen_editada = imagen_editada.crop((corte_izquierda, corte_arriba, corte_derecha, corte_abajo))

            # Guardar imagen editada en la carpeta de destino
            imagen_editada.save(ruta_imagen_destino)

if __name__ == "__main__":
    ventana_principal = Tk()
    editor = EditorImagenes(ventana_principal)
    ventana_principal.mainloop()
