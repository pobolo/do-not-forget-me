import redis
import os
from dotenv import load_dotenv

load_dotenv()

class RedisConfig:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisConfig, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.client = None
        self.connect()
    
    def connect(self):
        try:
            self.client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                password=os.getenv('REDIS_PASSWORD', None),
                db=int(os.getenv('REDIS_DB', 0)),
                decode_responses=True,
                socket_connect_timeout=5,
                retry_on_timeout=True
            )
            
            # Test connection
            self.client.ping()
            print("Connected to Redis successfully")
            
        except redis.ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error connecting to Redis: {e}")
            raise
    
    def get_client(self):
        if self.client is None:
            self.connect()
        return self.client
    
    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None

# Global instance
redis_config = RedisConfig()