class BirthYear:
    def __init__(self, year):
        if not str(year).isnumeric():
            raise ValueError("Birth year has to be a number")
        self.year = year

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, y):
        self._year = y
        if len(str(y)) == 2:
            self._year = int(y) + 1900

    def __str__(self):
        return str(self.year)

    def __eq__(self, other):
        return self.year == other

    def __repr__(self):
        return f"BirthYear({self.year})"
