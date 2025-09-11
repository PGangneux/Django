from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseNotFound, JsonResponse

from monApp.models import *


def home(request):
    if request.GET and request.GET["test"]:
        raise Http404
    return HttpResponse("Bonjour Monde!")

def contact(request):
    return render(request, 'monApp/contact.html')

def aboutUs(request):
    return render(request, 'monApp/about_us.html')


def ListProduits(request):
    prdts = Produit.objects.all()
    return render(request, 'monApp/list_produits.html',{'prdts': prdts})

def ListCategorie(request):
    categories = Categorie.objects.all()
    return render(request, 'monApp/list_categories.html',{'categories': categories})

def ListStatuts(request):
    statuts = Statut.objects.all()
    return render(request, 'monApp/list_statuts.html',{'statuts': statuts})

def ListRayons(request):
    rayons = Rayon.objects.all()
    return render(request, 'monApp/list_rayons.html',{'rayons': rayons})

def accueil(request,param):
    return HttpResponse("<h1>Hello " + param + " ! You're connected</h1>")

def ma_vue(request):
    return JsonResponse({'foo': 'bar'})