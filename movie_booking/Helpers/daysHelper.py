from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from bookingApp.Models.days import Days


@csrf_exempt
@require_http_methods(["GET"])
def GetDateByMovieId(request, movie_Id):
    try:
        result = Days.objects.get(movie_Id=movie_Id)
        return result
    except Exception as ex:
        return None