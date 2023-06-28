import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from bookingApp.Models.users.user import User


@csrf_exempt

def addData(request):
    if(not User.objects.filter(Email="booking-admin@gmail.com").exists()):
        user = User(FirstName="Booking",LastName = "App", Email='booking-admin@gmail.com', RoleType=0,RoleName="Admin",
                    Creation_Time=datetime.datetime.now(),PhoneNumber="+923000000000",
                    Deletion_Time=None, IsDeleted=False, IsActive=True)
        user.set_password('Admin@123')
        user.save()
    return JsonResponse({"msg":"Success"})