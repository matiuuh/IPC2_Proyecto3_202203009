from django.shortcuts import render
from django.http import HttpResponse

#este archivo "views" es donde definimos que queremos enviarle al cliente o navegador para que se vea en pantalla
#Prácicamente es para enviar archivos html

#request sirve para recibir información que el cliente me esté enviando
def esto_es_un_metodo(request):
    return HttpResponse("Hola mundo")

def ver_tienda(request):
    return render (request, 'Tienda_virtual.html')