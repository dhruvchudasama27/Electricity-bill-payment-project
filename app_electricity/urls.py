from django.urls import path
from . import views

from django.conf.urls import handler404  # Import handler404
from django.shortcuts import render  # Import render

# Custom 404 error view
def custom_404(request, exception):
    return render(request, '404.html', status=404)

# Link the custom view to handler404
handler404 = custom_404

urlpatterns = [
    path('', views.index, name="index"),
    path('error_404/', views.error_404, name="error_404"),
    path('about_us/', views.about_us, name="about_us"),
    path('billing_detail/', views.billing_detail, name="billing_detail"),
    path('add_billing_detail/<int:id>/', views.add_billing_detail, name="add_billing_detail"),
    path('edit_billing_detail/<int:id>/', views.edit_billing_detail, name="edit_billing_detail"),
    path('contact_us/', views.contact_us, name="contact_us"),
    path('contact_message/<int:id>/', views.contact_message, name="contact_message"),
    path('faq/', views.faq, name="faq"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('otp_generate/', views.otp_generate, name="otp_generate"),
    path('payment_history/', views.payment_history, name="payment_history"),
    path('payment/', views.payment, name="payment"),
    path('payment_filter/', views.payment_filter, name="payment_filter"),
    path('download_bill/<int:id>/', views.download_bill, name="download_bill"),
    path('privacy/', views.privacy, name="privacy"),
    path('profile/', views.profile, name="profile"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('registration/', views.registration, name="registration"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('terms/', views.terms, name="terms"),
    path('feedback/', views.feedback, name="feedback"),
]
