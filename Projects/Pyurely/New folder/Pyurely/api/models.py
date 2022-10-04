from email.policy import default
from django.db import models
import uuid
# Create your models here.
Role = (
    ('admin','admin'),
    ('user','user')
)

class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    class Meta:
        abstract = True

class Account(BaseModel):
    firstname = models.CharField(max_length=255, default= "")
    lastname = models.CharField(max_length=255, default= "")
    contactno = models.CharField(max_length=255, default= "")
    email = models.EmailField(max_length=255 ,default= "")
    password = models.TextField(default= "")
    role = models.CharField(choices=Role,max_length=20,default="user")
    Profile= models.ImageField(upload_to='Account/',default="SuperAdmin/dummy.jpg")
    Otp = models.IntegerField(default=0)
    OtpStatus = models.CharField(max_length=10, default="False")
    OtpCount = models.IntegerField(default=0)
    passwordstatus = models.CharField(max_length=10,default="False")

class whitelistToken(BaseModel):
    user = models.ForeignKey(Account, on_delete =models.CASCADE)
    token = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    useragent = models.TextField(default="")


class Category(BaseModel):
    name = models.CharField(max_length=255 ,default= "")
    description = models.TextField(max_length=255 ,default="")


class Product(BaseModel):
    name = models.CharField(max_length=255,default="")
    description = models.CharField(max_length=255,default="")
    price = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    longdescription = models.TextField(max_length=255,default="")
    shortdescription = models.TextField(max_length=255,default="")
    categoryid = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)

class Productimage(BaseModel):
    image = models.ImageField(upload_to='Product/',default="")
    productid = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)

class Order(BaseModel):
    name = models.CharField(max_length=255, default="")
    total = models.FloatField( default=0)
    subtotal = models.FloatField( default = 0)
    quantity = models.IntegerField(default=0)
    paymentmethod = models.CharField(max_length=255, default="")
    orderStatus = models.CharField(max_length=255, default="")
    paymenttoken = models.TextField( default="")
    productid = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)

