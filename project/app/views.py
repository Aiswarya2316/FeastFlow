from django.shortcuts import render,redirect
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
import razorpay
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def get_usr(req):
    data=Register.objects.get(Email=req.session['user'])
    return data


def get_shop(req):
    data=Shopreg.objects.get(Email=req.session['shop'])
    return data

def get_product(req):
    data=Product.objects.get(shop=req.session['product'])
    return data


def login(req):
    if 'user' in req.session:
        return redirect(userhome)
    if 'admin' in req.session:
        return redirect(adminhome)
    if 'shop' in req.session:
        return redirect(shophome)
    

    if req.method=='POST':
        Email=req.POST['Email']
        password=req.POST['password']
        try:
            data=Register.objects.get(Email=Email,password=password)
            req.session['user']=data.Email
            return redirect(userhome)
        except Register.DoesNotExist:
            admin=auth.authenticate(username=Email,password=password)
            if admin is not None:
                auth.login(req,admin)
                req.session['admin']=Email

                return redirect(viewshop)
            
            else:
                try:
                    data=Shopreg.objects.get(Email=Email,password=password)
                    req.session['shop']=data.Email

                    return redirect(viewpro)
                except Shopreg.DoesNotExist:


                     messages.warning(req, "INVALID INPUT !")
    return render(req,'login.html')



def logout(req):
    if 'user' in req.session:
        # req.session.flush()
        del req.session['user']
    if 'admin' in req.session:
        del req.session['admin']
    if 'shop' in req.session:
        del req.session['shop']
    return redirect(login)


def register(req):

    if req.method=='POST':
        name1=req.POST['name']
        email2=req.POST['Email']
        phonenumber3=req.POST['phonenumber']
        location4=req.POST['location']
        password5=req.POST['password']
         # Validate email
        try:
            validate_email(email2)
        except ValidationError:
            messages.warning(req, "Invalid email format, please enter a valid email.")
            return render(req, 'register.html')

        # Validate phone number (assuming 10-digit numeric format)
        if not re.match(r'^\d{10}$', phonenumber3):
            messages.warning(req, "Invalid phone number. Please enter a valid 10-digit phone number.")
            return render(req, 'register.html')
        # try:
        data=Register.objects.create(name=name1,Email=email2,phonenumber=phonenumber3,location=location4,password=password5)
        data.save() 
        return redirect(login)
        # except:
        messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'register.html')


def shopregister(req):

    if req.method=='POST':
        name1=req.POST['name']
        email2=req.POST['Email']
        phonenumber3=req.POST['phonenumber']
        location4=req.POST['location']
        password5=req.POST['password']
        try:
            data=Shopreg.objects.create(name=name1,Email=email2,phonenumber=phonenumber3,location=location4,password=password5)
            data.save()
            return redirect(login)
        except:
            messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'shopregister.html')
    print(shopregister)


def homes(req):
    return render(req,'home.html')


def userhome(req):
    if 'user' in req.session:
        data = Product.objects.all().order_by('-shop')[:6]
        data1 = Buy.objects.filter(user=get_usr(req)).order_by('-date_of_buying')[:2]  # Only get the latest 2 orders
        data2 = cart.objects.filter(user=get_usr(req)).order_by('-id')[:2]  # Get the latest 4 cart items

        return render(req,'user/userhome.html',{'data':data,'data1':data1,'data2':data2})
    else:
        return redirect(login)

def adminhome(req):
    
    return render(req,'admin/adminhome.html')


def shophome(req):
    
    return render(req,'shop/viewpro.html')

def deliverys(req):
    
    return render(req,'deliveryhome.html')

def addpro(req):
    if req.method=='POST':
        name = req.POST['name']
        discription = req.POST['discription']
        price = req.POST['price']
        quantity = req.POST['quantity']
        offerprice = req.POST['offerprice']
        image = req.FILES['image']
        data=Product.objects.create(name=name,discription=discription,price=price,quantity=quantity,offerprice=offerprice,image=image,shop=get_shop(req))
        data.save()
        return redirect(viewpro)
    return render(req,'shop/addpro.html')

    
