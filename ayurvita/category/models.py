from django.db import models
# from shop.models import Product
# Create your models here.

class Category(models.Model):
    category_name = models.CharField(max_length=30)
    category_desc=models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    def product_count(self):
        return self.product_set.all().count()