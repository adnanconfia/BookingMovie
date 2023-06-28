from django.db import models
from django.utils import timezone
from .movie import Movie

class Days(models.Model):
    Id = models.AutoField(primary_key=True)
    movie_Id = models.ForeignKey(Movie,on_delete=models.CASCADE)
    datetime = models.DateTimeField(unique=True,null=True,blank=True)
    # day = models.TextField(null=True,blank=True)
    isDeleted = models.BooleanField(default=False)
    creation_date = models.DateTimeField(default=timezone.now)
