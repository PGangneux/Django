from itertools import count
from django.forms import BaseModelForm
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponse, HttpResponseNotFound, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import  *
from monApp.forms import CategorieForm, ContactUsForm, ContenirForm, ProduitForm, RayonForm, StatutForm
from monApp.models import *
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Count, Prefetch
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required




class HomeView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['titreh1'] = "Hello DJANGO "
        if self.kwargs.get('param'):
            context['titreh1'] +=self.kwargs.get('param')
        return context

    def post(self, request, **kwargs):
        return render(request, self.template_name)
    

def ContactView(request):
    titreh1 = "Contact us !"
    if request.method=='POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            send_mail(
                subject=f'Message from {form.cleaned_data["name"] or "anonyme"} via TutoDjango Contact form',
                message=form.cleaned_data['message'],
                from_email=form.cleaned_data['email'],
                recipient_list=['admin@monApp.com'],
            )
            return redirect('email-sent')
    else:
        form = ContactUsForm()
    return render(request, "monApp/page_home.html",{'titreh1':titreh1, 'form':form})


class EmailSent(TemplateView):
    template_name = "monApp/email_sent.html"

    def get_context_data(self, **kwargs):
        context = super(EmailSent, self).get_context_data(**kwargs)
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)


class AboutView(TemplateView):
    template_name = "monApp/page_home.html"

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        context['titreh1'] = "About us..."
        return context
    
    def post(self, request, **kwargs):
        return render(request, self.template_name)


