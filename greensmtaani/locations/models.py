from django.db import models

# Create your models here.

class GeoLocation(models.Model):
    name = models.CharField(max_length=100)  
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_mama_mboga = models.BooleanField(default=False) 
    address = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({'Mama Mboga' if self.is_mama_mboga else 'Customer'})"