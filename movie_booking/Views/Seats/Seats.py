import json

from django.forms import model_to_dict
from rest_framework.generics import RetrieveUpdateAPIView
from bookingApp.Models.seats.seats import Seats
from bookingApp.Models.days import Days
from bookingApp.Models.movie import Movie
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from movie_booking.Helpers.getImageHelper import getImageFile
from rest_framework.decorators import permission_classes

class SeatsApiView(RetrieveUpdateAPIView):
    permission_classes(IsAuthenticated,)

    def get(self, request, pk):
        try:
            # dic = request.data
            # dic = json.dumps(dic)
            # d = json.loads(dic)
            pk = str(pk).replace('"', '')
            seat_status={0:"Available",1:"Reserved",2:"People with disabilities"}
            data = {}
            seat = []
            seats = Seats.objects.select_related("days_Id").filter(days_Id =pk)
            for s in seats:
                data['Id'] = s.Id
                data['movie_name']=s.days_Id.movie_Id.movie_name

                thumbnail = ''
                if s.days_Id.movie_Id.thumbnail.name != '':
                    thumbnail = getImageFile(s.days_Id.movie_Id.thumbnail.name)
                data['thumbnail'] = thumbnail
                data['datetime'] = s.days_Id.datetime
                seats_data = model_to_dict(s)
                # print(seats_data)
                for n in range(1, 51):
                    # print(seats_data['seat'+str(n)])
                    seat.append({
                        'seat_No': n,
                        'seat_status': seats_data['seat'+str(n)],
                        'seat_status_name': seat_status[seats_data['seat'+str(n)]]
                    })

            data['seats'] = seat

            return JsonResponse({'data': data, 'status': status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({'data': ex, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

    def post(self,request):
        try:
            dic = request.data
            dic = json.dumps(dic)
            d = json.loads(dic)
            print(d['seats'])
            print(d['seats'][0])
            print(d['seats'][1])
            Id = d['Id']
            if 'seats' in d.keys():
                query = Seats.objects.get(Id = Id)
                query_d = model_to_dict(query)
                seats = d['seats']
                for s in seats:
                    seat_no = s['seat_No']
                    seat_status = s['seat_status']
                    seat_str = "seat"+str(seat_no)
                    if seat_str == 'seat1':
                        query.seat1 = seat_status
                    if seat_str == 'seat2':
                        query.seat2 = seat_status
                    if seat_str == 'seat3':
                        query.seat3 = seat_status
                    if seat_str == 'seat4':
                        query.seat4 = seat_status
                    if seat_str == 'seat5':
                        query.seat5 = seat_status
                    if seat_str == 'seat6':
                        query.seat6 = seat_status
                    if seat_str == 'seat7':
                        query.seat7 = seat_status
                    if seat_str == 'seat8':
                        query.seat8 = seat_status
                    if seat_str == 'seat9':
                        query.seat9 = seat_status
                    if seat_str == 'seat10':
                        query.seat10 = seat_status
                    if seat_str == 'seat11':
                        query.seat11 = seat_status
                    if seat_str == 'seat12':
                        query.seat12 = seat_status
                    if seat_str == 'seat13':
                        query.seat13 = seat_status
                    if seat_str == 'seat14':
                        query.seat14 = seat_status
                    if seat_str == 'seat15':
                        query.seat15 = seat_status
                    if seat_str == 'seat16':
                        query.seat16 = seat_status
                    if seat_str == 'seat17':
                        query.seat17 = seat_status
                    if seat_str == 'seat18':
                        query.seat18 = seat_status
                    if seat_str == 'seat19':
                        query.seat19 = seat_status
                    if seat_str == 'seat20':
                        query.seat20 = seat_status
                    if seat_str == 'seat21':
                        query.seat21 = seat_status
                    if seat_str == 'seat22':
                        query.seat22 = seat_status
                    if seat_str == 'seat23':
                        query.seat23 = seat_status
                    if seat_str == 'seat24':
                        query.seat24 = seat_status
                    if seat_str == 'seat25':
                        query.seat25 = seat_status
                    if seat_str == 'seat26':
                        query.seat26 = seat_status
                    if seat_str == 'seat27':
                        query.seat27= seat_status
                    if seat_str == 'seat28':
                        query.seat28 = seat_status
                    if seat_str == 'seat29':
                        query.seat29 = seat_status
                    if seat_str == 'seat30':
                        query.seat30 = seat_status
                    if seat_str == 'seat31':
                        query.seat31 = seat_status
                    if seat_str == 'seat32':
                        query.seat32 = seat_status
                    if seat_str == 'seat33':
                        query.seat33 = seat_status
                    if seat_str == 'seat34':
                        query.seat34 = seat_status
                    if seat_str == 'seat35':
                        query.seat35 = seat_status
                    if seat_str == 'seat36':
                        query.seat36 = seat_status
                    if seat_str == 'seat37':
                        query.seat37 = seat_status
                    if seat_str == 'seat38':
                        query.seat38 = seat_status
                    if seat_str == 'seat39':
                        query.seat39 = seat_status
                    if seat_str == 'seat40':
                        query.seat40 = seat_status
                    if seat_str == 'seat41':
                        query.seat41 = seat_status
                    if seat_str == 'seat42':
                        query.seat42 = seat_status
                    if seat_str == 'seat43':
                        query.seat43= seat_status
                    if seat_str == 'seat44':
                        query.seat44 = seat_status
                    if seat_str == 'seat45':
                        query.seat45 = seat_status
                    if seat_str == 'seat46':
                        query.seat46 = seat_status
                    if seat_str == 'seat47':
                        query.seat47 = seat_status
                    if seat_str == 'seat48':
                        query.seat48 = seat_status
                    if seat_str == 'seat49':
                        query.seat49 = seat_status
                    if seat_str == 'seat50':
                        query.seat50 = seat_status
                    query.save()
                return JsonResponse({'data': "Seat booked successfully", 'status': status.HTTP_200_OK})
            return JsonResponse({'data': "Seat not reserved", 'status': status.HTTP_400_BAD_REQUEST})
        except Exception as ex:
            return JsonResponse({'data': ex, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})

