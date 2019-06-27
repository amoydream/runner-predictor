from .i_preparator import IPreparator
import time
import requests


class RaceEventOrientationPreparator(IPreparator):
    def __init__(self, race_group_id):
        self.race_group_id = race_group_id

    def data_results(self):
        r_group = self.race_group()
        for race_endpoint in r_group["races"]:
            req = requests.get(race_endpoint)
            race = req.json()
            race_result = dict()
            race_data = self.prepare_race_data(race, race_result)
            race_results = self.race_results(race)
            for race_result in race_results:
                del race_result["id"]
                del race_result["race"]
                print(self.runner_result(race_result))
                yield {**race_data, **race_result}

    def race_group(self):
        endpoint = (
            f"http://resultapi:8000/api/race-group/{self.race_group_id}/"
        )
        print(endpoint)
        req = requests.get(endpoint)
        return req.json()

    def race_results(self, race):
        endpoint = race["race_results_url"]
        req = requests.get(endpoint)
        return req.json()

    def runner_result(self, race_result):
        endpoint = f"http://runnerapi:8000/api/runners/?name={race_result['runner_name']}&birth_year={race_result['runner_birth']}"
        req = requests.get(endpoint)
        try:
            runner = req.json()[0]
        except IndexError:
            return None
        endpoint_results = runner["race_results_url"]
        req_results = requests.get(endpoint_results)
        return req_results.json()

    def prepare_race_data(self, race, race_result):
        race_result["race_group"] = self.race_group_id
        race_result["race_name"] = race["name"]
        race_result["start_date"] = race["start_date"]
        race_result["distance"] = race["distance"]
        race_result["elevation_gain"] = race["elevation_gain"]
        race_result["elevation_lost"] = race["elevation_lost"]
        race_result["itra"] = race["itra"]
        race_result["food_point"] = race["food_point"]
        race_result["time_limit"] = race["time_limit"]
        race_result["elevation_diff"] = race["elevation_diff"]
        return race_result
        # print(r.data)
        # race_result api find race group
        # find  group's races
        # get info about race
        # find all race_results http://localhost:8001/api/races/2/race_results/
        # get info about result runner name birth time result sex
        # find runner in runner api (birth, name)
        # find runner's best 10 km, since to race date
