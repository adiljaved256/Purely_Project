from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Productimage)
admin.site.register(Order)
admin.site.register(whitelistToken)

admin.site.site_header = 'Pyurely'






