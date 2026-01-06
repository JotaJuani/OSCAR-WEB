from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, ProductImage
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms

class ProductImageInlineForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = '__all__'
        widgets = {
            'description': CKEditor5Widget(config_name='default'),
        }

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    form = ProductImageInlineForm
    extra = 3  # cantidad de formularios vacíos por defecto
    max_num = 3  # solo 3 imágenes por producto
    fields = ('image', 'title', 'description', 'order')
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'available', 'created', 'updated', 'image_preview')
    list_filter = ('available', 'created', 'updated', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    readonly_fields = ('image_preview',)
    fields = ('category', 'name', 'slug', 'description', 'price', 'available', 'main_image', 'image_preview')

    def image_preview(self, obj):
        
        if obj.main_image:
            return format_html('<img src="{}" style="width: 120px; height: auto;" />', obj.main_image.url)
        return "(Sin imagen)"
    image_preview.short_description = "Vista previa principal"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'title', 'order')
