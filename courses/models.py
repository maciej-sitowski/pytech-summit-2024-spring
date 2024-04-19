from django.db import models

# Create your models here.

class Course(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50)
    