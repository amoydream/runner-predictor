import pytest
from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    yield client


@pytest.fixture
def sample_html_row():
    return """<tr class="odd">
                    <td>Karolina ROMANOWICZ</td>
                    <td class="r">03:41:46&nbsp;</td>
                    <td class="r">113</td>
                    <td class="c">Woman</td>
                    <td>Pologne</td>
                </tr>"""


def html_itra_runner_found_but_there_is_no_year():
    return """
    <div class="fc" id="run771669" style="background-image:url(/memb_pic/pic36325_01745c49.jpg);" data-url="/community/lai pui.hui/771669/36325/" >
        <div class="tit">Women</div>
            <div class="info">Lai Pui HUI
                <br/>
            <span>(HKG)</span>
        </div>
    </div>
    """  # noqa: E501


@pytest.fixture
def html_itra_runner_results():
    return """
    <div class="fc" id="run2408175"  data-url="/community/karolina.romanowicz/2408175//" >
        <div class="tit">Women, born in 1989</div>
            <div class="info">Karolina ROMANOWICZ<br/><span>(POL)</span>
        </div>
    </div>"""  # noqa: E501


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
"""  # noqa: E501


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

"""  # noqa: E501


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

"""  # noqa: E501


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
