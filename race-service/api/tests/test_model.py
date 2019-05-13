from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from .factories import RaceFactory


class ModelTest(TestCase):
    def test_race_str(self):
        """Test race string reprezentation"""
        race = RaceFactory.create()
        self.assertEqual(str(race), f"{race.name} {race.start_date}")

    def test_elevation_diff(self):
        """Test elevation diff calculation """
        race = RaceFactory.create(elevation_gain=1925, elevation_lost=3925)
        self.assertEqual(
            race.elevation_diff, (race.elevation_gain - race.elevation_lost)
        )

    def test_elevation_gain_validation(self):
        """Test validation of elevation gain is >= 0"""
        race = RaceFactory.build(elevation_gain=-1925)
        with self.assertRaisesRegexp(ValidationError, "elevation_gain"):
            race.full_clean()

    def test_elevation_lost_validation(self):
        """Test validation of elevation lost is >= 0"""
        race = RaceFactory.build(elevation_lost=-1925)

        with self.assertRaisesRegexp(ValidationError, "elevation_lost"):
            race.full_clean()

    def test_uniqness_of_the_races(self):
        """Test uniqness of the races.
            Race with same name and date on database"""

        RaceFactory.create(name="Prehyba", start_date="2019-04-27")

        with self.assertRaises(IntegrityError):
            RaceFactory.create(name="Prehyba", start_date="2019-04-27")

    def test_uniqness_of_the_races_django(self):
        """Test uniqness of the races.
            Race with same name and date on django"""
        RaceFactory.create(name="Prehyba", start_date="2019-04-27")
        race = RaceFactory.build(name="Prehyba", start_date="2019-04-27")

        with self.assertRaises(ValidationError):
            race.full_clean()

    # def test_str_representation_of_race_result(self):
