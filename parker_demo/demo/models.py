from django.db import models

class ParkerDemo(models.Model):
    title = models.CharField(max_length=140)
    summary = models.TextField(max_length=1000)
    link = models.CharField(max_length=1000)


