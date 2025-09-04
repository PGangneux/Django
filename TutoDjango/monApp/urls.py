from django.urls import path
from . import views

urlpatterns = [
    path('home/<param>',views.home ,name='home'),
    path('home/',views.home ,name='home'),
    path("contact/", views.contact, name="contact"),
    path("aboutUs/", views.aboutUs, name="aboutUs"),
]