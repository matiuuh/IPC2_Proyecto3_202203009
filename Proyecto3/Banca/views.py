from django.shortcuts import render

# Create your views here.
def ver_banca(request):
    return render (request, 'Banca.html')

def ver_tienda(request):
    return render(request, 'Tienda_virtual.html')