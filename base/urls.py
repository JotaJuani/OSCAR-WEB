from django.urls import path
from base import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =  [
    path('', views.homePage, name="home"),
    path('productos/', views.all_products_random, name='all_products_random'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact_view, name='contact'),    
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)