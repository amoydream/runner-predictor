from bs4 import BeautifulSoup
import requests


class ItraFetcher:
    def __init__(self, mode, **kwargs):
        self.mode = mode
        self.results = []
        self.raw_data = None
        self.itra_race_id = kwargs.get("itra_race_id", None)

    def fetch_results(self):
        self.raw_data = self.download_data()
        soup = BeautifulSoup(self.raw_data, "html.parser")
        trs = soup.select("tbody tr")
        for tr in trs:
            self.results.append(tr)

    def download_data(self):
        r = requests.post(
            "https://itra.run/fiche.php",
            data={"mode": self.mode, "idedition": self.itra_race_id},
        )
        return r.text

