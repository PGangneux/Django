
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from monApp.models import Produit


class ProduitCreateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client.login(username='testuser', password='secret')
        self.ctgr = Produit.objects.create(intituleProd="produitPourTestDetail", prixUnitaireProd=10.0)

    def test_produit_create_view_get(self):
        response = self.client.get(reverse('crt_prdt')) # Utilisation du nom de l'URL
        self.assertEqual(response.status_code, 200)
        # Tester que la vue de création renvoie le bon template
        self.assertTemplateUsed(response, 'monApp/create_produit.html')
        

    def test_produit_create_view_post_valid(self):
        data = {
            "intituleProd": "produitPourTestCreation",
            "prixUnitaireProd": 15.0,
            "dateFabProd": "2025-10-16"
        }
        response = self.client.post(reverse('crt_prdt'), data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Produit.objects.count(), 2)
        produit = Produit.objects.last()
        self.assertEqual(produit.intituleProd, "produitPourTestCreation")
        self.assertEqual(float(produit.prixUnitaireProd), 15.0)
        self.assertEqual(str(produit.dateFabProd), "2025-10-16")

    def test_produit_detail_view(self):
        response = self.client.get(reverse('dtl_prdt', args=[self.ctgr.refProd]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/detail_produit.html')
        # Vérifie que le nom de la produit est affiché
        self.assertContains(response, 'produitPourTestDetail')
        # Vérifie que l'id associé est affiché
        self.assertContains(response, '1')

    def test_produit_update_view_get(self):
        response = self.client.get(reverse('prdt_chng', args=[self.ctgr.refProd]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/update_produit.html')
    

    def test_update_view_post_valid(self):
        self.assertEqual(self.ctgr.intituleProd, 'produitPourTestDetail')
        self.assertEqual(self.ctgr.intituleProd, 'produitPourTestDetail')
        data = {
            'intituleProd': 'produitPourTestAfterUpdate',
            'prixUnitaireProd': '20.00',
            'dateFabProd': '2025-10-16'
        }
        response = self.client.post(reverse('prdt_chng', args=[self.ctgr.refProd]), data)

        # Redirection après la mise à jour
        self.assertEqual(response.status_code, 302)
        # Recharger l'objet depuis la base de données
        self.ctgr.refresh_from_db()
        # Vérifier la mise à jour du nom
        self.assertEqual(self.ctgr.intituleProd, 'produitPourTestAfterUpdate')
        self.assertEqual(self.ctgr.prixUnitaireProd, 20.0)
        self.assertEqual(str(self.ctgr.dateFabProd), '2025-10-16')

    def test_produit_delete_view_get(self):
        response = self.client.get(reverse('prdt_del', args=[self.ctgr.refProd]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'monApp/delete_produit.html')

    def test_produit_delete_view_post(self):
        response = self.client.post(reverse('prdt_del', args=[self.ctgr.refProd]))
        # Vérifier la redirection après la suppression
        self.assertEqual(response.status_code, 302)
        # Vérifier que l'objet a été supprimé
        self.assertFalse(Produit.objects.filter(refProd=self.ctgr.refProd).exists())
        # Vérifier que la redirection est vers la liste des catégories
        self.assertRedirects(response, reverse('lst_prdts'))