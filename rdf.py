import pandas as pd
import redis
import os
import __init__


class Rdf(pd.DataFrame):
    expire_time = os.getenv('REDIS_EXPIRE_SECONDS')
    port = int(os.getenv('REDIS_PORT'))
    host = os.getenv('REDIS_IP_ADDR')

    def __init__(self, *args,  **kwargs):
        super().__init__(*args, **kwargs) 
        self.redis_client = redis.Redis(
            host=self.host, port=self.port, decode_responses=True
        )
        if not self.redis_client.ping():
            raise ConnectionRefusedError(
                f'Could not connect to redis: {self.host}:{self.port}'
            )

    def to_redis(self, key, nx=True, **kwargs):
        df_string = self.to_csv(index=False)
        _ = self.redis_client.set(
            key, df_string, ex=self.expire_time, nx=nx, **kwargs
        )

    @classmethod
    def from_redis(cls, key, **kwargs):
        stored_df_string = cls().redis_client.get(key)
        if not stored_df_string:
            raise KeyError(f'No entry for "{key=}"')
        else:
            df = pd.read_csv(pd.io.common.StringIO(stored_df_string))
            return cls(df)

    def __repr__(self):
        return f'<redis_dataframe>'
