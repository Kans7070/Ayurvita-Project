from . import views
from django.urls import path

urlpatterns = [
    path('', views.shop, name='shop'),
    path('search/', views.search, name='search'),
    path('price_high_to_low/', views.price_high_to_low, name='price_high_to_low'),
    path('price_low_to_high/', views.price_low_to_high, name='price_low_to_high'),
    path('no_sort/', views.no_sort, name='no_sort'),
    path('product_not_found/', views.product_not_found, name='product_not_found'),

    path('shop-detail/<int:id>', views.shop_detail, name='shop_detail'),
    path('category/<int:category_id>', views.category, name='category'),

]
