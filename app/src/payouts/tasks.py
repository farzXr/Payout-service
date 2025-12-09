# tasks.py
import logging
import time
import os

from celery import shared_task
from django.db import transaction
from django.db.utils import OperationalError

from .models import Payout, PayoutStatus
import logging

loger = logging.getLogger("payout-tasks")
if not loger.handlers:
    log_dir = "/app/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    file_handler = logging.FileHandler("/app/logs/tasks.log")
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    loger.addHandler(file_handler)
    loger.addHandler(console_handler)
    loger.setLevel(logging.INFO)

@shared_task(bind=True, max_retries=3)
def process_payout(self, payout_id):

    loger.info(f"Старт задачи для выплаты #{payout_id}")
    try:
        with transaction.atomic():
            payout = Payout.objects.select_for_update().get(id=payout_id)
            loger.info(f"Выплата #{payout_id}: {payout.amount} {payout.currency}")

            if payout.status != PayoutStatus.PENDING:
                loger.warning(f"Payout {payout_id} is already in {payout.status} status")
                return

            payout.mark_as_processing()
            loger.info("Обрабатываем платеж...")
            time.sleep(10)

            import random

            if random.random() < 0.1:
                raise Exception("Random processing error")

            payout.mark_as_completed()
            loger.info(f"Выплата #{payout_id} обработана!")

    except OperationalError as e:
        loger.error(f"Database error processing payout {payout_id}: {e}")
    except Payout.DoesNotExist:
        loger.error(f"Payout {payout_id} not found")
    except Exception as e:
        loger.error(f"Error processing payout {payout_id}: {e}")
        payout.mark_as_failed()
