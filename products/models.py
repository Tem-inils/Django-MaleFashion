from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify

# models.py, admin.py, views.py, urls.py


class CategoryModels(models.Model):
    title = models.CharField(max_length=50)
    crate_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category"


class ProductModel(models.Model):

    category = models.ForeignKey(
        CategoryModels,
        on_delete=models.CASCADE,
        related_name="products",
    )

    title = models.CharField(max_length=50)
    '''
        without slug - products/15
        with slug - products/black-jacket/
    '''
    slug = models.SlugField(unique=True)
    descriptions = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveIntegerField(
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    image = models.FileField(upload_to="products/")
    color = models.CharField(max_length=50, blank=True)
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def final_price(self):
        if self.discount > 0:
            return self.price - (self.price * self.discount // 100)
        return self.price

    @property
    def has_discount(self):
        return self.discount > 0

    @property
    def in_stock(self):
        return self.stock > 0

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while ProductModel.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        if self.stock <= 0:
            self.is_available = False

        super().save(*args, **kwargs)


class FormModel(models.Model):
    username = models.CharField(max_length=30)
    age = models.IntegerField(default=0)
    comment = models.TextField()

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Form"
        verbose_name_plural = "Forms"
