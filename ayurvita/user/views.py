from django.shortcuts import render, redirect
from .form import RegistrationForm, EditForm
from django.contrib import auth, messages
from user.models import User
from shop.models import Product
from user.otp import verify, otp_verify
from cart.models import CartItem
from wishlist.models import WishList
from django.contrib.auth.decorators import login_required


# Create your views here.


def create_user(request):
    User.objects.create_user(
        first_name=request.session['first_name'],
        last_name=request.session['last_name'],
        email=request.session['email'],
        username=request.session['username'],
        password=request.session['password'],
        phone_number=request.session['phone_number'],
        city=request.session['city'],
        state=request.session['state']
    )


def home(request):
    products = Product.objects.all()
    try:
        cart_item = CartItem.objects.filter(user_id=request.user.id)
    except:
        cart_item = ''
    try:
        wishlist_item = WishList.objects.filter(user_id=request.user.id)
    except:
        wishlist_item = ''
    context = {
        'products': products,
        'cart_item': cart_item,
        'wishlist_item': wishlist_item,
    }
    return render(request, 'index.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        user = auth.authenticate(
            email=request.POST['email'], password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if request.POST['password'] == request.POST['password1']:
            if form.is_valid():
                form.store(request)
                otp_verify(form.cleaned_data['phone_number'])
                messages.info(
                    request, 'you were registered then please verify phone number')
                return redirect('otp')
        else:
            messages.error(request, 'passwords given does not match')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


@login_required(redirect_field_name=None, login_url='login')
def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('login')
    else:
        return redirect('login')


def otp(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        if verify(request.session['phone_number'], request.POST['otp']):
            create_user(request)
            return redirect('login')
        else:
            messages.error(request, 'please enter valid otp')
    return render(request, 'otp.html')


def change_password_mobile(request):
    if request.method == 'POST':
        request.session['phone_number'] = request.POST['phone_number']
        if User.objects.get(phone_number=request.POST['phone_number']):
            otp_verify(request.POST['phone_number'])
            return redirect('change_password_OTP')
        else:
            messages.error(
                request, 'You are new,Try again by using already registered phone number.')
    return render(request, 'mobile_otp_change_password.html')


def change_password_OTP(request):
    if request.method == 'POST':
        if verify(request.session['phone_number'], request.POST['otp']):
            return redirect('change_password')
    return render(request, 'otp.html')


def change_password(request):
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            user = User.objects.get(
                phone_number=request.session['phone_number'])
            user.set_password(request.POST['password'])
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'entered password is not same')
    return render(request, 'change_password_otp.html')


@login_required(redirect_field_name=None, login_url='login')
def profile(request):
    return render(request, 'profile.html')


@login_required(redirect_field_name=None, login_url='login')
def edit_profile(request, id):
    form = EditForm(instance=User.objects.get(id=id))
    context = {
        'form': form,
    }
    if request.method == 'POST':
        form = EditForm(
            request.POST,
            request.FILES,
            instance=User.objects.get(id=id)
        )
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'edit_profile.html', context)


@login_required(redirect_field_name=None, login_url='login')
def change_password_profile(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        if auth.authenticate(username=user.email, password=request.POST['current_password']):
            if request.POST['password'] == request.POST['password1']:
                user.set_password(request.POST['password'])
                user.save()
                auth.login(request, user)
                return redirect('profile')
            else:
                messages.error(request, 'give same password')
        else:
            messages.error(request, 'wrong password')
    return render(request, 'change_password.html')


def resent_register_otp(request):
    request.session['phone_number']
    otp_verify(request.session['phone_number'])
    return redirect('otp')


def resent_change_password_otp(request):
    otp_verify(request.session['phone_number'])
    return redirect('change_password_OTP')
