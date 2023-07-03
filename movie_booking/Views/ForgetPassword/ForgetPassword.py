from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
import json
from django.http import JsonResponse
from rest_framework import status
from movie_booking.Helpers.User.User import getUserByMail
import random
from bookingApp.Models.users.user import User
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.mail import EmailMessage
from django.core import mail as _mail


class ForgetPassAPI(RetrieveUpdateAPIView):
    permission_classes = [AllowAny,]

    def get(self,request):
        try:
            d = request.data
            d = json.dumps(d)
            dic = json.loads(d)
            data = []
            userDetails = {}
            if 'email' in dic.keys():
                user = User.objects.filter(IsDeleted = False, Email=dic['email'])

                if user is not None:
                    for u in user:
                        userDetails['email'] = u.Email
                        userDetails['userName'] = str(u.FirstName)+" "+str(u.LastName)
                    otp = random.randint(1000,9999)
                    userDetails['otp'] = otp
                    subject = ""
                    body = "Hello,Your OTP is "+str(otp)+" Thank You"
                    sender = "contact@confiatech.com"
                    recipients = ["hr@confiatech.com"]
                    password = "Confia@123"

                    send_email(subject,body,sender,recipients,password,otp)
                    return JsonResponse({"data": userDetails,"status":status.HTTP_200_OK})
                else:
                    return JsonResponse({"data":"Email not found","status":status.HTTP_404_NOT_FOUND})
            else:
                return JsonResponse({"data":"Email is required","status": status.HTTP_400_BAD_REQUEST})
        except Exception as ex:
            return JsonResponse({"data":ex,"status":status.HTTP_500_INTERNAL_SERVER_ERROR})



def send_email(subject,body, sender, recipients, password,otp):
    assert isinstance(recipients,list)
    msg=MIMEMultipart('alternative')
    msg['From']=sender
    msg['To']=", ".join(recipients)
    msg['Subject']=subject
    txt_part=MIMEText(body,'plain')
    msg.attach(txt_part)

    html_part = MIMEText(f"<p>Here is your password reset OTP</p><h1>{otp}</h1>", 'html')
    msg.attach(html_part)
    msg_str=msg.as_string()
    server=smtplib.SMTP(host='mail.confiatech.com',port=587)
    server.ehlo()
    server.starttls()
    server.login(sender,password)
    server.sendmail(sender,recipients,msg_str)
    server.quit()