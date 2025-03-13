from django.shortcuts import render
from Core.models import Testimonial
from .models import Product
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
import json
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime

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
    if request.method == 'POST':
        product = get_object_or_404(Product, id=id)
        quantity = int(request.POST.get('quantity', 1))

        cart = request.session.get('cart', {})

        if str(product.id) in cart:
            cart[str(product.id)]['quantity'] += quantity
        else:
            cart[str(product.id)] = {
                'quantity': quantity,
                'price': product.price,
                'name': product.name,
                'image': product.thumbnail.url,
                'id': product.id  # Ensure the product ID is stored
            }
        request.session['cart'] = cart

        return JsonResponse({'success': True, 'cart_size': len(cart)})

    return redirect('shop')

def cart(request):
    cart = request.session.get('cart', {})
    subtotal = 0

    for product_id, item in cart.items():
        item['total_price'] = item['quantity'] * item['price']
        subtotal += item['total_price']

    shipping = 45
    total = subtotal + shipping

    context = {
        'cart': cart,
        'subtotal': subtotal,
        'total': total
    }
    return render(request, 'shop/cart.html', context)

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart_view')

def update_cart(request):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        data = json.loads(request.body)
        product_id = str(data.get("product_id"))
        action = data.get("action")

        if product_id in cart:
            if action == "increase":
                cart[product_id]["quantity"] += 1
            elif action == "decrease" and cart[product_id]["quantity"] > 1:
                cart[product_id]["quantity"] -= 1

            cart[product_id]["total_price"] = cart[product_id]["quantity"] * cart[product_id]["price"]

        request.session["cart"] = cart
        request.session.modified = True  

        # Calculate subtotal and total
        subtotal = sum(item["total_price"] for item in cart.values())
        shipping = 45
        total = subtotal + shipping

        return JsonResponse({
            "success": True,
            "new_quantity": cart[product_id]["quantity"],
            "total_price": cart[product_id]["total_price"],
            "subtotal": subtotal,
            "total": total
        })

    return JsonResponse({"success": False})


def checkout(request):
    cart = request.session.get('cart', {})
    subtotal = 0

    for product_id, item in cart.items():
        item['total_price'] = item['quantity'] * item['price']
        subtotal += item['total_price']

    shipping = 45
    total = subtotal + shipping

    context = {
        'cart': cart,
        'subtotal': subtotal,
        'total': total
    }

    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        if phone_number:
            consumer_key = "35im46KRmbipxDiUX37GRnxj9oJlW3Lqf9GBAPiE2VMzyAWU"
            consumer_secret = "2SqmH7TQ7nRTkGbfv5mR0KeyMYUFd2QO0H5AWetNzvbB0T8AW7Rwuy2Ui9nzGtSn"
            access_token = get_access_token(consumer_key, consumer_secret)
            stk_response = stk_push(phone_number, total, access_token)
            # Handle the STK push response
            return redirect('index')

    return render(request, 'shop/checkout.html', context)