def viewpro(req):
    if 'shop' in req.session:
        data = Product.objects.filter(shop=get_shop(req))
        return render(req, 'shop/viewpro.html', {'data': data})  
    
    # Redirect to login page or show a message if shop is not in session
    messages.warning(req, "You must be logged in to view products.")
    return redirect("login")   

def edit(req,id):
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
        return redirect(viewpro)
    return render(req,'shop/edit.html',{'data':data})

def delete(req,id):
    data=Product.objects.get(pk=id)
    data.delete()
    return redirect(viewpro) 


###profile of user
def profile(req):
    if 'user' in req.session:
        # data=Register.objects.get(Email=req.session['user'])
        return render(req,'user/userprofile.html',{'data':get_usr(req)})
    else:
        return redirect(login)
    

###profile update
def upload(req):
    if 'user' in req.session:
        try:
            data = Register.objects.get(Email=req.session['user'])
        except Register.DoesNotExist:
            return redirect(login)

        if req.method == 'POST':
            name = req.POST['name']
            phonenumber = req.POST['phonenumber']
            location = req.POST['location']
            if not re.match(r'^[789]\d{9}$', phonenumber):
                return render(req, 'user/updateprofile.html', {
                    'data': data,
                    'error_message': 'Invalid phone number'
                })
            Register.objects.filter(Email=req.session['user']).update(name=name, phonenumber=phonenumber, location=location)
            return redirect(profile)
        return render(req, 'user/updateprofile.html', {'data': data})

    else:

        return redirect(login)
    
def userviewproduct(req):
    data=Product.objects.all()
    return render(req,'user/userviewproduct.html',{'data':data})

def prodetails(req,id):
    data=Product.objects.get(pk=id)
    if req.method=='POST':
        user=get_usr(req)
        shop=data.shop
        # product=Product.objects.get(pk=id)
        message = req.POST['message']
        rating = req.POST['rating']
        submitted_at = req.POST['submitted_at']
        
        feedback=Feedback.objects.create(user=user,shop=shop,product=data,message=message,rating=rating,submitted_at=submitted_at)
        feedback.save()
    return render(req,'user/prodetails.html',{'data':data})

def shopprodetails(req,id):
    data=Product.objects.get(pk=id)
    feedback = Feedback.objects.filter(product=data).order_by('-submitted_at')
    return render(req,'shop/shopprodetails.html',{'data':data,'feedback':feedback})



def user_cart(req,id):
    if 'user' in req.session:
        product=Product.objects.get(pk=id)
        user=get_usr(req)
        qty=1
        try:
            dtls=cart.objects.get(product=product,user=user)
            dtls.quantity+=1
            dtls.save()
        except:
            data=cart.objects.create(product=product,user=user,quantity=qty)
            data.save()
        return redirect(user_view_cart)
    else:
        return redirect(login)
    
def user_view_cart(req):
    if 'user' in req.session:
        data=cart.objects.filter(user=get_usr(req))
        return render(req,'user/addtocart.html',{'data':data})
def qty_incri(req,id):
    data=cart.objects.get(pk=id)
    data.quantity+=1
    data.save()
    return redirect(user_view_cart)

def qty_decri(req,id):
    data=cart.objects.get(pk=id)
    if data.quantity>1:
        data.quantity-=1
        data.save()
    return redirect(user_view_cart)



def buynow1(req,id):
    if 'user' in req.session:
        product=Product.objects.get(pk=id)
        user=get_usr(req)
        quantity=1
        date=datetime.datetime.now().strftime("%x")
        price=product.price
        order=Buy.objects.create(product=product,user=user,quantity=quantity,date_of_buying=date,price=price)
        order.save()
    return redirect(orderdetails)

def buynow(req,id):
     if 'user' in req.session:
        cart_product=cart.objects.get(pk=id)
        user=get_usr(req)
        quantity=cart_product.quantity
        date=datetime.datetime.now().strftime("%x")
        price=cart_product.product.price
        order=Buy.objects.create(product=cart_product.product,user=user,quantity=quantity,date_of_buying=date,price=price)
        order.save()
        return redirect(user_view_cart)
     
def deleteitem(req,id):
    data=cart.objects.get(pk=id)
    data.delete()
    return redirect(user_view_cart)

