import json
import base64
from urllib.parse import urlparse, parse_qs
from django.core.files.base import ContentFile
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from bookingApp.Models.movie import Movie
from movie_booking.Helpers.getImageHelper import getImageFile
from rest_framework.decorators import permission_classes

class MovieAPIView(RetrieveUpdateAPIView):
    # permission_classes = [IsAuthenticated,]
    permission_classes(IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            dic = request.data
            dic = json.dumps(dic)
            d = json.loads(dic)
            thumbnail = ''
            if d['thumbnail'] != '':
                thumbnail_name = d['thumbnail'].split('\\')[-1]
                thumbnail_name = thumbnail_name.split('.')[0]
                print(thumbnail_name)
            imagefile = ''
            if d['thumbnailSource'] != '':
                thumbnail_b64 = d['thumbnailSource']
                format, imgstr = thumbnail_b64.split(';base64,')
                ext = format.split('/')[-1]
                thumbnail = ContentFile(base64.b64decode(imgstr), name=thumbnail_name + "." + ext)
            # if d['category'] != '':
            category_Id = 0
            if d['category_Id'] != '':
                if int(d['category_Id']) == 0:
                    category_Id = d['category_Id']
                    category = 'Presale'
                if int(d['category_Id']) == 1:
                    category_Id = d['category_Id']
                    category = 'Premieres'
                if int(d['category_Id']) == 2:
                    category_Id = d['category_Id']
                    category = 'Billboard'
            movie = Movie(movie_name=d['movie_name'], category=category,category_Id=category_Id, duration=d['duration'],
                          description=d['description'], genre=d['genre'], thumbnail=thumbnail)
            movie.save()
            return JsonResponse({'data': 'Movie added successfully', 'status': status.HTTP_201_CREATED})
        except Exception as ex:
            return JsonResponse({'data': ex, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

    def put(self, request, pk, *args, **kwargs):
        try:
            dic = request.data
            dic = json.dumps(dic)
            d = json.loads(dic)
            pk = str(pk).replace('"', '')
            movie = Movie.objects.get(Id=pk)
            if movie is None:
                return JsonResponse(
                    {"data": "No data found having Id: " + str(d['Id']), "status": status.HTTP_404_NOT_FOUND})
            else:
                thumbnail = ''
                if d['thumbnail'] != '':
                    thumbnail_name = d['thumbnail'].split('\\')[-1]
                    thumbnail_name = thumbnail_name.split('.')[0]
                    print(thumbnail_name)
                thumbnailfile = ''
                if d['thumbnailSource'] != '':
                    thumbnail_b64 = d['thumbnailSource']
                    format, imgstr = thumbnail_b64.split(';base64,')
                    ext = format.split('/')[-1]
                    thumbnail = ContentFile(base64.b64decode(imgstr), name=thumbnail_name + "." + ext)
                if 'movie_name' in d.keys():
                    movie.movie_name = d['movie_name']
                if 'category_Id' in d.keys():
                    if int(d['category_Id']) == 0:
                        category_Id = d['category_Id']
                        category = 'Presale'
                    if int(d['category_Id']) == 1:
                        category_Id = d['category_Id']
                        category = 'Premieres'
                    if int(d['category_Id']) == 2:
                        category_Id = d['category_Id']
                        category = 'Billboard'
                    movie.category = category
                    movie.category_Id = category_Id
                if 'duration' in d.keys():
                    movie.duration = d['duration']
                if 'description' in d.keys():
                    movie.description = d['description']
                if 'genre' in d.keys():
                    movie.genre = d['genre']
                if ("isDeleted" in d.keys()):
                    movie.isDeleted = d['isDeleted']
                if 'thumbnail' in d.keys():
                    if d['thumbnail'] != '':
                        movie.thumbnail = thumbnail
                movie.save()
                return JsonResponse({'data': 'Record updated successfully', 'status': status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({'data': ex, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

    def get(self, request, *args, **kwargs):
        try:
            data = []
            row = Movie.objects.filter(isDeleted=False).order_by('-creation_date')
            if row is None:
                return JsonResponse({'data': data, 'status': status.HTTP_404_NOT_FOUND})
            else:
                for r in row:
                    thumbnail = ''
                    if r.thumbnail.name != '':
                        thumbnail = getImageFile(r.thumbnail.name)
                    data.append({
                        'Id': r.Id,
                        'movie_name': r.movie_name,
                        'category': r.category,
                        'duration': r.duration,
                        'description': r.description,
                        'genre': r.genre,
                        'thumbnail': thumbnail
                    })
            return JsonResponse({'data': data, 'status': status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({'data': ex, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})
