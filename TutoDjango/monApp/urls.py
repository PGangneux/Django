from django.urls import path
from . import views

urlpatterns = [
    #path('home/<param>',views.home ,name='home'),
    path('home/',views.home ,name='home'),
    path("contact/", views.contact, name="contact"),
    path("aboutUs/", views.aboutUs, name="aboutUs"),
    path("produits/", views.ListProduits, name="produits"),
    path("categories/", views.ListCategorie, name="categories"),
    path("statuts/", views.ListStatuts, name="statuts"),
    path('accueil/<param>',views.accueil ,name='accueil'),
    path('rayons/',views.ListRayons ,name='rayons'),
    path('json/',views.ma_vue ,name='json'),
]