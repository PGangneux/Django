from django.urls import path
from . import views
from django.views.generic import  *


urlpatterns = [
    #path('home/<param>',views.home ,name='home'),
    #path('home/',views.home ,name='home'),
    path('home/<param>',views.HomeView.as_view()),
    path("home/", views.HomeView.as_view()),
    path("contact/", views.Contact.as_view()),
    path("aboutUs/", views.AboutView.as_view()),
    path("produits/",views.ProduitListView.as_view()),
    path("produit/<pk>/",views.ProduitDetailView.as_view()),
    path("categories/", views.ListCategorie, name="categories"),
    path("statuts/", views.ListStatuts, name="statuts"),
    path('accueil/<param>',views.accueil ,name='accueil'),
    path('rayons/',views.ListRayons ,name='rayons'),
    path('json/',views.ma_vue ,name='json'),
]