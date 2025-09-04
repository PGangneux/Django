from django.shortcuts import render
from django.http import HttpResponse

from monApp.models import Produit


def home(request, param=None):
    if param:
        return HttpResponse(f"<h1>Hello Django!</h1><p>Bonjour {param}</p>")
    else:
        return HttpResponse("<h1>Hello Django!</h1>")

def contact(request):
    return HttpResponse("<h1>contact us</h1>")

def aboutUs(request):
    return HttpResponse("<h1>about us</h1>")


def ListProduits(request):
    prdts = Produit.objects.all()
    html = "<ul> "
    for prod in prdts:
        html += "<li>" +  prod.intituleProd + "</li>"
    html += "</ul>"
    return HttpResponse(html)