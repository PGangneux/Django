
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from monApp.models import Rayon


class RayonCreateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.ctgr = Rayon.objects.create(nomRayon="rayonPourTestDetail")

    def test_Rayon_create_view_get(self):
        response = self.client.get(reverse('crt_rayon')) # Utilisation du nom de l'URL
        self.assertEqual(response.status_code, 200)
        # Tester que la vue de création renvoie le bon template
        self.assertTemplateUsed(response, 'monApp/create_rayon.html')
        
    def test_Rayon_create_view_post_valid(self):
        data = { "nomRayon": "rayonPourTestCreation" }
        response = self.client.post(reverse('crt_rayon'), data)
        # Vérifie la redirection après la création
        self.assertEqual(response.status_code, 302)
        # Vérifie qu'un objet a été créé
        self.assertEqual(Rayon.objects.count(), 2)
        # Vérifie la valeur de l'objet créé
        self.assertEqual(Rayon.objects.last().nomRayon, 'rayonPourTestCreation')

    def test_Rayon_detail_view(self):
        response = self.client.get(reverse('dtl_rayon', args=[self.ctgr.idRayon]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/detail_rayon.html')
        # Vérifie que le nom de la rayon est affiché
        self.assertContains(response, 'rayonPourTestDetail')
        # Vérifie que l'id associé est affiché
        self.assertContains(response, '1')

    def test_Rayon_update_view_get(self):
        response = self.client.get(reverse('rayon_chng', args=[self.ctgr.idRayon]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/update_rayon.html')
    

    def test_update_view_post_valid(self):
        self.assertEqual(self.ctgr.nomRayon, 'rayonPourTestDetail')
        data = {'nomRayon': 'rayonPourTestAfterUpdate'}
        response = self.client.post(reverse('rayon_chng', args=[self.ctgr.idRayon]), data)
        # Redirection après la mise à jour
        self.assertEqual(response.status_code, 302)
        # Recharger l'objet depuis la base de données
        self.ctgr.refresh_from_db()
        # Vérifier la mise à jour du nom
        self.assertEqual(self.ctgr.nomRayon, 'rayonPourTestAfterUpdate')

    def test_Rayon_delete_view_get(self):
        response = self.client.get(reverse('rayon_del', args=[self.ctgr.idRayon]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/delete_rayon.html')

    def test_Rayon_delete_view_post(self):
        response = self.client.post(reverse('rayon_del', args=[self.ctgr.idRayon]))
        # Vérifier la redirection après la suppression
        self.assertEqual(response.status_code, 302)
        # Vérifier que l'objet a été supprimé
        self.assertFalse(Rayon.objects.filter(idRayon=self.ctgr.idRayon).exists())
        # Vérifier que la redirection est vers la liste des catégories
        self.assertRedirects(response, reverse('lst_rayons'))