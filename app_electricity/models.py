from django.db import models

# Create your models here.


class user(models.Model):
    name = models.CharField(max_length=150,null=True,blank=True)
    mobile_number = models.CharField(max_length=15,unique=True)
    email = models.EmailField(unique=True,null=True,blank=True)
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
