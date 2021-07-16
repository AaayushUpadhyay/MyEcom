from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Item,Itemincart,Cart,Customer,Order,OrderUpdate

admin.site.register(Item)
admin.site.register(Itemincart)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderUpdate)
