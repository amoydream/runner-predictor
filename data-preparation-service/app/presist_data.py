from .i_preparator import IPreparator
import redis

data_redis = redis.Redis(host="datapreparation_redis", port=6379, db=0)


class PresistData:
    def __init__(self, preparator):
        if not isinstance(preparator, IPreparator):
            raise ValueError("Preparator should implement IPreparator")
        self.preparator = preparator
        # self.save_to_redis()
        self.get_from_redis()

    def save_to_redis(self):
        data_to_save = self.preparator.data_results()
        for data in data_to_save:
            redis_key = f"race_group_{data['race_group']}:id_{data['id']}"
            print(redis_key, data)
            data_redis.hmset(redis_key, data)

    def get_from_redis(self):
        cursor = 0
        data = data_redis.scan(cursor=0, match="race_group_1:*", count=1000)

        cursor, keys = data

        for k in keys:
            r = data_redis.hgetall(k)
            print(r)
