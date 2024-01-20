# En conversion/views.py
from django.shortcuts import render, redirect
from .forms import ImagenForm

def cargar_imagen(request):
    if request.method == 'POST':
        form = ImagenForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Agregar lógica de conversión a PDF aquí
            return redirect('cargar_imagen')  # Redirige para cargar más imágenes
    else:
        form = ImagenForm()

    return render(request, 'cargar_imagen.html', {'form': form})

