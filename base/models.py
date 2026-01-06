from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #Imagen principal para la card o portada del producto
    main_image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Imagen principal')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    title = models.CharField(max_length=200, blank=True, null=True)
    description = CKEditor5Field(config_name='default', blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Orden de aparición (1, 2, 3...)")

    class Meta:
        verbose_name = 'Imagen del producto'
        verbose_name_plural = 'Imágenes del producto'
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - {self.title or 'Imagen'}"
