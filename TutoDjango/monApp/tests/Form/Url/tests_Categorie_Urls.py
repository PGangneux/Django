from django.test import TestCase
from django.urls import reverse, resolve
from monApp.views import CategorieCreateView, CategorieDeleteView, CategorieListView, CategorieDetailView, CategorieUpdateView,

class CategorieUrlsTest(TestCase):
    def test_categorie_list_url_is_resolved(self):
        url = reverse('lst_cats')
        self.assertEqual(resolve(url).view_name, 'lst_cats')
        self.assertEqual(resolve(url).func.view_class,CategorieListView)

    def test_categorie_detail_url_is_resolved(self):
        url = reverse('dtl_cats', args=[1])
        self.assertEqual(resolve(url).view_name, 'dtl_cats')
        self.assertEqual(resolve(url).func.view_class, CategorieDetailView)

    def test_categorie_create_url_is_resolved(self):
        url = reverse('crt_cats')
        self.assertEqual(resolve(url).view_name, 'crt_cats')
        self.assertEqual(resolve(url).func.view_class, CategorieCreateView)

    def test_categorie_update_url_is_resolved(self):
        url = reverse('cats_chng', args=[1])
        self.assertEqual(resolve(url).view_name, 'cats_chng')
        self.assertEqual(resolve(url).func.view_class, CategorieUpdateView)

    def test_categorie_delete_url_is_resolved(self):
        url = reverse('cats_del', args=[1])
        self.assertEqual(resolve(url).view_name, 'cats_del')
        self.assertEqual(resolve(url).func.view_class, CategorieDeleteView)