from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    path('islands', views.island, name="islands"),
    #path('bookrum', views.bookrum, name="bookrum"),
    #path('bookmuck', views.bookmuck, name="bookmuck"),
    #path('bookeigg', views.bookeigg, name="bookeigg"),
    path('bookferry', views.bookferry, name="bookferry"),
    path('booked', views.bookings, name="booked"),
    path('signup', views.register, name="signup"),
    path('logout', views.logout_request, name="logout"),
    path('login', views.login_request, name="login"),
   
]
