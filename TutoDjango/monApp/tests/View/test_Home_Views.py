from django.shortcuts import render
from django.test import Client, TestCase
from django.urls import reverse

class HomeViewTests(TestCase):

    def test_get_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_home.html')
    
    def test_get_home_parametres(self):
        response = self.client.get("/monApp/home/1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/page_home.html')



    

    
