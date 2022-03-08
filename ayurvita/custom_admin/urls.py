from unicodedata import name
from . import views
from django.urls import path



urlpatterns =[
    path('',views.admin,name='admin'),
    path('users',views.users,name='users'),
    path('product',views.product,name='product'),
    path('admin_category',views.admin_category,name='admin_category'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('admin_logout',views.admin_logout,name='admin_logout'),
    path('add_product',views.add_product,name='add_product'),
    path('add_category',views.add_category,name='add_category'),
    path('orders_history',views.orders_history,name='orders_history'),
    path('offers',views.offers,name='offers'),
    path('add_product_offer',views.add_product_offer,name='add_product_offer'),
    path('add_category_offer',views.add_category_offer,name='add_category_offer'),



    path('user_view/<int:id>',views.user_view,name='user_view'),
    path('user_block/<int:id>',views.user_block,name='user_block'),
    path('user_unblock/<int:id>',views.user_unblock,name='user_unblock'),
    path('edit_product/<int:id>',views.edit_product,name='edit_product'),
    path('delete_product/<int:id>',views.delete_product,name='delete_product'),
    path('delete_category/<int:id>',views.delete_category,name='delete_category'),
    path('edit_category/<int:id>',views.edit_category,name='edit_category'),
    path('edit_product_offers/<int:id>',views.edit_product_offers,name='edit_product_offers'),
    path('edit_category_offers/<int:id>',views.edit_category_offers,name='edit_category_offers'),

]