from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from django.http import JsonResponse
from rest_framework import status
from movie_booking.Helpers.User.User import getUserById
from movie_booking.Helpers.movieHelper import GetMovieById
from bookingApp.Models.Booking.booking import Booking
from movie_booking.Helpers.getImageHelper import getImageFile


class BookingAPI(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        try:
            d = request.data
            d = json.dumps(d)
            dic = json.loads(d)
            if "user_Id" in dic.keys():
                user = getUserById(dic['user_Id'])
            if "movie_Id" in dic.keys():
                movie = GetMovieById(dic['movie_Id'])
            datetime = dic['datetime']
            booking = Booking(user_Id=user, movie_Id=movie, datatime=datetime)
            booking.save()
            return JsonResponse({"data":"","message": "Booking details save successfully", "status": status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({"data":"","message": ex, "status": status.HTTP_500_INTERNAL_SERVER_ERROR})

    def get(self,request,pk):
        try:
            user_Id = str(pk).replace('"', '')
            data = []
            booking_details = {}
            record = Booking.objects.select_related("user_Id").filter(user_Id=user_Id)
            for r in record:
                booking_details['movie_name'] = r.movie_Id.movie_name
                thumbnail = ""
                if r.movie_Id.thumbnail.name != "":
                    thumbnail = getImageFile(r.movie_Id.thumbnail.name)
                booking_details['thumbnail'] = thumbnail
                booking_details['datetime'] = r.datetime
            data.append(booking_details)
            return JsonResponse({"data": data,"message":"success", "status": status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({"data":"","message": ex, "status": status.HTTP_500_INTERNAL_SERVER_ERROR})