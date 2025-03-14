import requests, base64, json, re, os
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from Core.models import Testimonial
from .models import Product, Transaction
from dotenv import load_dotenv

load_dotenv()

# M-Pesa credentials and configuration
CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE')
MPESA_PASSKEY = os.getenv('MPESA_PASSKEY')
CALLBACK_URL = os.getenv('CALLBACK_URL')
MPESA_BASE_URL = os.getenv('MPESA_BASE_URL')

def format_phone_number(phone):
    phone = phone.replace("+", "")
    if re.match(r"^254\d{9}$", phone):
        return phone
    elif phone.startswith("0") and len(phone) == 10:
        return "254" + phone[1:]
    else:
        raise ValueError("Invalid phone number format")

def generate_access_token():
    try:
        credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/json",
        }
        response = requests.get(
            f"{MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials",
            headers=headers,
        ).json()

        if "access_token" in response:
            return response["access_token"]
        else:
            raise Exception("Access token missing in response.")

    except requests.RequestException as e:
        raise Exception(f"Failed to connect to M-Pesa: {str(e)}")

def initiate_stk_push(phone, amount):
    try:
        token = generate_access_token()
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        stk_password = base64.b64encode(
            (MPESA_SHORTCODE + MPESA_PASSKEY + timestamp).encode()
        ).decode()

        request_body = {
            "BusinessShortCode": MPESA_SHORTCODE,
            "Password": stk_password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": MPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": CALLBACK_URL,
            "AccountReference": "account",
            "TransactionDesc": "Payment for goods",
        }

        response = requests.post(
            f"{MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest",
            json=request_body,
            headers=headers,
        ).json()

        return response

    except Exception as e:
        print(f"Failed to initiate STK Push: {str(e)}")
        return e

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
                'id': product.id
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
        phone = request.POST.get('phone')
        try:
            formatted_phone = format_phone_number(phone)
            response = initiate_stk_push(formatted_phone, total)
            print(response)

            if response.get("ResponseCode") == "0":
                checkout_request_id = response["CheckoutRequestID"]
                return render(request, "shop/pending.html", {"checkout_request_id": checkout_request_id})
            else:
                error_message = response.get("errorMessage", "Failed to send STK push. Please try again.")
                context['error_message'] = error_message

        except ValueError as e:
            context['error_message'] = str(e)
        except Exception as e:
            context['error_message'] = f"An unexpected error occurred: {str(e)}"

    return render(request, 'shop/checkout.html', context)

@csrf_exempt
def payment_callback(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Only POST requests are allowed")

    try:
        callback_data = json.loads(request.body)
        result_code = callback_data["Body"]["stkCallback"]["ResultCode"]

        if result_code == 0:
            checkout_id = callback_data["Body"]["stkCallback"]["CheckoutRequestID"]
            metadata = callback_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]

            amount = next(item["Value"] for item in metadata if item["Name"] == "Amount")
            mpesa_code = next(item["Value"] for item in metadata if item["Name"] == "MpesaReceiptNumber")
            phone = next(item["Value"] for item in metadata if item["Name"] == "PhoneNumber")

            Transaction.objects.create(
                amount=amount,
                checkout_id=checkout_id,
                mpesa_code=mpesa_code,
                phone_number=phone,
                status="Success"
            )
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Payment successful"})

        return JsonResponse({"ResultCode": result_code, "ResultDesc": "Payment failed"})

    except (json.JSONDecodeError, KeyError) as e:
        return HttpResponseBadRequest(f"Invalid request data: {str(e)}")
