from dotenv import load_dotenv
load_dotenv()

from rq import SimpleWorker
from app.jobs.queue import redis_conn, review_queue

if __name__ == "__main__":
    worker = SimpleWorker([review_queue], connection=redis_conn)
    worker.work()