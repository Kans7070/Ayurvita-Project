from django.db import models
from category.models import Category
from offers.models import ProductOffer, CategoryOffer

# Create your models here.


class Product(models.Model):
    product_name = models.CharField(
        unique=True, max_length=50, null=False, blank=False)
    product_desc = models.CharField(max_length=250, null=False,)
    brand = models.CharField(null=False, blank=False, max_length=50)
    product_price = models.FloatField(null=False, blank=False,)
    product_image1 = models.ImageField(
        null=False, blank=False, upload_to='products')
    product_image2 = models.ImageField(
        null=False, blank=False, upload_to='products')
    product_image3 = models.ImageField(
        null=True, blank=True, upload_to='products')
    quantity = models.IntegerField(null=False, blank=False)
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_updated = models.DateTimeField(auto_now_add=True,)
    is_available = models.BooleanField(default=True)

    def get_price(self):
        return self.product_price

    def get_offer(self):
        category_discount = ""
        product_discount = ""
        try:
            try:
                product_discount = ProductOffer.objects.get(
                    product=self.id, is_active=True)
                offer = True
            except:
                category_discount = CategoryOffer.objects.get(
                    category=self.category, is_active=True)
                offer = True

        except:
            offer = False
            pass
        if offer:
            if product_discount:
                if category_discount:
                    if category_discount.discount > product_discount.discount:
                        discount = category_discount.discount
                        return discount
                    else:
                        discount = product_discount.discount
                        return discount
                else:
                    discount = product_discount.discount
                    return discount
            else:
                discount = category_discount.discount
                return discount
        else:
            return None

    def get_mrp(self):
        category_discount = ""
        product_discount = ""
        try:
            product_discount = ProductOffer.objects.get(
                product=self.id, is_active=True)
        except:
            pass
        try:
            category_discount = CategoryOffer.objects.get(
                category=self.category, is_active=True)
        except:
            pass
        if product_discount:

            if category_discount:
                if category_discount.discount > product_discount.discount:
                    mrp = self.product_price-self.product_price * \
                        (category_discount.discount/100)
                    self.mrp = mrp
                    return mrp
                else:
                    mrp = self.product_price-self.product_price * \
                        (product_discount.discount/100)
                    self.mrp = mrp
                    return mrp
            else:
                mrp = self.product_price-self.product_price * \
                    (product_discount.discount/100)
                self.mrp = mrp
                return mrp
        elif category_discount:
            discount = category_discount
            mrp = self.product_price-self.product_price*(discount.discount/100)
            self.mrp = mrp
            return mrp
        else:
            return self.product_price


class ShopWelcome(models.Model):
    welcome_image1 = models.ImageField(
        null=False, blank=False, upload_to='welcome')
