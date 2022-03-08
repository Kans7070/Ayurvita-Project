from address.models import Address
from django import forms

class AddressForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={
    "class": "form-control",
    "onkeypress": "return /[a-z]/i.test(event.key) "
    }))

    phone = forms.CharField(widget=forms.TextInput(attrs={
    "class": "form-control",
    "oninput": "this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*)\./g, '$1');",
    "maxlength": "10"
    }))

    labelled_as = forms.CharField(widget=forms.TextInput(attrs={
    "class": "form-control",
    "onkeypress": "return /[a-z]/i.test(event.key) "
    }))

    pin_code = forms.CharField(widget=forms.TextInput(attrs={
    "class": "form-control",
    "oninput": "this.value = this.value.replace(/[^0-9]/g, '').replace(/(\..*)\./g, '$1');",
    "maxlength": "6"
    }))

    address = forms.CharField(widget=forms.Textarea(attrs={
    "class": "form-control",
    "style": "height:100px;width:100%;",
    }))

    class Meta:
        model = Address
        fields=["name","phone","labelled_as","pin_code","address"]