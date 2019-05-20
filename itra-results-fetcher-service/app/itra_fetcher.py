from bs4 import BeautifulSoup
import requests
import redis


from app.race_result import RaceResult

red = redis.Redis(host="itra_redis_cache", port=6379, db=0)


class ItraRaceResultsFetcher:
    """Scrap results from itra page"""

    def __init__(self, **kwargs):
        self.results = []
        self.itra_race_id = kwargs.get("itra_race_id", None)

    def fetch_results(self):
        raw_data = self.download_data()
        soup = BeautifulSoup(raw_data, "html.parser")
        trs = soup.select("tbody tr")
        for tr in trs:
            data = self.extract_data_from_row(tr)
            print(data)
            try:
                race_result = RaceResult(**data)
            except ValueError as error:
                print(error, data)
                continue
            race_result.birth_year = ItraRunnerYearFetcher(
                race_result.name, itra_race_id=self.itra_race_id
            ).fetch_year()
            self.results.append(race_result)
            print(race_result)

    def download_data(self):

        r = requests.post(
            "https://itra.run/fiche.php",
            data={"mode": "getCourse", "idedition": self.itra_race_id},
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


class ItraRunnerYearFetcher:
    """Responisbile for scrap birth year for given user"""

    def __init__(self, name, **kwargs):
        self.name = name
        self.itra_race_id = kwargs.get("itra_race_id", None)

    def fetch_year(self):
        year_cache_key = f"itra_race:{self.itra_race_id}:{self.name}"
        year_from_redis = red.get(year_cache_key)
        if year_from_redis:
            if year_from_redis.decode("utf-8") == "None":
                return None
            return int(year_from_redis.decode("utf-8"))

        raw_data = self.download_data()
        soup = BeautifulSoup(raw_data, "html.parser")

        year = self.extract_year(soup.select(".tit"))

        red.set(year_cache_key, str(year))
        return year

    def download_data(self):

        extract_name = self.name.split(" ")
        r = requests.post(
            "https://itra.run/fiche.php",
            data={
                "mode": "search",
                "pnom": extract_name[0],
                "nom": extract_name[1],
            },
        )

        return r.text

    @staticmethod
    def extract_year(div_with_year_text):
        if len(div_with_year_text) == 0:
            return None
        years = []
        for div in div_with_year_text:
            year = div.text[-4:]
            if year.isdigit():
                years.append(int(year))
        years = set(years)
        if len(years) > 1 or len(years) == 0:
            return None
        return list(years)[0]