class ProduitListView(ListView):
    model = Produit
    template_name = "monApp/list_produits.html"
    context_object_name = "prdts"

    def get_queryset(self):
        # Surcouche pour filtrer les résultats en fonction de la recherche
        # Récupérer le terme de recherche depuis la requête GET
        query = self.request.GET.get('search')
        if query:
            return Produit.objects.filter(intituleProd__icontains=query).select_related('categorie').select_related('status')
        # Si aucun terme de recherche, retourner tous les produits
        # Charge les catégories en même temps
        return Produit.objects.select_related('categorie').select_related('status')


    def get_context_data(self, **kwargs):
        context = super(ProduitListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes produits"
        return context
    
class ProduitDetailView(DetailView):
    model = Produit
    template_name = "monApp/detail_produit.html"
    context_object_name = "prdt"
    
    def get_context_data(self, **kwargs):
        context = super(ProduitDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du produit"
        return context

@method_decorator(login_required, name='dispatch')
class ProduitCreateView(CreateView):
    model = Produit
    form_class=ProduitForm
    template_name = "monApp/create_produit.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('dtl_prdt', prdt.refProd) 

@method_decorator(login_required, name='dispatch')
class ProduitUpdateView(UpdateView):
    model = Produit
    form_class=ProduitForm
    template_name = "monApp/update_produit.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        prdt = form.save()
        return redirect('dtl_prdt', prdt.refProd)
    
@method_decorator(login_required, name='dispatch')    
class ProduitDeleteView(DeleteView):
    model = Produit
    template_name = "monApp/delete_produit.html"
    success_url = reverse_lazy('lst_prdts')
    

@method_decorator(login_required, name='dispatch')
class CategorieListView(ListView):
    model = Categorie
    template_name = "monApp/list_categories.html"
    context_object_name = "categories"

    
    def get_queryset(self):
        # Surcouche pour filtrer les résultats en fonction de la recherche
        # Récupérer le terme de recherche depuis la requête GET
        query = self.request.GET.get('search')
        if query:
            return Categorie.objects.filter(nomCat__icontains=query)
        # Si aucun terme de recherche, retourner tous les produits
        # Charge les catégories en même temps
        return Categorie.objects.annotate(nb_produits=Count('produits_categorie'))
    
        
    def get_context_data(self, **kwargs):
        context = super(CategorieListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes catégories"
        return context


class CategorieDetailView(DetailView):
    model = Categorie
    template_name = "monApp/detail_categorie.html"
    context_object_name = "categorie"

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Categorie.objects.annotate(nb_produits=Count('produits_categorie'))
            
    def get_context_data(self, **kwargs):
        context = super(CategorieDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail de la catégorie"
        context['prdts'] = self.object.produits_categorie.all()
        return context

@method_decorator(login_required, name='dispatch')
class CategorieCreateView(CreateView):
    model = Categorie
    form_class=CategorieForm
    template_name = "monApp/create_categorie.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        cats = form.save()
        return redirect('dtl_cats', cats.idCat) 


@method_decorator(login_required, name='dispatch')
class CategorieUpdateView(UpdateView):
    model = Categorie
    form_class=CategorieForm
    template_name = "monApp/update_categorie.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        cat = form.save()
        return redirect('dtl_cats', cat.idCat)
    

@method_decorator(login_required, name='dispatch')
class CategorieDeleteView(DeleteView):
    model = Categorie
    template_name = "monApp/delete_categorie.html"
    success_url = reverse_lazy('lst_cats')


class StatusListView(ListView):
    model = Statut
    template_name = "monApp/list_statuts.html"
    context_object_name = "statuts"
    

    def get_queryset(self):
        # Surcouche pour filtrer les résultats en fonction de la recherche
        # Récupérer le terme de recherche depuis la requête GET
        query = self.request.GET.get('search')
        if query:
            return Statut.objects.filter(libelleStatus__icontains=query)
        # Si aucun terme de recherche, retourner tous les produits
        # Charge les catégories en même temps
        return Statut.objects.annotate(nb_produits=Count('produits_status'))
    
    def get_context_data(self, **kwargs):
        context = super(StatusListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes statuts"
        return context
    
class StatutDetailView(DetailView):
    model = Statut
    template_name = "monApp/detail_statut.html"
    context_object_name = "statut"

    def get_queryset(self):
        # Annoter chaque catégorie avec le nombre de produits liés
        return Statut.objects.annotate(nb_produits=Count('produits_status'))
    
    def get_context_data(self, **kwargs):
        context = super(StatutDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du statut"
        context['prdts'] = self.object.produits_status.all()
        return context
    

@method_decorator(login_required, name='dispatch')
class StatutCreateView(CreateView):
    model = Statut
    form_class=StatutForm
    template_name = "monApp/create_statut.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        statut = form.save()
        return redirect('dtl_statut', statut.idStatus) 
    
@method_decorator(login_required, name='dispatch')
class StatutUpdateView(UpdateView):
    model = Statut
    form_class=StatutForm
    template_name = "monApp/update_statut.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        statut = form.save()
        return redirect('dtl_statut', statut.idStatus)
    

@method_decorator(login_required, name='dispatch')
class StatutDeleteView(DeleteView):
    model = Statut
    template_name = "monApp/delete_statut.html"
    success_url = reverse_lazy('lst_statuts')


class RayonsListView(ListView):
    model = Rayon
    template_name = "monApp/list_rayons.html"
    context_object_name = "rayons"
        

    def get_queryset(self):
        # Surcouche pour filtrer les résultats en fonction de la recherche
        # Récupérer le terme de recherche depuis la requête GET
        query = self.request.GET.get('search')
        if query:
            return Rayon.objects.filter(nomRayon__icontains=query)
        # Si aucun terme de recherche, retourner tous les rayons
        return Rayon.objects.prefetch_related(
            Prefetch("contenir_rayon", queryset=Contenir.objects.select_related("produit"))
        )

    
    
    def get_context_data(self, **kwargs):
        context = super(RayonsListView, self).get_context_data(**kwargs)
        context['titremenu'] = "Liste de mes rayons"
        ryns_dt = []
        for rayon in context['rayons']:
            total = 0
            for contenir in rayon.contenir_rayon.all():
                total += contenir.produit.prixUnitaireProd * contenir.Qte
            ryns_dt.append({'rayon': rayon,'total_stock': total})
        context['ryns_dt'] = ryns_dt
        return context
    
class RayonDetailView(DetailView):
    model = Rayon
    template_name = "monApp/detail_rayon.html"
    context_object_name = "rayon"
    
    def get_context_data(self, **kwargs):
        context = super(RayonDetailView, self).get_context_data(**kwargs)
        context['titremenu'] = "Détail du rayon"
        prdts_dt = []
        total_rayon = 0
        total_nb_produit = 0
        for contenir in self.object.contenir_rayon.all():
            total_produit = contenir.produit.prixUnitaireProd * contenir.Qte
            prdts_dt.append({ 'produit': contenir.produit,
                'qte': contenir.Qte,
                'prix_unitaire': contenir.produit.prixUnitaireProd,
                'total_produit': total_produit}
            )
            total_rayon += total_produit
            total_nb_produit += contenir.Qte

        context['prdts_dt'] = prdts_dt
        context['total_rayon'] = total_rayon
        context['total_nb_produit'] = total_nb_produit
        return context


@method_decorator(login_required, name='dispatch')
class RayonCreateView(CreateView):
    model = Rayon
    form_class=RayonForm
    template_name = "monApp/create_rayon.html"
    
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        rayon = form.save()
        return redirect('dtl_rayon', rayon.idRayon) 
    


@method_decorator(login_required, name='dispatch')
class RayonUpdateView(UpdateView):
    model = Rayon
    form_class=RayonForm
    template_name = "monApp/update_rayon.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        rayon = form.save()
        return redirect('dtl_rayon', rayon.idRayon)
    

@method_decorator(login_required, name='dispatch')    
class RayonDeleteView(DeleteView):
    model = Rayon
    template_name = "monApp/delete_rayon.html"
    success_url = reverse_lazy('lst_rayons')


@method_decorator(login_required, name='dispatch')
class ContenirCreateView(CreateView):
    model = Contenir
    form_class = ContenirForm
    template_name = "monApp/create_contenir.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rayon = get_object_or_404(Rayon, pk=self.kwargs['pk'])
        context['rayon'] = rayon
        return context

    def form_valid(self, form):
        rayon = get_object_or_404(Rayon, pk=self.kwargs['pk'])
        contenir = form.save(commit=False)
        contenir.rayon = rayon
        qte =  self.object.contenir_rayon.all()
            
        contenir.save()
        return redirect('dtl_rayon', pk=rayon.idRayon)
    
    
@method_decorator(login_required, name='dispatch')
class ContenirUpdateView(UpdateView):
    model = Contenir
    form_class = ContenirForm
    template_name = "monApp/update_contenir.html"

    def form_valid(self, form):
        rayon = get_object_or_404(Rayon, pk=self.kwargs['pkR'])
        produit = get_object_or_404(Produit, pk=self.kwargs['pkP'])
        contenir = form.save(commit=False)
        contenir.produit = produit
        contenir.rayon = rayon
        contenir.save()
        return redirect('dtl_rayon', pk=rayon.idRayon)



def accueil(request,param):
    return HttpResponse("<h1>Hello " + param + " ! You're connected</h1>")

def ma_vue(request):
    return JsonResponse({'foo': 'bar'})



class ConnectView(LoginView):
    template_name = 'monApp/page_login.html'
    def post(self, request, **kwargs):
        lgn = request.POST.get('username', False)
        pswrd = request.POST.get('password', False)
        user = authenticate(username=lgn, password=pswrd)
        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'monApp/page_home.html', {'param': lgn, 'message': "You're connected"})
        else:
            return render(request, 'monApp/page_register.html')
        
class RegisterView(TemplateView):
    template_name = 'monApp/page_register.html'
    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        mail = request.POST.get('mail', False)
        password = request.POST.get('password', False)
        user = User.objects.create_user(username, mail, password)
        user.save()
        if user is not None and user.is_active:
            return render(request, 'monApp/page_login.html')
        else:
            return render(request, 'monApp/page_register.html')
        
class DisconnectView(TemplateView):
    template_name = 'monApp/page_logout.html'
    def get(self, request, **kwargs):
        logout(request)
        return render(request, self.template_name)
