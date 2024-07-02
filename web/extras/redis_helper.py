import json
from redis import StrictRedis


class RedisHelper:
    def __init__(self):
        self.client = StrictRedis(host='redis', port=6379)

    def set_value(self, key, value, expiration=60):
        # default expiry set to 60 seconds
        if isinstance(value, (str, int, float)):
            self.client.setex(key, expiration, value)
        else:
            self.client.setex(key, expiration, json.dumps(value, default=str))

    def get_value(self, key):
        if not self.client.exists(key):
            print(f"Key '{key}' does not exist.")
            return None
        value = self.client.get(key)
        try:
            # Try to load the value as JSON to handle complex types
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            # If JSON loading fails, return the value as is (for simple types)
            return value

    # Invalidate all keys in the current database
    def invalidate_all_keys_in_db(self):
        self.client.flushdb()

    # Invalidate all keys in all databases
    def invalidate_all_keys_in_all_dbs(self):
        self.client.flushall()

    def incrementer(self, key):
        self.client.incr(key)


