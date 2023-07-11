import json
import requests
from datetime import datetime
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from bookingApp.Models.users.user import User as UserModel
from ...Helpers.User.User import UserExistsByEmail, getUserById, getUserByMail, getAllUsers
from bookingApp.Models.users.userSerializer import UserSerializer
import jwt
from django.utils.dateparse import parse_date
class User(CreateAPIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        try:
            data = request.data
            dic = json.dumps(data)
            dic = json.loads(dic)
            id=0
            if("Id" in dic.keys()):
                id=dic['Id']
            if(id==0):
                if 'Email' in dic.keys():
                    if UserExistsByEmail(dic['Email']):
                        return Response(
                            {"data":"","message": "user with email: '"+ dic['Email']+ "' already exists", "status": status.HTTP_400_BAD_REQUEST},
                            status=status.HTTP_400_BAD_REQUEST)
                    else:
                        password = ""
                        if("Password" in dic.keys()):
                            password = dic['Password']
                        else:
                            return Response(
                                {"data":"","message": "Password is required",
                                 "status": status.HTTP_400_BAD_REQUEST},
                                status=status.HTTP_400_BAD_REQUEST)
                        FirstName=""
                        LastName=""
                        CI =""
                        UserName = ""
                        DOB = ""
                        Gender = ""
                        RoleType=1
                        RoleName="User"
                        PhoneNumber = ""
                        if('FirstName' in dic.keys()):
                            FirstName = dic['FirstName']
                        if('LastName' in dic.keys()):
                            LastName = dic['LastName']
                        if('UserName' in dic.keys()):
                            UserName = dic['UserName']
                        if('PhoneNumber' in dic.keys()):
                            PhoneNumber = dic['PhoneNumber']
                        if('DOB' in dic.keys()):
                            DOB = dic['DOB']
                        if('CI' in dic.keys()):
                            CI = dic['CI']
                        if('Gender' in dic.keys()):
                            Gender = dic['Gender']
                        user = UserModel(Email=dic['Email'],
                                         FirstName=FirstName,
                                         LastName = LastName,
                                         CI = CI,
                                         DOB = DOB,
                                         UserName = UserName,
                                         PhoneNumber = PhoneNumber,
                                         Gender = Gender,
                                         RoleType=RoleType,
                                         RoleName=RoleName,
                                         IsDeleted=False,
                                         IsActive=True,)
                        user.set_password(password)
                        user.save()
                        # Knox endpoint
                        data = UserSerializer(user).data
                        print(data)
                        print(data['Email'])
                        # url = "https://your-knox-host:port/gateway/knoxsso/api/v1/token"
                        #
                        # # Set the credentials
                        # credentials = {"username": data['Email']}
                        #
                        # # Make a POST request with the credentials
                        # response = requests.post(url, json=credentials)
                        # print(auth_token = response.json()["auth_token"])
                        payload = {"sub": data['Id'], "email": data['Email'], "iat": 1516239022}
                        secret_key = "jdkdeomd209303kdks9kdk9md93"
                        jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
                        data['token'] = jwt_token
                        # print(jwt_token)
                        return Response(
                            {"data": data,"message":"success", "status": status.HTTP_200_OK},
                            status=status.HTTP_200_OK)

                else:
                    return Response(
                        {"data":"","message": "Email is required", "status": status.HTTP_400_BAD_REQUEST},
                        status=status.HTTP_400_BAD_REQUEST)
            else:
                user = getUserById(id)
                if (user is None):
                    return Response(
                        {"data":"","message": "User doesn't exists",
                         "status": status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND)
                else:
                    if ("Email" in dic.keys()):
                        checkUser = getUserByMail(dic['Email'])
                        if (checkUser is not None):
                            if checkUser.Id != id:
                                return Response({"data":"","message": "User with email : '" + str(dic['Email']) + "' already exists",
                                                 "status": status.HTTP_226_IM_USED}, status=status.HTTP_226_IM_USED)
                        else:
                            user.Email = dic['Email']
                    if ("Password" in dic.keys()):
                        password = dic['Password']
                        user.set_password(password)
                    if ('FirstName' in dic.keys()):
                        FirstName = dic['FirstName']
                        user.FirstName =FirstName
                    if ('LastName' in dic.keys()):
                        LastName = dic['LastName']
                        user.LastName = LastName
                    if ('CI' in dic.keys()):
                        CI = dic['CI']
                        user.CI =CI
                    if ('PhoneNumber' in dic.keys()):
                        PhoneNumber = dic['PhoneNumber']
                        user.PhoneNumber = PhoneNumber
                    if('DOB' in dic.keys()):
                        DOB = dic['DOB']
                        user.DOB = DOB
                    if ('Gender' in dic.keys()):
                        Gender = dic['Gender']
                        user.Gender = Gender
                    if('IsActive' in dic.keys()):
                        user.IsActive = dic['IsActive']
                    if("IsDeleted" in dic.keys()):
                        user.IsDeleted = dic['IsDeleted']
                        if(dic['IsDeleted'] ==True):
                            user.Deletion_Time = datetime.now()
                        else:
                            user.Deletion_Time = None
                    user.save()
                    data = UserSerializer(user).data

                    return Response({"data": data,"message":"User update successfully", "status": status.HTTP_200_OK},
                                    status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({"data":"","message": str(ex), "status": status.HTTP_500_INTERNAL_SERVER_ERROR},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
