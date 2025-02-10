from django.urls import path
from . import views

urlpatterns = [
path('',views.login),
path('logout/',views.logout,name='logout'),
path('userreg/',views.userregister,name='userreg'),
path('servicereg/',views.serviceregister,name='servicereg'),
path('userhome/',views.userhome,name='userhome'),
path('adminhome/',views.adminhome,name='adminhome'),
path('servicehome/',views.servicehome,name='servicehome'),
path('about/',views.about,name='about'),
path('contact/',views.contact,name='contact'),
path('menu/',views.menu,name='menu'),
path('service/',views.service,name='service'),
path('gallery/',views.gallery,name='gallery'),
path('adddishes/',views.adddishes,name='adddishes'),
path('viewdishes/',views.viewdishes,name='viewdishes'),
path('editdishes/<int:id>',views.editdishes,name='editdishes'),
path('deletedishes/<int:id>',views.deletedishes,name='deletedishes'),
]
