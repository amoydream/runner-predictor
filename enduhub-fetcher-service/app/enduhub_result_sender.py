import requests


class EnduhubResultSender:
    """Send data fetched from enduhub to runner service"""

    def __init__(self, data):
        self.data = data

    def send_data(self):
        runner_response = self.__get_runner()
        runner = runner_response.json()

        if str(runner_response.status_code).startswith("20"):
            race_payload = {
                "event_name": self.data["race_name"],
                "distance": self.data["distance"],
                "race_date": self.data["race_date"],
                "result_of_the_race": self.data["result_of_the_race"],
                "race_type": self.data["race_type"],
            }
            breakpoint()
            link_template = "http://runnerapi:8000/api/runners/{}/race_results/".format(
                runner["id"]
            )
            r = requests.post(link_template, race_payload)
            print(r.content)
            return r

    def __get_runner(self):
        runner_payload = {
            "name": self.data["runner_name"],
            "birth_year": self.data["runner_birth"],
        }
        r = requests.post(
            "http://runnerapi:8000/api/runners/get_or_create/", runner_payload
        )
        return r
