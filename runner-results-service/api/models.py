from django.db import models
from django.core.validators import MinValueValidator
from django.db.models.signals import pre_save


class Runner(models.Model):
    name = models.CharField(max_length=100)
    birth_year = models.IntegerField(validators=[MinValueValidator(1900)])

    class Meta:
        unique_together = ["name", "birth_year"]

    def __str__(self):
        return "{}, {}".format(self.name, self.birth_year)


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
