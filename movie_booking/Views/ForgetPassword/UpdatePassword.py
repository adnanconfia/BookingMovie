from movie_booking.Helpers.User.User import getUserByMail,getUserById
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from django.http import JsonResponse
from rest_framework import status


class UpdatePassAPI(RetrieveUpdateAPIView):
    permission_classes = [AllowAny,]

    def post(self,request):
        try:
            d = request.data
            d = json.dumps(d)
            dic = json.loads(d)
            if 'id' in dic.keys():
                Id = dic['id']
                user = getUserById(Id)

            if 'email' in dic.keys():
                Email = dic['email']
                user = getUserByMail(Email)

            password = dic['password']
            user.set_password(password)
            user.save()
            return JsonResponse({"data":"","message":"Password reset successfully","status":status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse ({"data":"","message":ex,"status":status.HTTP_500_INTERNAL_SERVER_ERROR})