from datetime import timedelta


class RaceResult:
    """Race result representation"""

    # TODO remove it and send this funcionality to race-service
    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.time = kwargs.get("time")
        self.rank = kwargs.get("rank")
        self.sex = kwargs.get("sex")
        self.nationality = kwargs.get("nationality")
        self.birth_year = kwargs.get("birth_year")

    def __str__(self):
        return f"{self.name}, {self.birth_year}, {self.time}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, d):
        if not d:
            raise ValueError("Name cannot be empty")
        self._name = d.title()

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, d):
        if not d:
            raise ValueError("Time cannot be empty")
        time_numbers = [int(n) for n in d.split(":") if n.isdigit()]
        if not len(time_numbers) == 3:
            raise ValueError("Time format is wrong")
        self._time = timedelta(
            hours=time_numbers[0],
            minutes=time_numbers[1],
            seconds=time_numbers[2],
        )

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, d):
        if not d.isdigit():
            raise ValueError("Rank format is wrong")
        self._rank = int(d)

    @property
    def sex(self):
        return self._sex

    @sex.setter
    def sex(self, d):
        if not d:
            self._sex = d
            return
        if not d.lower().startswith("w") and not d.lower().startswith("m"):
            raise ValueError("Sex format is wrong")
        self._sex = d.lower()[0]
