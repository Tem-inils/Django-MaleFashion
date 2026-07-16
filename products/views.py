from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView, TemplateView, DetailView

from products.forms import FormModelForm
from products.models import CategoryModels, ProductModel


class HomePage(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        products = ProductModel.objects.filter(
            is_available=True
        ).select_related("category", "brand")

        context["featured_products"] = products.filter(
            is_featured=True
        ).order_by("homepage_order", "-created_at")[:8]

        context["best_sellers"] = products.filter(
            is_best_seller=True
        ).order_by("homepage_order", "-created_at")[:8]

        context["new_arrivals"] = products.filter(
            is_new_arrival=True
        ).order_by("homepage_order", "-created_at")[:8]

        context["hot_sales"] = products.filter(
            is_hot_sale=True
        ).order_by("homepage_order", "-created_at")[:8]

        context["homepage_products"] = products.filter(
            Q(is_best_seller=True) |
            Q(is_new_arrival=True) |
            Q(is_hot_sale=True)
        ).distinct().order_by("homepage_order", "-created_at")[:8]

        context["main_categories"] = CategoryModels.objects.filter(
            is_active=True,
            parent__isnull=True,
        ).prefetch_related("children")

        return context


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
