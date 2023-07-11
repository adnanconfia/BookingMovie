from django.db import models
from ..movie import Movie
from ..users.user import User
from django.utils import timezone


class Booking(models.Model):
    Id = models.AutoField(primary_key=True)
    user_Id = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_Id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    datetime = models.TextField(null=True, blank=True)
    seat_no = models.TextField(null=True,blank=True)
    isDeleted = models.BooleanField(default=False)
    creation_date = models.DateTimeField(default=timezone.now)
