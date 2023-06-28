from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from bookingApp.Models.users.userSerializer import UserSerializer
def get_token_for_user(user):

    refresh = RefreshToken.for_user(user)

    return {
        # 'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def verify_token(request):
    try:
        JWT_authenticator = JWTAuthentication()
        response = JWT_authenticator.authenticate(request)
        if response is not None:
            # unpacking
            user, token = response

            userData = UserSerializer(user).data
            return Response({"data": {"valid": True,"Token":str(token),"user":userData}, "status": 200}, status=status.HTTP_200_OK
                            )
        else:

            return Response({"data": {"valid": False}, "status": 200}, status=status.HTTP_200_OK)
    except Exception as ex:
        return Response({"data": {"valid": False}, "status": 200}, status=status.HTTP_200_OK)