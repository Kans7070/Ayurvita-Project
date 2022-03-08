from django import forms
from user.models import User


class RegistrationForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        "onkeypress": "return /[a-z]/i.test(event.key) ",
        'style':"margin:0px auto",
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        "onkeypress": "return /[a-z]/i.test(event.key)",
        'style':"margin:0px auto",
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        "onkeydown": "javascript:checkContents(this)",
        'style':"margin:0px auto",
        'class': 'form-control',
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        "oninput": "this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*)\./g, '$1');",
        "maxlength": "10",
        'style':"margin:0px auto",
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={

        'class': 'form-control ',
        'style':"margin:0px auto",
    }))
    city = forms.CharField(widget=forms.TextInput(attrs={

        'class': 'form-control',
        'style':"margin:0px auto",
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={

        'class': 'form-control',
        'style':"margin:0px auto",
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={

        'class': 'form-control',
        'style':"margin:0px auto",
    }))

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email",
                  "phone_number", "city", "state", "password", ]


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password", ]


class EditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','phone_number','profile_img','state','city']