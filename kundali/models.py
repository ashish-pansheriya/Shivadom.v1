from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timezone = models.CharField(max_length=50)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.country}"

class KundaliRequest(models.Model):
    birth_date = models.DateField()
    birth_time = models.TimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timezone = models.CharField(max_length=50)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Kundali for {self.birth_date} {self.birth_time}"