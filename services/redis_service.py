import json
import logging
from typing import Any, Dict, List, Optional, Union
from config.redis_config import redis_config

logger = logging.getLogger(__name__)

class RedisService:
    def __init__(self):
        self.client = redis_config.get_client()
        self.default_ttl = 3600  # 1 hour in seconds
    
    # Basic Key-Value operations
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        try:
            serialized_value = json.dumps(value)
            if ttl:
                return self.client.setex(key, ttl, serialized_value)
            else:
                return self.client.set(key, serialized_value)
        except Exception as e:
            logger.error(f"Redis SET error for key {key}: {e}")
            raise
    
    def get(self, key: str) -> Optional[Any]:
        try:
            value = self.client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Redis GET error for key {key}: {e}")
            raise
    
    def delete(self, key: str) -> bool:
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"Redis DELETE error for key {key}: {e}")
            raise
    
    def exists(self, key: str) -> bool:
        try:
            return bool(self.client.exists(key))
        except Exception as e:
            logger.error(f"Redis EXISTS error for key {key}: {e}")
            raise
    
    # Hash operations
    def hset(self, key: str, field: str, value: Any) -> bool:
        try:
            serialized_value = json.dumps(value)
            return bool(self.client.hset(key, field, serialized_value))
        except Exception as e:
            logger.error(f"Redis HSET error for key {key}, field {field}: {e}")
            raise
    
    def hget(self, key: str, field: str) -> Optional[Any]:
        try:
            value = self.client.hget(key, field)
            return json.loads(value) if value else None
        except Exception as e:
            logger.error(f"Redis HGET error for key {key}, field {field}: {e}")
            raise
    
    def hgetall(self, key: str) -> Dict[str, Any]:
        try:
            result = self.client.hgetall(key)
            return {k: json.loads(v) for k, v in result.items()}
        except Exception as e:
            logger.error(f"Redis HGETALL error for key {key}: {e}")
            raise
    
    def hdel(self, key: str, field: str) -> bool:
        try:
            return bool(self.client.hdel(key, field))
        except Exception as e:
            logger.error(f"Redis HDEL error for key {key}, field {field}: {e}")
            raise
    
    # Set operations
    def sadd(self, key: str, *members: Any) -> int:
        try:
            serialized_members = [json.dumps(member) for member in members]
            return self.client.sadd(key, *serialized_members)
        except Exception as e:
            logger.error(f"Redis SADD error for key {key}: {e}")
            raise
    
    def smembers(self, key: str) -> List[Any]:
        try:
            members = self.client.smembers(key)
            return [json.loads(member) for member in members]
        except Exception as e:
            logger.error(f"Redis SMEMBERS error for key {key}: {e}")
            raise
    
    def srem(self, key: str, *members: Any) -> int:
        try:
            serialized_members = [json.dumps(member) for member in members]
            return self.client.srem(key, *serialized_members)
        except Exception as e:
            logger.error(f"Redis SREM error for key {key}: {e}")
            raise
    
    # Sorted Set operations
    def zadd(self, key: str, mapping: Dict[Any, float]) -> int:
        try:
            serialized_mapping = {json.dumps(member): score for member, score in mapping.items()}
            return self.client.zadd(key, serialized_mapping)
        except Exception as e:
            logger.error(f"Redis ZADD error for key {key}: {e}")
            raise
    
    def zrange(self, key: str, start: int, stop: int, withscores: bool = False) -> List[Any]:
        try:
            result = self.client.zrange(key, start, stop, withscores=withscores)
            if withscores:
                return [(json.loads(member), score) for member, score in result]
            else:
                return [json.loads(member) for member in result]
        except Exception as e:
            logger.error(f"Redis ZRANGE error for key {key}: {e}")
            raise
    
    def zrevrange(self, key: str, start: int, stop: int, withscores: bool = False) -> List[Any]:
        try:
            result = self.client.zrevrange(key, start, stop, withscores=withscores)
            if withscores:
                return [(json.loads(member), score) for member, score in result]
            else:
                return [json.loads(member) for member in result]
        except Exception as e:
            logger.error(f"Redis ZREVRANGE error for key {key}: {e}")
            raise
    
    def zrem(self, key: str, *members: Any) -> int:
        try:
            serialized_members = [json.dumps(member) for member in members]
            return self.client.zrem(key, *serialized_members)
        except Exception as e:
            logger.error(f"Redis ZREM error for key {key}: {e}")
            raise
    
    # List operations
    def lpush(self, key: str, *values: Any) -> int:
        try:
            serialized_values = [json.dumps(value) for value in values]
            return self.client.lpush(key, *serialized_values)
        except Exception as e:
            logger.error(f"Redis LPUSH error for key {key}: {e}")
            raise
    
    def rpush(self, key: str, *values: Any) -> int:
        try:
            serialized_values = [json.dumps(value) for value in values]
            return self.client.rpush(key, *serialized_values)
        except Exception as e:
            logger.error(f"Redis RPUSH error for key {key}: {e}")
            raise
    
    def lrange(self, key: str, start: int, stop: int) -> List[Any]:
        try:
            values = self.client.lrange(key, start, stop)
            return [json.loads(value) for value in values]
        except Exception as e:
            logger.error(f"Redis LRANGE error for key {key}: {e}")
            raise
    
    # Key pattern matching
    def keys(self, pattern: str) -> List[str]:
        try:
            return self.client.keys(pattern)
        except Exception as e:
            logger.error(f"Redis KEYS error for pattern {pattern}: {e}")
            raise
    
    # TTL operations
    def expire(self, key: str, ttl: int) -> bool:
        try:
            return self.client.expire(key, ttl)
        except Exception as e:
            logger.error(f"Redis EXPIRE error for key {key}: {e}")
            raise
    
    def ttl(self, key: str) -> int:
        try:
            return self.client.ttl(key)
        except Exception as e:
            logger.error(f"Redis TTL error for key {key}: {e}")
            raise
    
    # Database operations
    def flushdb(self) -> bool:
        try:
            return self.client.flushdb()
        except Exception as e:
            logger.error(f"Redis FLUSHDB error: {e}")
            raise
    
    def info(self) -> Dict[str, Any]:
        try:
            return self.client.info()
        except Exception as e:
            logger.error(f"Redis INFO error: {e}")
            raise

# Global instance
redis_service = RedisService()