import requests


class ItraResultSender:
    """this class is responsible for sending results to the race api"""

    RACE_SERVICE_HOST = "resultapi"

    def __init__(self, race_results, race_id):
        self.race_results = race_results
        self.race_id = race_id
        self.sended = False

    def send_to_race_service(self):
        for result in self.race_results:
            self.send_result(result)
        self.sended = True

    def send_result(self, result):
        race_api_link = (
            f"http://resultapi:8000/api/races/{self.race_id}/race_results/"
        )
        data = {
            "runner_name": result.name,
            "runner_birth": result.birth_year,
            "time_result": str(result.time),
        }
        print(data)
        r = requests.post(race_api_link, json=data)

        print(r.json())
