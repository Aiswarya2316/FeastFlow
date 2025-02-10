from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _


class userreg(models.Model):
    email = models.EmailField(unique=True)
    name = models.TextField()
    phonenumber = models.IntegerField()
    password = models.TextField()
    location= models.TextField()

    def __str__(self):
        return self.name

class servicereg(models.Model):
    email = models.EmailField(unique=True)
    name = models.TextField()
    phonenumber = models.IntegerField()
    password = models.TextField()
    location= models.TextField()

    def __str__(self):
        return self.name
    

    
class Product(models.Model):
    service = models.ForeignKey(servicereg,on_delete=models.CASCADE)
    name = models.TextField()
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    offerprice = models.IntegerField()
    image = models.FileField()


    def __str__(self):
        return self.name
    

class Booking(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(userreg,on_delete=models.CASCADE)
    date_of_buying = models.TextField()
    quantity = models.IntegerField()
    price = models.IntegerField()

     # New field for delivery status
    DELIVERY_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("In Transit", "In Transit"),
        ("Delivered", "Delivered"),
    ]
    delivery_status = models.CharField(
        max_length=20, choices=DELIVERY_STATUS_CHOICES, default="Pending"
    )

    # Optional: define a string representation for clarity in admin
    def __str__(self):
        return f"{self.product.name} - {self.delivery_status}"