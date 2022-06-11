from django import forms
from user.models import User


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        "onkeypress": "return /[a-z]/i.test(event.key) ",
        'style': "margin:0px auto;width:100%",
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        "onkeypress": "return /[a-z]/i.test(event.key)",
        'style': "margin:0px auto;width:100%",
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "onkeydown": "javascript:checkContents(this)",
        'style': "margin:0px auto;width:100%",
        'class': 'form-control',
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "oninput": "this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*)\./g, '$1');",
        "maxlength": "10",
        'style': "margin:0px auto;width:100%",
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control ',
        'style': "margin:0px auto;width:100%",
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style': "margin:0px auto;width:100%",
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'style': "margin:0px auto;width:100%",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'style': "margin:0px auto;width:100%",
    }))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email",
                  "phone_number", "city", "state", "password", ]
    
    def store(self,request):
        first_name = self.cleaned_data['first_name']
        request.session['first_name'] = first_name
        last_name = self.cleaned_data['last_name']
        request.session['last_name'] = last_name
        phone_number = self.cleaned_data['phone_number']
        email = self.cleaned_data['email']
        request.session['email'] = email
        password = self.cleaned_data['password']
        request.session['password'] = password
        username = self.cleaned_data['username']
        request.session['username'] = username
        request.session['phone_number'] = phone_number
        city = self.cleaned_data['city']
        request.session['city'] = city
        state = self.cleaned_data['state']
        request.session['state'] = state



class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password", ]


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'phone_number', 'profile_img', 'state', 'city']
