from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('services/', views.catering_service_list, name='catering_service_list'),
    path('book/<int:event_id>/', views.book_catering, name='book_catering'),
    path('booking_confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
]
