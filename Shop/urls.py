from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.shop, name='shop'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
]