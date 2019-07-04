from datetime import timedelta, date
import pytest
from unittest.mock import patch
from app.presist_data import PresistData
from app.race_event_orientation_preparator import (
    RaceEventOrientationPreparator,
)
from app.runner_results_stat import RunnerResultsStat
from app.runner_results_stat import (
    convert_time_to_hours_decimal,
    string_to_timedelta,
    strfdelta,
)


def test_presist_data_init():
    race_group_id = 1
    race_event_preparator = RaceEventOrientationPreparator(race_group_id)
    prep = PresistData(race_event_preparator)
    assert isinstance(prep, PresistData)


def test_event_orientation_data_init():
    race_group_id = 1
    race_event_preparator = RaceEventOrientationPreparator(race_group_id)
    assert isinstance(race_event_preparator, RaceEventOrientationPreparator)


@pytest.fixture
def results():
    results = [
        {
            "id": 533,
            "runner": 36,
            "event_name": "Run 10 3",
            "distance": "10.0",
            "race_date": "2010-02-10",
            "result_of_the_race": "00:47:47",
            "race_type": "Bieganie",
        },
        {
            "id": 532,
            "runner": 36,
            "event_name": "Run 10 2",
            "distance": "10.0",
            "race_date": "2009-06-14",
            "result_of_the_race": "00:48:47",
            "race_type": "Bieganie",
        },
        {
            "id": 533,
            "runner": 36,
            "event_name": "Run 10",
            "distance": "10.0",
            "race_date": "2010-02-10",
            "result_of_the_race": "00:49:47",
            "race_type": "Bieganie",
        },
        {
            "id": 534,
            "runner": 36,
            "event_name": "V Jurajski Półmaraton",
            "distance": "21.0",
            "race_date": "2009-06-14",
            "result_of_the_race": "01:47:47",
            "race_type": "Bieganie",
        },
    ]
    return results


@pytest.mark.fast
def test_strfdelta():
    time_string = "00:47:47"
    time_time_delta = string_to_timedelta(time_string)
    assert strfdelta(time_time_delta, "%H:%M:%S") == time_string


@pytest.mark.fast
def test_string_to_timedelta():
    timedelta_string = "00:00:12"
    assert isinstance(string_to_timedelta(timedelta_string), timedelta)
    assert string_to_timedelta(timedelta_string).seconds == 12


@pytest.mark.fast
def test_convert_time_to_hours_decimal():
    assert convert_time_to_hours_decimal("00:47:47") == 0.796


@pytest.mark.fast
def test_runner_stats_best(results):
    assert len(results) == 4
    runner_stat = RunnerResultsStat(results)
    best_time_on_ten = runner_stat.best_time(10, "Bieganie")
    assert best_time_on_ten == {"time": "00:47:47", "decimal": 0.796}


@pytest.mark.fast
def test_runner_stats_best_no_results():
    results = []
    assert len(results) == 0
    runner_stat = RunnerResultsStat(results)
    best_time_on_ten = runner_stat.best_time(10, "Bieganie")
    assert best_time_on_ten is None


## api test
@pytest.mark.fast
@patch.object(PresistData, "get_from_redis")
def test_api(mocked_get_from_redis, client):
    mocked_get_from_redis.return_value = [1, 2]
    rv = client.get("/race_group/1/redownload/0")
    assert rv.status_code == 200
    assert rv.json == [1, 2]

