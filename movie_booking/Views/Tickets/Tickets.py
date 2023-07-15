from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from django.http import JsonResponse
from rest_framework import status
from movie_booking.Helpers.User.User import getUserById
from movie_booking.Helpers.movieHelper import GetMovieById
from bookingApp.Models.Booking.booking import Booking
from movie_booking.Helpers.getImageHelper import getImageFile


class TicketAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ]

    def get(self,request,pk):
        try:
            user_Id = str(pk).replace('"', '')
            data = []
            record = Booking.objects.filter(user_Id=user_Id).values('user_Id', 'movie_Id').distinct()
            # record = Booking.objects.filter(user_Id=user_Id)
            print(len(record))
            for r in record:
                booking_details = {}
                seat_no = []

                seats = Booking.objects.filter(user_Id=r['user_Id'],movie_Id= r['movie_Id'])
                for s in seats:
                    booking_details['movie_name'] = s.movie_Id.movie_name
                    thumbnail = ""
                    if s.movie_Id.thumbnail.name != "":
                        thumbnail = getImageFile(s.movie_Id.thumbnail.name)
                    booking_details['thumbnail'] = thumbnail
                    booking_details['datetime'] = s.datetime
                    seat_no.append(s.seat_no)
                booking_details['seat_no']= seat_no
                data.append(booking_details)
            return JsonResponse({"data": data,"message":"success", "status": status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({"data":"","message": ex, "status": status.HTTP_500_INTERNAL_SERVER_ERROR})