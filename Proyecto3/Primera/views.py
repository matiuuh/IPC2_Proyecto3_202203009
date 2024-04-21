from django.shortcuts import render

# Create your views here.

#render sirve para enviar la página
def Principal (request):
    return render(request, 'Principal.html')

def Tablas (request):
    return render (request, 'Tablas.html')

