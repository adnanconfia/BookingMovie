from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from bookingApp.Models.users.user import User as UserModel
from ...Helpers.User.User import UserExistsByEmail, getUserById, getUserByMail, getAllUsers
from bookingApp.Models.users.userSerializer import UserSerializer
import jwt
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils.dateparse import parse_date
from bookingApp.Models.users.user import User
from django.http import JsonResponse


class UserAdmin(CreateAPIView):
    permission_classes = [IsAuthenticated,]

    def get(self,request):
        try:
            data = []
            records = User.objects.filter(IsDeleted = False).order_by('-Creation_Time')
            if records is not None:
                for r in records:
                    data.append({
                        'Id': r.Id,
                        'FirstName':r.FirstName,
                        'LastName':r.LastName,
                        'Email':r.Email,
                        'UserName':r.UserName,
                        'DOB':r.DOB,
                        'CI':r.CI,
                        'PhoneNumber':r.PhoneNumber,
                        'Gender':r.Gender,
                        'RoleName':r.RoleName,
                        'RoleType':r.RoleType
                    })
            return JsonResponse({"data":data,"message":"success","status":status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({"data":"","message":str(ex),"status":status.HTTP_500_INTERNAL_SERVER_ERROR})


class GetUserById(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        try:
            pk = str(pk).replace('"', '')
            user = User.objects.get(Id = pk)
            data = []
            data.append({
                'Id': user.Id,
                'FirstName':user.FirstName,
                'LastName':user.LastName,
                'UserName':user.UserName,
                'Email':user.Email,
                'DOB':user.DOB,
                'CI':user.CI,
                'PhoneNumber':user.PhoneNumber,
                'Gender':user.Gender
            })
            return JsonResponse({"data":data,"message":"success","status":status.HTTP_200_OK})
        except Exception as ex:
            return JsonResponse({"data":"","message":str(ex),"status":status.HTTP_500_INTERNAL_SERVER_ERROR})
