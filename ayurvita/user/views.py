
from django.shortcuts import render, redirect
from matplotlib.style import context
from .form import RegistrationForm, EditForm
from django.contrib import auth, messages
from user.models import User
from shop.models import Product
from user.otp import verify, otp_verify
from cart.models import CartItem
from wishlist.models import WishList
from django.contrib.auth.decorators import login_required



# Create your views here.


def home(request):
    print("Welcome")
    if request.user.is_authenticated:
        id=request.user.id
        cart_item=CartItem.objects.filter(user_id=id)
        product = Product.objects.all()
        for products in product:
            products.mrp=products.get_mrp()
            products.save()
        wishlist_item= WishList.objects.filter(user_id=id)
        context = {
            'product': product,
            'cart_item': cart_item,
            'wishlist_item':wishlist_item,
        }
        return render(request, 'index.html', context)
    else:
        return redirect('login')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']
            
            user = auth.authenticate(username=email, password=password)

            
            if user is not None:
                users=User.objects.get(email=email)
                request.session['id'] = user.id
                request.session['email'] = user.email
                request.session['password'] = user.password
                user_id=user.id
                
                
                auth.login(request, user)
                return redirect('home')
               
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('login')

        return render(request, 'login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = RegistrationForm()
        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            password=request.POST['password']
            print(password)
            password1=request.POST['password1']
            if password1 == password:
                if form.is_valid():
                    first_name = form.cleaned_data['first_name']
                    request.session['first_name'] = first_name
                    last_name = form.cleaned_data['last_name']
                    request.session['last_name'] = last_name
                    phone_number = form.cleaned_data['phone_number']
                    email = form.cleaned_data['email']
                    request.session['email'] = email
                    password = form.cleaned_data['password']
                    request.session['password'] = password
                    username = form.cleaned_data['username']
                    request.session['username'] = username
                    request.session['phone_number'] = phone_number
                    city = form.cleaned_data['city']
                    request.session['city'] = city
                    state = form.cleaned_data['state']
                    request.session['state'] = state
                    otp_verify(phone_number)
                    messages.info(
                        request, 'you were registered then please verify phone number')
                    return redirect('otp')
                else:
                    messages.error(request, 'please enter a valid form')
                    form = RegistrationForm()
                    return redirect('register')
            else:
                messages.error(request, 'passwords given does not match')
                form = RegistrationForm()
                return redirect('register')
        else:
            context = {
                'form': form
            }
            return render(request, 'register.html', context)


def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect('login')
    else:
        return redirect('login')


def otp(request):
    phone_number = request.session['phone_number']
    context = {
        'phone_number': phone_number
    }
    try:
        if request.user.is_authenticated:
            return redirect('home')
        if request.method == 'POST':
            otp = request.POST['otp1']
            phone_number = request.session['phone_number']
            if verify(phone_number,otp):
                first_name = request.session['first_name']
                del request.session['first_name']
                last_name = request.session['last_name']
                del request.session['last_name']
                email = request.session['email']
                username = request.session['username']
                password = request.session['password']
                city = request.session['city']
                state = request.session['state']
                
                user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email,
                                                   username=username, password=password, phone_number=phone_number, city=city, state=state)
                user.save()
                return redirect('login')
            else:
                messages.error(request, 'please enter valid otp')
                
                return redirect('otp')
    except:
        
        pass
    return render(request, 'otp.html', context)


def change_password(request):
    mobile= request.session['mobile']
    if request.method == 'POST':
        password= request.POST['password1']
        password2= request.POST['password2']
        if password2 == password:
            user=User.objects.get(phone_number=mobile)
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            messages.error(request,'entered password is not same')
            return redirect('change_password')
    return render(request, 'change_password_otp.html')


def change_password_mobile(request):
    if request.method == 'POST':
        mobile = request.POST['mobile']
        request.session['mobile']= mobile
        if User.objects.get(phone_number=mobile):
            otp_verify(mobile)
            return redirect('change_password_OTP')
        else:
            messages.error(request, 'You are new,Try again by using already registered phone number.')
            return redirect('change_password')
    else:
        return render(request, 'mobile_otp_change_password.html')


def change_password_OTP(request):
    mobile = request.session['mobile']
    context = {
        'mobile' : mobile
    }
    if request.method == 'POST':
        otp = request.POST['otp1']
        if verify(mobile,otp):
            return redirect('change_password')
    else:    
        return render(request, 'otp_for_change_password.html',context)


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html')
    else:
        return redirect('login')


def edit_profile(request, id):
    form=EditForm(request.POST)
    list_user = User.objects.get(id=id)
    form = EditForm(instance=list_user)
    context = {
        'form': form,
        'id' :id
    }
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES, instance=list_user)
        
        if form.is_valid():
            
            form.save()
            return redirect('profile')

    return render(request, 'edit_profile.html', context)


def change_password_profile(request, id):
    if request.method == 'POST':
        password = request.POST['current_password']
        user=User.objects.get(id=id)
        
        if auth.authenticate(username=user.email,password=password):
            new_password=request.POST['password']
            password1=request.POST['password1']
            if new_password == password1:
                user.set_password(new_password)
                user.save()
                auth.login(request, user )
                return redirect('profile')
            else:
                messages.error(request, 'give same password')
                return redirect('change_password_profile')
        else:
            messages.error(request, 'wrong password')
            return redirect('change_password_profile')
    else:
        return render(request, 'change_password.html')


def resent_register_otp(request):
    phone_number = request.session['phone_number']
    otp_verify(phone_number)
    return redirect('otp')


def resent_change_password_otp(request):
    phone_number = request.session['phone_number']
    otp_verify(phone_number)
    return redirect('change_password_OTP')


