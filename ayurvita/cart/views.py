from django.shortcuts import render, redirect
from matplotlib.style import context
from cart.models import CartItem
from user.models import User
from shop.models import Product
from django.views.decorators.cache import never_cache
from address.models import Address

# Create your views here.




@never_cache
def cart_page(request):
    try:
        del request.session['shops']
    except:
        pass
    try:
        del request.session['shop-detail']
    except:
        pass
    count=1
    request.session['count']= count
    id = request.user.id
    sum=0
    cart_item = CartItem.objects.filter(user=id)
    for item in cart_item:
        total=item.sub_total()
        sum=sum+total

    # cart_item.save()
    context = {
        'cart_item': cart_item,
        "sum":sum
    }
    if request.user.is_authenticated:
        print(context)
        return render(request, 'cart_page.html', context)
    else:
        return redirect('login')




@never_cache
def add_to_cart(request, product_id):
    id = request.user.id
    user = User.objects.get(id=id)

    product = Product.objects.get(id=product_id)

    is_cart_item_exists = CartItem.objects.filter(
        product=product, user=user).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.get(user=user, product=product)
        cart_item.quantity += 1
        cart_item.save()
        if request.session.has_key('shops'):
            return redirect('shop')
    else:
        cart_item = CartItem.objects.create(
            product=product, quantity=1, user=request.user)
        cart_item.save()
        if request.session.has_key('shop-detail'):
            return redirect('shop_detail',product_id )
    return redirect('cart_page')

@never_cache
def decrease_quantity(request, product_id):
    id = request.user.id
    user = User.objects.get(id=id)
    product = Product.objects.get(id=product_id)
    is_cart_item_exists = CartItem.objects.filter(
        product=product, user=user).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.get(user=user, product=product)
        cart_item.quantity -= 1
    
        if cart_item.quantity==0:
            cart_item.delete()
        else:
            cart_item.save()
    else:
        cart_item = CartItem.objects.create(
            product=product, quantity=1, user=request.user)
        cart_item.save()
    return redirect('cart_page')


@never_cache
def remove_cart(request,product_id):
    id = request.user.id
    user = User.objects.get(id=id)
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(user=user, product=product)
    cart_item.delete()
    return redirect('cart_page')


