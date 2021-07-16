from django.contrib import admin
from django.urls import path,include
from .views import home,product,cart,addtocart,checkout,inc,delItem,dec,del_order,pay,success, tracker
urlpatterns = [
    
    path('',home,name="home"),
    path('success/',success,name="success"),
    path('product/<pk>/',product,name="product"),
    path('cart/',cart,name="cart"),
    path('addtocart/',addtocart,name="addtocart"),
    path('checkout/',checkout,name="checkout"),
    path('inc/',inc,name="inc"),
    path('del/<int:id>/',delItem,name="del"),
    path('dec/',dec,name="dec"),
    path('pay/',pay,name="pay"),
    path('tracker/',tracker,name="tracker"),
    
    # path('payment/',success,name="payment"),
    path('dorder/',del_order,name="dorder"),
   
    
    
]
