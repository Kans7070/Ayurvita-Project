from email.headerregistry import Address
from django.db import models
from user.models import User
from address.models import Address

# Create your models here.
my_choices=(
    ("not packed", "not packed"),
    ("shipped", "shipped"),
    ("delivered", "delivered"),
)

class OrderHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    product_name = models.CharField(max_length=50)
    product_quantity = models.IntegerField(null=False, blank=False,)
    product_image1 = models.ImageField(null=False, blank=False, upload_to='products')
    product_image2 = models.ImageField(
        null=False, blank=False, upload_to='products')
    product_image3 = models.ImageField(
        null=True, blank=True, upload_to='products')
    date_created = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, )
    date_updated = models.DateTimeField(auto_now_add=True,)
    status = models.CharField(choices=my_choices,default="not packed",max_length=50)
    price = models.PositiveIntegerField()
    address=models.ForeignKey(Address, null=True,on_delete=models.CASCADE)
    payment=models.BooleanField(default=False)