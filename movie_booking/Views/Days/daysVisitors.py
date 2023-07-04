import json
import base64
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from bookingApp.Models.days import Days
from bookingApp.Models.movie import Movie
from rest_framework.decorators import permission_classes
class DaysAPIViewVisitor(RetrieveUpdateAPIView):
    permission_classes(IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        try:
            d = request.body
            # d = json.dumps(d)
            dic = json.loads(d)
            times = []
            if 'movie_Id' in dic.keys():
                movie_Id = dic['movie_Id']
            if 'date' in dic.keys():
                date = dic['date']
            m = Movie.objects.get(pk = movie_Id)
            record = Days.objects.filter(movie_Id = m.Id, datetime__date=date).values_list('datetime', flat=True)
            if record is not None:
                for r in record:
                    times.append(r.time())
            return JsonResponse({'data': times,"message":"success", 'status': status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({'data':"","message": ex, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})
