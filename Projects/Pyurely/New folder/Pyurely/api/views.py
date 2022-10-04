from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import api.usable as uc
from .models import *
from passlib.hash import django_pbkdf2_sha256 as handler
import jwt 
import random
import datetime
from decouple import config

# Create your views here.

### ADMIN  AND CUSTUMER LOGIN
class admin_login(APIView):
     def post(self,request):
         requireFields = ['email','password']
         validator = uc.keyValidation(True,True,request.data,requireFields)
            
         if validator:
            return Response(validator,status = 200)
            
         else:
               email = request.data.get('email')
               password = request.data.get('password')
               fetchAccount = Account.objects.filter(email=email).first()
               if fetchAccount:
                  if handler.verify(password,fetchAccount.password):
                     if fetchAccount.role == 'admin':
                        access_token_payload = {
                              'id':str(fetchAccount.uid),
                              'firstname':fetchAccount.firstname, 
                              'email':fetchAccount.email, 
                              'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                              'iat': datetime.datetime.utcnow(),

                           }

                        
                        access_token = jwt.encode(access_token_payload,config('adminkey'),algorithm = 'HS256')
                        data = {'uid':fetchAccount.uid,'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'email':fetchAccount.email,'contactno':fetchAccount.contactno,'role':fetchAccount.role,'Profile':fetchAccount.Profile.url}

                        whitelistToken(user = fetchAccount,token = access_token,useragent = request.META['HTTP_USER_AGENT'],created_at = datetime.datetime.now()).save()

                        
                        return Response({"status":True,"message":"Login Successlly","token":access_token,"admindata":data})

                     else:
                        access_token_payload = {
                              'id':str(fetchAccount.uid),
                              'firstname':fetchAccount.firstname, 
                              'email':fetchAccount.email, 
                              'exp': datetime.datetime.utcnow() + datetime.timedelta(days=22),
                              'iat': datetime.datetime.utcnow(),

                           }

                        
                        access_token = jwt.encode(access_token_payload,config('customerkey'),algorithm = 'HS256')
                        data = {'uid':fetchAccount.uid,'firstname':fetchAccount.firstname,'lastname':fetchAccount.lastname,'email':fetchAccount.email,'contactno':fetchAccount.contactno,'role':fetchAccount.role,'Profile':fetchAccount.Profile.url}

                        whitelistToken(user = fetchAccount,token = access_token,useragent = request.META['HTTP_USER_AGENT'],created_at = datetime.datetime.now()).save()

                        
                        return Response({"status":True,"message":"Login Successlly","token":access_token,"custumerdata":data})
                  else:
                     return Response({"status":False,"message":"Please Enter correct role"})
               else:
                  return Response({"status":False,"message":"Please Enter a correct Password"})
          
        
### PASSWORD ENCRYPTED

class encryptpass(APIView):
    def post(self,request):
        try:    
            passw = handler.hash(request.data.get('passw'))


            return HttpResponse(passw)

        except Exception as e:
            
            message = {'status':'Error','message':str(e)}
            return Response(message)


class categoryAdd(APIView):

### CATEGORY ADD
   def post(self,request):
      requireFields = ['name','description']
      validator = uc.keyValidation(True,True,request.data,requireFields)
            
      if validator:
         return Response(validator,status = 200)
            
      else:
         my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
         if my_token:
            name  = request.data.get('name')
            description = request.data.get('description')
            
            data = Category(name = name, description = description)
            data.save()

            return Response ({"status":True,"message":"Category Successlly Add"})
         else:
            return Response ({"status":False,"message":"Unauthorized"})

### CATEGORY GETssss
class Getcategory(APIView):
   def get (self,request):
      my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
      if my_token:
         data = Category.objects.all().values('uid','name','description').order_by("-uid")
         return Response ({"status":True,"data":data })
      else:
         return Response ({"status":False,"message":"Unauthorized"})

### CATEGORY UPDATE
class Updatecategory(APIView):
   def put (self,request):
      requireFields = ['uid','name','description']
      validator = uc.keyValidation(True,True,request.data,requireFields)
            
      if validator:
         return Response(validator,status = 200)
            
      else:
         my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
         if my_token:
            uid = request.data.get('uid')

            checkcategory= Category.objects.filter(uid = uid).first()

            if checkcategory:
               checkcategory.name = request.data.get('name') 
               checkcategory.description = request.data.get('description') 

               checkcategory.save()
               return Response({"status":True,"message":"Category Updated Successfully"})
            else:
               return Response({"status":True,"message":"Data not found"})

         else:
            return Response ({"status":False,"message":"Unauthorized"})

### CATEGORY DELETE 
class deletecategory(APIView):
   def delete(self,request):
      requireFields = ['uid']
      validator = uc.keyValidation(True,True,request.GET,requireFields)
            
      if validator:
         return Response(validator,status = 200)
            
      else:
         my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
         if my_token:
            uid = request.GET['uid']
            data = Category.objects.filter(uid = uid).first()
            if data:
               data.delete()
               return Response({"status":True,"message":"Data Deleted Successfully"})
            else:
               return Response({"status":False,"message":"Data not found"})

class Getspecificcategory(APIView):
   def get(self,request):
      requireFields = ['uid']
      validator = uc.keyValidation(True,True,request.GET,requireFields)
            
      if validator:
         return Response(validator,status = 200)
            
      else:
         my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
         if my_token:
               uid = request.GET['uid']
               data = Category.objects.filter(uid = uid).values("uid","name",'description').first()
               if data:
                  return Response({"status":True,"data":data},200)
               else:
                  return Response({"status":False,"message":"Data not found"})
      
### ADMIN PRODUCT ADD

class productsAdd(APIView):
### ADD PRODUCT
   def post(self,request):
      requireFields = ['name','description','price','discount','longdescription','shortdescription','categoryid']
      validator = uc.keyValidation(True,True,request.data,requireFields)
            
      if validator:
         return Response(validator,status = 200)
      else:
         my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
         if my_token:
            name = request.data.get('name')
            description = request.data.get('description')
            price = request.data.get('price')
            discount = request.data.get('discount')
            longdescription = request.data.get('longdescription')
            shortdescription = request.data.get('shortdescription')
            categoryid = request.data.get('categoryid')
            image = request.data.getlist('image')

            getcategory = Category.objects.filter(uid = categoryid).first()

            data = Product(name = name ,description = description, price = price,discount = discount,longdescription = longdescription,shortdescription = shortdescription, categoryid = getcategory)
            data.save()

            for i in range(len(image)):

               imageObj = Productimage(productid = data,image =image[i]  )
               imageObj.save()

            return Response ({"status":True,"message":"Product created successfully"})
         
         else:
            return Response ({"status":False,"message":"Unauthorized"})

### GET PRODUCT
class productsGet(APIView):
   def get (self,request):
      my_token = uc.customertokenauth(request.META['HTTP_AUTHORIZATION'][7:])
      if my_token:
         data = Product.objects.all().values('uid','name','description','price','discount','longdescription','shortdescription','categoryid').order_by("-uid")
         return Response ({"status":True,"data":data })
      else:
         return Response ({"status":False,"message":"Unauthorized"})


### GET CUSTUMERDATA

class GetCustomerData(APIView):
    def get (self, request):
         my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
         if my_token:
               data = Account.objects.filter(role="user").values('uid','firstname','lastname','contactno','email','password','Profile').order_by('-uid')
               return Response({"status":True,"data":data})
         else:
               return Response({"status":False,"message":"Unauthenticated"})


class GetOrders(APIView):
   def get(self, request):
      my_token = uc.admintokenauth(request.META['HTTP_AUTHORIZATION'][7:])
      if my_token:
         data = Order.objects.all().values('uid','name','total','subtotal','quantity','paymentmethod','orderStatus','paymenttoken','productid').order_by('-uid')
         return Response({"status":True,"data":data})
      else:
            return Response({"status":False,"message":"Unauthenticated"})


      
### CUSTUMER SIGNIN

class signup(APIView):
   def post(self,request):
      requireFields = ['firstname','lastname','contactno','email','password','Profile']
      validator = uc.keyValidation(True,True,request.data,requireFields)
            
      if validator:
         return Response(validator,status = 200)
            
      else:
         firstname  = request.data.get('firstname')
         lastname  = request.data.get('lastname')
         contactno  = request.data.get('contactno')
         email  = request.data.get('email')
         password  = request.data.get('password')
         Profile  = request.data.get('Profile')
         
         if uc.checkemailforamt(email):
            if not uc.passwordLengthValidator(password):
               return Response({"status":False, "message":"Password should not be than 8 or greater than 20"})

            checkemail=Account.objects.filter(email=email).first()
            if checkemail:
               return Response({"status":False, "message":"Email already exists"})

            checkcontactno=Account.objects.filter(contactno=contactno).first()
            if checkcontactno:
               return Response({"status":False, "message":"phone no already existsplease try different number"})
      
            data = Account(firstname=firstname,lastname=lastname,password= handler.hash(password),email = email, 
            contactno=contactno, role= 'user', Profile=Profile)
         
            
            data.save()

            return Response({"status":True,"message":"Account Created Successfully"})

         else:
            return Response({"status":False,"message":"Email Format Is Incorrect"})


# Product Get
class ProductGet(APIView):
   def get (self,request):
         data = Product.objects.all().values('uid','name','description','price','discount','longdescription','shortdescription','categoryid').order_by("-uid")
         
         return Response ({"status":True, "data":data })


class CategoryGet(APIView):
   def get(self, request):
        data = Category.objects.all().values('name','description')
        
        return Response({'status':True, 'data': data})


# Product Get
class ProductCategoryGet(APIView):
   def get (self,request):

         data = Product.objects.all().values('uid','name','description','price','discount','longdescription','shortdescription','categoryid').order_by("-uid")
         user = Category.objects.all().values('uid','name','description')

         return Response ({"status":True, "data":data , "user":user})



class Getspecificcategory(APIView):
   def get(self,request):
      requireFields = ['name']
      
      validator = uc.keyValidation(True,True,request.GET,requireFields)
            
      if validator:
         return Response(validator,status = 200)
        
      else:
         name = request.GET['name']
         
         data = Product.objects.filter(name = name).values('uid','name','description','price','discount','longdescription','shortdescription','categoryid').order_by("-uid").first()
         if data:
           
            return Response({"status":True,"data":data},200)
         
         else:
            return Response({"status":False,"message":"Data not found"})
    

class signup(APIView):
   def post(self,request):
      requireFields = ['firstname','lastname','contactno','email','password','Profile']
      validator = uc.keyValidation(True,True,request.data,requireFields)
            
      if validator:
         return Response(validator,status = 200)
            
      else:
         firstname  = request.data.get('firstname')
         lastname  = request.data.get('lastname')
         contactno  = request.data.get('contactno')
         email  = request.data.get('email')
         password  = request.data.get('password')
         Profile  = request.data.get('Profile')
         
         if uc.checkemailforamt(email):
            if not uc.passwordLengthValidator(password):
               return Response({"status":False, "message":"Password should not be than 8 or greater than 20"})

            checkemail=Account.objects.filter(email=email).first()
            if checkemail:
               return Response({"status":False, "message":"Email already exists"})

            checkcontactno=Account.objects.filter(contactno=contactno).first()
            if checkcontactno:
               return Response({"status":False, "message":"phone no already existsplease try different number"})
      
            data = Account(firstname=firstname,lastname=lastname,password= handler.hash(password),email = email, 
            contactno=contactno,  Profile=Profile)
         
            
            data.save()

            return Response({"status":True,"message":"Account Created Successfully"})

         else:
            return Response({"status":False,"message":"Email Format Is Incorrect"})