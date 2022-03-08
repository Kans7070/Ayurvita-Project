from django.db import models
from category.models import Category

# Create your models here.

class ProductOffer(models.Model):
    product = models.ForeignKey("shop.Product", on_delete=models.CASCADE,)
    discount = models.IntegerField()
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


class CategoryOffer(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.IntegerField()
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)


