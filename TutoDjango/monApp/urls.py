from django.urls import path
from . import views
from django.views.generic import  *


urlpatterns = [
    #path('home/<param>',views.home ,name='home'),
    #path('home/',views.home ,name='home'),
    path('home/<param>',views.HomeView.as_view()),
    path("home/", views.HomeView.as_view(), name="home"),

    path("contact/", views.ContactView, name="contact"),

    path("aboutUs/", views.AboutView.as_view()),

    path("produit/<pk>/" ,views.ProduitDetailView.as_view(), name="dtl_prdt"),
    path("produits/",views.ProduitListView.as_view(),name="lst_prdts"),
    path("produit/",views.ProduitCreateView.as_view(), name="crt_prdt"),
    path("produit/<pk>/update/",views.ProduitUpdateView.as_view(), name="prdt_chng"),
    path("produit/<pk>/delete/",views.ProduitDeleteView.as_view(), name="prdt_del"),


    path("categories/", views.CategorieListView.as_view(), name="lst_cats"),
    path("categorie/<pk>/" ,views.CategorieDetailView.as_view(), name="dtl_cats"),
    path("categorie/",views.CategorieCreateView.as_view(), name="crt_cats"),
    path("categorie/<pk>/update/",views.CategorieUpdateView.as_view(), name="cats_chng"),
    path("categorie/<pk>/delete/",views.CategorieDeleteView.as_view(), name="cats_del"),

    path("statuts/", views.StatusListView.as_view(), name="lst_statuts"),
    path("statut/<pk>/", views.StatutDetailView.as_view(), name="dtl_statut"),
    path("statut/",views.StatutCreateView.as_view(), name="crt_statut"),
    path("statut/<pk>/update/",views.StatutUpdateView.as_view(), name="statut_chng"),
    path("statut/<pk>/delete/",views.StatutDeleteView.as_view(), name="statut_del"),

    path('rayons/',views.RayonsListView.as_view() ,name='lst_rayons'),
    path('rayon/<pk>',views.RayonDetailView.as_view() ,name='dtl_rayon'),
    path("rayon/",views.RayonCreateView.as_view(), name="crt_rayon"),
    path("rayon/<pk>/update/",views.RayonUpdateView.as_view(), name="rayon_chng"),
    path("rayon/<pk>/delete/",views.RayonDeleteView.as_view(), name="rayon_del"),
    path("rayon/<pk>/cntnr/", views.ContenirCreateView.as_view(), name='cntnr_crt'),
    path("rayon/<pkR>/produit/<pkP>/update/", views.ContenirUpdateView.as_view(), name='cntnr_chng'),


    path('accueil/<param>',views.accueil ,name='accueil'),

    path('json/',views.ma_vue ,name='json'),

    path('login/', views.ConnectView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.DisconnectView.as_view(), name='logout'),

    path('email/',views.EmailSent.as_view() ,name='email-sent'),

    
]