from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.contrib import messages,auth
from .models import Token
from core.models import Customer,Cart
from django_email_verification import send_email
import json

# Create your views here.

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        zipcode=request.POST['zipcode']
        state=request.POST['state']
        city=request.POST['city']
        pno=request.POST['pno']
        address=request.POST['address']
        if User.objects.filter(username=username).exists():
                messages.warning(request,'Username already exists')
                return redirect('register')
        else:
            if User.objects.filter(email=email).exists():
                messages.warning(request,'Email already exists')
                return redirect('register')
            else:
                user=User.objects.create_user(first_name=fname,last_name=lname,username=username,email=email,password=password)
                user.is_active = False  # Example
                send_email(user)
                customer=Customer(user=user,bill_state=state,bill_city=city,bill_zipcode=zipcode,bill_phone=pno,bill_address=address)
                customer.save()
                messages.success(request,'Account created successfully')
                return redirect('login')
        return redirect('login')

        



    return render(request,'info/register.html')
def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Credentials')
            return redirect('login')



    return render(request,'info/login.html')


def logout_user(request):
    logout(request)
    return redirect('home')

def profile(request,pk):
    user=User.objects.get(id=pk)
    customer=Customer.objects.get(user=user)
    cart=Cart.objects.filter(user=user).first()
    if cart==None:
        return render(request,'info/profile.html',{'user':user,'customer':customer,'cq':0})
    else :
        if cart.itemincart_set.count()==0:
            return render(request,'info/profile.html',{'user':user,'customer':customer,'cq':0})

        

    print(customer)
    return render(request,'info/profile.html',{'user':user,'customer':customer,'cq':cart.itemincart_set.count()})

def profile_pic_update(request,pk):
    user=User.objects.get(id=pk)
    if request.method=="POST":
        img=request.FILES['profile_pic']
        user.profile.image=img
        user.profile.save()
        message="Your profile pic has been updated"
        return redirect('profile',pk=user.id)
    return redirect('profile',pk=user.id)

def set(request):
    context=[]
    try:
        if request.method=="POST":
            pk=request.POST.get('pk')
            user=User.objects.get(id=pk)
            customer=Customer.objects.get(user=user)
            context.append({'state':customer.bill_state,'city':customer.bill_city,'address':customer.bill_address,'zip':customer.bill_zipcode})
            response=json.dumps(context)

            return HttpResponse(response)
    except Exception as e:
        return HttpResponse(f'{e}')
    return HttpResponse('nice try')
    

        

