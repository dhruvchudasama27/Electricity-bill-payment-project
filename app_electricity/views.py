from django.shortcuts import render, HttpResponse , redirect , get_object_or_404
from .models import *
import random
from django.core.mail import send_mail
import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import razorpay
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
# Create your views here.

def index(request):
    current_date = timezone.now().date()
    date_12_months_ago = current_date - timedelta(days=365)
    get_rate = Electricity_rate.objects.filter(date__gte=date_12_months_ago).order_by('-date')[:12]
    get_news = Electricity_news.objects.all().order_by('-date')[:10]
    get_feedback = Feedback.objects.all().order_by('-user_id')[:10]
    contex = {"get_rate":get_rate,"get_feedback":get_feedback,"get_news":get_news}
    return render(request,"index.html",contex)

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
    uid = user.objects.get(email=request.session['email'])
    contex = {"uid":uid}
    return render(request,"contact_us.html",contex)

def contact_message(request,id):
    if request.POST:
        uid = user.objects.get(id=id)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        message = request.POST['message']
        Contact_message.objects.create(user=uid,first_name=first_name,last_name=last_name,email=email,message=message)
    return redirect("contact_us")

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
    if request.POST:
        email = request.POST['email']
        otp = random.randint(100000,999999)
        try:
            uid = user.objects.get(email=email)
            uid.otp = otp
            uid.save()
            send_mail("Django",f"Your otp is {otp} , Don't share with anyone", "dhruvchudasama999@gmail.com" ,[email])
            contex = {"uid":uid,"email":email}
            return render(request,"reset_password.html",contex)
        except:
            wrong_email = "Email does not exixt please enter different email"
            contex = {"wrong_email":wrong_email}
            return render(request,"otp_generate.html",contex)
    return render(request,"otp_generate.html")


def payment_filter(request):
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date and end_date:
        try:
            start_date = datetime.strptime(start_date,'%Y-%m-%d').date()
            end_date = datetime.strptime(end_date,'%Y-%m-%d').date() + timedelta(days=1)

            get_payment_history = Payment_history.objects.filter(date__range=[start_date,end_date])
        except ValueError:
            get_payment_history = Payment_history.objects.none()
    else:
        get_payment_history = Payment_history.objects.all()

    return render(request,"payment_history.html",{"get_payment_history":get_payment_history})

def payment_history(request):
    uid = user.objects.get(email=request.session['email'])
    get_payment_history = Payment_history.objects.filter(user=uid)
    contex = {"get_payment_history":get_payment_history}
    return render(request,"payment_history.html",contex)

def payment(request):
    uid = user.objects.get(email=request.session['email'])
    billing_detail = Billing_detail.objects.get(user=uid)

    if request.POST:
        bill_amount = request.POST['amount']
    else:
        bill_amount = 0

    amount = max(int(bill_amount), 1) * 100
    client = razorpay.Client(auth=('rzp_test_bilBagOBVTi4lE', '77yKq3N9Wul97JVQcjtIVB5z'))
    response = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': 1})
    if int(bill_amount) > 0:
        Payment_history.objects.create(
            user = uid,
            payment_order = response['id'],
            amount = bill_amount,
            status = "success",
            date = timezone.now()
        )
        return redirect("payment_history")
    

    contex = {
        "uid": uid,
        "billing_detail": billing_detail,
        "response":response
    }
    return render(request, "payment.html", contex)


def download_bill(request, id):
    uid = user.objects.get(email=request.session['email'])
    payment = get_object_or_404(Payment_history, id=id)
    
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    data = [
        ['Bill ID:', f"{payment.id}"],
        ['Date:', f"{payment.date.strftime('%Y-%m-%d')}"],
        ['Amount:', f"${payment.amount}"],
        ['Status:', f"{payment.status}"],
        ['Name:', f"{uid.name}"],
        ['Mobile:', f"{uid.mobile_number}"],
        ['Email:', f"{uid.email}"],
        # Paragraph wraps the text in the address cell
        ['Address:', Paragraph(f"{uid.street_address}, {uid.city}, {uid.state}, {uid.country}", normal_style)],
    ]

    table = Table(data, colWidths=[2 * inch, 4 * inch])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ])
    table.setStyle(style)

    elements.append(table)

    doc.build(elements)

    buffer.seek(0)
    
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="bill_{payment.id}.pdf"'
    return response



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
    if request.POST:
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        otp = request.POST['otp']
        try:
            uid = user.objects.get(otp=otp)
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
                        return render(request,"reset_password.html",contex)
                    else:
                        uid.password = password
                        uid.otp = None
                        uid.save()
                        return redirect("login")
                else:
                    message_for_password_length = "password length must have 8 character"
                    contex = {"message_for_password_length":message_for_password_length}
                    return render(request,"reset_password.html",contex)
            else:
                message_for_password_not_same = "password and confirm password are does not match"
                contex = {"message_for_password_not_same":message_for_password_not_same}
                return render(request,"reset_password.html",contex)
        except:
            wrong_otp = "OTP is wrong"
            contex = {"wrong_otp":wrong_otp}
            return render(request,"reset_password.html",contex)

def terms(request):
    contex = {"title":'terms - ElectraPay'}
    return render(request,"terms.html",contex)

def feedback(request):
    if request.POST:
        uid = user.objects.get(email=request.session['email'])
        message = request.POST['feedback']
        Feedback.objects.create(user=uid,name=uid.name,image=uid.profile_photo,feedback_message=message)
        return redirect("index")
    else:
        contex = {"title":'feedback - ElectraPay'}
        return render(request,"feedback.html",contex)

