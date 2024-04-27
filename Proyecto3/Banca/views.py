from django.shortcuts import render
from django.http import JsonResponse
import requests # type: ignore
import xml.etree.ElementTree as ET
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import xml.etree.ElementTree as ET

# Create your views here.
def ver_banca(request):
    return render (request, 'Banca.html')

def ver_tienda(request):
    return render(request, 'Tienda_virtual.html')

# Puedes incluir todas las importaciones que necesites aquí.
@csrf_exempt
def grabar_configuracion(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({"message": "No se ha seleccionado un archivo."}, status=400)
        
        # Procesa el archivo XML como en el ejemplo de Flask...
        contenido_xml = file.read().decode('utf-8')
        root = ET.fromstring(contenido_xml)
        
        # Aquí se implementaría la lógica de procesamiento del archivo XML
        
        # ...

        # Finalmente, devolver la respuesta
        return JsonResponse({"message": "Archivo procesado correctamente"})

    return JsonResponse({"error": "Método no permitido"}, status=405)


def cargar_configuracion(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo_configuracion')
        if archivo:
            # Procesar el archivo XML aquí
            tree = ET.parse(archivo)
            root = tree.getroot()
            
            # Convertir el XML a una lista o lo que necesites
            # ...

            # Guardar en la base de datos o donde sea necesario
            # ...

            return JsonResponse({'status': 'success', 'message': 'Archivo procesado correctamente'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No se subió ningún archivo'})
    else:
        # Si no es un POST, solo muestra el formulario (o lo que necesites hacer)
        return render(request, 'ruta/al/formulario.html')

def cargar_transacciones(request):
    # Lógica para la carga de transacciones.
    pass

def resetear_datos(request):
    # Lógica para resetear datos.
    pass

def consultar_estado_de_cuenta(request):
    # Lógica para consultar el estado de cuenta.
    pass

def consultar_ingresos(request):
    # Lógica para consultar ingresos.
    pass
