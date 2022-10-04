from django.urls import path,include
from api.views import *

urlpatterns = [

#web urls  home
path('admin_login',admin_login.as_view()),
path('encryptpass',encryptpass.as_view()),
path('categoryAdd',categoryAdd.as_view()),
path('Getspecificcategory',Getspecificcategory.as_view()),
path('signup',signup.as_view()),
path('productsAdd',productsAdd.as_view()),
path('GetCustomerData',GetCustomerData.as_view()),
path('GetOrders',GetOrders.as_view()),
path('ProductGet',ProductGet.as_view()),
path('CategoryGet',CategoryGet.as_view()),
path('productsGet',productsGet.as_view()),
path('deletecategory',deletecategory.as_view()),
path('Getcategory',Getcategory.as_view()),
path('Updatecategory',Updatecategory.as_view()),
path('ProductCategoryGet',ProductCategoryGet.as_view()),
path('Getspecificcategory',Getspecificcategory.as_view()),


]

