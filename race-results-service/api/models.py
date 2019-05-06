from django.db import models
from django.core.validators import MinValueValidator


class Race(models.Model):
    name = models.CharField(max_length=256, blank=True)
    start_date = models.DateField(null=True)
    distance = models.DecimalField(max_digits=10, decimal_places=1, null=True)
    elevation_gain = models.IntegerField(null=True)
    elevation_lost = models.IntegerField(null=True)
    itra = models.IntegerField(null=True)
    food_point = models.IntegerField(null=True)
    time_limit = models.DecimalField(
        max_digits=10, decimal_places=1, null=True
    )

    def __str__(self):
        return f"{self.name} {self.start_date}"

    @property
    def elevation_diff(self):
        """Calculating difference between elevation gain and lost"""
        return self.elevation_gain - self.elevation_lost
