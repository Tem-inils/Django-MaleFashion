from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from .models import CategoryModels


# models.py, admin.py, views.py, urls.py

# def home_page(request):
#     return HttpResponse("<h1>Hello</h1>")
from products.forms import FormModelForm
from products.models import ProductModel


def index_page(request):
    # products = ProductModel.objects.all().filter(title__icontains="Iphone12")
    # products = ProductModel.objects.all().order_by('-id')

    return render(request, 'index.html', )


# def shop_page(request):
#     products = ProductModel.objects.all()
#     return render(request, 'shop.html', {'products': products})

class ShopPageView(ListView):
    template_name = 'shop.html'
    queryset = ProductModel.objects.all()
    context_object_name = 'products'
    paginate_by = 1

def get_quaryset(self):
    qs = ProductModel.objects.all()
    q = self.request.GET.get('q')
    category = self.request.GET.get('category')

    if q:
        qs = qs.filter(title__icontains=q)
        #title
        #title__icontais = ищет по буквам

    elif category:
        qs = qs.filter(category_id=category)

    return q


def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryModels.objects.all()

        return context

class About_us(TemplateView):
    template_name = 'about.html'


# context ={}
#
#     # add the dictionary during initialization
#     form = GeeksForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#     context['form']= form
#     return render(request, "create_view.html", context)
def send_form(request):
    context = {}

    form = FormModelForm(request.POST)
    if form.is_valid():
        form.save()

    context['blabla'] = form
    return render(request, 'forms.html', context)
