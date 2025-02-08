from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Event, CateringService, Booking
from django.contrib.auth.decorators import login_required

def event_list(request):
    events = Event.objects.all()
    return render(request, 'catering/event_list.html', {'events': events})

def catering_service_list(request):
    services = CateringService.objects.all()
    return render(request, 'catering/catering_service_list.html', {'services': services})

@login_required
def book_catering(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        service_id = request.POST['service']
        number_of_guests = int(request.POST['guests'])
        catering_service = CateringService.objects.get(id=service_id)
        booking = Booking.objects.create(
            customer=request.user,
            event=event,
            catering_service=catering_service,
            number_of_guests=number_of_guests
        )
        booking.calculate_total_cost()
        return redirect('booking_confirmation', booking_id=booking.id)

    services = CateringService.objects.all()
    return render(request, 'catering/book_catering.html', {'event': event, 'services': services})

def booking_confirmation(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    return render(request, 'catering/booking_confirmation.html', {'booking': booking})

