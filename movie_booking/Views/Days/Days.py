import json
import base64
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from bookingApp.Models.days import Days
from movie_booking.Helpers.movieHelper import GetMovieById
from bookingApp.Models.seats.seats import Seats
from rest_framework.decorators import permission_classes
class DaysAPIView(RetrieveUpdateAPIView):
    permission_classes(IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            dic = request.data
            dic = json.dumps(dic)
            d = json.loads(dic)
            movie = GetMovieById(d['movie_Id'])
            days = Days(movie_Id=movie, datetime=d['datetime'])
            days.save()
            record = Days.objects.all().last()
            seats = Seats(days_Id=record)
            seats.save()
            return JsonResponse({'data':"","message": 'Record added successfully', 'status': status.HTTP_201_CREATED})
        except Exception as ex:
            return JsonResponse({"data":"","message": ex, "status": status.HTTP_500_INTERNAL_SERVER_ERROR})

    def put(self, request, pk, *args, **kwargs):
        try:
            dic = request.data
            dic = json.dumps(dic)
            d = json.loads(dic)
            pk = str(pk).replace('"', '')
            record = Days.objects.get(Id=pk)
            if record is None:
                return JsonResponse(
                    {"data":"","message": "No data found having Id: " + str(d['Id']), "status": status.HTTP_404_NOT_FOUND})
            else:
                if 'movie_Id' in d.keys():
                    record.movie_Id = d['movie_Id']
                if 'date' in d.keys():
                    record.date = d['date']
                if 'day' in d.keys():
                    record.day = d['day']
                record.save()
                return JsonResponse({'data':"","message": 'Record updated successfully', 'status': status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({"data":"","message": ex, "status": status.HTTP_500_INTERNAL_SERVER_ERROR})

    def get(self, request, *args, **kwargs):
        try:
            data = []
            row = Days.objects.filter(isDeleted=False).order_by('-creation_date')
            if row is None:
                return JsonResponse({'data': data,"message":"No record found", 'status': status.HTTP_404_NOT_FOUND})
            else:
                for r in row:
                    data.append({
                        'Id': r.Id,
                        'movie_Id': r.movie_Id,
                        'date': r.date,
                        'day': r.day
                    })
            return JsonResponse({'data': data,"message":"success", 'status': status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({"data":"","message": ex, "status": status.HTTP_500_INTERNAL_SERVER_ERROR})
