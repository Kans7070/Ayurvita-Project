

from django.urls import path
from . import views


urlpatterns = [
    
    path('',views.address, name='address'),
    path('delete_address/<int:id>', views.delete_address,name='delete_address'),

    
]