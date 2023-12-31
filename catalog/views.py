from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView
from catalog.forms import ProductForm, VersionForm, ContactForm
from catalog.models import *
from catalog.services import categories_get_cache, send_message_mail


class CatalogView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_staff:
            context['products'] = Product.objects.all().filter(is_published=True)
        else:
            context['products'] = Product.objects.all()
        return context


class ContactsView(LoginRequiredMixin, CreateView):
    model = Contacts
    form_class = ContactForm
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save()
        send_message_mail(obj)
        return super().form_valid(form)


    def categories(request):
        category_list = categories_get_cache()
        return render(request, 'catalog/categories.html', {'object_list': category_list})


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'catalog/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_staff:
            context['products'] = Product.objects.filter(category=self.kwargs['pk']).filter(is_published=True)
        else:
            context['products'] = Product.objects.filter(category=self.kwargs['pk'])
        return context


class ProductCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_create.html'
    permission_required = 'catalog.product_create'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        obj = form.save()
        obj.owner = self.request.user
        obj.save()
        return super().form_valid(form)

    def test_func(self):
        return not self.request.user.is_staff


class ProductDetailView(DetailView):
    model = Product


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    permission_required = 'catalog.product_update'

    def get_success_url(self):
        return reverse_lazy('product', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            formset = VersionFormset(self.request.POST, instance=self.object)
        else:
            formset = VersionFormset(instance=self.object)
        context['formset'] = formset
        return context

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        obj = form.save()
        if formset.is_valid():
            formset.instance = obj
            formset.save()
        else:
            form.add_error(None, 'Ошибка в версиях')
            return self.form_invalid(form)
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_staff:
            return False
        return self.request.user == Product.objects.get(pk=self.kwargs['pk']).owner


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('home')

    def test_func(self):
        return not self.request.user.is_staff
