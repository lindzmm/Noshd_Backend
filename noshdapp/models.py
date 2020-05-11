from django.db import models
from django.contrib.auth.models import AbstractUser



class Post(models.Model):
    establishment_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.establishment_name

