from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import OrderHistory
from cart.models import CartItem
from address.models import Address
from address.forms import AddressForm
from django.contrib import auth, messages
import razorpay
from ayurvita import settings
from user.models import User
from shop.models import Product


# Create your views here.

razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def pay(request):
    
    user = request.user
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
            messages.error(request,'select or give an address')
            return redirect('buynow',product_id)
        messages.error(request, 'select or give an address')
        return redirect('cart_checkout')
    order_id = request.session['order_id']
    OrderHistory.objects.filter(id=order_id).update(payment=True)
    
    try:
        del request.session['order_id']
    except:
        pass
    cart_item = CartItem.objects.filter(user=user)

    cart_item.delete()
    return redirect('home')


def my_orders(request):
    orders = OrderHistory.objects.filter(
        user=request.user,payment=True).order_by("-date_created")
    return render(request, "my_orders.html", {'orders': orders})


def razorpay(request,amount):
    data = {"amount": amount, "currency": "INR", "receipt": "order_rcptid_11"}
    payment = razorpay_client.order.create(data=data)
    key = settings.RAZOR_KEY_ID
    payment_id = payment['id']
    return key,payment_id

def cart_checkout(request):
    buynow=False  
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
    except:
        return redirect('shop')


    sum = 0
    for item in cart_item:
        total = item.sub_total()
        sum = sum+total


    addresses = Address.objects.filter(user=user)
    

    
    count = request.session['count']
    if count == 1:
        orders = OrderHistory.objects.all()
        cart_item = CartItem.objects.filter(user=user)

        for items in cart_item:
            
            order = orders.create(user=user, product_name=items.product.product_name, product_quantity=items.quantity, product_image1=items.product.product_image1,
                                product_image2=items.product.product_image2, product_image3=items.product.product_image3, category=items.product.category, price=sum,)
        count = 0
        request.session['count'] = count

    try:
        order_id = order.id
    except:
        messages.error(request,"no product for checkout")
        return redirect('cart_page')

    request.session['order_id'] = order_id
    

    amount = int(sum*100)
    key,payment_id=razorpay(request,amount)
    buynow=False
    context = {
        "payment_id": payment_id,
        "key": key,
        "form": form,
        "addresses": addresses,
        "cart_item": cart_item,
        "sum": sum,
        "selected_address": selected_address,
        "order_id": order_id,
        "amount": amount,
        "address_bool": address_bool,
        "buynow":buynow
    }
    return render(request, "checkout.html", context)




def buynow(request,product_id):
    buynow=True
    request.session['product_id'] = product_id
    request.session['buynow'] = buynow
    id = request.user.id
    user = User.objects.get(id=id)
    product = Product.objects.get(id=product_id)
    orders=OrderHistory.objects.all()
    sum=product.get_mrp()
    try:
        count=request.session['count']

    except:
        count = 0
    count=0
    if count==0:
        order=orders.create(user=user, product_name=product.product_name, product_quantity=1, product_image1=product.product_image1,
                                product_image2=product.product_image2, product_image3=product.product_image3, category=product.category, price=sum,)
        count=+1
        request.session['count']= count
    print(order.id)
   
    order_id = order.id        
    request.session['order_id'] = order_id
    order = OrderHistory.objects.get(id=order_id)
    quantity = order.product_quantity
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
    key,payment_id=razorpay(request,amount)
    context = {
        "payment_id": payment_id,
        "key": key,
        "form": form,
        "addresses": addresses,
        "sum": sum,
        "selected_address": selected_address,
        "order_id": order_id,
        "amount": amount,
        "address_bool": address_bool,
        "buynow":buynow,
        "product": product,
        "quantity": quantity,
    }
    return render(request, "checkout.html", context)


def address_checkout_with_id(request, id):
    request.session['address'] = id
    try:
        buynow = request.session['buynow']
        product_id = request.session['product_id']
    except:
        buynow=False
    if buynow:
        return redirect('buynow',product_id)
    else:
        return redirect('cart_checkout')


def address_checkout(request):
    try:
        buynow = request.session['buynow']
        product_id = request.session['product_id']
    except:
        buynow=False

    if buynow:
        if request.method == 'POST':
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                labelled_as = address.labelled_as
                
                if Address.objects.filter(user=request.user, labelled_as=labelled_as).exists():
                    messages.error(request, 'this address already exists')
                    return redirect('buynow',product_id)
                else:
                    address.user = request.user
                    address.save()
                    address = Address.objects.get(
                        user=request.user, labelled_as=labelled_as)
                    request.session['address'] = address.id
                    return redirect('buynow',product_id)
            else:
                messages.error(request, 'please enter a valid form')
                return redirect('buynow',product_id)
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

    