from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import pre_save

import re
import logging

logger = logging.getLogger(__name__)


class Runner(models.Model):
    SEX_CHOICES = [("M", "Male"), ("F", "Female")]
    name = models.CharField(max_length=100)
    birth_year = models.IntegerField(validators=[MinValueValidator(1900)])
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)

    class Meta:
        unique_together = ["name", "birth_year"]

    def __str__(self):
        return "{}, {}, {}".format(self.name, self.birth_year, self.sex)


def correct_birth_year(sender, instance, **kwargs):
    """Change short year date to full format"""
    if len(str(instance.birth_year)) == 2:
        instance.birth_year = "19" + str(instance.birth_year)


def pre_save_handler(sender, instance, *args, **kwargs):
    instance.full_clean()


pre_save.connect(correct_birth_year, sender=Runner)
pre_save.connect(pre_save_handler, sender=Runner)


class RaceResult(models.Model):
    runner = models.ForeignKey(
        Runner, on_delete=models.CASCADE, related_name="race_results"
    )
    event_name = models.CharField(max_length=300)
    distance = models.DecimalField(
        max_digits=10, decimal_places=1, validators=[MinValueValidator(1)]
    )
    race_date = models.DateField()
    result_of_the_race = models.DurationField()
    race_type = models.CharField(max_length=300)

    class Meta:
        ordering = ["-race_date"]

    def __str__(self):
        return f"{self.race_date}, {self.event_name}, {self.distance} km, {self.result_of_the_race}, {self.race_type}"


def correct_distance(sender, instance, **kwargs):
    """Clean distance input"""
    str_distance = str(instance.distance).strip()
    find_digit = re.match(r"\d+\.*\d*", str_distance)
    if find_digit:
        result = find_digit.group()
        instance.distance = float(result)

    elif str_distance.lower() == "maraton":
        instance.distance = 42.1
    elif str_distance.lower() in ["połmaraton", "polmaraton", "półmaraton"]:
        instance.distance = 21.05

    logger.info(f"Disnance converted {str_distance} to {instance.distance}")


pre_save.connect(correct_distance, sender=RaceResult)
