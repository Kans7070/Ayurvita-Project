from django.shortcuts import render, redirect
from user.views import home
from user.models import User
from shop.models import Product
from django.contrib import auth, messages
from category.models import Category
from .form import ProductUpdate, AddProduct, AddCategoryForm, EditCategoryForm, AddCategoryOfferForm, AddProductOfferForm
from order.models import OrderHistory
from offers.models import ProductOffer, CategoryOffer
from django.contrib.auth.decorators import login_required

# Create your views here.


def admin_login(request):
    try:
        if not request.user.is_admin:
            return redirect(home)
    except:
        pass                    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        admin = auth.authenticate(
            username=email, password=password)
        if admin is not None:
            if admin.is_admin:
                auth.login(request, admin)
                request.session['admin'] = admin.id
                return redirect('admin')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('admin_login')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('admin_login')
    else:
        return render(request, 'admin_login.html')


@login_required(redirect_field_name=None, login_url='admin_login')
def admin(request):
    if not request.user.is_admin:
        return redirect(home)
    return render(request, 'admin.html')


@login_required(redirect_field_name=None, login_url='admin_login')
def users(request):
    if not request.user.is_admin:
        return redirect(home)
    user = User.objects.all()
    context = {
        'user': user
    }
    return render(request, 'admin_pages/Users.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def product(request):
    if not request.user.is_admin:
        return redirect(home)
    products = Product.objects.all()
    context = {
        'product': products
    }
    return render(request, 'admin_pages/product.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def admin_logout(request):
    if not request.user.is_admin:
        return redirect(home)
    auth.logout(request)
    return redirect('admin')


@login_required(redirect_field_name=None, login_url='admin_login')
def admin_category(request):
    if not request.user.is_admin:
        return redirect(home)
    CategoryList = Category.objects.all()
    context = {
        'CategoryList': CategoryList
    }
    return render(request, 'admin_pages/category.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def user_view(request, id):
    if not request.user.is_admin:
        return redirect(home)
    users = User.objects.get(id=id)
    context = {
        'user': users
    }
    return render(request, 'admin_pages/profile.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def user_block(request, id):
    if not request.user.is_admin:
        return redirect(home)
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    return redirect('users')


@login_required(redirect_field_name=None, login_url='admin_login')
def user_unblock(request, id):
    if not request.user.is_admin:
        return redirect(home)
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect('users')


@login_required(redirect_field_name=None, login_url='admin_login')
def add_product(request):
    if not request.user.is_admin:
        return redirect(home)
    if request.method == 'POST':
        form = AddProduct(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product')
        else:
            messages.error(request, "product invalid")
            return redirect('add_product')
    form = AddProduct()
    context = {
        'form': form,
        'title':'Add products'
    }
    return render(request, 'admin_pages/form.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def edit_product(request, id):
    if not request.user.is_admin:
        return redirect(home)
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductUpdate(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product')
    form = ProductUpdate(instance=product)
    context = {
        'form': form,
        'title':'Edit products'
    }
    return render(request, 'admin_pages/form.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def delete_product(request, id):
    if not request.user.is_admin:
        return redirect(home)
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('product')


@login_required(redirect_field_name=None, login_url='admin_login')
def add_category(request):
    if not request.user.is_admin:
        return redirect(home)
    form = AddCategoryForm()
    if request.method == 'POST':
        form = AddCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_category')
        else:
            messages.error(request, "product invalid")
            return redirect('add_category')
    context = {
        'form': form,
        'title':'Add category'
    }
    return render(request, 'admin_pages/form.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def delete_category(request, id):
    if not request.user.is_admin:
        return redirect(home)
    product = Category.objects.get(id=id)
    product.delete()
    return redirect('admin_category')


@login_required(redirect_field_name=None, login_url='admin_login')
def edit_category(request, id):
    if not request.user.is_admin:
        return redirect(home)
    category = Category.objects.get(id=id)
    form = EditCategoryForm(instance=category)
    if request.method == 'POST':
        form = EditCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_category')
    context = {
        'form': form,
        'title':'Edit Category'
    }
    return render(request, 'admin_pages/form.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def orders_history(request):
    if not request.user.is_admin:
        return redirect(home)
    orders = OrderHistory.objects.all()
    context = {
        "orders": orders
    }
    return render(request, 'admin_pages/orders_history.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def offers(request):
    if not request.user.is_admin:
        return redirect(home)
    product_offers = ProductOffer.objects.all()
    category_offers = CategoryOffer.objects.all()
    context = {
        "product_offers": product_offers,
        "category_offers": category_offers
    }
    return render(request, 'admin_pages/offers.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def edit_product_offers(request, id):
    if not request.user.is_admin:
        return redirect(home)
    product_offer = ProductOffer.objects.get(id=id)
    form = AddProductOfferForm(instance=product_offer)
    if request.method == 'POST':
        form = AddProductOfferForm(request.POST, instance=product_offer)
        if form.is_valid():
            form.save()
            return redirect('offers')
    context = {
        'form': form,
        'title':'Edit product'
    }
    return render(request, 'admin_pages/form.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def edit_category_offers(request, id):
    if not request.user.is_admin:
        return redirect(home)
    form = AddCategoryOfferForm(request.POST)
    category_offer = CategoryOffer.objects.get(id=id)
    form = AddCategoryOfferForm(instance=category_offer)
    if request.method == 'POST':
        form = AddCategoryOfferForm(request.POST, instance=category_offer)
        if form.is_valid():
            form.save()
            return redirect('offers')
    context = {
        'form': form,
        'title':'Edit Category'
    }
    return render(request, 'admin_pages/form.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def add_product_offer(request):
    if not request.user.is_admin:
        return redirect(home)
    form = AddProductOfferForm()
    if request.method == 'POST':
        form = AddProductOfferForm(request.POST)
        product = request.POST['product']
        if ProductOffer.objects.filter(product=product).exists():
            messages.error(
                request, "offer for this product is already available")
            return redirect('add_product_offer')
        else:
            if form.is_valid():
                form.save()
                return redirect('offers')
            else:
                messages.error(request, "offer is not added")
                return redirect('add_product_offer')
    context = {
        'form': form,
        'title':'Add Product Offers'
    }
    return render(request, 'admin_pages/form.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def add_category_offer(request):
    if not request.user.is_admin:
        return redirect(home)
    form = AddCategoryOfferForm()
    if request.method == 'POST':
        form = AddCategoryOfferForm(request.POST)
        category = request.POST['category']
        if CategoryOffer.objects.filter(category=category).exists():
            messages.error(
                request, "offer for this category is already exists")
            return redirect('add_category_offer')
        else:
            if form.is_valid():
                form.save()
                return redirect('offers')
            else:
                messages.error(request, "form is not valid")
                return redirect('add_category_offer')
    context = {
        'form': form,
        'title':'Add Category Offer'
    }
    return render(request, 'admin_pages/form.html', context)


@login_required(redirect_field_name=None, login_url='admin_login')
def delete_offer(request, id):
    if not request.user.is_admin:
        return redirect(home)
    try:
        product = Product.objects.get(id=id)
        product_offer = ProductOffer.objects.get(product=product)
        product.is_deleted = True
        product_offer.save()
    except:
        category = Category.objects.get(id=id)
        category_offer = CategoryOffer.objects.get(category=category)
        category_offer.is_deleted = True
        category_offer.save()
    return redirect('offers')
