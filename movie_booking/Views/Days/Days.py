import json
import base64
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from bookingApp.Models.days import Days
from bookingApp.Models.movie import Movie
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

    def put(self, request, *args, **kwargs):
        try:
            dic = request.data
            dic = json.dumps(dic)
            d = json.loads(dic)
            Id = d['Id']
            record = Days.objects.get(Id=Id)
            if record is None:
                return JsonResponse(
                    {"data":"","message": "No data found having Id: " + str(d['Id']), "status": status.HTTP_404_NOT_FOUND})
            else:
                if 'movie_Id' in d.keys():
                    movie = GetMovieById(d['movie_Id'])
                    record.movie_Id = movie
                if 'datetime' in d.keys():
                    record.datetime = d['datetime']
                # if 'day' in d.keys():
                #     record.day = d['day']
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
                    # movie = Movie.objects.get(Id= r.movie_Id.Id)
                    data.append({
                        'Id': r.Id,
                        'movie_Id': r.movie_Id.Id,
                        'movie_name':r.movie_Id.movie_name,
                        'datetime': r.datetime
                    })
            return JsonResponse({'data': data,"message":"success", 'status': status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({"data":"","message": ex, "status": status.HTTP_500_INTERNAL_SERVER_ERROR})


class GetDaysById(RetrieveUpdateAPIView):
    permission_classes(IsAuthenticated,)

    def get(self,request,pk):
        try:
            data = []
            pk = str(pk).replace('"', '')
            r = Days.objects.get(Id=pk)
            data.append({
                'Id': r.Id,
                'movie_Id': r.movie_Id.Id,
                'movie_name':r.movie_Id.movie_name,
                'datetime': r.datetime})
            return JsonResponse({'data': data,"message":"success", 'status': status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({"data":"","message": ex, "status": status.HTTP_500_INTERNAL_SERVER_ERROR})


