from django.http import JsonResponse
from django.shortcuts import render, redirect
from numpy import product
from .models import OrderHistory
from cart.models import CartItem
from address.models import Address
from address.forms import AddressForm
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
import razorpay
from ayurvita import settings
from user.models import User
from shop.models import Product


# Create your views here.

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


@login_required(redirect_field_name=None, login_url='login')
def pay(request, product_id=None):
    try:
        address_id = request.session['selected_address']
        address = Address.objects.get(id=address_id)
        del request.session['selected_address']
    except:
        try:
            buynow = request.session['buynow']
        except:
            buynow = None
        if buynow:
            product_id = request.session['product_id']
            messages.error(request, 'select or give an address')
            return redirect('buynow', product_id)
        messages.error(request, 'select or give an address')
        return redirect('cart_checkout')
    if product_id:
        product = Product.objects.get(id=product_id)
        order = OrderHistory.objects.create(user=request.user, product_name=product.product_name, product_quantity=1, product_image1=product.product_image1,
                                            product_image2=product.product_image2, product_image3=product.product_image3, category=product.category, price=product.get_mrp(),)
        del request.session['buynow']
    else:
        cart = CartItem.objects.filter(user=request.user)
        for item in cart:
            order = OrderHistory.objects.create(user=request.user, product_name=item.product.product_name, product_quantity=item.quantity, product_image1=item.product.product_image1,
                                                product_image2=item.product.product_image2, product_image3=item.product.product_image3, category=item.product.category, price=item.product.get_mrp(),)
        cart.delete()

    return redirect('home')


@login_required(redirect_field_name=None, login_url='login')
def my_orders(request):
    orders = OrderHistory.objects.filter(
        user=request.user).order_by("-date_created")
    return render(request, "my_orders.html", {'orders': orders})


def razorpay(request, amount):
    data = {"amount": amount, "currency": "INR", "receipt": "order_rcptid_11"}
    payment = razorpay_client.order.create(data=data)
    key = settings.RAZOR_KEY_ID
    payment_id = payment['id']
    return key, payment_id


@login_required(redirect_field_name=None, login_url='login')
def cart_checkout(request):
    try:
        cart_item = CartItem.objects.filter(user=request.user)
    except:
        messages.error(request, 'there is no item for checkout')
        return redirect('cart_page')
    selected_address = ""
    address_bool = False
    try:
        try:
            address_id = request.session['address']
            request.session['selected_address'] = address_id
            address_bool = True
            del request.session['address']
            selected_address = Address.objects.get(id=address_id)
        except:
            address = request.session['address']
            request.session['selected_address'] = address_id
            del request.session['address']
            selected_address = Address.objects.get(id=address_id)
    except:
        pass
    form = AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('address')
        else:
            messages.error(request, 'please enter a valid form')
            return redirect('address')
    user = request.user
    try:
        cart_item = CartItem.objects.filter(user=user)
        if not cart_item:
            messages.error(request, "no product for checkout")
            return redirect('cart_page')
    except:
        return redirect('shop')
    sum = 0
    for item in cart_item:
        total = item.sub_total()
        sum = sum+total
    addresses = Address.objects.filter(user=user)
    amount = int(sum*100)
    key, payment_id = razorpay(request, amount)
    buynow = False
    context = {
        "payment_id": payment_id,
        "key": key,
        "form": form,
        "addresses": addresses,
        "cart_item": cart_item,
        "sum": sum,
        "selected_address": selected_address,
        "amount": amount,
        "address_bool": address_bool,
        "buynow": buynow
    }
    return render(request, "checkout.html", context)


@login_required(redirect_field_name=None, login_url='login')
def buynow(request, product_id):
    buynow = True
    request.session['product_id'] = product_id
    request.session['buynow'] = buynow
    id = request.user.id
    user = User.objects.get(id=id)
    product = Product.objects.get(id=product_id)
    sum = product.get_mrp()
    quantity = 1
    selected_address = ""
    address_bool = False
    try:
        try:
            address_id = request.session['address']
            request.session['selected_address'] = address_id
            address_bool = True
            del request.session['address']
            selected_address = Address.objects.get(id=address_id)
        except:
            address = request.session['address']
            request.session['selected_address'] = address_id
            del request.session['address']
            selected_address = Address.objects.get(id=address_id)
    except:
        pass
    form = AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('address')
        else:

            messages.error(request, 'please enter a valid form')
            return redirect('address')
    user = request.user
    addresses = Address.objects.filter(user=user)

    amount = int(sum*100)
    key, payment_id = razorpay(request, amount)
    context = {
        "payment_id": payment_id,
        "key": key,
        "form": form,
        "addresses": addresses,
        "sum": sum,
        "selected_address": selected_address,
        "amount": amount,
        "address_bool": address_bool,
        "buynow": buynow,
        "product": product,
        "quantity": quantity,
    }
    return render(request, "checkout.html", context)


@login_required(redirect_field_name=None, login_url='login')
def address_checkout_with_id(request, id):
    request.session['address'] = id
    try:
        buynow = request.session['buynow']
        product_id = request.session['product_id']
    except:
        buynow = False
    buynow = False
    if buynow:
        return redirect('buynow', product_id)
    else:
        return redirect('cart_checkout')


@login_required(redirect_field_name=None, login_url='login')
def address_checkout(request):
    try:
        buynow = request.session['buynow']
        product_id = request.session['product_id']
    except:
        buynow = False

    if buynow:
        if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                labelled_as = address.labelled_as

                if Address.objects.filter(user=request.user, labelled_as=labelled_as).exists():
                    messages.error(request, 'this address already exists')
                    return redirect('buynow', product_id)
                else:
                    address.user = request.user
                    address.save()
                    address = Address.objects.get(
                        user=request.user, labelled_as=labelled_as)
                    request.session['address'] = address.id
                    return redirect('buynow', product_id)
            else:
                messages.error(request, 'please enter a valid form')
                return redirect('buynow', product_id)
    else:
        if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                labelled_as = address.labelled_as
                if Address.objects.filter(user=request.user, labelled_as=labelled_as).exists():
                    messages.error(request, 'this address already exists')
                    return redirect('cart_checkout')
                else:
                    address.user = request.user
                    address.save()
                    address = Address.objects.get(
                        user=request.user, labelled_as=labelled_as)
                    request.session['address'] = address.id
                    return redirect('cart_checkout')
            else:
                messages.error(request, 'please enter a valid form')
                return redirect('cart_checkout')


@login_required(redirect_field_name=None, login_url='login')
def order(request):
    try:
        cart = CartItem.objects.get(user=request.user)
    except:
        messages.error(request, "no product for checkout")
        return redirect('cart_page')
    for item in cart:
        order = OrderHistory.objects.create(user=request.user, product_name=item.product.product_name, product_quantity=1, product_image1=item.product.product_image1,
                                            product_image2=item.product.product_image2, product_image3=item.product.product_image3, category=item.product.category, price=item.product.product_price,)
