from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from monApp.models import Categorie


class CategorieCreateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.ctgr = Categorie.objects.create(nomCat="CategoriePourTestDetail")

    def test_categorie_create_view_get(self):
        response = self.client.get(reverse('crt_cats')) # Utilisation du nom de l'URL
        self.assertEqual(response.status_code, 200)
        # Tester que la vue de création renvoie le bon template
        self.assertTemplateUsed(response, 'monApp/create_categorie.html')
        
    def test_categorie_create_view_post_valid(self):
        data = { "nomCat": "CategoriePourTestCreation" }
        response = self.client.post(reverse('crt_cats'), data)
        # Vérifie la redirection après la création
        self.assertEqual(response.status_code, 302)
        # Vérifie qu'un objet a été créé
        self.assertEqual(Categorie.objects.count(), 2)
        # Vérifie la valeur de l'objet créé
        self.assertEqual(Categorie.objects.last().nomCat, 'CategoriePourTestCreation')

    def test_categorie_detail_view(self):
        response = self.client.get(reverse('dtl_cats', args=[self.ctgr.idCat]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/detail_categorie.html')
        # Vérifie que le nom de la categorie est affiché
        self.assertContains(response, 'CategoriePourTestDetail')
        # Vérifie que l'id associé est affiché
        self.assertContains(response, '1')

    def test_categorie_update_view_get(self):
        response = self.client.get(reverse('cats_chng', args=[self.ctgr.idCat]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/update_categorie.html')
    

    def test_update_view_post_valid(self):
        self.assertEqual(self.ctgr.nomCat, 'CategoriePourTestDetail')
        data = {'nomCat': 'CategoriePourTestAfterUpdate'}
        response = self.client.post(reverse('cats_chng', args=[self.ctgr.idCat]), data)
        # Redirection après la mise à jour
        self.assertEqual(response.status_code, 302)
        # Recharger l'objet depuis la base de données
        self.ctgr.refresh_from_db()
        # Vérifier la mise à jour du nom
        self.assertEqual(self.ctgr.nomCat, 'CategoriePourTestAfterUpdate')

    def test_categorie_delete_view_get(self):
        response = self.client.get(reverse('cats_del', args=[self.ctgr.idCat]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/delete_categorie.html')

    def test_categorie_delete_view_post(self):
        response = self.client.post(reverse('cats_del', args=[self.ctgr.idCat]))
        # Vérifier la redirection après la suppression
        self.assertEqual(response.status_code, 302)
        # Vérifier que l'objet a été supprimé
        self.assertFalse(Categorie.objects.filter(idCat=self.ctgr.idCat).exists())
        # Vérifier que la redirection est vers la liste des catégories
        self.assertRedirects(response, reverse('lst_cats'))