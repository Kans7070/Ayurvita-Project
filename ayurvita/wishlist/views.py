from django.shortcuts import render, redirect
from matplotlib.style import context
from wishlist.models import WishList
from user.models import User
from shop.models import Product
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(redirect_field_name=None, login_url='login')
def wishlist_page(request):
    try:
        del request.session['shops']
    except:
        pass
    try:
        del request.session['shop-detail']
    except:
        pass
    id = request.user.id
    wishlist_item = WishList.objects.filter(user=id)
    context = {
        'wishlist_item': wishlist_item
    }
    if request.user.is_authenticated:

        return render(request, 'wishlist.html', context)
    else:
        return redirect('login')


@login_required(redirect_field_name=None, login_url='login')
def add_to_wishlist(request, product_id):
    id = request.user.id
    user = User.objects.get(id=id)
    product = Product.objects.get(id=product_id)
    wishlist_item = WishList.objects.create(
        product=product, user=request.user)
    wishlist_item.save()
    if request.session.has_key('shop-detail'):
        return redirect('shop_detail', product_id)
    return redirect('shop')


@login_required(redirect_field_name=None, login_url='login')
def remove_wishlist(request, product_id):
    id = request.user.id
    user = User.objects.get(id=id)
    product = Product.objects.get(id=product_id)
    wishlist_item = WishList.objects.get(user=user, product=product)
    wishlist_item.delete()
    return redirect('shop')
