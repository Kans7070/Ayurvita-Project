from ast import Break
from math import prod
from django.shortcuts import render, redirect
from shop.models import Product, ShopWelcome
from category.models import Category
from cart.models import CartItem
from wishlist.models import WishList
from offers.models import ProductOffer, CategoryOffer


# Create your views here.


def shop(request):
    try:
        del request.session['shop-detail']
    except:
        request.session['shops'] = 'shops'
    try:
        wishlist_item = WishList.objects.filter(user=request.user)
    except:
        wishlist_item = None
    try:
        category_id = request.session['category']
        category = Category.objects.get(id=category_id)
        del request.session['category']
        products = Product.objects.filter(category=category)
    except:
        products = Product.objects.all()
    category = Category.objects.all()
    context = {
        'products': products,
        'category': category,
        'wishlist_item': wishlist_item,
    }
    return render(request, 'shop.html', context)


def shop_detail(request, id):
    try:
        del request.session['shops']
    except:
        request.session['shop-detail'] = 'shop-detail'
    try:
        del request.session['count']
    except:
        pass
    try:
        cart_item = CartItem.objects.filter(user=request.user)
        for products in cart_item:
            if products.product.id == product.id:
                go_to_cart = True
                break
            else:
                go_to_cart = False
    except:
        cart_item = None
        go_to_cart = False
    product = Product.objects.get(id=id)
    context = {
        'product': product,
        'go_to_cart': go_to_cart,
    }
    return render(request, 'shop_detail.html', context)


def search(request):
    if request.method == 'POST':
        if request.POST['item'] == "":
            return redirect('shop')
        else:
            if Product.objects.filter(product_name=request.POST['item']):
                product = Product.objects.get(
                    product_name=request.POST['item'])
                return redirect('shop_detail', product.id)
            elif Category.objects.filter(category_name=request.POST['item']):
                category = Category.objects.get(
                    category_name=request.POST['item'])
                request.session['category'] = category.id
            else:
                return redirect('product_not_found')
    return redirect("shop")


def product_not_found(request):
    category = Category.objects.all()
    context = {
        "category": category
    }
    return render(request, "shop.html", context)


def category(request, category_id):
    id = category_id
    category = Category.objects.get(id=id)
    request.session["category"] = category.id
    return redirect('shop')