def orderdetails(req):
    data=Buy.objects.filter(user=get_usr(req))[::-1]
    return render(req,'user/orderdetails.html',{'data':data})
    
def delregister(req):

    if req.method=='POST':
        name1=req.POST['name']
        email2=req.POST['Email']
        phonenumber3=req.POST['phonenumber']
        location4=req.POST['rout']
        password5=req.POST['password']
    
        try:
            data=delivery.objects.create(name=name1,Email=email2,phonenumber=phonenumber3,rout=location4,password=password5)
            data.save()
            return redirect(login)
        except:
            messages.warning(req, "Email Already Exits , Try Another Email.")
    return render(req,'deliveryreg.html')
    print(delregister)




def viewshop(req):
    data=Shopreg.objects.all()
    return render(req,'admin/viewshop.html',{'data':data})

def aboutus(req):
    
    return render(req,'user/aboutus.html')

def contact(req):
    
    return render(req,'user/contact.html')

def service(req):
    
    return render(req,'user/service.html')

def bookinghistry(req):
    #  if 'shop' in req.session:
    l=[]
    data=Product.objects.filter(shop=get_shop(req))
    for i in data:
        data1=Buy.objects.filter(product=i)
        l.append(data1)
    print(l)
    # data1=delivery.objects.all()
    return render(req,'shop/bookinghistry.html',{'data':l})




def product_search(request):
    query = request.POST.get('query')  # Get the search term from the request
    products = []
    if query:
        products = Product.objects.filter(name=query)
        
    return render(request, 'user/product_search.html', {'products': products, 'query': query})


#####payment#######

def home(request):
    return render(request, "user/payment.html")



def order_payment(request, id):
    # Fetch the product based on product_id
        product = Product.objects.get (pk=id)

    # if request.method == "POST":
        name = product.name
        amount = product.price  # Get price directly from the product

        # Razorpay client setup
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # Create Razorpay order
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order_id = razorpay_order["id"]

        # Save the order in the database
        order = Order.objects.create(
            name=name, 
            amount=amount, 
            provider_order_id=order_id,
            product=product
        )
        order.save()

        return render(
                request,
                "user/payment.html",
                {
                    "callback_url": "http://" + "127.0.0.1:8000" + "/razorpay/callback/",  # Add trailing slash
                    "razorpay_key": settings.RAZORPAY_KEY_ID,
                    "order": order,
                    "product": product,  
                },
            )

    # return render(request, "user/payment.html", {"product": product})
@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature(response_data)
            return True  # Signature is valid
        except razorpay.errors.SignatureVerificationError:
            return False  # Signature is invalid

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        
        # Fetch the order from the database
        try:
            order = Order.objects.get(provider_order_id=provider_order_id)
        except Order.DoesNotExist:
            return render(request, "callback.html", context={"status": "FAILURE", "message": "Order not found."})

        order.payment_id = payment_id
        order.signature_id = signature_id

        # Correct the signature verification check
        if verify_signature(request.POST):  # ✅ Corrected Condition
            order.status = "SUCCESS"  # ✅ Ensure it's stored as a string
        else:
            order.status = "FAILURE"

        order.save()
        print("Order status:", order.status)  # Debugging statement
        return render(request, "callback.html", context={"status": order.status})  # ✅ Fixed

    else:
        try:
            error_metadata = json.loads(request.POST.get("error[metadata]", "{}"))
            payment_id = error_metadata.get("payment_id", "")
            provider_order_id = error_metadata.get("order_id", "")
            
            order = Order.objects.get(provider_order_id=provider_order_id)
            order.payment_id = payment_id
            order.status = "FAILURE"
            order.save()
        except (Order.DoesNotExist, json.JSONDecodeError):
            return render(request, "callback.html", context={"status": "FAILURE", "message": "Order not found or invalid error data."})

        return render(request, "callback.html", context={"status": order.status})  # ✅ Fixed


from django.shortcuts import render
from .models import Order

def booking_history(request):
    user = request.user  # Assuming user is logged in
    successful_orders = Order.objects.filter(status="SUCCESS")
    print(successful_orders) 
    return render(request, "user/booking_history.html", {"orders": successful_orders})



