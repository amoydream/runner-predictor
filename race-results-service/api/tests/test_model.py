from django.test import TestCase
from django.core.exceptions import ValidationError
from api import models


class ModelTest(TestCase):
    def test_race_str(self):
        """Test race string reprezentation"""
        race = models.Race.objects.create(
            name="Wielka Prehyba",
            start_date="2019-04-27",
            distance=43.3,
            elevation_gain=1925,
            elevation_lost=1925,
            itra=2,
            food_point=3,
            time_limit=9,
        )
        self.assertEqual(str(race), f"{race.name} {race.start_date}")

    def test_elevation_diff(self):
        """Test elevation diff calculation """
        race = models.Race.objects.create(
            elevation_gain=1925, elevation_lost=1925
        )
        self.assertEqual(
            race.elevation_diff, (race.elevation_gain - race.elevation_lost)
        )

    def test_elevation_gain_validation(self):
        """Test validation of elevation gain is >= 0"""
        race = models.Race.objects.create(
            name="Prehyba", elevation_gain=-10, elevation_lost=1925
        )

        with self.assertRaisesRegexp(ValidationError, "elevation_gain"):
            race.full_clean()

    def test_elevation_lost_validation(self):
        """Test validation of elevation lost is >= 0"""
        race = models.Race.objects.create(
            name="Prehyba", elevation_gain=10, elevation_lost=-25
        )

        with self.assertRaisesRegexp(ValidationError, "elevation_lost"):
            race.full_clean()
