import datetime
import json
import jwt
from django.contrib.auth import authenticate, user_logged_in
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from bookingApp.Models.users.userSerializer import UserSerializer
from bookingApp.Models.users.user import User
from movie_booking.Helpers.Auth.token import get_token_for_user, verify_token
from django.forms import model_to_dict
from django.http import JsonResponse
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework.generics import RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from movie_booking import settings
from django.views.decorators.http import require_http_methods

from movie_booking.Helpers.User.User import getUserById, getUserByMail, UserExistsByEmail


@csrf_exempt
@api_view(["POST"])
@permission_classes([AllowAny])
def Login(request):
    try:
        x = request.body

        # print(x)
        # x = json.dumps(x)

        x = json.loads(x)
        # print(x)

        email = x['Email']

        password = x['Password']
        # print(email)
        # print(password)

        # password = PasswordManager.encrypt(password)

        user = authenticate(Email=email, password=password)
        # print(user,"User")

        if user and user.IsDeleted == False and user.IsActive == True:
            try:
                user.id=user.Id
                payload = get_token_for_user(user)
                # token = jwt.encode(payload, settings.SECRET_KEY)

                user_details = {}
                user_details['Token'] = payload['access']

                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                user_details["user"] = UserSerializer(user).data


                return Response({"data""": user_details, "status": status.HTTP_200_OK})
            except Exception as e:

                return Response({"data": str(e), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            res = 'can not authenticate with the given credentials or the account has been deactivated'
            return Response({"data": str(res), "status":status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)


    except KeyError:
        res =  'please provide a email and a password'
        return Response({"data": str(res), "status": 500}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class TokenVerify(TokenViewBase):
    # permission_classes = (IsAuthenticated,)
    serializer_class = TokenObtainPairSerializer

    def post(self, request):
        # authenitcate() verifies and decode the token
        # if token is invalid, it raises an exception and returns 401
        return verify_token(request)

# class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     permission_classes = (AllowAny,)
#
#     def post(self, request):
#
#         data = request.data
#         # print(user)
#         dic = json.dumps(data)
#         # print(type(dic))
#         dic = json.loads(dic)
#
#         if (dic['Id'] == 0 or dic['Id'] is None):
#             if user.objects.filter(Email=dic['Email'], IsDeleted=False).exists():
#                 return Response(
#                     {"error": "User already exists"},
#                     status=status.HTTP_500_INTERNAL_SERVER_ERROR
#                 )
#             if (user.objects.filter(Email=dic['Email'], IsDeleted=True).exists()):
#                 _user = user.objects.get(Email=dic['Email'], IsDeleted=True)
#                 _user.delete()
#             # print((dic),"dic")
#
#             _user =user(UserName=dic['Name'], Email=dic['Email'],FirstName=dic['FirstName'], LastName= dic['LastName'],DOB=dic['DOB'],
#                         Creation_Time=datetime.datetime.now(), Deletion_Time=None, isDeleted=False,
#                         isActive=dic['isActive'],
#                         )
#             _user.set_password(dic['Password'])
#             _user.save()
#             serializer = UserSerializer(_user)
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             _user = user.objects.get(pk=dic['Id'])
#             if ("Password" in dic.keys()):
#                 IsActive = False
#                 IsDeleted = False
#                 if ("FristName" in dic.keys()):
#                     _user.FristName = dic['FristName']
#                 if ("LastName" in dic.keys()):
#                     _user.LastName = dic['LastName']
#                 if ("DOB" in dic.keys()):
#                     _user.DOB = dic['DOB']
#                 if (dic['isActive'] == True):
#                     IsActive = True
#                     IsDeleted = False
#                 if (dic['isDeleted'] == True):
#                     IsActive = False
#                     IsDeleted = True
#                 if ("UserName" in dic.keys()):
#                     _user.UserName = dic['UserName']
#                 if ("Email" in dic.keys()):
#                     _user.Email = dic['Email']
#                 _user.RoleType = dic['RoleType']
#                 _user.RoleName = dic['RoleName']
#                 _user.IsActive = IsActive
#                 _user.IsDeleted = IsDeleted
#                 _user.set_password(dic['Password'])
#
#                 _user.save()
#                 serializer = UserSerializer(_user)
#
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#             else:
#                 _user = user.objects.get(pk=dic['Id'])
#
#                 IsActive = False
#                 IsDeleted = False
#                 if ("FristName" in dic.keys()):
#                     _user.FristName = dic['FristName']
#                 if ("LastName" in dic.keys()):
#                     _user.LastName = dic['LastName']
#                 if ("DOB" in dic.keys()):
#                     _user.DOB = dic['DOB']
#                 if (dic['isActive'] == True):
#                     IsActive = True
#                     IsDeleted = False
#                 if (dic['isDeleted'] == True):
#                     IsActive = False
#                     IsDeleted = True
#                 if("UserName" in dic.keys()):
#                     _user.UserName = dic['UserName']
#                 if("Email" in dic.keys()):
#                     _user.Email = dic['Email']
#                 # _user.RoleType = dic['RoleType']
#                 # _user.RoleName = dic['RoleName']
#                 _user.IsActive = IsActive
#                 # _user.Country=dic['Country']
#                 # _user.PhoneNumber = dic['PhoneNumber']
#                 _user.IsDeleted = IsDeleted
#
#
#                 _user.save()
#                 serializer = UserSerializer(_user)
#
#
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
#     # Allow only authenticated users to access this url
#     # permission_classes = (AllowAny,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = UserSerializer
#
#     def get(self, request, *args, **kwargs):
#         # serializer to handle turning our `User` object into something that
#         # can be JSONified and sent to the client.
#         # print(request.user)
#         user = request.user
#         serializer = self.serializer_class(user)
#         data = serializer.data
#
#         # print(serializer.data)
#         return Response(data, status=status.HTTP_200_OK)
#
#     def put(self, request, *args, **kwargs):
#
#         serializer_data = request.data.get('user', {})
#
#         serializer = UserSerializer(
#             request.user, data=serializer_data, partial=True
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#
#         return Response(serializer.data, status=status.HTTP_200_OK)

