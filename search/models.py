from django.db import models

class Location(models.Model):
    country = models.TextField(max_length=255)
    city = models.TextField(max_length=255, null=True)
