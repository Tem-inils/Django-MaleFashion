from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Case, When, Value, F, CharField, IntegerField

from products.models import CategoryModels, FormModel, ProductModel, Brand


class CategoryParentFilter(admin.SimpleListFilter):
    title = "Category"
    parameter_name = "category"

    def lookups(self, request, model_admin):
        main_categories = CategoryModels.objects.filter(
            parent__isnull=True
        ).order_by("title")

        choices = [
            ("main", "Main categories"),
        ]

        for category in main_categories:
            choices.append((str(category.id), category.title))

        return choices

    def queryset(self, request, queryset):
        value = self.value()

        if value == "main":
            return queryset.filter(parent__isnull=True)

        if value:
            return queryset.filter(parent_id=value)

        return queryset


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug", "is_active"]
    list_filter = ["is_active"]
    search_fields = ["title", "slug"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(CategoryModels)
class CategoryModelsAdmin(admin.ModelAdmin):
    ordering = []
    sortable_by = []

    list_display = [
        "id",
        "tree_title",
        "category_path",
        "parent_category",
        "slug",
        "products_count",
        "children_count",
        "is_active",
        "created_at",
    ]

    list_filter = [
        CategoryParentFilter,
    ]

    search_fields = [
        "title",
        "slug",
        "parent__title",
    ]

    list_editable = [
        "is_active",
    ]

    prepopulated_fields = {
        "slug": ("title",),
    }

    readonly_fields = [
        "created_at",
        "updated_at",
        "products_count",
        "children_count",
    ]

    autocomplete_fields = [
        "parent",
    ]

    list_select_related = [
        "parent",
    ]

    @admin.display(description="Category")
    def tree_title(self, obj):
        if obj.parent:
            return format_html(
                '<span style="padding-left: 30px;">└── {}</span>',
                obj.title
            )

        return format_html(
            '<strong>📁 {}</strong>',
            obj.title
        )

    @admin.display(description="Path")
    def category_path(self, obj):
        if obj.parent:
            return f"{obj.parent.title} → {obj.title}"
        return obj.title

    @admin.display(description="Parent")
    def parent_category(self, obj):
        if obj.parent:
            return obj.parent.title
        return "Main category"

    @admin.display(description="Products")
    def products_count(self, obj):
        return obj.products.count()

    @admin.display(description="Subcategories")
    def children_count(self, obj):
        return obj.children.count()

    def get_queryset(self, request):
        queryset = super().get_queryset(request).select_related("parent").order_by()

        return queryset.annotate(
            tree_group=Case(
                When(parent__isnull=True, then=F("title")),
                default=F("parent__title"),
                output_field=CharField(),
            ),
            tree_level=Case(
                When(parent__isnull=True, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            ),
        ).order_by(
            "tree_group",
            "tree_level",
            "title",
        )


@admin.register(ProductModel)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "title",
        "category",
        "brand",
        "price",
        "discount",
        "final_price",
        "color",
        "stock",
        "is_available",
        "is_featured",
        "is_best_seller",
        "is_new_arrival",
        "is_hot_sale",
        "created_at",
    ]

    list_filter = [
        "category",
        "brand",
        "color",
        "is_available",
        "is_featured",
        "is_best_seller",
        "is_new_arrival",
        "is_hot_sale",
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
        "is_featured",
        "is_best_seller",
        "is_new_arrival",
        "is_hot_sale",
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
