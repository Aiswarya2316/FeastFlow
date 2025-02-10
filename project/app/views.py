from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.db.models import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib import messages
import re
from django.core.mail import send_mail
from django.contrib.auth.models import User,auth
import datetime
from django.conf import settings
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def get_usr(req):
    data=userreg.objects.get(email=req.session['user'])
    return data



from django.shortcuts import render, redirect
from .models import Product, servicereg

def get_service(req):
    """Retrieve the logged-in service provider from the session."""
    if 'service' not in req.session:
        return None  # Handle missing session case
    
    try:
        return servicereg.objects.get(email=req.session['service'])
    except servicereg.DoesNotExist:
        return None  # Handle case where the service provider does not exist


def get_product(req):
    data=Product.objects.get(shop=req.session['product'])
    return data


def login(req):
    if 'user' in req.session:
        return redirect(userhome)
    if 'admin' in req.session:
        return redirect(adminhome)
    if 'service' in req.session:
        return redirect(servicehome)
    

    if req.method=='POST':
        email=req.POST['email']
        password=req.POST['password']
        try:
            data=userreg.objects.get(email=email,password=password)
            req.session['user']=data.email
            return redirect(userhome)
        except userreg.DoesNotExist:
            admin=auth.authenticate(username=email,password=password)
            if admin is not None:
                auth.login(req,admin)
                req.session['admin']=email

                return redirect(adminhome)
            
            else:
                try:
                    data=servicereg.objects.get(email=email,password=password)
                    req.session['shop']=data.email

                    return redirect(servicehome)
                except servicereg.DoesNotExist:


                     messages.warning(req, "INVALID INPUT !")
    return render(req,'login.html')



def logout(req):
    if 'user' in req.session:
        # req.session.flush()
        del req.session['user']
    if 'admin' in req.session:
        del req.session['admin']
    if 'service' in req.session:
        del req.session['service']
    return redirect(login)


def userregister(req):

    if req.method=='POST':
        name1=req.POST['name']
        email2=req.POST['email']
        phonenumber3=req.POST['phonenumber']
        location4=req.POST['location']
        password5=req.POST['password']
         # Validate email
        try:
            validate_email(email2)
        except ValidationError:
            messages.warning(req, "Invalid email format, please enter a valid email.")
            return render(req, 'userreg.html')

        # Validate phone number (assuming 10-digit numeric format)
        if not re.match(r'^\d{10}$', phonenumber3):
            messages.warning(req, "Invalid phone number. Please enter a valid 10-digit phone number.")
            return render(req, 'userreg.html')
        # try:
        data=userreg.objects.create(name=name1,email=email2,phonenumber=phonenumber3,location=location4,password=password5)
        data.save()
        return redirect(login)
        # except:
        messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'userreg.html')


def serviceregister(req):

    if req.method=='POST':
        name1=req.POST['name']
        email2=req.POST['email']
        phonenumber3=req.POST['phonenumber']
        location4=req.POST['location']
        password5=req.POST['password']
        try:
            data=servicereg.objects.create(name=name1,email=email2,phonenumber=phonenumber3,location=location4,password=password5)
            data.save()
            return redirect(login)
        except:
            messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'servicereg.html')
    print(serviceregister)


def userhome(req):
        return render(req,'user/userhome.html')
    

def adminhome(req):
    return render(req,'admin/adminhome.html')


def servicehome(req):
    return render(req,'service/servicehome.html')


def about(req):
    return render(req,'user/about.html')


def contact(req):
    return render(req,'user/contact.html')


def service(req):
    return render(req,'user/service.html')

def menu(req):
    return render(req,'user/menu.html')


def gallery(req):  
    return render(req,'user/gallery.html')



from django.shortcuts import render, redirect
from .models import Product, servicereg

def adddishes(req):
    if req.method == 'POST':
        if not req.user.is_authenticated:
            return HttpResponse("Error: User not logged in.")

        service = get_service(req)
        print("Logged-in User Email:", req.user.email)
        print("Service Object:", service)  

        if not service:  # If service is None, return an error
            return HttpResponse("Error: Service is missing or invalid.")

        name = req.POST.get('name')
        description = req.POST.get('description')
        price = req.POST.get('price')
        quantity = req.POST.get('quantity')
        offerprice = req.POST.get('offerprice')
        image = req.FILES.get('image')

        product = Product.objects.create(
            service=service,
            name=name,
            description=description,
            price=int(price),
            quantity=int(quantity),
            offerprice=int(offerprice) if offerprice else 0,
            image=image
        )
        product.save()
        return redirect('viewdishes')

    return render(req, 'service/adddishes.html')


    
def viewdishes(req):
    if 'service' in req.session:
        data = Product.objects.filter(service=get_service(req))
        return render(req, 'service/viewdishes.html', {'data': data})
    else:
        return redirect('servicehome')  # Redirect to home if not logged in
 

def editdishes(req,id):
    data=Product.objects.get(pk=id)
    if req.method=='POST':
        name1=req.POST['name']
        price=req.POST['price']
        offerprice=req.POST['offerprice']
        quantity=req.POST['quantity']
        image=req.FILES.get('image')
        print(type(image))
        if image:

         Product.objects.filter(pk=id).update(name=name1,price=price,offerprice=offerprice,quantity=quantity)
         data=Product.objects.get(pk=id)
         data.image=image
         data.save()
        else:
            Product.objects.filter(pk=id).update(name=name1,price=price,offerprice=offerprice,quantity=quantity)
        return redirect(viewdishes)
    return render(req,'service/editdishes.html',{'data':data})

def deletedishes(req,id):
    data=Product.objects.get(pk=id)
    data.delete()
    return redirect(viewdishes)