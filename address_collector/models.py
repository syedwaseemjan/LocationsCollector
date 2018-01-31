from django.db import models
from django.utils import timezone


class Address(models.Model):
    address = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_on = models.DateTimeField('Created On', default=timezone.now)
    updated_on = models.DateTimeField('Updated On', default=timezone.now)

    class Meta:
        unique_together = ('latitude', 'longitude',)

    def __str__(self):
        return """Address:{}, Lat:{}, Lng:{},
        Created On:{}, Last Updated On:{}""".format(
            self.address,
            self.latitude,
            self.longitude,
            self.created_on,
            self.updated_on)
