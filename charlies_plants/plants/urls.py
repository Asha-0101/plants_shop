from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('cart/', views.cart_page, name='cart'),
    path('remove_cart/<str:cid>/', views.remove_cart, name='remove_cart'),
    path('blogs/', views.blogs, name='blogs'),
    path('blogs/<str:name>/', views.blogsview, name='blogsview'), 
    path('product/<str:cname>/<str:pname>/', views.product_details, name='product_details'),
    path('addtocart/', views.add_to_cart, name='addtocart'),
    path('search/', views.search_products, name='search_products'), 
    path('payment1/', views.payment1, name='payment1'),
    path('payment2/', views.payment2, name='payment2'),
    path('payment3/', views.payment3, name='payment3'),
    path('checkout/', views.checkout, name='checkout'),
]   