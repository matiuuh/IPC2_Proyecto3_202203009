from django.shortcuts import render

# Create your views here.
# Tienda/views.py

from django.shortcuts import render
from .models import Cliente, Factura
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def Tavlas(request):
    # Tu lógica para la vista aquí.
    return render(request, 'Tavlas.html')

def Tienda1(request):
    return render(request, 'Tiendas.html')

@csrf_exempt  # Solo para propósitos de prueba, en producción maneja adecuadamente CSRF
def enviar_formulario(request):
    if request.method == 'POST':
        # Aquí procesarías los datos del formulario
        return HttpResponse("Formulario recibido")
    else:
        return HttpResponse("Método no permitido", status=405)