from django.shortcuts import render
from django.views.generic import ListView, TemplateView

from products.forms import FormModelForm
from products.models import CategoryModels, ProductModel


class HomePage(TemplateView):
    template_name = "index.html"


class ShopPageView(ListView):
    template_name = "shop.html"
    model = ProductModel
    context_object_name = "products"
    paginate_by = 15

    def get_queryset(self):
        queryset = ProductModel.objects.all()

        q = self.request.GET.get("q")
        category = self.request.GET.get("category")

        if q:
            queryset = queryset.filter(title__icontains=q)

        if category:
            queryset = queryset.filter(category_id=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = CategoryModels.objects.all()
        context["q"] = self.request.GET.get("q", "")
        context["selected_category"] = self.request.GET.get("category", "")

        return context


class AboutUsView(TemplateView):
    template_name = "about.html"


class ShopDetails(TemplateView):
    template_name = "shop-details.html"


class ShoppingCart(TemplateView):
    template_name = "shopping-cart.html"


class CheckOut(TemplateView):
    template_name = "checkout.html"


class BlogDetails(TemplateView):
    template_name = "blog-details.html"


class Blog(TemplateView):
    template_name = "blog.html"


class Contacts(TemplateView):
    template_name = "contact.html"


def send_form(request):
    success = False

    if request.method == "POST":
        form = FormModelForm(request.POST)

        if form.is_valid():
            form.save()
            success = True
            form = FormModelForm()
    else:
        form = FormModelForm()

    context = {
        "form": form,
        "blabla": form,
        "success": success,
    }

    return render(request, "forms.html", context)
