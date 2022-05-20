from calendar import c
from django.shortcuts import render, redirect
from user.models import User
from shop.models import Product
from django.contrib import auth, messages
from category.models import Category
from .form import ProductUpdate,AddProduct,AddCategoryForm,EditCategoryForm,AddCategoryOfferForm,AddProductOfferForm
from order.models import OrderHistory
from offers.models import ProductOffer,CategoryOffer

# Create your views here.


def admin_login(request):
    if request.user.is_authenticated:
        return redirect('admin')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            
            admin = auth.authenticate(
                username=email, password=password)
            if admin is not None:
		if admin.is_admin:
                	auth.login(request, admin)
                	return redirect('admin')
		else:
			messages.error(request,'Invalid credentials')
			return redirect('admin_login')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('admin_login')
        else:
            return render(request, 'admin_login.html')


def admin(request):
    if request.user.is_authenticated:
        return render(request, 'admin.html')
    else:
        return redirect('admin_login')


def users(request):
    user = User.objects.all()
    context = {
        'user': user
    }
    return render(request, 'admin_pages/Users.html', context)


def product(request):
    products = Product.objects.all()
    context = {
        'product': products
    }
    return render(request, 'admin_pages/product.html', context)


def admin_logout(request):
    auth.logout(request)
    return redirect('admin')


def admin_category(request):
    CategoryList = Category.objects.all()
    context = {
        'CategoryList' : CategoryList
    }
    return render(request, 'admin_pages/category.html', context)


def user_view(request,id):
    users=User.objects.get(id=id)
    context = {
        'user':users
    }
    return render(request, 'admin_pages/profile.html', context)


def user_block(request,id):
    user=User.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect('users')


def user_unblock(request,id):
    user=User.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect('users')


def add_product(request):
    form=AddProduct()
    context={
        'form':form
    }
    if request.method == 'POST':
        form=AddProduct(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product')
        else:
            messages.error(request, "product invalid")
            return redirect('add_product')
    return render(request, 'admin_pages/add_product.html',context)



def edit_product(request,id):
    form=ProductUpdate(request.POST)
    product=Product.objects.get(id=id)
    form=ProductUpdate(instance=product)
    context = {
        'form': form,
        'id' : id
    }
    if request.method == 'POST':
        form = ProductUpdate(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            
            form.save()
            return redirect('product')

    return render(request, 'admin_pages/edit_product.html', context)


def delete_product(request,id):
    product=Product.objects.get(id=id)
    product.delete()
    return redirect('product')


def add_category(request):
    form=AddCategoryForm()
    context={
        'form':form
    }
    if request.method == 'POST':
        form=AddCategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('admin_category')
        else:
            messages.error(request, "product invalid")
            return redirect('add_category')
    return render(request, 'admin_pages/add_category.html',context)


def delete_category(request,id):
    product=Category.objects.get(id=id)
    product.delete()
    return redirect('admin_category')


def edit_category(request,id):
    form=EditCategoryForm(request.POST)
    category=Category.objects.get(id=id)
    form=EditCategoryForm(instance=category)
    context = {
        'form': form,
        'id' : id
    }
    if request.method == 'POST':
        form = EditCategoryForm(request.POST, instance=category)
        
        if form.is_valid():
            
            form.save()
            return redirect('admin_category')

    return render(request, 'admin_pages/edit_category.html', context)


def orders_history(request):
    orders=OrderHistory.objects.all()
    context={
        "orders": orders
    }
    return render(request, 'admin_pages/orders_history.html',context)


def offers(request):
    product_offers=ProductOffer.objects.all()
    category_offers=CategoryOffer.objects.all()
    context={
        "product_offers": product_offers,
        "category_offers": category_offers
    }
    return render(request, 'admin_pages/offers.html',context)


def edit_product_offers(request,id):
    form=AddProductOfferForm(request.POST)
    product_offer=ProductOffer.objects.get(id=id)
    form=AddProductOfferForm(instance=product_offer)
    context = {
        'form': form,
        'id' : id
    }
    if request.method == 'POST':
        form = AddProductOfferForm(request.POST, instance=product_offer)
        
        if form.is_valid():
            
            form.save()
            return redirect('offers')

    return render(request, 'admin_pages/edit_product_offer.html', context)


def edit_category_offers(request,id):
    form=AddCategoryOfferForm(request.POST)
    category_offer=CategoryOffer.objects.get(id=id)
    form=AddCategoryOfferForm(instance=category_offer)
    context = {
        'form': form,
        'id' : id
    }
    if request.method == 'POST':
        form = AddCategoryOfferForm(request.POST, instance=category_offer)
        
        if form.is_valid():
            
            form.save()
            return redirect('offers')

    return render(request, 'admin_pages/edit_category_offer.html', context)


def add_product_offer(request):
    form=AddProductOfferForm()
    context={
        'form':form
    }
    if request.method == 'POST':
        form=AddProductOfferForm(request.POST)
        product=request.POST['product']
        if ProductOffer.objects.filter(product=product).exists():
            messages.error(request,"offer for this product is already available")
            return redirect('add_product_offer')
        else:
            if form.is_valid():
                form.save()
                return redirect('offers')
            else:
                messages.error(request, "offer is not added")
                return redirect('add_product_offer')
    return render(request, 'admin_pages/add_product_offer.html',context)
   



def add_category_offer(request):
    form=AddCategoryOfferForm()
    context={
        'form':form
    }
    if request.method == 'POST':
        form=AddCategoryOfferForm(request.POST)
        category = request.POST['category']
        if CategoryOffer.objects.filter(category=category).exists():
            messages.error(request, "offer for this category is already exists")
            return redirect('add_category_offer')
        else:
            if form.is_valid():
                form.save()
                return redirect('offers')
            else:
                messages.error(request, "form is not valid")
                return redirect('add_category_offer')
    else:
        return render(request, 'admin_pages/add_category_offer.html',context)


def delete_offer(request,id):
    try:     
        product = Product.objects.get(id=id)
        product_offer=ProductOffer.objects.get(product=product)
        product.is_deleted=True
        product_offer.save()
    except:
        category= Category.objects.get(id=id)
        category_offer=CategoryOffer.objects.get(category=category)
        category_offer.is_deleted=True
        category_offer.save()
    return redirect('offers')


