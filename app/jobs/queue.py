import os
from redis import Redis
from rq import Queue

redis_conn = Redis.from_url(os.getenv("REDIS_URL"))
review_queue = Queue("pr_reviews", connection=redis_conn)