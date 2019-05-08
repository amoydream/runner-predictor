import pytest
import json
from app import app
from itra_fetcher import ItraFetcher
from unittest.mock import patch


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


@patch("itra_fetcher.requests.post")
def test_fetcher_parser_results(mocker, html_itra_results):
    # print(html_itra_results)
    fetcher = ItraFetcher("getCourse", itra_race_id=32181)
    mock_return = mocker.return_value
    mock_return.text = html_itra_results
    fetcher.fetch_results()
    assert len(fetcher.results) == 4


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
