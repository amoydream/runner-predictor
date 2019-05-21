class EnduhubFetcher:
    """Responsible for download results from enduhub"""

    def __init__(self, runner_name, birth_year):
        self.runner_name = runner_name
        self.birth_year = birth_year

    def __str__(self):
        return "{}, {}".format(self.runner_name, self.birth_year)
