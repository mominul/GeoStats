from django.db import models

class Location(models.Model):
    location_id = models.IntegerField(null=False)
    country = models.TextField(max_length=255)
    city = models.TextField(max_length=255, null=True)
    name = models.TextField(max_length=255, null=True)
    code = models.CharField(max_length=255, null=False)
