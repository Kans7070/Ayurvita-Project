from django.db import models
from user.models import User
from shop.models import Product

# Create your models here.

class Cart(models.Model):
    # cart_id = models.CharField(max_length=200,blank=True,null = True)
    date_added = models.DateField(auto_now_add=True)
    
    def __int__(self):
        return self.cart_id 
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)
    cart    = models.ForeignKey(Cart ,on_delete=models.CASCADE,null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    
    
    def sub_total(self):
        return self.product.get_mrp() * self.quantity
    
    def __unicode__(self):
        return self.product
    
    def product_name(self):
        name=self.product.product_name.replace(" ", "_")
        
        return name