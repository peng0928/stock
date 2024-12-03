import json

import redis


class RedisClient:
    def __init__(self, host='localhost', port=6379, db=0, max_connections=10):
        # 创建连接池
        self.pool = redis.ConnectionPool(host=host, port=port, db=db, max_connections=max_connections)
        # 使用连接池创建Redis对象
        self.redis = redis.Redis(connection_pool=self.pool)

    def lpush(self, key, value):
        """设置键值对"""
        if isinstance(value, dict):
            value = json.dumps(value)
        self.redis.lpush(key, value)
        return f"lpush {key} => {value}"

    def rpush(self, key, value):
        """设置键值对"""
        self.redis.rpush(key, value)
        return f"Set {key} = {value}"

    def lrange(self, key, start, end):
        """获取列表"""
        return self.redis.lrange(key, start, end)
    def lpop(self, key, count):
        """获取列表"""
        return self.redis.lpop(key, count)

    def set_value(self, key, value):
        """设置键值对"""
        self.redis.set(key, value)
        return f"Set {key} = {value}"

    def get_value(self, key):
        """获取键对应的值"""
        value = self.redis.get(key)
        if value:
            return f"Get {key} = {value.decode('utf-8')}"
        else:
            return f"Key: {key} not found"

    def delete_key(self, key):
        """删除键"""
        self.redis.delete(key)
        return f"Deleted key: {key}"

    def update_value(self, key, value):
        """更新键对应的值"""
        if self.redis.exists(key):
            self.redis.set(key, value)
            return f"Updated {key} = {value}"
        else:
            return f"Key: {key} not found, cannot update"

    def close(self):
        """关闭连接池"""
        # 关闭Redis连接
        self.redis.close()
        # 断开连接池
        self.pool.disconnect()


# 使用示例
if __name__ == "__main__":
    client = RedisClient()
    for i in range(10):
        print(client.lpush('name', {'John': 1}))
    # print(client.lrange('name', 0, 0))
