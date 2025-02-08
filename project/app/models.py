from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class CateringService(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    available_from = models.DateField()
    available_to = models.DateField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    catering_service = models.ForeignKey(CateringService, on_delete=models.CASCADE)
    number_of_guests = models.PositiveIntegerField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=100, choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed')], default='Pending')

    def __str__(self):
        return f"{self.customer.username} - {self.event.name} - {self.status}"

    def calculate_total_cost(self):
        self.total_cost = self.number_of_guests * self.catering_service.price_per_person
        self.save()

class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment for {self.booking.event.name} by {self.booking.customer.username}"

