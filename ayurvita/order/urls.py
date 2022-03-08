
from unicodedata import name
from . import views
from django.urls import path

urlpatterns = [   
    path('pay', views.pay,name='pay'),
    path('address_checkout/>',views.address_checkout, name='address_checkout'),
    path('cart_checkout',views.cart_checkout,name='cart_checkout'),
    path('buynow/<int:product_id>',views.buynow,name='buynow'),
    path('my_orders',views.my_orders,name='my_orders'),

    path('address_checkout_with_id/<int:id>',views.address_checkout_with_id, name='address_checkout_with_id'),
]
