from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request,'recipes/home.html', context = {
        'name':'Cláudio Rocha'
    })

def contato(request):
    return HttpResponse('CONTATO 1')

def sobre(request):
    return HttpResponse('SOBRE 1')
