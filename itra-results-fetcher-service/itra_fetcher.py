from bs4 import BeautifulSoup
import requests

from race_result import RaceResult


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
            print(tr)
            data = self.extract_data_from_row(tr)
            self.results.append(RaceResult(**data))

    def download_data(self):
        r = requests.post(
            "https://itra.run/fiche.php",
            data={"mode": self.mode, "idedition": self.itra_race_id},
        )
        return r.text

    @staticmethod
    def extract_data_from_row(row):

        soup = BeautifulSoup(str(row), "html.parser")
        td = soup.select("tr td")
        name = td[0].text.strip()
        time = td[1].text.strip()
        rank = td[2].text.strip()
        sex = td[3].text.strip()
        nationality = td[4].text.strip()
        d = dict(
            name=name, time=time, rank=rank, sex=sex, nationality=nationality
        )
        return d
