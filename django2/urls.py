from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django2 import settings
from products.views import index_page, ShopPageView, send_form, About_us

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_page, name='home'),
    path('shop', ShopPageView.as_view(), name='shop'),
    path('about', About_us.as_view(), name='about'),
    path('form', send_form),
    path('accounts/', include('allauth.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
