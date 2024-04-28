from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
import requests
import xml.etree.ElementTree as ET
from django.core.files.storage import default_storage
from django.shortcuts import redirect

# Create your views here.
def ver_banca(request):
    return render (request, 'Banca.html')

@csrf_exempt  # Desactivar CSRF si es necesario
def cargar_configuracion(request):
    if request.method == 'POST' and request.FILES.get('archivo_configuracion'):
        archivo = request.FILES['archivo_configuracion']

        # URL del endpoint de Flask que maneja la carga de configuración
        flask_url = 'http://127.0.0.1:8000/cargar-configuracion'

        try:
            # Preparar el archivo para enviar a Flask
            files = {'archivo_configuracion': (archivo.name, archivo, archivo.content_type)}

            # Enviar el archivo al servidor de Flask
            response = requests.post(flask_url, files=files)

            # Verificar la respuesta de Flask
            if response.status_code == 200:
                return HttpResponse("Archivo de configuración cargado y procesado correctamente.")
            else:
                return HttpResponse("Error al procesar el archivo de configuración.", status=500)
        except requests.exceptions.RequestException as error:
            return HttpResponse(f"Error al conectar con el servidor de Flask: {str(error)}", status=500)
    else:
        return render(request, 'Banca.html', {'error': 'Debe seleccionar un archivo válido.'})

@csrf_exempt  # Desactivar la protección CSRF si estás enviando el formulario a un dominio diferente (Flask)
def cargar_transacciones(request):
    if request.method == 'POST' and request.FILES.get('archivo_transacciones'):
        archivo = request.FILES['archivo_transacciones']

        # URL del endpoint de Flask que maneja la carga de transacciones
        flask_url = 'http://127.0.0.1:8000/cargar-transacciones'
        
        try:
            # Prepara el archivo para la solicitud
            files = {'archivo_transacciones': (archivo.name, archivo, archivo.content_type)}

            # Hacer una solicitud POST al backend de Flask
            response = requests.post(flask_url, files=files)

            # Verifica si la solicitud fue exitosa
            if response.status_code == 200:
                # Aquí puedes decidir qué hacer con la respuesta de Flask
                # Por ejemplo, podrías redireccionar o enviar un mensaje de éxito
                return HttpResponse("Archivo de transacciones cargado y procesado correctamente.")
            else:
                # Si hubo un problema, puedes enviar un mensaje de error
                return HttpResponse("Hubo un error al procesar el archivo de transacciones.", status=response.status_code)
        except requests.exceptions.RequestException as e:
            # Maneja excepciones que puedan ocurrir durante la solicitud a Flask
            return HttpResponse("Error al conectarse con el servicio de backend.", status=500)
    else:
        # Si no es un POST o no se ha subido archivo, puedes decidir qué hacer
        # Por ejemplo, mostrar el formulario de carga o enviar un mensaje de error
        return render(request, 'Banca.html', {'error': 'Debes subir un archivo.'})


@csrf_exempt
def resetear_datos(request):
    if request.method == 'POST':
        # URL del endpoint de Flask que maneja el reseteo de datos
        flask_reset_url = 'http://127.0.0.1:8000/reset'  # Cambia el puerto si es necesario
        
        # Hacer una solicitud POST al servidor de Flask para resetear los datos
        response = requests.post(flask_reset_url)
        
        # Puedes decidir qué hacer dependiendo de la respuesta del servidor de Flask
        if response.status_code == 200:
            return HttpResponse("Datos reseteados correctamente.")
        else:
            return HttpResponse("Hubo un problema al resetear los datos.", status=500)
    else:
        # Si no es una solicitud POST, quizás quieras devolver un error o una página diferente
        return HttpResponse("Método no permitido", status=405)

def consultar_estado_de_cuenta(request):
    nit_cliente = request.GET.get('nit_cliente')
    if nit_cliente:
        try:
            # URL del endpoint de Flask que retorna el estado de cuenta basado en el NIT
            flask_url = f'http://127.0.0.1:8000/estado-cuenta/{nit_cliente}'
            # Hacer la solicitud GET al servidor Flask
            response = requests.get(flask_url)

            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                # Convertir la respuesta a JSON y enviarla de vuelta al cliente
                estado_cuenta = response.json()
                return JsonResponse(estado_cuenta)
            else:
                # Manejar respuestas que no son exitosas
                return HttpResponse("No se pudo obtener el estado de cuenta.", status=response.status_code)
        except requests.exceptions.RequestException as e:
            # Manejar excepciones de la solicitud, como problemas de red
            return HttpResponse("Error al conectarse con el servicio de backend.", status=500)
    else:
        return HttpResponse("Debe proporcionar un NIT.", status=400)

def consultar_ingresos(request):
    mes = request.GET.get('mes')
    año = request.GET.get('año')
    
    if mes and año:
        try:
            # URL del endpoint de Flask que retorna los ingresos basado en el mes y el año
            flask_url = f'http://127.0.0.1:8000/ingresos?mes={mes}&año={año}'
            # Hacer la solicitud GET al servidor Flask
            response = requests.get(flask_url)

            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                # Convertir la respuesta a JSON y enviarla de vuelta al cliente
                ingresos = response.json()
                return JsonResponse(ingresos)
            else:
                # Manejar respuestas que no son exitosas
                return HttpResponse("No se pudo obtener los ingresos.", status=response.status_code)
        except requests.exceptions.RequestException as e:
            # Manejar excepciones de la solicitud, como problemas de red
            return HttpResponse("Error al conectarse con el servicio de backend.", status=500)
    else:
        return HttpResponse("Mes y año son requeridos.", status=400)
