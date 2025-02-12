from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Register)
admin.site.register(cart)
admin.site.register(Buy)
admin.site.register(Product_quantity)
admin.site.register(Feedback)

