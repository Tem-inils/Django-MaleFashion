from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django2 import settings
from products.views import (HomePage,
                            ShopPageView,
                            send_form,
                            AboutUsView,
                            ShopDetails,
                            ShoppingCart,
                            CheckOut,
                            BlogDetails,
                            Blog,
                            Contacts
                            )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePage.as_view(), name='home'),
    path('shop', ShopPageView.as_view(), name='shop'),
    path('about', AboutUsView.as_view(), name='about'),
    path('shop-detail', ShopDetails.as_view(), name='shop-detail'),
    path('shopping-cart', ShoppingCart.as_view(), name='shopping-cart'),
    path('checkout', CheckOut.as_view(), name='checkout'),
    path('blog-details', BlogDetails.as_view(), name='blog-details'),
    path('blog', Blog.as_view(), name='blog'),
    path('contacts', Contacts.as_view(), name='contacts'),
    path('form', send_form),
    path('accounts/', include('allauth.urls'))
    # path('forms',)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
