from . import views
from django.urls import path

urlpatterns = [
    path('', views.shop, name='shop'),
    path('search/', views.search, name='search'),
    path('product_not_found/', views.product_not_found, name='product_not_found'),
    path('shop-detail/<int:id>', views.shop_detail, name='shop_detail'),
    path('category/<int:category_id>', views.category, name='category'),

]
