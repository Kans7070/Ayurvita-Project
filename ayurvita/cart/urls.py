

from django.urls import path
from . import views


urlpatterns = [
    
    path('',views.cart_page, name='cart_page'),
    path('add_to_cart/<int:product_id>', views.add_to_cart,name='add_to_cart'),
    path('decrease_quantity/<int:product_id>', views.decrease_quantity,name='decrease_quantity'),
    path('remove_cart/<int:product_id>', views.remove_cart,name='remove_cart'),
]