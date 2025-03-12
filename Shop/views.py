from django.shortcuts import render
from Core.models import Testimonial
from .models import Product
from django.shortcuts import get_object_or_404, redirect

# Create your views here.
def shop(request):
    products = Product.objects.all()
    context = {
        'products': products
        
    }
    return render(request, 'shop/shop.html', context)

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    related_products = Product.objects.filter(category=product.category).exclude(id=id)
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'shop/product_detail.html', context)

def add_to_cart(request, id):
    # Logic to add product to cart
    return redirect('shop')
