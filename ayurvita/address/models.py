from django.db import models
from user.models import User

# Create your models here.


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=20,null=False)
    phone=models.CharField(max_length=10)
    labelled_as = models.CharField(max_length=20,null=False)
    pin_code= models.CharField(max_length=6,null=False)
    address=models.CharField(max_length=200,null=False)
    
