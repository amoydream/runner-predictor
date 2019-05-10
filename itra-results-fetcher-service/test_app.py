from datetime import timedelta
import pytest
import json

from unittest.mock import patch

from app import app
from itra_fetcher import ItraFetcher, ItraRunnerFetcher
from race_result import RaceResult


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client


def test_sample_post(client):
    """Testing sample post"""
    data = json.dumps(dict(itra_race_id=1929))
    rv = client.post("/", data=data, content_type="application/json")
    assert b"1929" in rv.data


@patch("itra_fetcher.ItraRunnerFetcher.download_data")
@patch("itra_fetcher.ItraFetcher.download_data")
def test_fetcher_parser_results(
    mocker, mocker_runner, html_itra_results, html_itra_runner_results
):
    # print(html_itra_results)
    fetcher = ItraFetcher(itra_race_id=32181)
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


@patch("itra_fetcher.requests.post")
def test_fetcher_itra_runner_with_doubled(
    mocker, html_itra_runner_results_with_doubled
):
    """Some times runner is doubled with the same year"""
    fetcher = ItraRunnerFetcher("Łukasz Adamczyk")
    mock_return = mocker.return_value
    mock_return.text = html_itra_runner_results_with_doubled
    assert fetcher.fetch_year() == 1983


@patch("itra_fetcher.requests.post")
def test_fetcher_itra_runner_with_wrong_year(
    mocker, html_itra_runner_results_with_one_wrong
):
    """Some times runner is doubled and have strange birth year"""
    fetcher = ItraRunnerFetcher("Łukasz Adamczyk")
    mock_return = mocker.return_value
    mock_return.text = html_itra_runner_results_with_one_wrong
    assert fetcher.fetch_year() == 1983


@patch("itra_fetcher.requests.post")
def test_fetcher_itra_runner_results_same_name_diffent_year(
    mocker, html_itra_runner_results_same_name_diffent_year
):
    """When found runners with same name and diffrent year dont assing birth"""
    fetcher = ItraRunnerFetcher("Łukasz Adamczyk")
    mock_return = mocker.return_value
    mock_return.text = html_itra_runner_results_same_name_diffent_year
    assert fetcher.fetch_year() is None


@patch("itra_fetcher.requests.post")
def test_fetcher_itra_runner(mocker, html_itra_runner_results):
    fetcher = ItraRunnerFetcher("Karolina Romanowicz")
    mock_return = mocker.return_value
    mock_return.text = html_itra_runner_results
    assert fetcher.fetch_year() == 1989


def test_extract_data_from_row(sample_html_row):
    """Testing extract_data_from_row method"""
    extracted_data = ItraFetcher.extract_data_from_row(sample_html_row)
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


@pytest.fixture
def sample_html_row():
    return """<tr class="odd">
                    <td>Karolina ROMANOWICZ</td>
                    <td class="r">03:41:46&nbsp;</td>
                    <td class="r">113</td>
                    <td class="c">Woman</td>
                    <td>Pologne</td>
                </tr>"""


@pytest.fixture
def html_itra_runner_results():
    return """
    <div class="fc" id="run2408175"  data-url="/community/karolina.romanowicz/2408175//" >
        <div class="tit">Women, born in 1989</div>
            <div class="info">Karolina ROMANOWICZ<br/><span>(POL)</span>
        </div>
    </div>"""


@pytest.fixture
def html_itra_runner_results_with_one_wrong():
    """Some runner have wrong birth year"""
    return """
        <div class="fc" id="run407546"  data-url="/community/lukasz.adamczyk/407546//" >
            <div class="tit">Men, born in ??</div>
            <div class="info">Lukasz ADAMCZYK
                <br/>
                <span>(POL)</span>
            </div>
        </div>
        <div class="fc" id="run711990"  data-url="/community/lukasz.adamczyk/711990//" >
            <div class="tit">Men, born in 1983</div>
            <div class="info">Łukasz ADAMCZYK
                <br/>
                <span>(POL)</span>
            </div>
        </div>
"""


@pytest.fixture
def html_itra_runner_results_with_doubled():
    """Some runner have wrong birth year"""
    return """
        <div class="fc" id="run407546"  data-url="/community/lukasz.adamczyk/407546//" >
            <div class="tit">Men, born in 1983</div>
            <div class="info">Lukasz ADAMCZYK
                <br/>
                <span>(POL)</span>
            </div>
        </div>
        <div class="fc" id="run711990"  data-url="/community/lukasz.adamczyk/711990//" >
            <div class="tit">Men, born in 1983</div>
            <div class="info">Łukasz ADAMCZYK
                <br/>
                <span>(POL)</span>
            </div>
        </div>

"""


@pytest.fixture
def html_itra_runner_results_same_name_diffent_year():
    """Some runner have wrong birth year"""
    return """
        <div class="fc" id="run407546"  data-url="/community/lukasz.adamczyk/407546//" >
            <div class="tit">Men, born in 1982</div>
            <div class="info">Lukasz ADAMCZYK
                <br/>
                <span>(POL)</span>
            </div>
        </div>
        <div class="fc" id="run711990"  data-url="/community/lukasz.adamczyk/711990//" >
            <div class="tit">Men, born in 1983</div>
            <div class="info">Łukasz ADAMCZYK
                <br/>
                <span>(POL)</span>
            </div>
        </div>

"""


@pytest.fixture
def html_itra_results():
    return """		
        <h2>Lemkowyna Ultra-Trail® 2018 - Łemko Trail</h2>
        <table class="palmares" >
            <thead>
                <tr>
                    <th>Name / Surname</th>
                    <th class="r">Time</th>
                    <th class="r">Overall Rank.</th>
                    <th class="c">Sex</th>
                    <th>Nationality</th>
                </tr>
            </thead>
            <tbody>
                <tr class="odd">
                    <td>Karolina ROMANOWICZ</td>
                    <td class="r">03:41:46&nbsp;</td>
                    <td class="r">113</td>
                    <td class="c">Woman</td>
                    <td>Pologne</td>
                </tr>
                <tr class="even">
                    <td>Marcin ZARZEKA</td>
                    <td class="r">03:42:04&nbsp;</td>
                    <td class="r">114</td>
                    <td class="c">Man</td>
                    <td>Pologne</td>
                </tr>
                <tr class="odd">
                    <td>Iwona LUDWINEK-ZARZEKA</td>
                    <td class="r">03:42:04&nbsp;</td>
                    <td class="r">115</td>
                    <td class="c">Woman</td>
                    <td>Pologne</td>
                </tr>
                <tr class="even">
                    <td>Tomasz ZARZYCKI</td>
                    <td class="r">03:42:42&nbsp;</td>
                    <td class="r">116</td>
                    <td class="c">Man</td>
                    <td>Pologne</td>
                </tr>
                          
             
           
            
                </tbody>
            </table> """
