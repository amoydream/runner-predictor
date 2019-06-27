from django.db import models
import requests

# TODO add RaceGroup model: grouping te same events year by years


class RaceGroup(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Race(models.Model):
    race_group = models.ForeignKey(
        RaceGroup,
        on_delete=models.SET_NULL,
        related_name="races",
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=256)
    start_date = models.DateField()
    distance = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    elevation_gain = models.PositiveIntegerField(null=True, blank=True)
    elevation_lost = models.PositiveIntegerField(null=True, blank=True)
    itra = models.PositiveIntegerField(null=True, blank=True)
    itra_race_id = models.PositiveIntegerField(null=True, blank=True)
    food_point = models.PositiveIntegerField(null=True, blank=True)
    time_limit = models.DecimalField(
        max_digits=10, decimal_places=1, null=True, blank=True
    )

    def download_from_enduhub(self):
        for race_result in self.race_results.all():
            race_result.download_from_enduhub()

    def download_from_itra(self):
        payload = {
            "itra_race_id": self.itra_race_id,
            "callback_race_id": self.id,
        }

        r = requests.post("http://itrafetcher:5000/", json=payload)
        return r.content

    class Meta:
        ordering = ["-start_date"]
        verbose_name_plural = "races"
        unique_together = ["name", "start_date"]

    def __str__(self):
        return f"{self.name} {self.start_date}"

    @property
    def elevation_diff(self):
        """Calculating difference between elevation gain and lost"""
        if not self.elevation_gain or not self.elevation_lost:
            return None
        return self.elevation_gain - self.elevation_lost


class RaceResult(models.Model):
    SEX_CHOICES = [("m", "Man"), ("w", "Woman")]
    race = models.ForeignKey(
        Race, on_delete=models.CASCADE, related_name="race_results"
    )
    runner_name = models.CharField(max_length=300)
    runner_birth = models.PositiveIntegerField()
    time_result = models.DurationField()
    sex = models.CharField(
        max_length=1, choices=SEX_CHOICES, null=True, blank=True
    )

    def download_from_enduhub(self):
        payload = {"name": self.runner_name, "birth": self.runner_birth}
        r = requests.post("http://enduhubfetcher:5000/", json=payload)
        return r.content

    def __str__(self):
        str_repr = (
            f"{self.race.name} {self.race.start_date} {self.runner_name}"
            f" {self.runner_birth} {self.time_result}"
        )
        return str_repr

    class Meta:
        ordering = ["time_result"]
        verbose_name_plural = "race_results"
        unique_together = [
            "race",
            "runner_name",
            "runner_birth",
            "time_result",
        ]
