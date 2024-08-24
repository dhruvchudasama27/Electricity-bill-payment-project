from django.shortcuts import render, HttpResponse , redirect
from .models import *
import random
from django.core.mail import send_mail
import requests
from django.conf import settings

# Create your views here.

def index(request):
    return render(request,"index.html")

def error_404(request):
    return render(request,"404.html")

def about_us(request):
    return render(request,"about_us.html")

def billing_detail(request):
    uid = user.objects.get(email=request.session['email'])
    contex = {"uid":uid}
    return render(request,"billing_detail.html",contex)

def add_billing_detail(request,id):
    if request.POST:
        uid = user.objects.get(id=id)
        account_num = request.POST.get('account_number')
        cus_id = request.POST.get('customer_id')
        bill_address = request.POST.get('billing_address')
        Billing_detail.objects.create(user = uid,account_number=account_num,customer_id=cus_id,billing_address=bill_address)
        return redirect("profile")
    else:
        return redirect("login")
    
def edit_billing_detail(request,id):
    billing_detail = Billing_detail.objects.get(id=id)
    if request.POST:
        billing_detail.account_number = request.POST['a_number']
        billing_detail.customer_id = request.POST['c_id']
        billing_detail.billing_address = request.POST['b_address']
        billing_detail.save()
        return redirect("profile")

def contact_us(request):
    return render(request,"contact_us.html")

def faq(request):
    return render(request,"faq.html")

def login(request):
    if 'email' in request.session:
        uid = user.objects.get(email=request.session['email'])
        return render(request,"index.html")
    else:
        if request.POST:
            email = request.POST["email"]
            password = request.POST["password"]
            try:
                data = user.objects.get(email=email,password=password)
                request.session['email'] = data.email
                request.session.set_expiry(settings.SESSION_COOKIE_AGE)
                return redirect("index")
            except:
                message_for_login = "Invalid login"
                contex = {"message_for_login":message_for_login}
                return render(request,"login.html",contex)
        return render(request,"login.html")
    
def logout(request):
    if 'email' in request.session:
        del(request.session['email'])
        return redirect("login")
    else:
        return redirect("login")

def otp_generate(request):
    return render(request,"otp_generate.html")

def payment_confirmation(request):
    return render(request,"payment_confirmation.html")

def payment_history(request):
    return render(request,"payment_history.html")

def payment(request):
    return render(request,"payment.html")

def privacy(request):
    return render(request,"privacy.html")

def profile(request):
    if 'email' in request.session:
        uid = user.objects.get(email=request.session['email'])
        billing_detail = Billing_detail.objects.filter(user=uid).first()
        contex = {"uid":uid,"billing_detail":billing_detail}
        return render(request,"profile.html",contex)
    else:
        return render(request,"login.html")
    
def edit_profile(request):
    if 'email' in request.session:
        uid = user.objects.get(email=request.session['email'])
        if request.method == 'POST':
            uid.name = request.POST.get('name')
            uid.mobile_number = request.POST.get('mobile_number')
            uid.email = request.POST.get('email')
            uid.street_address = request.POST.get('street_address')
            uid.pincode = request.POST.get('pincode')
            uid.city = request.POST.get('city')
            uid.state = request.POST.get('state')
            uid.country = request.POST.get('country')
            if 'profile_photo1' in request.FILES:
                uid.profile_photo = request.FILES['profile_photo1']
            uid.save()
            return redirect("profile")
        return render(request,"profile.html")
    else:
        return render(request,"login.html")

def registration(request):
    if request.POST:
        name=request.POST['full_name']
        mobile_number=request.POST['phone_number']
        email=request.POST['email']
        street_address=request.POST['street_address']
        pincode=request.POST['pincode']
        city=request.POST['city']
        state=request.POST['state']
        country=request.POST['country']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        profile_photo=request.FILES.get('profile_photo')
        response = requests.get(f"https://emailvalidation.abstractapi.com/v1/?api_key=6089bc4afeb248cfbae263ac6dd99ef8&email={email}")

        try:
            uid = user.objects.get(email=email)
            message_for_email = "email already exist"
            contex={"message_for_email":message_for_email}
            return render(request,"registration.html",contex)
        except:
            if response.status_code == 200:
                data = response.json()
                if data["deliverability"] == "DELIVERABLE":
                    if password == confirm_password:
                        if len(password)>= 8:
                            lower = []
                            upper = []
                            digit = []
                            special = []
                            for i in password:
                                if i.islower():
                                    lower.append(i)
                                elif i.isupper():
                                    upper.append(i)
                                elif i.isdigit():
                                    digit.append(i)
                                else:
                                    special.append(i)
                            if len(lower) == 0 or len(upper) == 0 or len(digit) == 0 or len(special) == 0 :
                                message_for_password_critearea = "password have does not follow the conditions"
                                contex = {"message_for_password_critearea":message_for_password_critearea}
                                return render(request,"registration.html",contex)
                            else:
                                user.objects.create(name=name,mobile_number=mobile_number,email=email,street_address=street_address,pincode=pincode,city=city,state=state,country=country,password=password,profile_photo=profile_photo)
                                return redirect("login")
                        else:
                            message_for_password_length = "password length must have 8 character"
                            contex = {"message_for_password_length":message_for_password_length}
                            return render(request,"registration.html",contex)

                    else:
                        message_for_password_not_same = "password and confirm password are does not match"
                        contex = {"message_for_password_not_same":message_for_password_not_same}
                        return render(request,"registration.html",contex)
                else:
                    message_for_email_not_available = "email is not on google"
                    contex = {"message_for_email_not_available":message_for_email_not_available}
                    return render(request,"registration.html",contex)

            else:
                message_for_email_failed = "Failed to validate email"
                contex = {"message_for_email_failed":message_for_email_failed}
                return render(request,"registration.html",contex)
    else:
        return render(request,"registration.html")

def reset_password(request):
    return render(request,"reset_password.html")

def terms(request):
    return render(request,"terms.html")

