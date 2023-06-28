from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status

from bookingApp.Models.movie import Movie
from .getImageHelper import getImageFile


def GetMovieById(Id):
    try:
        movie = Movie.objects.get(pk=Id)
        return movie
    except Exception as ex:
        return None

@csrf_exempt
@require_http_methods(["GET"])
def GetMovieAll(request):
    try:
        data = []
        result = Movie.objects.filter(isDeleted= False).order_by('creation_date')
        if result.count() == 0:
            for r in result:
                thumbnail = ''
                if r.thumbnail.name != '':
                    thumbnail = getImageFile(r.thumbnail.name)
                if r.category == 'avatar':
                    avatar = []
                    avatar.append( {
                        'Id': r.Id,
                        'movie_name': r.movie_name,
                        'category': r.category,
                        'duration': r.duration,
                        'description': r.description,
                        'genre': r.genre,
                        'thumbnail': thumbnail
                    })
                if r.category == 'billboard':
                    billboard = []
                    avatar.append( {
                        'Id': r.Id,
                        'movie_name': r.movie_name,
                        'category': r.category,
                        'duration': r.duration,
                        'description': r.description,
                        'genre': r.genre,
                        'thumbnail': thumbnail
                    })
            data.append({
                'avatar':avatar,
                'billboard':billboard
            })
        return JsonResponse({'data':data,'status':status.HTTP_200_OK})
    except Exception as ex:
        return JsonResponse({'data':ex,'status':status.HTTP_500_INTERNAL_SERVER_ERROR})