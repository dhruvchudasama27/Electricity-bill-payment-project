from django.db import models

# Create your models here.


class user(models.Model):
    name = models.CharField(max_length=150,null=True,blank=True)
    mobile_number = models.CharField(max_length=15,unique=True)
    email = models.EmailField(unique=True,null=True,blank=True)
    otp = models.IntegerField(default=0,null=True,blank=True)
    street_address = models.TextField()
    pincode = models.IntegerField()
    city = models.CharField(max_length=50,null=True,blank=True)
    state = models.CharField(max_length=50,null=True,blank=True)
    country = models.CharField(max_length=50,null=True,blank=True)
    password = models.CharField(max_length=128,null=True,blank=True)
    profile_photo = models.ImageField(upload_to="media/images/",null=True,blank=True)

    def __str__(self) -> str:
        return self.name
    
class Billing_detail(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE,blank=True,null=True)
    account_number = models.CharField(max_length=50,blank=True,null=True)
    customer_id = models.CharField(max_length=50,blank=True,null=True)
    billing_address = models.TextField()

    def __str__(self) -> str:
        return self.user.name


class Contact_message(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE,blank=True,null=True)
    first_name = models.CharField(max_length=150,null=True,blank=True)
    last_name = models.CharField(max_length=150,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    message = models.TextField()

    def __str__(self) -> str:
        return self.user.name


class Electricity_rate(models.Model):
    date = models.DateField(null=True,blank=True)
    rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self) -> str:
        return self.date.strftime('%B %Y')
    
class Electricity_news(models.Model):
    news = models.TextField()
    date = models.DateField(null=True,blank=True)

    def __str__(self) -> str:
        return self.news
    
choice = (("On the way","On the way"),("Delivered","Delivered"),("Cancelled","Cancelled"),("Returned","Returned"))
class Payment_history(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE,blank=True,null=True)
    payment_order = models.CharField(max_length=60,blank=True,null=True)
    amount = models.IntegerField()
    date = models.DateTimeField(blank=True,null=True)
    status = models.CharField(choices=choice,max_length=60,null=True,blank=True)

    def __str__(self) -> str:
        return self.status

class Feedback(models.Model):
    user = models.ForeignKey(user,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=150,null=True,blank=True)
    image = models.ImageField(blank=True,null=True)
    feedback_message = models.TextField()

    def __str__(self) -> str:
        return self.name

