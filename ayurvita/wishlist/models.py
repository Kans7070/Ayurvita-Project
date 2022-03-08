from django.db import models
from user.models import User
from shop.models import Product

# Create your models here.


    
class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    def __unicode__(self):
        return self.product