from django.http.response import JsonResponse
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse, request
from .models import Cart, Customer, Item,Itemincart,Order,OrderUpdate
import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required,user_passes_test
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from twilio.rest import Client
from django.conf import settings

# Create your views here.
@login_required
def home(request):
    item=[]
    cart=Cart.objects.filter(user=request.user).first()
    print(cart)
    if cart == None:
        for i in Item.objects.all():
            item.append({'i':i,'iqty':None})
        context={'items':item,'cq':0}            
    else:
        if cart.itemincart_set.count()==0:
            for i in Item.objects.all():
                item.append({'i':i,'iqty':None})
                context={'items':item,'cq':cart.itemincart_set.count()}
        else:
            
            for i in Item.objects.all():
                if cart.itemincart_set.filter(item=i).first() == None:
                     item.append({'i':i,'iqty':False})
                else:
                    item.append({'i':i,'iqty':True})
            context={'items':item,'cq':cart.itemincart_set.count()}
    return render(request,'core/home.html',context)
                        
        
       
        
        
        
@login_required
def product(request,pk):
    item=[]
    product=Item.objects.get(id=pk)
    cart=Cart.objects.filter(user=request.user).first()
    if cart == None:
        item.append({'i':product,'iqty':None})
        context={'product':item,'cq':0}
    else:
        if cart.itemincart_set.count()==0:
            item.append({'i':product,'iqty':None})
            context={'product':item,'cq':cart.itemincart_set.count()}
        else:
            if cart.itemincart_set.filter(item=product).first() == None:
                item.append({'i':product,'iqty':False})
            else:
                item.append({'i':product,'iqty':True})
            context={'product':item,'cq':cart.itemincart_set.count()}
    return render(request,'core/product.html',context)

@login_required
def cart(request):
    cart=Cart.objects.filter(user=request.user).first()
    if cart==None:
        context={'cart':False,'cq':0}
    else:
        if cart.itemincart_set.count()==0:
            context={'cart':False,'cq':0}
        else:
            s=0
            items=cart.itemincart_set.all()
            iics=Itemincart.objects.filter(cart=cart)
            for item in iics:
                s=s+item.total()
            context={'cart':True,
            'cq':cart.itemincart_set.count(),
            'items':items,
            'sum':s,
            }

        
    
    return render(request,'core/cart.html',context)



@login_required
def checkout(request):
    cart=Cart.objects.filter(user=request.user).first()
    context={
            'cq':0,
        }
    if cart==None:
        context['c_is_empty']=True
    else:
        if cart.itemincart_set.count()==0:
            context['c_is_empty']=True
        else:
            s=0
            context['c_is_empty']=False
            context['cq']=cart.itemincart_set.count()
            items=cart.itemincart_set.all()
            iics=Itemincart.objects.filter(cart=cart)
            for item in iics:
                s=s+item.total()
            context['sum']=s
            context['items']=items
        


    
    

        
    return render(request,'core/checkout.html',context)
    




@login_required
def addtocart(request):
    if request.method=="POST":
        try:
            itemId=request.POST.get('itemId')
            item=Item.objects.get(id=itemId)
            cart=Cart.objects.filter(user=request.user).first()
            if cart==None:
                Cart.objects.create(user=request.user)
                c=Cart.objects.get(user=request.user)
                Itemincart.objects.create(cart=c,item=item,qty=1)
                item.quantity-=1
                item.save()
                # return HttpResponse(f'cart is created and item is added')
                updates=[]
                updates.append({'cq':c.itemincart_set.count()})
                response=json.dumps(updates)
                return HttpResponse(response)
            else:
                c=Cart.objects.get(user=request.user)
                if cart.itemincart_set.filter(item=item).first() == None:
                    Itemincart.objects.create(cart=c,item=item,qty=1)
                    item.quantity-=1
                    item.save()
                    # return HttpResponse(f' item is added')
                    updates=[]
                    updates.append({'cq':c.itemincart_set.count()})
                    response=json.dumps(updates)
                    return HttpResponse(response)
                else:
                    iic=Itemincart.objects.get(item=item)
                    iic.qty+=1
                    iic.save()
                    # return HttpResponse(f'item was already there its quantity is updated')
                    updates=[]
                    updates.append({'cq':cart.itemincart_set.count()})
                    response=json.dumps(updates)
                    return HttpResponse(response)

                
        except Exception as e:
            return HttpResponse(f'{e} cart wala')
    return HttpResponse(f'hello')


@login_required
def inc(request):
    try:
        user=request.user
        cart=Cart.objects.filter(user=request.user).first()
        if request.method=='POST':
            iic_id=request.POST.get('ItemInCartId')
            iic=Itemincart.objects.get(id=iic_id)
            iic_item=iic.item
            updates=[]
            in_stock_qty=iic_item.quantity
            s=0
            if iic_item.quantity==0:
                iic_item.in_stock=False
                updates.append({'in_stock':False,'iic':iic_item.name})
                response=json.dumps(updates)
                return HttpResponse(response)
            
            if iic_item.in_stock:
                iic.qty+=1
                iic.save()
                iic_item.quantity-=1
                iic_item.save()
                print(iic_item.quantity)
                if iic_item.quantity==0:
                    iic_item.save()
                    iics=Itemincart.objects.filter(cart=cart)
                    for item in iics:
                        s=s+item.total()
                    updates.append({'in_stock':True,'iic_qty':iic.qty,'iic_total':iic.total(),'sum':s,'added_all':True})
                    response=json.dumps(updates)
                    return HttpResponse(response)
                iics=Itemincart.objects.filter(cart=cart)
                for item in iics:
                    s=s+item.total()
                updates.append({'in_stock':True,'iic_qty':iic.qty,'iic_total':iic.total(),'sum':s,'added_all':False})
                response=json.dumps(updates)
                return HttpResponse(response)
                
            return HttpResponse(f'{iic_id}  {iic}')
        return HttpResponse(f'{user}  {cart}')
    except Exception as e:
        return HttpResponse(f'{e}')
    return HttpResponse(f'hello')
            



