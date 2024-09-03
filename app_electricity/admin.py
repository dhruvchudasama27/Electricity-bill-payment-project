from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(user)
admin.site.register(Billing_detail)
admin.site.register(Contact_message)
admin.site.register(Electricity_rate)
admin.site.register(Electricity_news)
admin.site.register(Payment_history)
admin.site.register(Feedback)