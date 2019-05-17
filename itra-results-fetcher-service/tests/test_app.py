from datetime import timedelta
import pytest


from unittest.mock import patch


from app.itra_fetcher import ItraRaceResultsFetcher, ItraRunnerYearFetcher
from app.race_result import RaceResult


@patch("app.app.fetch_data_from_itra.delay")
def test_sample_post(mock, client):
    """Testing sample post"""
    data = dict(callback_race_id=2, itra_race_id=1929)
    rv = client.post("/", json=data)
    json_data = rv.get_json()

    assert json_data == "run que"


@patch("app.itra_fetcher.ItraRunnerYearFetcher.download_data")
@patch("app.itra_fetcher.ItraRaceResultsFetcher.download_data")
def test_fetcher_parser_results(
    mocker, mocker_runner, html_itra_results, html_itra_runner_results
):
    # print(html_itra_results)
    fetcher = ItraRaceResultsFetcher(itra_race_id=32181)
    mocker.return_value = html_itra_results
    mocker_runner.return_value = html_itra_runner_results
    fetcher.fetch_results()
    assert len(fetcher.results) == 4
    race_result = fetcher.results[0]
    assert isinstance(race_result, RaceResult)
    assert race_result.name == "Karolina Romanowicz"
    assert race_result.sex == "w"
    assert race_result.nationality == "Pologne"
    assert race_result.birth_year == 1989


@patch("app.itra_fetcher.red.get")
@patch("app.itra_fetcher.requests.post")
def test_fetcher_itra_runner_with_doubled(
    mocker, mocker_redis, html_itra_runner_results_with_doubled
):
    """Some times runner is doubled with the same year"""
    fetcher = ItraRunnerYearFetcher("Łukasz Adamczyk")
    mock_return = mocker.return_value
    mock_return.text = html_itra_runner_results_with_doubled
    mocker_redis.return_value = None
    assert fetcher.fetch_year() == 1983


@patch("app.itra_fetcher.red.get")
@patch("app.itra_fetcher.requests.post")
def test_fetcher_itra_runner_with_wrong_year(
    mocker, mocker_redis, html_itra_runner_results_with_one_wrong
):
    """Sometimes runner is doubled and have strange birth year"""
    fetcher = ItraRunnerYearFetcher("Łukasz Adamczyk")
    mock_return = mocker.return_value
    mock_return.text = html_itra_runner_results_with_one_wrong
    mocker_redis.return_value = None
    assert fetcher.fetch_year() == 1983


@patch("app.itra_fetcher.red.get")
@patch("app.itra_fetcher.requests.post")
def test_fetcher_itra_runner_no_year(
    mocker, mocker_redis, html_itra_runner_found_but_there_is_no_year
):
    """Sometimes there will be a runner, but unfortunately
    there is no year of birth next to him"""
    fetcher = ItraRunnerYearFetcher("Łukasz Adamczyk")
    mock_return = mocker.return_value
    mock_return.text = html_itra_runner_found_but_there_is_no_year
    mocker_redis.return_value = None
    assert fetcher.fetch_year() is None


@patch("app.itra_fetcher.red.get")
@patch("app.itra_fetcher.requests.post")
def test_fetcher_itra_runner_results_same_name_diffent_year(
    mocker, mocker_redis, html_itra_runner_results_same_name_diffent_year
):
    """When found runners with same name and diffrent year dont assing birth"""
    fetcher = ItraRunnerYearFetcher("Łukasz Adamczyk")
    mock_return = mocker.return_value
    mock_return.text = html_itra_runner_results_same_name_diffent_year
    mocker_redis.return_value = None
    assert fetcher.fetch_year() is None


@patch("app.itra_fetcher.red.get")
@patch("app.itra_fetcher.requests.post")
def test_fetcher_itra_runner(mocker, mocker_redis, html_itra_runner_results):
    fetcher = ItraRunnerYearFetcher("Karolina Romanowicz")
    mock_return = mocker.return_value
    mock_return.text = html_itra_runner_results
    mocker_redis.return_value = None
    assert fetcher.fetch_year() == 1989


def test_extract_data_from_row(sample_html_row):
    """Testing extract_data_from_row method"""
    extracted_data = ItraRaceResultsFetcher.extract_data_from_row(
        sample_html_row
    )
    assert extracted_data["name"] == "Karolina ROMANOWICZ"
    assert extracted_data["time"] == "03:41:46"
    assert extracted_data["sex"] == "Woman"
    assert extracted_data["rank"] == "113"
    assert extracted_data["nationality"] == "Pologne"


def test_creating_race_result():
    """Test Creating RaceResult from dictionary"""
    name = "Karolina ROMANOWICZ"
    time = "03:41:46"
    rank = "113"
    sex = "Woman"
    nationality = "Pologne"
    result_dict = dict(
        name=name, time=time, rank=rank, sex=sex, nationality=nationality
    )
    result_obj = RaceResult(**result_dict)
    assert result_obj.name == "Karolina Romanowicz"
    assert isinstance(result_obj.time, timedelta)
    assert result_obj.rank == 113
    assert result_obj.sex == "w"
    assert result_obj.nationality == "Pologne"


def test_required_name_field():
    """Test if race result without name rise error"""
    with pytest.raises(ValueError):
        RaceResult(name=None)


def test_required_time_field():
    """Test if race result without time rise error"""
    with pytest.raises(ValueError):
        RaceResult(name="Test name", time=None)


def test_required_time_format():
    """Test if time not in format 00:00:00  rise error"""
    with pytest.raises(ValueError):
        RaceResult(name="Test name", time="39:39")
    with pytest.raises(ValueError):
        RaceResult(name="Test name", time="39")
    with pytest.raises(ValueError):
        RaceResult(name="Test name", time="39.3")


def test_required_rank_format():
    """Test if rank is not a digit rise error"""
    with pytest.raises(ValueError):
        RaceResult(name="Test name", time="39:39:39", rank="")
    with pytest.raises(ValueError):
        RaceResult(name="Test name", time="39:39:39", rank="b")


def test_required_sex_format():
    """Test if sex is not stats with w or m rise error"""
    with pytest.raises(ValueError):
        RaceResult(name="Test name", time="39:39:39", rank="123", sex="01")
    with pytest.raises(ValueError):
        RaceResult(name="Test name", time="39:39:39", rank="232", sex="test")
    race_result = RaceResult(
        name="Test name", time="39:39:39", rank="232", sex=None
    )
    assert race_result.sex is None

