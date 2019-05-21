from app.enduhub_fetcher import EnduhubFetcher


def test_enduhub_fetcher_object_init():
    """EnduhubFetcher  initalization test"""
    endu = EnduhubFetcher("Michal Mojek", 1980)
    assert isinstance(endu, EnduhubFetcher)


def test_enduhub_fetcher_string():
    """Test String representatation of EnduhubFetcher object"""
    endu = EnduhubFetcher("Michal Mojek", 1980)
    assert str(endu) == "Michal Mojek, 1980"
