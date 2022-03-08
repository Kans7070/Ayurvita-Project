from django import forms
from shop.models import Product
from category.models import Category
from offers.models import ProductOffer,CategoryOffer


class ProductUpdate(forms.ModelForm):

    class Meta:
        model = Product
        fields=["product_name","product_desc","category","quantity","brand","product_price","product_image1","product_image2","product_image3"]


class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields=["product_name","product_desc","category","quantity","brand","product_price","product_image1","product_image2", "product_image3"]


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields=["category_name","category_desc"]


class AddCategoryOfferForm(forms.ModelForm):
    class Meta:
        model = CategoryOffer
        fields=["category","discount","is_active"]


class AddProductOfferForm(forms.ModelForm):
    class Meta:
        model = ProductOffer
        fields=["product","discount","is_active"]

    
class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields=["category_name","category_desc"]    


