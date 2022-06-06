from ast import Break
from django.shortcuts import render, redirect
from shop.models import Product, ShopWelcome
from category.models import Category
from cart.models import CartItem
from wishlist.models import WishList
from offers.models import ProductOffer,CategoryOffer


# Create your views here.


def shop(request):
    product_discount,category_discount,discount="","",""
    try:
        del request.session['shop-detail']
    except:
        pass
    if request.user.is_authenticated:
        try:
            product_id = request.session['product']
            del request.session['product']
            product = Product.objects.filter(id=product_id)
            try:
                try:
                    offer= ProductOffer.objects.get(product=product)
                    product_discount=offer.discount
                    offer=CategoryOffer.objects.get(category=product.category)
                    category_discount=offer.discount
                except:
                    offer=CategoryOffer.objects.get(category=product.category)
                    category_discount=offer.discount
            except:  
                pass
            if product_discount:
                if category_discount:
                    if product_discount>category_discount:
                        discount=product_discount
                    else:
                        discount=category_discount
                else:
                    discount=product_discount
            else:
                discount=category_discount
            product_count = product.count()
            category = Category.objects.all()
            welcome = ShopWelcome.objects.all()
            request.session['shops']='shops'
            user=request.user
            wishlist_item= WishList.objects.filter(user=user)
            context = {
                'product': product,
                'product_count': product_count,
                'category': category,
                'welcome': welcome,
                'wishlist_item': wishlist_item,
                'discount': discount,
            }
            return render(request, 'shop.html', context)
        except:
            try:
                category = request.session['category']
                del request.session['category']
                product = Product.objects.filter(category=category)
                try:
                    try:
                        offer= ProductOffer.objects.get(product=product)
                        product_discount=offer.discount
                        offer=CategoryOffer.objects.get(category=product.category)
                        category_discount=offer.discount
                    except:
                        offer=CategoryOffer.objects.get(category=product.category)
                        category_discount=offer.discount
                except:  
                    pass
                if product_discount:
                    if category_discount:
                        if product_discount>category_discount:
                            discount=product_discount
                        else:
                            discount=category_discount
                    else:
                        discount=product_discount
                else:
                    discount=category_discount
                product_count = product.count()
                category = Category.objects.all()
                welcome = ShopWelcome.objects.get(id=1)
                request.session['shops']='shops'
                user=request.user
                wishlist_item= WishList.objects.filter(user=user)
                context = {
                    'product': product,
                    'product_count': product_count,
                    'category': category,
                    'welcome': welcome,
                    'wishlist_item': wishlist_item,               
                    'discount': discount,
                }
                return render(request, 'shop.html', context)
            except:
                try:
                    high_low=request.session['high_low']
                except:
                    high_low=False
                try:
                    low_high=request.session['low_high']
                except:
                    low_high=False
                if high_low:
                    products = Product.objects.all().order_by("-product_price")
                elif low_high:
                    products = Product.objects.all().order_by("product_price")
                else:
                    products = Product.objects.all()
                for product in products:
                    try:
                        try:
                            offer= ProductOffer.objects.get(product=product)
                            product_discount=offer.discount
                            offer=CategoryOffer.objects.get(category=product.category)
                            category_discount=offer.discount
                        except:
                            offer=CategoryOffer.objects.get(category=product.category)
                            category_discount=offer.discount
                    except:  
                        pass
                    if product_discount:
                        if category_discount:
                            if product_discount>category_discount:
                                discount=product_discount
                            else:
                                discount=category_discount
                        else:
                            discount=product_discount
                    else:
                        discount=category_discount
                product_count = products.count()
                category = Category.objects.all()
                welcome = ShopWelcome.objects.all()
                request.session['shops']='shops'
                user=request.user
                wishlist_item= WishList.objects.filter(user=user)
                context = {
                    'products': products,
                    'product_count': product_count,
                    'category': category,
                    'welcome': welcome,
                    'wishlist_item': wishlist_item,                
                    'discount':discount,
                    "high_low":high_low,
                    "low_high":low_high
                }
                return render(request, 'shop.html', context)
    else:
        return redirect('login')


def shop_detail(request, id):
    product_discount,category_discount,discount="","",""
    try:
        del request.session['shops']
    except:
        pass
    try:
        del request.session['count']
    except:
        pass
    
    
    request.session['shop-detail'] = 'shop-detail'
    user=request.user
    if request.user.is_authenticated:
        cart_item=CartItem.objects.filter(user=user)
        product = Product.objects.get(id=id)   
        try:
            try:
                offer= ProductOffer.objects.get(product=product)
                product_discount=offer.discount
                offer=CategoryOffer.objects.get(category=product.category)
                category_discount=offer.discount
            except:
                offer=CategoryOffer.objects.get(category=product.category)
                category_discount=offer.discount
        except:  
            pass
        if product_discount:
            if category_discount:
                if product_discount>category_discount:
                    discount=product_discount
                else:
                    discount=category_discount
            else:
                discount=product_discount
        else:
            discount=category_discount
        go_to_cart=False
        for products in cart_item:
            if products.product.id == product.id:
                go_to_cart=True
                break
            else:
                go_to_cart=False
        price_same=False
        if product.product_price == product.get_mrp():
            price_same=True
        else:
            price_same=False
        context = {
            'product': product,
            'go_to_cart': go_to_cart,
            'price_same': price_same,
            'discount': discount,

        }
        return render(request, 'shop_detail.html', context)
    else:
        return redirect('login')


def search(request):
    if request.method == 'POST':
        item = request.POST['item']
        if item == "":
            return redirect('shop')
        else:
            if Product.objects.filter(product_name=item):
                product = Product.objects.get(product_name=item)
                id = product.id
                return redirect('shop_detail',id)
            elif Category.objects.filter(category_name=item):
                category = Category.objects.get(category_name=item)
                
                product = Product.objects.get(category=category)
                if product:
                    request.session['product'] = product.id
                    return redirect('shop')
                else:
                    not_found = True
            else:
                not_found = True
        if not_found:
            return redirect('product_not_found')
    else:
        return redirect("shop")


def product_not_found(request):
    category = Category.objects.all()
    context = {
        "category": category
    }
    return render(request,"product_not_found.html",context)


def category(request,category_id):
    id=category_id
    category = Category.objects.get(id=id)    
    request.session["category"] = category.id    
    return redirect('shop')


def no_sort(request):
    try:
        del request.session['low_high']
    except:
        pass
    try:
        del request.session['high_low']
    except:
        pass
    return redirect('shop')


def sort(request):
    try:
        del request.session['low_high']
    except:
        pass
    try:
        del request.session['high_low']
    except:
        pass


def price_high_to_low(request):
    sort(request)
    
    request.session['high_low']=True
    return redirect('shop')


def price_low_to_high(request):
    sort(request)
    request.session['low_high']=True
    return redirect('shop')

