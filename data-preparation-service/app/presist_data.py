from .i_preparator import IPreparator
import redis

data_redis = redis.StrictRedis(
    host="datapreparation_redis", port=6379, db=0, decode_responses=True
)


class PresistData:
    def __init__(self, preparator, force_redownload=False):
        if not isinstance(preparator, IPreparator):
            raise ValueError("Preparator should implement IPreparator")
        self.preparator = preparator
        downloaded = data_redis.get(
            f"race_group_{self.preparator.race_group_id}_downloaded"
        )
        print("downloaded", type(downloaded))
        if force_redownload or not int(downloaded):
            self.save_to_redis()

    def save_to_redis(self):

        data_to_save = self.preparator.data_results()
        data_redis.set(
            f"race_group_{self.preparator.race_group_id}_downloaded", 0
        )
        for data in data_to_save:
            redis_key = f"race_group_{data['race_group']}:id_{data['id']}"
            print(redis_key, data)
            data_redis.hmset(redis_key, data)
        data_redis.set(
            f"race_group_{self.preparator.race_group_id}_downloaded", 1
        )

    def get_from_redis(self):
        # TODO while cursor by 10
        # send dato to csv
        cursor = 0
        do_loop = True
        while do_loop:
            data = data_redis.scan(
                cursor=cursor,
                match=f"race_group_{self.preparator.race_group_id}:*",
                count=100,
            )
            cursor, keys = data
            print("cursor", cursor)
            for k in keys:
                r = data_redis.hgetall(k)
                yield r
            if cursor == 0:
                do_loop = False
