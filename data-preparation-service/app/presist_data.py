from .i_preparator import IPreparator


class PresistData:
    def __init__(self, preparator):
        if not isinstance(preparator, IPreparator):
            raise ValueError("Preparator should implement IPreparator")
        self.preparator = preparator
        self.save_to_redis()

    def save_to_redis(self):
        data_to_save = self.preparator.data_results()
        for data in data_to_save:
            print(data)

