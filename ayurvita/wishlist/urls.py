

from django.urls import path
from . import views


urlpatterns = [
    
    path('',views.wishlist_page, name='wishlist_page'),
    path('add_to_wishlist/<int:product_id>', views.add_to_wishlist,name='add_to_wishlist'),
    path('remove_wishlist/<int:product_id>', views.remove_wishlist,name='remove_wishlist'),
    
]