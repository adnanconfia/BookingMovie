from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from django.http import JsonResponse
from rest_framework import status

import random
from bookingApp.Models.users.user import User
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from movie_booking import settings
from bookingApp.Models.users.userSerializer import UserSerializer


class ForgetPassAPI(RetrieveUpdateAPIView):
    permission_classes = [AllowAny,]

    def post(self,request):
        try:
            d = request.data
            d = json.dumps(d)
            dic = json.loads(d)
            data = {}
            userDetails = {}
            if 'email' in dic.keys():
                user = User.objects.filter(IsDeleted = False, Email=dic['email'])

                if user is not None:
                    for u in user:
                        data['user'] =UserSerializer(u).data
                    otp = random.randint(1000,9999)
                    data['otp']=otp
                    # data['UserDetails']=userDetails
                    subject = ""
                    body = "Hello,Your OTP is "+str(otp)+" Thank You"
                    sender = settings.EMAIL_HOST_USER
                    recipients = dic['email']
                    # recipients = "hr"
                    password = settings.EMAIL_HOST_PASSWORD

                    send_email(subject,body,sender,recipients,password,otp)
                    return JsonResponse({"data": data,"message":"success","status":status.HTTP_200_OK})
                else:
                    return JsonResponse({"data":"","message":"Email not found","status":status.HTTP_404_NOT_FOUND})
            else:
                return JsonResponse({"data":"","message":"Email is required","status": status.HTTP_400_BAD_REQUEST})
        except Exception as ex:
            return JsonResponse({"data":"","message":ex,"status":status.HTTP_500_INTERNAL_SERVER_ERROR})




def send_email(subject,body, sender, recipients, password,otp):
    # assert isinstance(recipients,list)
    msg=MIMEMultipart('alternative')
    msg['From']=sender
    msg['To']=recipients
    msg['Subject']=subject
    txt_part=MIMEText(body,'plain')
    msg.attach(txt_part)

    html_part = MIMEText(f"<p>Here is your password reset OTP</p><h1>{otp}</h1>", 'html')
    msg.attach(html_part)
    msg_str=msg.as_string()
    server=smtplib.SMTP(host=settings.EMAIL_HOST,port=settings.EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(sender,password)
    server.sendmail(sender,recipients,msg_str)
    server.quit()