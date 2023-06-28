from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from django.db.models.functions import Cast
from django.db.models import DateField
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from bookingApp.Models.movie import Movie
from movie_booking.Helpers.category import category
from movie_booking.Helpers.getImageHelper import getImageFile
from bookingApp.Models.days import Days
from rest_framework.decorators import permission_classes

class GetMovieAllForVisitor(RetrieveUpdateAPIView):
    permission_classes(IsAuthenticated,)
    def get(self, request):
        try:
            data = {}
            result = Movie.objects.filter(isDeleted=False).order_by('creation_date')
            if result is not None:
                billboard = []
                premieres = []
                presale = []
                for r in result:
                    thumbnail = ''
                    if r.thumbnail.name != '':
                        thumbnail = getImageFile(r.thumbnail.name)
                    if int(r.category_Id) == 0:
                        presale.append({
                            'Id': r.Id,
                            'movie_name': r.movie_name,
                            'category': r.category,
                            'duration': r.duration,
                            'description': r.description,
                            'genre': r.genre,
                            'thumbnail': thumbnail
                        })
                    if int(r.category_Id) == 1:
                        premieres.append({
                            'Id': r.Id,
                            'movie_name': r.movie_name,
                            'category': r.category,
                            'duration': r.duration,
                            'description': r.description,
                            'genre': r.genre,
                            'thumbnail': thumbnail
                        })
                    if int(r.category_Id) == 2:
                        billboard.append({
                            'Id': r.Id,
                            'movie_name': r.movie_name,
                            'category': r.category,
                            'duration': r.duration,
                            'description': r.description,
                            'genre': r.genre,
                            'thumbnail': thumbnail
                        })
                data['presale'] = presale
                data['premieres'] = premieres
                data['billboard'] = billboard
            return JsonResponse({'data': data, 'status': status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({'data': ex, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})


class GetDetails(RetrieveAPIView):
    permission_classes = [AllowAny,]
    def get(self, request, pk):
        try:
            data = {
                # dates:[]
            }
            dates = []
            pk = str(pk).replace('"', '')

            movie = Movie.objects.get(pk=pk)
            days = Days.objects.filter(movie_Id=movie.Id)
            converted_queryset = days.annotate(
                date_only=Cast('datetime', output_field=DateField())
            )

            # Retrieve unique dates from the queryset
            unique_dates = converted_queryset.values('date_only').distinct()
            data['Id'] = movie.Id
            data['movie_name'] = movie.movie_name

            thumbnail = ''
            if movie.thumbnail.name !='':
                thumbnail = getImageFile(movie.thumbnail.name)
            data['thumbnail']= thumbnail
            # if int(movie.category_Id) == 0:
            #     data['category'] = category['0']
            data['category'] = movie.category
            data['duration'] = movie.duration
            data['description'] = movie.description
            data['genre'] = movie.genre

            for day in unique_dates:
                dates.append(day['date_only'])
            data['dates'] = dates
            print(data)
            return JsonResponse({'data': data, 'status': status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({'data': ex, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

