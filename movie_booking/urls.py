"""movie_booking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from movie_booking.Views.Login import Login
from movie_booking.Views.Login.Login import TokenVerify
from movie_booking.Views.Movie.Movie import MovieAPIView
from movie_booking import settings
from movie_booking.Views.Movie.movieVisitors import GetMovieAllForVisitor,GetDetails
from movie_booking.Views.Days.Days import DaysAPIView
from movie_booking.Views.Users.Users import User
from movie_booking.Views.appData import addData
from movie_booking.Views.Days.daysVisitors import DaysAPIViewVisitor
from movie_booking.Views.Seats.Seats import SeatsApiView
from movie_booking.Views.Booking.Bookings import BookingAPI
from movie_booking.Views.ForgetPassword.ForgetPassword import ForgetPassAPI
from movie_booking.Views.ForgetPassword.UpdatePassword import UpdatePassAPI

urlpatterns = [

    path('migrate',addData),
    path('login/', Login.Login),
    path('token/verify',TokenVerify.as_view() ),
    path('user/create', User.as_view()),
    path('movie',MovieAPIView.as_view()),
    path('datetime',DaysAPIView.as_view()),
    path('movie/<int:pk>',MovieAPIView.as_view()),
    path('movieVisitors',GetMovieAllForVisitor.as_view()),
    path('getMovieDetails/<int:pk>',GetDetails.as_view()),
    path('getTimes',DaysAPIViewVisitor.as_view()),
    path('getSeats/<int:pk>',SeatsApiView.as_view()),
    path('getSeats',SeatsApiView.as_view()),
    path('booking',BookingAPI.as_view()),
    path('booking/<int:pk>',BookingAPI.as_view()),
    path('forget',ForgetPassAPI.as_view()),
    path('updatepass',UpdatePassAPI.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
