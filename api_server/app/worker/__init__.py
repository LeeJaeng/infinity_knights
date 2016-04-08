import os

from celery import Celery


william = Celery('william')
william.conf.update(BROKER_URL=os.environ.get('CELERY_BROKER_URL'),
                    BROKER_POOL_LIMIT=1,
                    BROKER_HEARTBEAT=None,
                    BROKER_CONNECTION_TIMEOUT=30,
                    CELERY_RESULT_BACKEND=None,
                    CELERY_SEND_EVENTS=False,
                    CELERY_EVENT_QUEUE_EXPIRES=60,
                    CELERY_ACCEPT_CONTENT=['pickle', 'json', 'msgpack', 'yaml'])


from app.worker.tasks import *
