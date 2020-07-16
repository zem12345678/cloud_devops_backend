import dramatiq
import requests
from dramatiq.brokers.redis import RedisBroker
from cloud_devops_backend.settings import REDIS_HOST,REDIS_PORT,REDIS_PASSWORD

redis_broker = RedisBroker(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
dramatiq.set_broker(redis_broker)

@dramatiq.actor
def count_words(url):
    print(url)

count_words.send("http://example.com")