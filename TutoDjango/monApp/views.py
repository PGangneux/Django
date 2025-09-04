from django.shortcuts import render
from django.http import HttpResponse


def home(request, param=None):
    if param:
        return HttpResponse(f"<h1>Hello Django!</h1><p>Bonjour {param}</p>")
    else:
        return HttpResponse("<h1>Hello Django!</h1>")

def contact(request):
    return HttpResponse("<h1>contact us</h1>")

def aboutUs(request):
    return HttpResponse("<h1>about us</h1>")