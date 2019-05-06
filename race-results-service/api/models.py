from django.db import models


class Race(models.Model):
    name = models.CharField(max_length=256)
    start_date = models.DateField(null=True, blank=True)
    distance = models.DecimalField(
        max_digits=10, decimal_places=1, null=True, blank=True
    )
    elevation_gain = models.PositiveIntegerField(null=True, blank=True)
    elevation_lost = models.PositiveIntegerField(null=True, blank=True)
    itra = models.PositiveIntegerField(null=True, blank=True)
    food_point = models.PositiveIntegerField(null=True, blank=True)
    time_limit = models.DecimalField(
        max_digits=10, decimal_places=1, null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} {self.start_date}"

    @property
    def elevation_diff(self):
        """Calculating difference between elevation gain and lost"""
        return self.elevation_gain - self.elevation_lost
