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
    path("produit/<pk>/" ,views.ProduitDetailView.as_view(), name="dtl_prdt"),
    path("produits/",views.ProduitListView.as_view(),name="lst_prdts"),
    path("categories/", views.CategorieListView.as_view(), name="lst_cats"),
    path("categorie/<pk>/" ,views.CategorieDetailView.as_view(), name="dtl_cats"),
    path("statuts/", views.StatusListView.as_view(), name="lst_statuts"),
    path('rayons/',views.RayonsListView.as_view() ,name='lst_rayons'),
    path('rayon/<pk>',views.RayonDetailView.as_view() ,name='dtl_rayons'),
    path('accueil/<param>',views.accueil ,name='accueil'),

    path('json/',views.ma_vue ,name='json'),
]