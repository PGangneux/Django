
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from monApp.models import Statut


class statutCreateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.ctgr = Statut.objects.create(libelleStatus="statutPourTestDetail")

    def test_Statut_create_view_get(self):
        response = self.client.get(reverse('crt_statut')) # Utilisation du nom de l'URL
        self.assertEqual(response.status_code, 200)
        # Tester que la vue de création renvoie le bon template
        self.assertTemplateUsed(response, 'monApp/create_statut.html')
        
    def test_Statut_create_view_post_valid(self):
        data = { "libelleStatus": "statutPourTestCreation" }
        response = self.client.post(reverse('crt_statut'), data)
        # Vérifie la redirection après la création
        self.assertEqual(response.status_code, 302)
        # Vérifie qu'un objet a été créé
        self.assertEqual(Statut.objects.count(), 2)
        # Vérifie la valeur de l'objet créé
        self.assertEqual(Statut.objects.last().libelleStatus, 'statutPourTestCreation')

    def test_Statut_detail_view(self):
        response = self.client.get(reverse('dtl_statut', args=[self.ctgr.idStatus]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/detail_statut.html')
        # Vérifie que le nom de la statut est affiché
        self.assertContains(response, 'statutPourTestDetail')
        # Vérifie que l'id associé est affiché
        self.assertContains(response, '1')

    def test_Statut_update_view_get(self):
        response = self.client.get(reverse('statut_chng', args=[self.ctgr.idStatus]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/update_statut.html')
    

    def test_update_view_post_valid(self):
        self.assertEqual(self.ctgr.libelleStatus, 'statutPourTestDetail')
        data = {'libelleStatus': 'statutPourTestAfterUpdate'}
        response = self.client.post(reverse('statut_chng', args=[self.ctgr.idStatus]), data)
        # Redirection après la mise à jour
        self.assertEqual(response.status_code, 302)
        # Recharger l'objet depuis la base de données
        self.ctgr.refresh_from_db()
        # Vérifier la mise à jour du nom
        self.assertEqual(self.ctgr.libelleStatus, 'statutPourTestAfterUpdate')

    def test_Statut_delete_view_get(self):
        response = self.client.get(reverse('statut_del', args=[self.ctgr.idStatus]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/delete_statut.html')

    def test_Statut_delete_view_post(self):
        response = self.client.post(reverse('statut_del', args=[self.ctgr.idStatus]))
        # Vérifier la redirection après la suppression
        self.assertEqual(response.status_code, 302)
        # Vérifier que l'objet a été supprimé
        self.assertFalse(Statut.objects.filter(idStatus=self.ctgr.idStatus).exists())
        # Vérifier que la redirection est vers la liste des catégories
        self.assertRedirects(response, reverse('lst_statuts'))