from django.db import models
from django.utils import timezone


class Movie(models.Model):
    Id = models.AutoField(primary_key=True)
    movie_name = models.TextField(null=True, blank=True)
    thumbnail = models.ImageField(null=True, blank=True, upload_to='images/')
    category = models.TextField(null=True,blank=True)
    category_Id = models.IntegerField(null=True,blank=True,default=0)
    duration = models.TextField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    genre = models.TextField(null=True,blank=True)
    isDeleted = models.BooleanField(default=False)
    creation_date = models.DateTimeField(default=timezone.now)
