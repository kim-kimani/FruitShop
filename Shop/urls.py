from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart_view'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path("update-cart/", views.update_cart, name="update_cart"),
    path('checkout/', views.checkout, name='checkout'),
]