@login_required
def dec(request):
    user=request.user
    cart=Cart.objects.filter(user=request.user).first()
    if request.method=='POST':
        iic_id=request.POST.get('ItemInCartId')
        iic=Itemincart.objects.get(id=iic_id)
        iic_item=iic.item
        updates=[]
        s=0
        if iic_item.in_stock:
            iic.qty-=1
            if iic.qty==0:
                iic_item.quantity+=1
                iic_item.save()
                iic.delete()
                updates.append({'is_gone':True,'cart_qty':cart.itemincart_set.count()})
                response=json.dumps(updates)
                return HttpResponse(response)
            iic.save()
            iic_item.quantity+=1
            iic_item.save()
            print(iic_item.quantity)
            iics=Itemincart.objects.filter(cart=cart)
            for item in iics:
                s=s+item.total()
            updates.append({'iic_qty':iic.qty,'iic_total':iic.total(),'sum':s,'cart_qty':cart.itemincart_set.count(),'is_gone':False})
            response=json.dumps(updates)
            return HttpResponse(response)
            iics=Itemincart.objects.filter(cart=cart)
            for item in iics:
                s=s+item.total()
            updates.append({'in_stock':True,'iic_qty':iic.qty,'iic_total':iic.total(),'sum':s,'added_all':False})
            response=json.dumps(updates)
            return HttpResponse(response)



@login_required        
def delItem(request,id):
    cart=Cart.objects.filter(user=request.user)
    iic=Itemincart.objects.get(id=id)
    iic.item.quantity+=iic.qty
    iic.item.save()
    iic.delete()    
    return redirect('cart')




def pay(request):
    try:
        context=dict()

        if request.method=="POST":
            updates=[]
            # updates.append({'cq':c.itemincart_set.count()})
            z=request.POST.get('zipcode')
            a=request.POST.get('address')
            s=request.POST.get('state')
            c=request.POST.get('city')
            amt=request.POST.get('amt')
            user=request.user
            customer=Customer.objects.get(user=user)
            order=Order(user=user,Customer=customer,order_total=amt,order_zipcode=z,order_state=s,order_city=c,order_address=a)
            order.save()
            order.token_create()
            order.save()
            price=int(request.POST.get("amt"))*100
            client=razorpay.Client(auth=("rzp_test_daHPr4QhX1TJ4V","xyxpeNlfNMDktLHfBkpGx75W"))
            payment=client.order.create({'amount':price, 'currency':"INR",'payment_capture':'1'})
            context['payment']=payment
            context['order_id']=order.order_id
            return render(request,'core/r.html',context)
        return render(request,'core/checkout.html')

    except Exception as e:
        return HttpResponse({e})

                    
        










    
    
                
                
                
    # if request.method=='POST':
    #     cart=Cart.objects.filter(user=request.user).first()
    #     customer=Customer.objects.get(user=request.user)
    #     x=cart.itemincart_set.all()
    #     s=0
    #     for i in range(len(x)):
    #         s=s+x[i].total()
    #     context['total']=s
    #     order=Order(user=request.user,Customer=customer,order_total=s,order_state=request.POST['state'],order_city=request.POST['city'],order_zipcode=request.POST['zipcode'],order_address=request.POST['address'])
    #     order.save()
    #     order.token_create()
    #     order.save()
    #     context['order_id']=order.order_id
    #     print(context)
    #     return redirect('pay')
        # we will send a sms to user.
    


        
        # context['i']=request.POST
    

@login_required
def del_order(request):
    if request.method=='POST':
        oid=request.POST.get('oid')
        order=Order.objects.get(order_id=oid)
        order.delete()
        return HttpResponse(request)




def payed(request):
    if request.method=='POST':
        oid=request.POST.get('oid')
        id=request.POST.get('id')
        print(oid,id)
        return redirect(request,"core/pay.html")


# def suc(request):
#             return HttpResponse("success")


# def success(request):
#     a=1
#     if a==1:
#         return suc(request)


@csrf_exempt
def success(request):
    if request.method=='POST':
        oid=request.POST.get('oid')
        order=Order.objects.get(order_id=oid)
        order.is_paid=True
        order.save()
        cart=Cart.objects.get(user=order.user)
        cart.delete()
        account_sid = settings.TWILIO_ACCOUNT_SID
        auth_token = settings.TWILIO_AUTH_TOKEN
        client = Client(account_sid, auth_token)

        message = client.messages \
                            .create(
                                body="Your order id is-  "+str(oid),
                                from_=settings.TWILIO_NO,
                                to=settings.MY_NO
                            )

        print(message.sid)
        return redirect('success')
    return render(request,'core/success.html')

def tracker(request):
    updates=[]
    try:
        if request.method=='POST':
            oid=request.POST.get('oid');
            email=request.POST.get('email');
            user=User.objects.filter(email=email)
            print(user)
            if user.first()!=None:
                order=Order.objects.filter(order_id=oid)
                if order.first()!=None:
                    o=order.first()
                    update=o.orderupdate_set.all()
                    
                    for item in update:
                        updates.append({'text':item.update_desc,'time':item.timestamp,'is_error':0})
                    response=json.dumps(updates,default=str)
                    return HttpResponse(response)
                else:
                    response=json.dumps(updates)
                    return HttpResponse(response)
            else:
                
                response=json.dumps(updates)
                return HttpResponse(response)
                    
    except Exception as e:
        return HttpResponse(f'{e}')

            
        
    return render(request,'core/tracker.html')