from unittest.mock import patch

from app.enduhub_fetcher import EnduhubFetcher


def test_enduhub_fetcher_object_init():
    """EnduhubFetcher  initalization test"""
    endu = EnduhubFetcher("Michal Mojek", 1980)
    assert isinstance(endu, EnduhubFetcher)


def test_enduhub_fetcher_string():
    """Test String representatation of EnduhubFetcher object"""
    endu = EnduhubFetcher("Michal Mojek", 1980)
    assert str(endu) == "Michal Mojek, 1980"


@patch("app.enduhub_fetcher.EnduhubFetcher.download_page")
def test_enduhub_fetcher_number_of_pages_founder(
    mock_downloaded_page, html_with_results
):
    """Tests the extraction of the number of pages to download"""
    mock_downloaded_page.return_value = html_with_results
    endu = EnduhubFetcher("Paweł Wójcik", 1976)
    assert endu.number_of_pages == 0
    endu.prepare_web_links()
    assert len(endu.pages_content) == 1
    assert endu.number_of_pages == 7


@patch("app.enduhub_fetcher.EnduhubFetcher.download_page")
def test_enduhub_fetcher_fetch_results(
    mock_downloaded_page, html_with_results
):
    """Tests the extraction of race_results"""
    mock_downloaded_page.return_value = html_with_results
    endu = EnduhubFetcher("Paweł Wójcik", 1976)
    endu.prepare_web_links()
    results = endu.fetch_results()
    first_results_on_list = results[0]
    assert first_results_on_list["race_date"] == "2019-05-16"
