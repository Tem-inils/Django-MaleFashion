from django.contrib import admin

from products.models import ProductModel, FormModel, CategoryModels

# 1) python manage.py startapp products
# 2) products поставить в settings.py installed apps

@admin.register(CategoryModels)
class CategoryModelsAdmin(admin.ModelAdmin):
    pass




@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'created_at']
    search_fields = ['title', 'price']
    list_filter = ['created_at']


@admin.register(FormModel)
class FormModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'age', 'comment']