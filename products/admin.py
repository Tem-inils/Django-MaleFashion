from django.contrib import admin

from products.models import CategoryModels, FormModel, ProductModel


@admin.register(CategoryModels)
class CategoryModelsAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "category",
        "price",
        "discount",
        "final_price",
        "color",
        "stock",
        "is_available",
        "created_at",
    ]
    list_filter = [
        "category",
        "color",
        "is_available",
        "created_at",
    ]
    search_fields = [
        "title",
        "descriptions",
        "color",
    ]
    list_editable = [
        "price",
        "discount",
        "color",
        "stock",
        "is_available",
    ]
    prepopulated_fields = {
        "slug": ("title",),
    }
    readonly_fields = [
        "final_price",
        "created_at",
        "updated_at",
    ]


@admin.register(FormModel)
class FormModelAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "age", "comment"]
