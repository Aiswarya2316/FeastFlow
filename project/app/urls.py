from django.urls import path
from . import views
urlpatterns = [
path('login/',views.login),
path('logout/',views.logout),
path('register/',views.register),
path('shopregister/',views.shopregister),
path('',views.homes,name='homes'),
path('userhome/',views.userhome),
path('adminhome/',views.adminhome),
path('shophome/',views.shophome),
path('deliveryhome/',views.deliverys),
path('addpro/',views.addpro),
path('viewpro/',views.viewpro),
path('edit/<int:id>',views.edit),
path('delete/<int:id>',views.delete),
path('profile/',views.profile),
path('upload/',views.upload),
path('userviewproduct/',views.userviewproduct),
path('prodetails/<int:id>',views.prodetails),
path('shopprodetails/<int:id>',views.shopprodetails),
path('addtocart/<int:id>',views.user_cart),
path('user_view_cart/',views.user_view_cart),
path('qty_incri/<int:id>',views.qty_incri),
path('qty_decri/<int:id>',views.qty_decri),
path('buynow1/<int:id>',views.buynow1),
path('buynow/<int:id>',views.buynow),
path('deleteitem/<int:id>',views.deleteitem),
path('orderdetails/',views.orderdetails),
path('delregister/',views.delregister),
path('viewshop/',views.viewshop),
path('aboutus/',views.aboutus),
path('contact/',views.contact),
path('service/',views.service),
path('bookinghistry/',views.bookinghistry),
 path("booking-history/", views.booking_history, name="booking_history"),
path('search/', views.product_search, name='product_search'),
path("payment/<int:id>", views.order_payment, name="payment"),
path("razorpay/callback/", views.callback, name="callback"),

# path('submit_feedback/', views.submit_feedback, name='submit_feedback'),
# path('feedback_list/', views.feedback_list, name='feedback_list'),










]