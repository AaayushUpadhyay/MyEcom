from django.contrib.auth.decorators import permission_required
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

import secrets,string
class Item(models.Model):
    name=models.CharField(max_length=255,null=False,blank=False)
    description=models.CharField(max_length=255)
    price=models.PositiveIntegerField(null=False,blank=False)
    discount_price=models.IntegerField(null=True,blank=True)
    quantity=models.PositiveIntegerField(null=False,blank=False,default=0)
    in_stock=models.BooleanField(default=False)
    image=models.ImageField(default="default1.jpg",upload_to="profile_pics")



    def __str__(self):
        return self.name

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bill_address=models.CharField(max_length=255,null=False,blank=False)
    bill_zipcode=models.PositiveIntegerField(null=False,blank=False)
    bill_state=models.CharField(max_length=255,null=False,blank=False)
    bill_city=models.CharField(max_length=255,null=False,blank=False)
    bill_phone=models.PositiveIntegerField(null=False,blank=False)
    can_pay=models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    cart_id=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    created_on=models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'{self.user.username} cart'

class Itemincart(models.Model):
    class Meta:
        unique_together=(('cart','item'),)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    qty=models.PositiveIntegerField()

    def total(self):
        return self.item.price*self.qty

class Order(models.Model):
    class Meta:
        get_latest_by='created_on'
    choices=(
        (1,'not ready'),
        (2,'ready to be shipped'),
        (3,'dispatched'),
        (4,'delivered')
    )
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    status=models.IntegerField(choices=choices,default=1)
    Customer=models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True)
    order_total=models.PositiveIntegerField(blank=True,null=True)
    order_id=models.CharField(max_length=30,blank=True,null=True)
    order_state=models.CharField(max_length=100,blank=True,null=True)
    order_city=models.CharField(max_length=100,blank=True,null=True)
    order_address=models.CharField(max_length=100,blank=True,null=True)
    order_zipcode=models.PositiveIntegerField(max_length=100,blank=True,null=True)
    is_paid=models.BooleanField(default=False)
    created_on=models.DateTimeField(default=datetime.now,blank=True,null=True)


    def token_create(self):
        token=''.join([secrets.choice(self.user.username+'0123456789') for i in range(10)])
        self.order_id=token
    
    def __str__(self):
        return self.user.username
    

class OrderUpdate(models.Model):
    update_id=models.AutoField(primary_key=True)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    update_desc=models.CharField(max_length=5000)
    timestamp=models.DateField(auto_now_add=True)

    def __str__(self):
        return f'update for order-{self.order.order_id} is {self.update_desc[0:7]}+"...."'




    
    
        
        
