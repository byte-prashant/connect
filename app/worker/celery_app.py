from celery import Celery
import os

celery_ins = Celery(__name__)
celery_ins.conf.broker_url = os.environ['CELERY_BROKER_URL']
celery_ins.conf.result_backend = os.environ['CELERY_RESULT_BACKEND']

@celery_ins.task(name="sms worker")
def sms_worker(body, to) -> str:
    from app.utils import send_sms
    return send_sms(body, to)