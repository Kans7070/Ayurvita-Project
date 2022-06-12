from django.shortcuts import render,redirect
from address.forms import AddressForm
from address.models import Address
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(redirect_field_name=None, login_url='login')
def address(request):
    form = AddressForm()
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address=form.save(commit=False)
            labelled_as=address.labelled_as
            if Address.objects.filter(user=request.user,labelled_as=labelled_as).exists():
                messages.error(request,'this address already exists')
                return redirect('cart_checkout')
            else:
                address.user = request.user
                address.save()
             
            return redirect('address')
        else:
            
            messages.error(request, 'please enter a valid form')  
            return redirect('address')
    user=request.user
    addresses=Address.objects.filter(user=user)
    context = {
        "form": form,
        "addresses": addresses
    }
    return render(request, 'address.html',context)

@login_required(redirect_field_name=None, login_url='login')
def delete_address(request,id):
    address = Address.objects.get(id=id,user=request.user)
    address.delete()
    return redirect('address')